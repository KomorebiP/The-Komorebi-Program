"""All-index P-recursive polyphase lifting via exact rational companion matrices.

Author: Komorebi P.

If sum_j p_j(n)a_(n+j)=0 and p_d(n) is certified nonzero for n>=T,
the state v_n=(a_n,...,a_(n+d-1)) obeys v_(n+1)=M(n)v_n.
For a residue class m*k+r, multiply m exact M matrices and eliminate
state coordinates over Q(k) to prove a polynomial-coefficient recurrence
of order <=d for the extracted subsequence.

The leading-coefficient domain is proved via nonzero same-sign shifted
polynomial coefficients; this is sufficient but not necessary. Never assume
a finite OEIS prefix proves an infinite sequence identity.
"""
from __future__ import annotations
import argparse,hashlib,json,sqlite3
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
from sequence_holonomic_compiler import (
    Rat, fraction_eval, pzero, pshift, peval, pdivmod, pgcd,
    normalize_operator, trim, compile_formula,
)


def safe_leader(leader, max_shift=40):
    """A constructive positivity/sign certificate for all integer n>=T."""
    for T in range(max_shift+1):
        v=pshift(leader,T)
        if v[0]>0 and all(x>=0 for x in v):return T,1
        if v[0]<0 and all(x<=0 for x in v):return T,-1
    return None


def mat_identity(d):return [[Rat((int(i==j),)) for j in range(d)] for i in range(d)]

def matmul(a,b):
    if len(a[0])!=len(b):raise ValueError('matrix shape mismatch')
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),Rat((0,)))
             for j in range(len(b[0]))] for i in range(len(a))]

def matshift(a,k):return [[x.shift(k) for x in row] for row in a]


def companion(polys):
    d=len(polys)-1
    if d<1:raise ValueError('positive recurrence order required')
    if pzero(polys[-1]):raise ValueError('leading polynomial zero')
    mat=[[Rat((0,)) for _ in range(d)] for _ in range(d)]
    for i in range(d-1):mat[i][i+1]=Rat()
    for j in range(d):mat[d-1][j]=-Rat(polys[j],polys[-1])
    return mat


def primitive_nullvector(matrix):
    """Exact nonzero right kernel vector of d by d+1 rational matrix."""
    mat=[[x for x in row] for row in matrix]
    rows=len(mat);cols=len(mat[0]);pivots=[];r=0
    for col in range(cols):
        k=next((i for i in range(r,rows) if mat[i][col]),None)
        if k is None:continue
        mat[r],mat[k]=mat[k],mat[r]
        pivot=mat[r][col]
        mat[r]=[x/pivot for x in mat[r]]
        for i in range(rows):
            if i!=r and mat[i][col]:
                scalar=mat[i][col]
                mat[i]=[x-scalar*y for x,y in zip(mat[i],mat[r])]
        pivots.append(col);r+=1
        if r==rows:break
    free=[i for i in range(cols) if i not in pivots]
    if not free:raise ArithmeticError('no rational polynomial nullvector')
    z=[Rat((0,)) for _ in range(cols)];z[free[-1]]=Rat()
    for row,pivot in reversed(list(enumerate(pivots))):
        z[pivot]=-sum((mat[row][j]*z[j] for j in range(pivot+1,cols)),Rat((0,)))
    common=(F(1),)
    from sequence_holonomic_compiler import pmul
    for x in z:common=pmul(common,x.den)
    polys=[]
    for x in z:
        q,rem=pdivmod(common,x.den)
        if not pzero(rem):raise ArithmeticError('non-divisible rational denominator')
        polys.append(pmul(x.num,q))
    gcd=next((p for p in polys if not pzero(p)),(F(1),))
    for p in polys:
        if not pzero(p):gcd=pgcd(gcd,p)
    polys=[pdivmod(p,gcd)[0] for p in polys]
    out=normalize_operator(polys)
    for row in matrix:
        if sum((v*Rat(poly) for v,poly in zip(row,out)),Rat((0,))):
            raise AssertionError('cyclic state elimination failed as identity in Q(k)')
    return out


def lift(cert,ast,m,r,checks=5):
    if type(m) is not int or not 2<=m<=5 or type(r) is not int or not 0<=r<m:
        raise ValueError('invalid modulus/residue')
    polynomials=[tuple(F(v) for v in p) for p in cert['operator_coefficients']]
    d=len(polynomials)-1
    if not 1<=d<=3:raise ValueError('pilot supports recurrence orders 1..3')
    safe=safe_leader(polynomials[-1]);
    if safe is None:raise ValueError('not certified nonsingular on a bounded tail')
    shift,sign=safe
    base=cert['mathematical_start']+shift
    shifted=[pshift(p,shift) for p in polynomials]
    M=companion(shifted)
    # A single block transition from n=m*k+r to n=m*(k+1)+r.
    T=mat_identity(d)
    for s in range(m):
        T=matmul([[x.affine(m,r+s) for x in row] for row in M],T)
    # Sequence k+j is first coordinate of a product of shifted transitions.
    product=mat_identity(d)
    vectors=[]
    for j in range(d+1):
        if j:product=matmul(matshift(T,j-1),product)
        vectors.append(list(product[0]))
    kernel=primitive_nullvector([[vectors[j][i] for j in range(d+1)] for i in range(d)])
    # A second exact calculation checks the kernel against the formulas.
    for k in range(checks):
        total=sum((peval(kernel[j],k)*fraction_eval(ast,base+r+m*(k+j)) for j in range(d+1)),F(0))
        if total:raise AssertionError('independent symbolic phase test failed')
    return {
        'formula_id':cert['formula_id'],'oeis_id':cert['oeis_id'],
        'source_sha256':cert['source_sha256'],'evaluator_sha256':cert['evaluator_sha256'],
        'source_order':d,'result_order':len(kernel)-1,
        'mathematical_base_start':base,'original_mathematical_start':cert['mathematical_start'],
        'certified_leader_shift':shift,'leader_sign':sign,
        'modulus':m,'residue':r,
        'operator_coefficients':[[str(v) for v in p] for p in kernel],
        'base_value':str(fraction_eval(ast,base+r)),
        'proof_method':'Exact companion state over Q(k), m-step transition, symbolic row nullvector, and globally nonvanishing source leader',
        'scope':'All-index recurrence of the extracted formula polyphase; finite OEIS reference identity remains separate',
    }


def batch(db,input_ledger,output,summary=None,limit=1000,mods=(2,3)):
    seen=set();records=[];counts=Counter()
    for line in Path(input_ledger).open(encoding='utf8'):
        if not line.strip():continue
        cert=json.loads(line);fid=cert['formula_id']
        if fid in seen:continue
        seen.add(fid)
        if not 2<=cert['order']<=3:continue
        counts['eligible']+=1
        row=db.execute('''SELECT f.evaluator_json,f.oeis_id,f.verification,s.offset,s.terms_json,s.source_sha256
             FROM formulas f JOIN sequences s ON f.oeis_id=s.oeis_id
             WHERE f.formula_id=?''',(fid,)).fetchone()
        if not row:counts['missing']+=1;continue
        raw,sid,verification,offset,terms,sha=row
        spec=json.loads(raw)
        if verification!='finite_checked' or sid!=cert['oeis_id'] or sha!=cert['source_sha256']:
            counts['stale']+=1;continue
        if hashlib.sha256(json.dumps(spec,sort_keys=True,separators=(',',':')).encode()).hexdigest()!=cert['evaluator_sha256']:
            counts['stale']+=1;continue
        try:
            fresh=compile_formula(fid,sid,spec,offset,[int(x) for x in json.loads(terms)],sha)
        except (ArithmeticError,ValueError,OverflowError):
            counts['stale']+=1;continue
        if fresh is None or fresh['operator_coefficients']!=cert['operator_coefficients'] or fresh['mathematical_start']!=cert['mathematical_start']:
            counts['stale']+=1;continue
        for m in mods:
            for r in range(m):
                counts['attempted']+=1
                try:out=lift(cert,spec,m,r,checks=4)
                except (ArithmeticError,OverflowError,ValueError,AssertionError,ZeroDivisionError):
                    counts['unsupported']+=1;continue
                records.append(out);counts['certified']+=1
        if counts['eligible']>=limit:break
    Path(output).parent.mkdir(parents=True,exist_ok=True)
    with Path(output).open('w',encoding='utf8') as f:
        for rec in records:f.write(json.dumps(rec,sort_keys=True,separators=(',',':'))+'\n')
    stats=dict(status='exact_p_recursive_polyphase',**counts,moduli=mods,
        scope='All-index formal recurrences of extracted formulas, not infinite OEIS identifications')
    if summary:Path(summary).write_text(json.dumps(stats,indent=2)+'\n',encoding='utf8')
    return stats




def verify_lift(source, ast, certificate, checks=4):
    """Independently prove a STORED phase recurrence by matrix annihilation.

    Avoid repeating rational nullspace search: check its answer directly over
    Q(k), not merely a finite sample. Input source is separately rebuilt.
    """
    polys=[tuple(F(v) for v in p) for p in source['operator_coefficients']]
    d=len(polys)-1
    if d!=certificate['source_order'] or d!=certificate['result_order']:
        raise ValueError('reported recurrence order differs')
    safe=safe_leader(polys[-1])
    if safe is None or list(safe)!=[certificate['certified_leader_shift'],certificate['leader_sign']]:
        raise ValueError('nonsingular leader certificate differs')
    shift,_=safe;start=source['mathematical_start']+shift
    m,r=certificate['modulus'],certificate['residue']
    if not 2<=m<=5 or not 0<=r<m:raise ValueError('invalid phase')
    if start!=certificate['mathematical_base_start'] or source['mathematical_start']!=certificate['original_mathematical_start']:
        raise ValueError('phase starting index altered')
    M=companion([pshift(poly,shift) for poly in polys]);T=mat_identity(d)
    for s in range(m):T=matmul([[x.affine(m,r+s) for x in row] for row in M],T)
    product=mat_identity(d);vectors=[]
    for j in range(d+1):
        if j:product=matmul(matshift(T,j-1),product)
        vectors.append(list(product[0]))
    coeff=[tuple(F(x) for x in row) for row in certificate['operator_coefficients']]
    if len(coeff)!=d+1:raise ValueError('incorrect result order')
    for i in range(d):
        lhs=sum((Rat(coeff[j])*vectors[j][i] for j in range(d+1)),Rat((0,)))
        if lhs:raise AssertionError('stored phase recurrence fails Q(k) state identity')
    base=fraction_eval(ast,start+r)
    if str(base)!=certificate['base_value']:raise ValueError('changed phase initial value')
    for k in range(checks):
        lhs=sum((peval(coeff[j],k)*fraction_eval(ast,start+r+m*(k+j)) for j in range(d+1)),F(0))
        if lhs:raise AssertionError('stored phase recurrence fails direct formula check')
    return True


def replay(db,holonomic,phases):
    """Independent source-bound rebuild of every P-recursive phase certificate."""
    originals={}
    for line in Path(holonomic).open(encoding='utf8'):
        if not line.strip():continue
        c=json.loads(line)
        originals[c['formula_id']]=c
    checked=0;errors=[];source_cache={}
    for line in Path(phases).open(encoding='utf8'):
        if not line.strip():continue
        c=json.loads(line);checked+=1
        try:
            fid=c['formula_id'];original=originals[fid]
            if fid not in source_cache:
                row=db.execute('SELECT f.evaluator_json,f.oeis_id,f.verification,s.offset,s.terms_json,s.source_sha256 '
                    'FROM formulas f JOIN sequences s ON f.oeis_id=s.oeis_id WHERE f.formula_id=?',(fid,)).fetchone()
                if not row:raise ValueError('missing formula')
                raw,sid,verified,offset,terms,sha=row
                if verified!='finite_checked' or sid!=c['oeis_id'] or sha!=c['source_sha256']:
                    raise ValueError('stale source')
                ast=json.loads(raw)
                fresh=compile_formula(fid,sid,ast,offset,[int(x) for x in json.loads(terms)],sha)
                if fresh is None or fresh['operator_coefficients']!=original['operator_coefficients'] or fresh['mathematical_start']!=original['mathematical_start']:
                    raise ValueError('stale recurrence')
                source_cache[fid]=(fresh,ast)
            fresh,ast=source_cache[fid]
            if c['source_sha256']!=fresh['source_sha256'] or c['evaluator_sha256']!=fresh['evaluator_sha256'] or c['oeis_id']!=fresh['oeis_id']:
                raise ValueError('changed source receipt')
            verify_lift(fresh,ast,c)
        except (KeyError,ArithmeticError,ValueError,AssertionError,OverflowError,ZeroDivisionError) as exc:
            if len(errors)<15:errors.append({'formula_id':c.get('formula_id'),'modulus':c.get('modulus'),'residue':c.get('residue'),'error':str(exc)})
    return {'status':'passed' if not errors else 'failed','checked':checked,'errors':errors,
            'scope':'All-index formula-defined polyphase recurrences, not OEIS full identity'}


def main():
    p=argparse.ArgumentParser();p.add_argument('--db',type=Path,required=True);p.add_argument('--holonomic',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--summary',type=Path)
    p.add_argument('--limit',type=int,default=50);p.add_argument('--replay',action='store_true');a=p.parse_args()
    with sqlite3.connect(a.db) as db:result=(replay(db,a.holonomic,a.output) if a.replay else batch(db,a.holonomic,a.output,a.summary,limit=a.limit))
    print(json.dumps(result,indent=2))
    if result['status']=='failed':raise SystemExit(1)
if __name__=='__main__':main()
