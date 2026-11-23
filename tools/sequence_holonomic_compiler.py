"""Exact P-recursive certificates from finite sums of hypergeometric terms.

Author: Komorebi P.

Only declarative evaluator expressions are handled. The rational term-ratio
identity is derived structurally from factorial/binomial/affine rules, then a
rational-function nullspace gives polynomial-coefficient annihilators. The
result proves properties of those expressions for every index on an explicit
non-singular tail, not the identification of an OEIS entry for all n.

Stdlib Python 3.10+, no eval/exec or floating point.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, math, sqlite3
from collections import Counter
from fractions import Fraction as F
from functools import reduce
from math import comb, factorial
from pathlib import Path
from sequence_ratio_certificates import derive_ratio, ratio_polynomials
from oeis_formula_database import evaluate

DEGREE_LIMIT=80
BIT_LIMIT=16000


def trim(p):
    p=list(map(F,p))
    while len(p)>1 and not p[-1]:p.pop()
    return tuple(p or [F(0)])


def pzero(p):return len(p)==1 and p[0]==0


def padd(a,b):return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])

def pneg(a):return tuple(-x for x in a)

def psub(a,b):return padd(a,pneg(b))

def pmul(a,b):
    if pzero(a) or pzero(b):return (F(0),)
    p=[F(0)]*(len(a)+len(b)-1)
    if len(p)>DEGREE_LIMIT+1:raise ArithmeticError('polynomial degree cap')
    for i,x in enumerate(a):
        for j,y in enumerate(b):p[i+j]+=x*y
    if any(max(x.numerator.bit_length(),x.denominator.bit_length())>BIT_LIMIT for x in p):
        raise ArithmeticError('polynomial coefficient cap')
    return trim(p)

def pshift(a,b):
    """p(t+b)."""
    out=[F(0)]*len(a)
    for j,v in enumerate(a):
        for i in range(j+1):out[i]+=v*comb(j,i)*b**(j-i)
    return trim(out)

def paffine(a,m,b):
    """p(m*t+b)."""
    out=[F(0)]*len(a)
    for j,v in enumerate(a):
        for i in range(j+1):out[i]+=v*comb(j,i)*m**i*b**(j-i)
    return trim(out)

def peval(a,n):return sum(c*n**j for j,c in enumerate(a))

def pdivmod(a,b):
    if pzero(b):raise ZeroDivisionError('polynomial divide by zero')
    a=list(trim(a));b=trim(b)
    if len(a)<len(b):return (F(0),),tuple(a)
    q=[F(0)]*(len(a)-len(b)+1)
    while len(a)>=len(b) and not pzero(a):
        k=len(a)-len(b);v=a[-1]/b[-1];q[k]+=v
        for i,u in enumerate(b):a[i+k]-=v*u
        a=list(trim(a))
    return trim(q),trim(a)

def pgcd(a,b):
    a,b=trim(a),trim(b)
    while not pzero(b):
        _,r=pdivmod(a,b);a,b=b,r
    return trim(v/a[-1] for v in a) if not pzero(a) else (F(1),)

class Rat:
    __slots__=('num','den')
    def __init__(self,num=(1,),den=(1,)):
        num,den=trim(num),trim(den)
        if pzero(den):raise ZeroDivisionError('zero rational function denominator')
        if pzero(num):self.num,self.den=(F(0),),(F(1),);return
        g=pgcd(num,den)
        num,r=pdivmod(num,g);assert pzero(r)
        den,r=pdivmod(den,g);assert pzero(r)
        scalar=den[-1]
        self.num,self.den=trim(c/scalar for c in num),trim(c/scalar for c in den)
    @staticmethod
    def of(x):return x if isinstance(x,Rat) else Rat((F(x),))
    def __add__(self,y):
        y=Rat.of(y)
        return Rat(padd(pmul(self.num,y.den),pmul(y.num,self.den)),pmul(self.den,y.den))
    def __neg__(self):return Rat(pneg(self.num),self.den)
    def __sub__(self,y):return self+-Rat.of(y)
    def __mul__(self,y):
        y=Rat.of(y)
        return Rat(pmul(self.num,y.num),pmul(self.den,y.den))
    def __truediv__(self,y):
        y=Rat.of(y)
        if pzero(y.num):raise ZeroDivisionError('rational function divide by zero')
        return Rat(pmul(self.num,y.den),pmul(self.den,y.num))
    def __bool__(self):return not pzero(self.num)
    def __eq__(self,y):
        y=Rat.of(y)
        return self.num==y.num and self.den==y.den
    def shift(self,h):return Rat(pshift(self.num,h),pshift(self.den,h))
    def affine(self,m,h):return Rat(paffine(self.num,m,h),paffine(self.den,m,h))
    def at(self,t):return peval(self.num,t)/peval(self.den,t)
    def json(self):return {'numerator':[str(c) for c in self.num],'denominator':[str(c) for c in self.den]}


def normalize_operator(coeff):
    """Primitive integer polynomial coefficients, fixed leading sign."""
    polynomials=[trim(p) for p in coeff]
    denom=math.lcm(*(z.denominator for p in polynomials for z in p))
    ints=[[int(z*denom) for z in p] for p in polynomials]
    common=math.gcd(*(abs(z) for p in ints for z in p)) or 1
    ints=[[z//common for z in p] for p in ints]
    if next((p[-1] for p in ints[::-1] if any(p)),1)<0:ints=[[-z for z in p] for p in ints]
    return [list(trim(p)) for p in ints]


def nullspace_operator(ratios):
    """Annihilate the sum of k ratio-defined terms by Ore-style elimination.

    Columns j contain products r(n) ... r(n+j-1). Exact rational
    row reduction returns a nullvector. Clearing denominators yields
    polynomial coefficients p_j(n) with sum p_j(n) S^j a=0.
    """
    unique=[]
    for r in ratios:
        if r not in unique:unique.append(r)
    k=len(unique)
    if not 1<=k<=5:raise ValueError('requires one to five nonzero distinct ratios')
    matrix=[]
    for r in unique:
        row=[Rat()];acc=Rat()
        for j in range(1,k+1):
            acc=acc*r.shift(j-1);row.append(acc)
        matrix.append(row)
    # RREF over Q(t) with controlled polynomial rational operations.
    r=0;pivots=[]
    for col in range(k+1):
        pivot=next((i for i in range(r,k) if matrix[i][col]),None)
        if pivot is None:continue
        matrix[r],matrix[pivot]=matrix[pivot],matrix[r]
        factor=matrix[r][col]
        matrix[r]=[v/factor for v in matrix[r]]
        for i in range(k):
            if i!=r and matrix[i][col]:
                factor=matrix[i][col]
                matrix[i]=[v-factor*w for v,w in zip(matrix[i],matrix[r])]
        pivots.append(col);r+=1
        if r==k:break
    free=[j for j in range(k+1) if j not in pivots]
    if not free:raise ArithmeticError('full column rank unexpectedly')
    x=[Rat((0,)) for _ in range(k+1)];x[free[-1]]=Rat()
    for row,pivot in reversed(list(enumerate(pivots))):
        x[pivot]=-sum((matrix[row][j]*x[j] for j in range(pivot+1,k+1)),Rat((0,)))
    # Construct common denominator polynomial, then primitive integer operator.
    common=(F(1),)
    for f in x:common=pmul(common,f.den)
    poly=[]
    for f in x:
        q,rem=pdivmod(common,f.den)
        if not pzero(rem):raise ArithmeticError('operator denominator not divisible')
        poly.append(pmul(f.num,q))
    # Reduce any common polynomial factor and normalize integers.
    gcd=next((p for p in poly if not pzero(p)),(F(1),))
    for p in poly:
        if not pzero(p):gcd=pgcd(gcd,p)
    poly=[pdivmod(p,gcd)[0] for p in poly]
    out=normalize_operator(poly)
    if all(pzero(p) for p in out):raise ArithmeticError('zero annihilator')
    # Symbolic independent check against ORIGINAL ratio rows.
    for ratio in unique:
        total=Rat((0,));acc=Rat()
        for j,p in enumerate(out):
            if j:acc=acc*ratio.shift(j-1)
            total=total+Rat(p)*acc
        if total:raise AssertionError('nonzero exact annihilator remainder')
    return out


def mul_node(a,b):
    if a==1:return b
    if b==1:return a
    if a==0 or b==0:return 0
    return {'op':'mul','args':[a,b]}

def neg_node(a):return mul_node(-1,a)

def div_node(a,b):return {'op':'exact_div','num':a,'den':b}


def decompose(spec,start,limit=5):
    """Expand sums, bounded distributive products, and numerator sums safely.

    Every resulting term is subsequently required to have an exact structural
    rational ratio on the common tail. Never execute OEIS formula text.
    """
    if type(spec) is int and spec==0:return []
    try:
        if derive_ratio(spec,start) is not None:return [spec]
    except (ValueError,ArithmeticError,OverflowError):pass
    if not isinstance(spec,dict):raise ValueError('unsupported declaration')
    op=spec.get('op')
    if op=='add':
        out=[]
        for x in spec['args']:
            out+=decompose(x,start,limit)
            if len(out)>limit:raise ValueError('component count cap')
        return out
    if op=='sub':
        a,b=spec['args'];out=decompose(a,start,limit)
        out+=[neg_node(x) for x in decompose(b,start,limit)]
        if len(out)>limit:raise ValueError('component count cap')
        return out
    if op=='mul':
        out=[1]
        for x in spec['args']:
            terms=decompose(x,start,limit)
            out=[mul_node(a,b) for a in out for b in terms]
            if len(out)>limit:raise ValueError('component count cap')
        return out
    if op=='exact_div':
        if derive_ratio(spec['den'],start) is None:raise ValueError('unsupported sum denominator')
        return [div_node(x,spec['den']) for x in decompose(spec['num'],start,limit)]
    if op=='pow' and type(spec.get('exp')) is int and 0<=spec['exp']<=4:
        out=[1]
        for _ in range(spec['exp']):
            terms=decompose(spec['base'],start,limit)
            out=[mul_node(a,b) for a in out for b in terms]
            if len(out)>limit:raise ValueError('component count cap')
        return out
    raise ValueError('not a supported hypergeometric sum')


def fraction_eval(spec,n):
    """Independent rational evaluator for algebraically expanded summands.

    Integer-only exact_div in the source evaluator may split into rational
    summands. This evaluator does not weaken source formula validation.
    """
    if type(spec) is int:return F(spec)
    if not isinstance(spec,dict):raise ValueError('unrecognized fraction expression')
    op=spec.get('op')
    if op=='n':return F(n)
    if op=='add':return sum((fraction_eval(x,n) for x in spec['args']),F(0))
    if op=='sub':return fraction_eval(spec['args'][0],n)-fraction_eval(spec['args'][1],n)
    if op=='mul':return math.prod((fraction_eval(x,n) for x in spec['args']),start=F(1))
    if op=='exact_div':return fraction_eval(spec['num'],n)/fraction_eval(spec['den'],n)
    if op=='pow':
        e=fraction_eval(spec['exp'],n)
        if e.denominator!=1 or e<0 or e>5000:raise ValueError('exponent outside bounded integer range')
        return fraction_eval(spec['base'],n)**int(e)
    if op=='factorial':
        arg=fraction_eval(spec['arg'],n)
        if arg.denominator!=1 or not 0<=arg<=10000:raise ValueError('invalid factorial argument')
        return F(factorial(int(arg)))
    if op=='binomial':
        a=fraction_eval(spec['n'],n);b=fraction_eval(spec['k'],n)
        if a.denominator!=1 or b.denominator!=1 or not 0<=a<=10000:raise ValueError('invalid binomial')
        return F(comb(int(a),int(b))) if 0<=b<=a else F(0)
    if op=='at':
        x=fraction_eval(spec['index'],n)
        if x.denominator!=1 or x<0:raise ValueError('invalid shifted source index')
        return fraction_eval(spec['body'],int(x))
    raise ValueError('unsupported evaluator expression')


def start_and_components(spec,offset,terms,max_components=5,max_tail=20):
    # Mathematical source offsets matter. Find a common tail where each term
    # has nonzero values and nonsingular rational ratios for ALL later n.
    for shift in range(min(max_tail+1,max(1,len(terms)-5))):
        start=offset+shift
        if start<0:continue
        try:
            terms_ast=decompose(spec,start,max_components)
            if not terms_ast:continue
            ratio=[]
            for term in terms_ast:
                r=derive_ratio(term,start)
                if r is None:raise ValueError('nonhypergeometric component')
                v=fraction_eval(term,start)
                if v==0:raise ValueError('component initial value zero')
                # Independent one-step checks of the derived ratio.
                for h in (0,1,2):
                    v0=fraction_eval(term,start+h)
                    v1=fraction_eval(term,start+h+1)
                    if v0==0 or v1!=v0*r.ratio_at(start+h):
                        raise ArithmeticError('ratio derivation differs from direct evaluator')
                p,q=ratio_polynomials(r,start)
                ratio.append(Rat(p,q))
            # Reconcile decomposition against the original strict formula.
            for h in (0,1,3):
                if sum((fraction_eval(x,start+h) for x in terms_ast),F(0)) != evaluate(spec,start+h):
                    raise ArithmeticError('distributive decomposition changed the formula')
            return shift,terms_ast,ratio
        except (ValueError,ZeroDivisionError,ArithmeticError,OverflowError):continue
    return None


def compile_formula(formula_id,oeis_id,ast,offset,terms,source_hash,max_components=5):
    result=start_and_components(ast,offset,terms,max_components=max_components)
    if result is None:return None
    shift,components,ratios=result
    coeff=nullspace_operator(ratios)
    start=offset+shift
    checked=0
    # Check *all* available stored reference values, not merely an initial
    # eight-term window. This catches a corrupted later term and prevents a
    # false prefix coincidence from surviving the structural audit.
    for t in range(max(0,len(terms)-shift-len(coeff)+1)):
        predicted=sum(peval(coeff[j],t)*terms[shift+t+j] for j in range(len(coeff)))
        if predicted!=0:raise ValueError('operator differs from OEIS stored terms')
        checked+=1
    if checked<4:raise ValueError('insufficient independent check terms')
    return {'formula_id':formula_id,'oeis_id':oeis_id,'source_sha256':source_hash,
        'evaluator_sha256':hashlib.sha256(json.dumps(ast,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        'mathematical_start':start,'source_offset':offset,'tail_local_start':shift,
        'order':len(coeff)-1,'component_count':len(components),'unique_ratio_components':len(set((r.num,r.den) for r in ratios)),
        'operator_coefficients':[[str(v) for v in p] for p in coeff],
        'component_ast':components,'component_ratios':[r.json() for r in ratios],
        'checked_oeis_recursion_positions':checked,
        'proof_method':'Exact Q(t) shift-orbit nullspace, denominators cleared; independent algebraic row identities for every t>=0',
        'scope':'all-index identity for the supplied formula tail; OEIS formula identification finite-checked only'}


def compile_database(db,output,summary=None,max_components=5,max_records=None):
    counts=Counter();records=[]
    q='''SELECT f.formula_id,f.oeis_id,f.evaluator_json,s.offset,s.terms_json,s.source_sha256
        FROM formulas f JOIN sequences s ON s.oeis_id=f.oeis_id
        WHERE f.origin='oeis_normalized' AND f.verification='finite_checked'
        ORDER BY f.oeis_id,f.formula_id'''
    for fid,sid,raw,offset,term_json,sha in db.execute(q):
        if max_records is not None and counts['attempted']>=max_records:break
        counts['attempted']+=1
        try:
            certificate=compile_formula(fid,sid,json.loads(raw),offset,[int(x) for x in json.loads(term_json)],sha,max_components)
            if certificate is None:counts['unsupported']+=1;continue
            records.append(certificate);counts['certified']+=1
            counts['order_'+str(certificate['order'])]+=1
            if certificate['component_count']>1:counts['additive_recurrences']+=1
            if any(any(x.get('op') in ('factorial','binomial') for x in walk_ast(term)) for term in certificate['component_ast']):
                counts['factorial_or_binomial']+=1
        except (ValueError,ArithmeticError,ZeroDivisionError,OverflowError,AssertionError) as exc:
            counts['errors']+=1
            if counts['errors']<=12:counts['error_'+type(exc).__name__]+=1
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('w',encoding='utf8') as stream:
        for row in records:stream.write(json.dumps(row,separators=(',',':'))+'\n')
    stats={'status':'certified_formula_expressions_only','attempted':counts['attempted'],
        'certified':counts['certified'],'unsupported':counts['unsupported'],'errors':counts['errors'],
        'additive_recurrences':counts['additive_recurrences'],'factorial_or_binomial':counts['factorial_or_binomial'],
        'recurrence_order_counts':{k[6:]:v for k,v in counts.items() if k.startswith('order_')},
        'scope':'Exact recurrences of extracted formula expressions; OEIS global identification not proved'}
    if summary:Path(summary).write_text(json.dumps(stats,indent=2,sort_keys=True)+'\n',encoding='utf8')
    return stats


def walk_ast(node):
    if isinstance(node,dict):
        yield node
        for v in node.values():yield from walk_ast(v)
    elif isinstance(node,list):
        for v in node:yield from walk_ast(v)


def replay(db,ledger):
    counts=Counter();failures=[]
    for line in Path(ledger).open(encoding='utf8'):
        if not line.strip():continue
        cert=json.loads(line);counts['attempted']+=1
        row=db.execute('''SELECT f.evaluator_json,s.offset,s.terms_json,s.source_sha256
          FROM formulas f JOIN sequences s ON f.oeis_id=s.oeis_id
          WHERE f.formula_id=? AND f.oeis_id=? AND f.verification='finite_checked' ''',
          (cert['formula_id'],cert['oeis_id'])).fetchone()
        try:
            if not row:raise ValueError('formula not found or not finitely checked')
            raw,offset,terms,sha=row
            ast=json.loads(raw);canonical=hashlib.sha256(json.dumps(ast,sort_keys=True,separators=(',',':')).encode()).hexdigest()
            if sha!=cert['source_sha256'] or canonical!=cert['evaluator_sha256']:raise ValueError('stale source hash')
            fresh=compile_formula(cert['formula_id'],cert['oeis_id'],ast,offset,[int(x) for x in json.loads(terms)],sha,
                                  max_components=max(5,cert['component_count']))
            if fresh is None or fresh['operator_coefficients']!=cert['operator_coefficients'] or fresh['mathematical_start']!=cert['mathematical_start']:
                raise ValueError('recurrence certificate failed exact rebuild')
            counts['passed']+=1
        except (ValueError,ArithmeticError,ZeroDivisionError,AssertionError) as exc:
            counts['failed']+=1
            if len(failures)<12:failures.append({'formula':cert['formula_id'],'reason':str(exc)})
    return {'status':'passed' if not counts['failed'] else 'failed',**counts,'failure_samples':failures,
            'scope':'rederived polynomial recurrence for each formula, not independent OEIS identity'}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--summary',type=Path);p.add_argument('--replay',action='store_true');p.add_argument('--max-records',type=int)
    a=p.parse_args(argv)
    with sqlite3.connect(a.db) as db:
        stats=replay(db,a.output) if a.replay else compile_database(db,a.output,a.summary,max_records=a.max_records)
    print(json.dumps(stats,indent=2,sort_keys=True))
    if stats['status']=='failed':raise SystemExit(1)

if __name__=='__main__':main()
