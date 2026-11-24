#!/usr/bin/env python3
"""Exact ordinary algebraic GF branch and differential elimination gate.
Author: Komorebi P.
SymPy receives only constructed integer/rational polynomials, never raw text.
"""
from __future__ import annotations
import ast, re, json
from fractions import Fraction as Q
from pathlib import Path
from math import comb
from hashlib import sha1
import sympy as sp
from oeis_gap_automation import Rational, write_json
from oeis_identification_proofs import parse_record, ff
from oeis_precursive_gate import encode_rat
from oeis_shift_operator_gate import integer_guard, evaluate, ratio_evaluate

x,y,n=sp.symbols('x y n')
K=sp.QQ.frac_field(x)
MAX_X=12; MAX_Y=4; MAX_N=128

def ast_polynomial(s):
    if len(s)>400: raise ValueError('polynomial text budget')
    tree=ast.parse(s.strip().replace('^','**'),mode='eval')
    if len(list(ast.walk(tree)))>100: raise ValueError('AST budget')
    def read(t):
        if isinstance(t,ast.Constant) and type(t.value) is int and abs(t.value)<=10**8:return sp.Integer(t.value)
        if isinstance(t,ast.Name) and t.id in ('x','y'):return {'x':x,'y':y}[t.id]
        if isinstance(t,ast.UnaryOp) and isinstance(t.op,(ast.UAdd,ast.USub)):return (-1 if isinstance(t.op,ast.USub) else 1)*read(t.operand)
        if isinstance(t,ast.BinOp):
            a,b=read(t.left),read(t.right)
            if isinstance(t.op,ast.Add):v=a+b
            elif isinstance(t.op,ast.Sub):v=a-b
            elif isinstance(t.op,ast.Mult):v=a*b
            elif isinstance(t.op,ast.Div) and b.is_Rational and b!=0:v=a/b
            elif isinstance(t.op,ast.Pow) and b.is_Integer and 0<=b<=8:v=a**int(b)
            else:raise ValueError('unsupported polynomial operation')
            p=sp.Poly(v,x,y,domain=sp.QQ)
            if p.degree(x)>MAX_X or p.degree(y)>MAX_Y:raise ValueError('polynomial degree budget')
            return p.as_expr()
        raise ValueError('unsupported AST node')
    return sp.Poly(read(tree.body),x,y,domain=sp.QQ).as_expr()

def equation(statement):
    # A complete equation in the selected source line must explicitly identify
    # the ordinary generating function. Supported literal patterns only.
    s=statement.strip()
    s=re.sub(r'\s+-\s+_[^\n]+$','',s).rstrip('.')
    m=re.fullmatch(r'(?:G\.f\.\s*:|G\.f\.\s+A\(x\)\s+satisfies|The g\.f\.\s+satisfies)\s*(.*)',s,flags=re.I)
    if not m:raise ValueError('not an explicit ordinary GF equation')
    eq=m.group(1)
    # Catalan line also provides a radical expression. Only the explicitly
    # stated polynomial equality after this exact conjunction is used.
    if ', and satisfies ' in eq:eq=eq.split(', and satisfies ',1)[1]
    if eq.count('=')!=1:raise ValueError('ambiguous equation')
    a,b=eq.split('=')
    if not re.search(r'A\(x\)',eq):raise ValueError('missing A(x)')
    p=ast_polynomial(a.replace('A(x)','y'))-ast_polynomial(b.replace('A(x)','y'))
    p=sp.Poly(p,x,y,domain=sp.QQ)
    if p.degree(y)<1:raise ValueError('not algebraic in y')
    return p.as_expr()

def encode_poly(p,vars=(x,y)):
    return [[*map(int,e),str(c)] for e,c in sorted(sp.Poly(p,*vars,domain=sp.QQ).terms())]

def decode_poly(rows,vars=(x,y)):
    if len(rows)>200:raise ValueError('polynomial terms budget')
    p=sp.Integer(0)
    for row in rows:
        if len(row)!=len(vars)+1 or any(type(k) is not int or not 0<=k<=64 for k in row[:-1]):raise ValueError('bad exponent')
        c=Q(row[-1]);p+=sp.Rational(c.numerator,c.denominator)*sp.prod(v**k for v,k in zip(vars,row[:-1]))
    return p

def conv(a,b,N):
    z=[Q(0)]*N
    for i,u in enumerate(a[:N]):
        if u:
            for j,v in enumerate(b[:N-i]):z[i+j]+=u*v
    return z

def coefficient(P,values,k):
    terms=sp.Poly(P,x,y,domain=sp.QQ).terms();d=max(j for (i,j),c in terms)
    powers=[[Q(1)]+[Q(0)]*k]
    for _ in range(d):powers.append(conv(powers[-1],values,k+1))
    return sum((Q(c)*powers[j][k-i] for (i,j),c in terms if i<=k),Q(0))

def branch(P,a0,N):
    if not 1<=N<=MAX_N:raise ValueError('series budget')
    a0=Q(a0); at={x:0,y:sp.Rational(a0.numerator,a0.denominator)}
    slope=Q(sp.diff(P,y).subs(at))
    if P.subs(at)!=0 or not slope:raise ValueError('not a simple formal branch')
    a=[a0]
    # Coefficient of x^k in P(x,A) is slope*a_k plus a known expression.
    for k in range(1,N):a.append(-coefficient(P,a+[Q(0)],k)/slope)
    return a,slope

def differential(P):
    """D=d/dx + (-P_x/P_y)d/dy on Q(x)[y]/(P), P squarefree."""
    mod=sp.Poly(P,y,domain=K);d=mod.degree()
    py=sp.Poly(sp.diff(P,y),y,domain=K)
    inv=sp.invert(py,mod)
    if not (py*inv).rem(mod).is_one:raise ArithmeticError('inverse check')
    dy=(-sp.Poly(sp.diff(P,x),y,domain=K)*inv).rem(mod)
    v=sp.Poly(y,y,domain=K).rem(mod);vs=[v]
    unit=sp.Poly(1,y,domain=K)
    def vector(v):return [v.nth(i) for i in range(d)]
    # Include the constant basis vector. The resulting inhomogeneous operator
    # often has lower differential/recurrence order than a homogeneous one.
    for j in range(d+1):
        if j:
            v=(sp.Poly(sp.diff(v.as_expr(),x),y,domain=K)+v.diff()*dy).rem(mod);vs.append(v)
        M=sp.Matrix.hstack(*[sp.Matrix(vector(w)) for w in [*vs,unit]])
        for null in M.nullspace():
            if not null[-2]:continue
            den=sp.lcm([sp.denom(sp.cancel(c)) for c in null]);polys=[sp.cancel(c*den) for c in null]
            g=sp.gcd_list(polys);polys=[sp.cancel(c/g) for c in polys]
            op=polys[:-1];forcing=-polys[-1]
            rem=(sum((sp.Poly(c,y,domain=K)*w for c,w in zip(op,vs)),sp.Poly(0,y,domain=K))-sp.Poly(forcing,y,domain=K)).rem(mod)
            if not rem.is_zero:raise ArithmeticError('differential residual')
            return {'derivative_of_y':sp.cancel(dy.as_expr()),'operator':op,'forcing':forcing,'degree':d}
    raise ArithmeticError('dimension bound violated')

def coefficient_operator(op,forcing=sp.Integer(0)):
    # For each x^k D^j, [x^t] = (t-k+j)_falling_j a_(t-k+j).
    coeff={}
    for j,p in enumerate(op):
        for (k,),c in sp.Poly(p,x,domain=sp.QQ).terms():
            if not c:continue
            s=j-k
            coeff[s]=coeff.get(s,0)+c*sp.prod(n-k+j-h for h in range(j))
    coeff={s:sp.expand(p) for s,p in coeff.items() if sp.expand(p)!=0}
    lo,hi=min(coeff),max(coeff);d=hi-lo
    # t=n-lo >= 0. Terms with t<k and t-k+j>=0 vanish by a zero
    # falling-factorial factor. All normalized sequence indices are >=n.
    co=[sp.expand(coeff.get(s,sp.Integer(0)).subs(n,n-lo)) for s in range(lo,hi+1)]
    fdeg=int(sp.Poly(forcing,x).degree()) if forcing!=0 else -1
    base=max(0,lo,lo+fdeg+1)
    if not 1<=d<=8:raise ValueError('recurrence order outside supported cap')
    def tup(p):
        p=sp.Poly(p,n,domain=sp.QQ);return tuple(Q(p.nth(i)) for i in range(max(0,p.degree())+1)) if not p.is_zero else (Q(0),)
    # Do not discard common factors without proving the original leading coefficient nonzero.
    lead=tup(co[-1]);guard=integer_guard(lead,base);safe=guard['safe_from']
    c=[Rational(tup(-p),lead).reduce() for p in co[:-1]]
    return {'raw_coefficients':[encode_poly(p,(n,)) for p in co],'base_before_guard':base,'base':safe,'order':d,
            'coefficients':[encode_rat(v) for v in c],'leading_guard':guard,'rats':c}

def algebraic_profile(rec,statement):
    out={'id':rec.oeis_id,'sha256':rec.source_sha256,'offset':rec.offset,'status':'unsupported','definitions':[]}
    lines=[(i,s) for i,s in rec.formulas if s==statement]
    if rec.offset!=0 or not rec.terms or len(lines)!=1:return out
    try:
        P=equation(statement);a,slope=branch(P,rec.terms[0],len(rec.terms))
        if a!=list(map(Q,rec.terms)):
            out['status']='quarantined_contradiction';return out
        df=differential(P);r=coefficient_operator(df['operator'],df['forcing']);b,d=r['base'],r['order']
        if b+d>=len(a):raise ValueError('insufficient checked seeds')
        for i in range(b,len(a)-d):
            if a[i+d]!=sum((ratio_evaluate(c,i)*a[i+j] for j,c in enumerate(r['rats'])),Q(0)):raise ArithmeticError('coefficient recurrence check')
        if d>4:raise ValueError('derived recurrence exceeds Stage 4 interoperability cap')
        dd={'line':lines[0][0],'statement':statement,'base':b,'order':d,'coefficients':r['coefficients'],'initial':[ff(z) for z in a[b:b+d]],'guards':[r['leading_guard']],
            'method':'formal_algebraic_GF_differential_elimination','checked_recurrence_instances':len(a)-d-b}
        out.update(status='conditional_source_definition',definitions=[dd],algebraic={'P':encode_poly(P),'a0':ff(a[0]),'P_y_at_origin':ff(slope),'matched_terms':len(a),'operator':[encode_poly(p,(x,)) for p in df['operator']], 'forcing':encode_poly(df['forcing'],(x,)), 'raw_recurrence':r['raw_coefficients'],'base_before_guard':r['base_before_guard']})
        return out
    except (ValueError,ZeroDivisionError,SyntaxError,sp.NotInvertible) as exc:
        out['reason']=str(exc);return out

def rat_of(a):
    a=sp.cancel(a);u,v=sp.fraction(a)
    return {'num':encode_poly(u,(x,)),'den':encode_poly(v,(x,))}

def gf_transfer(source,target,phi,g,h):
    """Prove T(x)=g(x)S(phi(x))+h(x) by quotient and simple branch uniqueness."""
    if any(p['status']!='conditional_source_definition' or 'algebraic' not in p for p in (source,target)):return None
    A,B=source['algebraic'],target['algebraic'];P=decode_poly(A['P']);R=decode_poly(B['P'])
    phi,g,h=[sp.cancel(z) for z in (phi,g,h)]
    for f in (phi,g,h):
        u,v=sp.fraction(f)
        if not v.subs(x,0) or not f.free_symbols<={x}:return None
        try:sp.Poly(u,x,domain=sp.QQ);sp.Poly(v,x,domain=sp.QQ)
        except (sp.PolynomialError,sp.CoercionFailed):return None
    if phi.subs(x,0)!=0:return None
    a0=sp.Rational(A['a0']);b0=sp.Rational(B['a0'])
    if (g*a0+h).subs(x,0)!=b0:return None
    if phi==0:return None # constant substitution handled elsewhere, not this gate
    M=sp.Poly(P.subs(x,phi),y,domain=K)
    if M.degree()<1:return None
    C=sp.Poly(R.subs(y,g*y+h),y,domain=K)
    if not C.rem(M).is_zero:return None
    return {'source':source['id'],'target':target['id'],'source_sha256':source['sha256'],'target_sha256':target['sha256'],
            'phi':rat_of(phi),'g':rat_of(g),'h':rat_of(h),'branch_value':B['a0'],'evidence':'conditional_exact_algebraic_composition','admission':'conditional_overlay_only',
            'scope':'formal ordinary generating functions over Q[[x]]; selected source equations assumed'}

def verify_composition(edge,source,target):
    try:
        def read(row):return decode_poly(row['num'],(x,))/decode_poly(row['den'],(x,))
        return gf_transfer(source,target,*[read(edge[k]) for k in ('phi','g','h')])==edge
    except (ValueError,KeyError,TypeError,ZeroDivisionError,sp.PolynomialError):return False


def load_records(root,plan):
    from oeis_shift_operator_gate import definitions
    if plan.get('schema')!=1 or len(plan['records'])>64:raise ValueError('plan schema or size budget')
    profiles={}
    for row in plan['records']:
        id=row['id']
        if not re.fullmatch(r'A\d{6}',id) or id in profiles:raise ValueError('bad or duplicate id')
        path=root/'seq'/id[:4]/(id+'.seq');raw=path.read_bytes()
        if 'require_blob_sha1' in row and sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()!=row['require_blob_sha1']:raise ValueError('blob mismatch '+id)
        rec=parse_record(path,root)
        if 'require_blob_sha1' in row and (row['original_formula_line'],row['statement']) not in rec.formulas:raise ValueError('selected formula line mismatch '+id)
        if row['kind']=='algebraic':p=algebraic_profile(rec,row['statement'])
        elif row['kind']=='rational':p=definitions(rec,row['statement'])
        elif row['kind']=='rational_chain':
            # Explicitly selected equalities, each parsed by the existing safe kernel.
            from oeis_identification_proofs import gf_parse
            st=row['statement'];fs=[(i,s) for i,s in rec.formulas if s==st]
            if rec.offset!=0 or len(fs)!=1:raise ValueError('missing selected rational chain')
            ss=re.sub(r'\.\s+_[^\n]+$','.',st);left,right=ss.split(' = ',1)
            a,b=gf_parse(left),gf_parse('G.f.: '+right)
            if a is None or b is None or not a.minus(b).is_zero():raise ValueError('rational chain mismatch')
            from oeis_identification_proofs import series
            from oeis_shift_operator_gate import const
            d=len(a.den)-1
            p={'id':id,'sha256':rec.source_sha256,'offset':rec.offset,'status':'quarantined_contradiction','definitions':[]}
            if 1<=d<=4 and series(a.num,a.den,len(rec.terms))==list(map(Q,rec.terms)):
                base=max(0,len(a.num)-d);p.update(status='conditional_source_definition',definitions=[{'line':fs[0][0],'statement':st,'base':base,'order':d,'coefficients':[encode_rat(const(-a.den[d-j]/a.den[0])) for j in range(d)],'initial':[ff(v) for v in rec.terms[base:base+d]],'guards':[],'method':'rational_OGF_chain_identity'}])
        else:raise ValueError('unknown source type')
        profiles[id]=p
    return profiles


def family_normal_form(profile):
    """Recognize A = 1 + u(x) A + v(x) A^d and derive a Fuss-Catalan transfer.

    Formal theorem: if u(0)=v(0)=0, d>=2, then B=(1-u)A obeys
    B=1+v/(1-u)^d * B^d. The simple formal branch is unique.
    """
    if profile['status']!='conditional_source_definition' or 'algebraic' not in profile:return None
    P=decode_poly(profile['algebraic']['P']);p=sp.Poly(P,y);d=p.degree()
    q=p.nth(0)
    if not 2<=d<=MAX_Y or not q.is_Rational or not q or profile['algebraic']['a0']!='1':return None
    # Normalize P so the constant term is -1.
    p=sp.Poly(-P/q,y)
    if any(p.nth(j)!=0 for j in range(2,d)):return None
    u=sp.expand(1-p.nth(1));v=sp.expand(-p.nth(d))
    if u.subs(x,0)!=0 or v.subs(x,0)!=0 or v==0:return None
    g=1/(1-u);phi=sp.cancel(v/(1-u)**d)
    # Check the universal substitution polynomial identity, not just terms.
    normalized=sp.expand(-P/q)
    universal=y-1-phi*y**d
    if sp.cancel(normalized.subs(y,g*y)-universal)!=0:raise ArithmeticError('Fuss-Catalan normal form residual')
    data={'target':profile['id'],'target_sha256':profile['sha256'],'degree':d,'u':encode_poly(u,(x,)),'v':encode_poly(v,(x,)),
          'g':rat_of(g),'phi':rat_of(phi),'residual':'0','evidence':'conditional_exact_fuss_catalan_family_transfer',
          'admission':'conditional_overlay_only','scope':'formal branch A(0)=1; u(0)=v(0)=0'}
    up,vp=sp.Poly(u,x),sp.Poly(v,x)
    if up.degree()<=1 and len(vp.terms())==1:
        (s,),b=vp.terms()[0];a=up.nth(1)
        if s>=1:data['finite_sum_parameters']={'a':str(a),'b':str(b),'s':int(s),'d':int(d)}
    return data


def family_term(parameters,n):
    if type(n) is not int or not 0<=n<=MAX_N:raise ValueError('finite sum budget')
    a,b=Q(parameters['a']),Q(parameters['b']);s,d=parameters['s'],parameters['d']
    if not 1<=s<=MAX_X or not 2<=d<=MAX_Y:raise ValueError('family parameter budget')
    # [z^k]F_d(z)=1/((d-1)k+1)*binomial(dk,k), by Lagrange inversion.
    return sum((Q(comb(d*k,k),(d-1)*k+1)*b**k*a**(n-s*k)*comb(n-s*k+d*k,d*k) for k in range(n//s+1)),Q(0))


def audit(root,plan):
    from oeis_joint_transfer_gate import discover_joint,verify_joint,spectral_cover_jobs
    profiles=load_records(root,plan);edges=[];families=[]
    for p in profiles.values():
        f=family_normal_form(p)
        if f is not None:families.append(f)
    spectral_jobs=spectral_cover_jobs(profiles) if plan.get('auto_spectral_covers',False) else []
    jobs=plan.get('joint_jobs',[])+spectral_jobs
    seen=set()
    for job in jobs:
        key=(tuple(sorted(zip(job['sources'],map(tuple,job['lanes'])))),job['target'])
        if key in seen:continue
        seen.add(key)
        ss=[profiles[i] for i in job['sources']];t=profiles[job['target']]
        e=discover_joint(ss,t,job['lanes'],job.get('max_degree',1))
        if e is not None:
            if not verify_joint(e,ss,t):raise ArithmeticError('joint replay')
            edges.append(e)
    # Small exact template search, not a complete rational-composition solver.
    substitutions=[x,x**2/(1-x)**2,x/(1-x)**2,x**2/(1+x)**2,x/(1+x)**2,2*x/(1+x)**2]
    prefactors=[sp.Integer(1),1/(1-x),1/(1+x),1+x,1-x]
    gf=[]
    for a,b in plan.get('composition_pairs',[]):
        for phi in substitutions:
            for g in prefactors:
                e=gf_transfer(profiles[a],profiles[b],phi,g,sp.Integer(0))
                if e:
                    if not verify_composition(e,profiles[a],profiles[b]):raise ArithmeticError('composition replay')
                    gf.append(e)
    return {'schema':1,'author':'Komorebi P.','origin':plan.get('origin'),'scope':'conditional overlay only; no OEIS claim promotion','profiles':profiles,'spectral_cover_jobs':spectral_jobs,'joint_edges':edges,'composition_edges':gf,'family_normal_forms':families,'summary':{'records':len(profiles),'conditional_profiles':sum(p['status']=='conditional_source_definition' for p in profiles.values()),'algebraic_profiles':sum('algebraic' in p for p in profiles.values()),'joint_certificates':len(edges),'spectral_cover_jobs':len(spectral_jobs),'composition_certificates':len(gf),'family_normal_forms':len(families),'finite_sum_normal_forms':sum('finite_sum_parameters' in f for f in families)}}

def main():
    import argparse
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--oeis-root',type=Path,required=True);ap.add_argument('--plan',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--verify-report',action='store_true');a=ap.parse_args()
    result=audit(a.oeis_root,json.loads(a.plan.read_text()))
    if a.verify_report:
        if result!=json.loads(a.output.read_text()):raise SystemExit('source-bound report mismatch')
    else:write_json(a.output,result)
    print(json.dumps(result['summary'],indent=2))
if __name__=='__main__':main()
