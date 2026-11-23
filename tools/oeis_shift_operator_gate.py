#!/usr/bin/env python3
"""Source-bound affine-lane recurrence intertwiners over Q(n).

Author: Komorebi P.
No OEIS formula is executed. Exact identities are conditional on the selected
source definitions and seeds. No finite fit is promoted to an infinite proof.
"""
from __future__ import annotations
import argparse
import ast
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from math import ceil
from pathlib import Path
import json
import re

from oeis_gap_automation import Rational, trim, mul, divmod_poly, pgcd, write_json
from oeis_identification_proofs import parse_record, gf_parse, series, poly_shift, ff, strip_end_annotation
from oeis_hypergeometric_gate import sign_certificate, ratio_evaluate, evaluate
from oeis_precursive_gate import _linear_ast, encode_rat, decode_rat

MAX_ORDER=4
MAX_STRIDE=4
MAX_DEGREE=3
MAX_TERMS=256
MAX_GUARD_SCAN=1024
MAX_SHIFT=32
Z=Rational.constant(Q(0))
ONE=Rational.constant(Q(1))
TERM=re.compile(r'\ba\(\s*n\s*(?P<delta>[+-]\s*\d+)?\s*\)',re.I)
BOUND=re.compile(r',\s*(?:for\s+)?n\s*(>=|>)\s*([+-]?\d+)\s*$',re.I)


def const(x): return Rational.constant(Q(x))
def sumrat(items):
    out=Z
    for x in items: out=out.plus(x)
    return out


def affine(p, m, r):
    return trim(v*Q(m)**k for k,v in enumerate(poly_shift(p,r)))


def compose(f,m,r):
    return Rational(affine(f.num,m,r),affine(f.den,m,r)).reduce()


def integer_guard(poly,base):
    """Exact integer-root exclusion. If needed, isolate a finite bad prefix.

    First try a shifted coefficient-sign certificate. Otherwise use the
    Cauchy root bound |z| <= 1+max |p_i/p_d| and enumerate integer candidates.
    Refuse expensive bounds; do not infer nonvanishing from samples.
    """
    poly=trim(poly)
    if not any(poly): raise ValueError('identically zero guard')
    signed=sign_certificate(poly,base)
    if signed is not None:
        return {'polynomial':list(map(ff,poly)),'from':base,'safe_from':base,
                'excluded_integer_roots':[],'proof':signed}
    bound=ceil(1+max((abs(v/poly[-1]) for v in poly[:-1]),default=Q(0)))
    lo=max(base,-bound)
    if max(0,bound-lo+1)>MAX_GUARD_SCAN: raise ValueError('integer-root budget')
    roots=[n for n in range(lo,bound+1) if not evaluate(poly,n)]
    return {'polynomial':list(map(ff,poly)),'from':base,
            'safe_from':max(base,max(roots,default=base-1)+1),
            'excluded_integer_roots':roots,
            'proof':{'method':'Cauchy_bound_and_exact_integer_root_scan','absolute_bound':bound}}


def original_division_guards(tree,terms):
    """Track raw denominators before rational cancellation (including nested ones)."""
    from oeis_gap_automation import parse_safe_rhs
    guards=[]
    if len(list(ast.walk(tree)))>180: raise ValueError('AST budget')
    for node in ast.walk(tree):
        if isinstance(node,ast.BinOp) and isinstance(node.op,ast.Div):
            if any(isinstance(x,ast.Name) and x.id in terms for x in ast.walk(node.right)):
                raise ValueError('sequence denominator')
            value=parse_safe_rhs(ast.unparse(node.right))
            if value.is_zero(): raise ValueError('zero raw denominator')
            guards.extend((value.num,value.den))
    return guards


def equation(raw,offset):
    """Normalize a homogeneous linear source equation, including backward shifts.

    Domains are in the original OEIS index, not ordinal positions. The supplied
    equation, when no bound is written, is assumed on the natural defined tail.
    Unsupported annotations are rejected rather than silently discarded.
    """
    s=strip_end_annotation(raw)
    if len(s)>480: return None
    s=re.sub(r'^(?:D-finite with )?[Rr]ecurrence\s*:\s*','',s)
    b=BOUND.search(s); declared=None
    if b:
        declared=int(b[2])+(b[1]=='>');s=s[:b.start()].strip()
    if s.count('=')!=1 or any(x in s for x in (';', '[', ']', '{','}')): return None
    terms={}
    def replace(mt):
        k=int(re.sub(r'\s+','',mt['delta'] or '0'))
        if abs(k)>MAX_SHIFT: raise ValueError('shift budget')
        key='__term_'+str(k+MAX_SHIFT);terms[key]=k;return key
    try:
        lhs,rhs=map(str.strip,s.split('='))
        left=ast.parse(TERM.sub(replace,lhs).replace('^','**'),mode='eval').body
        right=ast.parse(TERM.sub(replace,rhs).replace('^','**'),mode='eval').body
        if len(set(terms.values()))<2:return None
        rawguards=original_division_guards(left,terms)+original_division_guards(right,terms)
        a,u=_linear_ast(left,terms);b,v=_linear_ast(right,terms)
        if not u.minus(v).is_zero():return None
        co={k:a.get(k,Z).minus(b.get(k,Z)) for k in set(a)|set(b)}
        # Retain the smallest written index even when its coefficient cancels.
        lo=min(terms.values());hi=max(terms.values());d=hi-lo
        if not 1<=d<=MAX_ORDER or co.get(hi,Z).is_zero():return None
        lead=co[hi];rawguards.extend((lead.num,lead.den))
        coeff=[compose(Z.minus(co.get(j,Z)).over(lead),1,-lo) for j in range(lo,hi)]
        rawguards=[affine(p,1,-lo) for p in rawguards]+[x.den for x in coeff]
        start=max(offset,declared+lo if declared is not None else offset)
        if not -1000<=start<=1000:return None
        return {'coeff':coeff,'natural_from':start,'guard_polynomials':tuple(dict.fromkeys(rawguards)),
                'method':'explicit_linear_recurrence','declared_original_bound':declared,
                'original_min_shift':lo,'statement':raw}
    except (ValueError,ZeroDivisionError,SyntaxError,OverflowError,RecursionError):return None


def definitions(rec,statement=None):
    """Select source premises; explicit selectors are exact %F text, not guesses."""
    out={'id':rec.oeis_id,'sha256':rec.source_sha256,'path':rec.source_path,'offset':rec.offset,
         'status':'unsupported','definitions':[],'rejected':[]}
    if rec.offset is None or not rec.terms:return out
    for line,raw in rec.formulas:
        if statement is not None and raw!=statement:continue
        try:
            op=equation(raw,rec.offset)
            if op is None and rec.offset==0:
                gf=gf_parse(raw)
                if gf is not None and gf.den[0] and 1<=len(gf.den)-1<=MAX_ORDER:
                    d=len(gf.den)-1
                    if series(gf.num,gf.den,len(rec.terms))!=list(map(Q,rec.terms)):
                        out['rejected'].append({'line':line,'reason':'source_OGF_contradicts_terms'});continue
                    op={'coeff':[const(-gf.den[d-j]/gf.den[0]) for j in range(d)],
                        'natural_from':max(0,len(gf.num)-d),'guard_polynomials':((Q(1),),),
                        'method':'rational_OGF_coefficient_identity','statement':raw,
                        'rational_ogf':encode_rat(gf)}
            if op is None:continue
            guards=[integer_guard(p,op['natural_from']) for p in op['guard_polynomials']]
            base=max([op['natural_from']]+[g['safe_from'] for g in guards]);d=len(op['coeff'])
            stop=rec.offset+len(rec.terms)-d
            # Check *every* reported nonsingular instance, including those before
            # the new safe tail. Initial conditions never bridge an actual pole.
            mismatch=None;checked=0
            for n in range(op['natural_from'],stop):
                if any(not evaluate(p,n) for p in op['guard_polynomials']):continue
                i=n-rec.offset
                if Q(rec.terms[i+d])!=sum((ratio_evaluate(c,n)*rec.terms[i+j] for j,c in enumerate(op['coeff'])),Q(0)):
                    mismatch=n;break
                checked+=1
            if mismatch is not None:
                out['rejected'].append({'line':line,'reason':'recurrence_contradicts_terms','index':mismatch});continue
            if base-rec.offset<0 or base+d>=rec.offset+len(rec.terms):continue
            data={k:v for k,v in op.items() if k not in ('coeff','guard_polynomials')}
            data.update({'line':line,'base':base,'order':d,'coefficients':[encode_rat(x) for x in op['coeff']],
                         'initial':[ff(x) for x in rec.terms[base-rec.offset:base-rec.offset+d]],
                         'guards':guards,'checked_recurrence_instances':checked})
            out['definitions'].append(data)
        except (ValueError,ZeroDivisionError,OverflowError,RecursionError):continue
    if out['rejected']:out['status']='quarantined_contradiction';return out
    if out['definitions']:
        out['status']='conditional_source_definition'
        # If no selector, only auto-admit identical normalized operators/seeds.
        signature=lambda p:(p['base'],tuple(p['initial']),json.dumps(p['coefficients'],sort_keys=True))
        if len({signature(p) for p in out['definitions']})>1:
            out['status']='multiple_source_premises_require_selector'
    return out


def terms_at(defn,n):
    d=defn['order'];b=defn['base'];i=n-b
    if not 0<=i<MAX_TERMS:raise ValueError('seed evaluation budget')
    v=list(map(Q,defn['initial']));c=list(map(decode_rat,defn['coefficients']))
    while len(v)<=i:
        k=len(v)-d
        v.append(sum((ratio_evaluate(c[j],b+k)*v[k+j] for j in range(d)),Q(0)))
    return v[i]


def lane_base(s,t,m,r):
    if not 1<=m<=MAX_STRIDE or abs(r)>MAX_SHIFT:raise ValueError('lane budget')
    return max(t['base'],-((r-s['base'])//m))


def state_rows(s,t,m,r):
    """Each v[i] expresses S(m*n+r+i) in the initial order-d source state."""
    d=s['order'];e=t['order'];c=list(map(decode_rat,s['coefficients']))
    rows=[[const(i==j) for j in range(d)] for i in range(d)]
    for i in range(d,m*e+d):
        k=i-d;cc=[compose(x,m,r+k) for x in c]
        rows.append([sumrat(cc[j].times(rows[k+j][h]) for j in range(d)) for h in range(d)])
    return rows


def output_row(g,v,m,k):
    return [sumrat(compose(g[j],1,k).times(v[m*k+j][h]) for j in range(len(g))) for h in range(len(g))]


def residual(s,t,m,r,g,v=None):
    v=v if v is not None else state_rows(s,t,m,r)
    e=t['order'];c=list(map(decode_rat,t['coefficients']))
    rows=[output_row(g,v,m,k) for k in range(e+1)]
    return [rows[e][h].minus(sumrat(c[k].times(rows[k][h]) for k in range(e))) for h in range(s['order'])]


def solve(rows,rhs,k):
    """Exact rectangular affine system; free coordinates canonically zero."""
    A=[list(row)+[b] for row,b in zip(rows,rhs)];p=[]
    for j in range(k):
        i=next((i for i in range(len(p),len(A)) if A[i][j]),None)
        if i is None:continue
        u=len(p);A[u],A[i]=A[i],A[u];a=A[u][j];A[u]=[x/a for x in A[u]]
        for i,row in enumerate(A):
            if i!=u and row[j]:A[i]=[x-row[j]*y for x,y in zip(row,A[u])]
        p.append(j)
    if any(not any(row[:-1]) and row[-1] for row in A):return None
    out=[Q(0)]*k
    for i,j in enumerate(p):out[j]=A[i][-1]
    return out,len(p)


def clear_columns(cols):
    """Clear a single rational row symbolically; equate *all* coefficients."""
    den=(Q(1),)
    for c in cols:
        gcd=pgcd(den,c.den);q,rem=divmod_poly(c.den,gcd)
        if any(rem):raise ArithmeticError('LCM remainder')
        den=mul(den,q)
        if len(den)>96:raise ValueError('symbolic denominator budget')
    p=[]
    for c in cols:
        q,rem=divmod_poly(den,c.den)
        if any(rem):raise ArithmeticError('denominator remainder')
        p.append(mul(c.num,q))
    return [[c[i] if i<len(c) else Q(0) for c in p] for i in range(max(map(len,p)))]


def determinant(A):
    from itertools import permutations
    d=len(A);det=Z
    for p in permutations(range(d)):
        z=const((-1)**sum(p[i]>p[j] for i in range(d) for j in range(i+1,d)))
        for i,j in enumerate(p):z=z.times(A[i][j])
        det=det.plus(z)
    return det


def certificate(source,target,m,r,g):
    """Independent checker for any rational coefficient operator in the cap."""
    if any(p['status']!='conditional_source_definition' for p in (source,target)):return None
    s,t=source['definitions'][0],target['definitions'][0]
    if len(g)!=s['order'] or all(c.is_zero() for c in g):return None
    base=lane_base(s,t,m,r)
    guards=[integer_guard(c.den,base) for c in g]
    base=max([base]+[p['safe_from'] for p in guards])
    v=state_rows(s,t,m,r)
    rem=residual(s,t,m,r,g,v)
    if any(not c.is_zero() for c in rem):return None
    seeds=[]
    for n in range(base,base+t['order']):
        a=sum((ratio_evaluate(c,n)*terms_at(s,m*n+r+j) for j,c in enumerate(g)),Q(0));b=terms_at(t,n)
        if a!=b:return None
        seeds.append({'index':n,'value':ff(b)})
    # State-reconstruction determinant for equal-dimensional source/target.
    # A nonsingular matrix certifies exact pointwise recovery of source state,
    # not inverse integer-lattice or finite precision recovery.
    det_receipt=None
    if s['order']==t['order']:
        try:
            d=s['order'];A=[output_row(g,v,m,k) for k in range(d)]
            det=determinant(A)
            if not det.is_zero():
                dg=integer_guard(det.num,base);dd=integer_guard(det.den,base)
                B=[]
                for i in range(d):
                    B.append([const((-1)**(i+j)).times(determinant(
                        [[A[row][col] for col in range(d) if col!=i] for row in range(d) if row!=j])).over(det)
                              for j in range(d)])
                if any(not sumrat(B[i][k].times(A[k][j]) for k in range(d)).minus(const(i==j)).is_zero()
                       for i in range(d) for j in range(d)):
                    raise ArithmeticError('state matrix inverse check failed')
                bg=[integer_guard(x.den,base) for row in B for x in row]
                det_receipt={'determinant':encode_rat(det),'recovery_from':max(g['safe_from'] for g in [dg,dd]+bg),
                             'guards':[dg,dd]+bg,'inverse_matrix':[[encode_rat(x) for x in row] for row in B],
                             'scope':'exact rational state recovery only'}
        except (ValueError,ZeroDivisionError):
            # Failure to certify optional recovery cannot invalidate a proved
            # forward relation. None means no recovery certificate, not loss.
            pass
    return {'source':source['id'],'target':target['id'],'source_sha256':source['sha256'],'target_sha256':target['sha256'],
            'source_line':s['line'],'target_line':t['line'],'stride':m,'residue_or_offset':r,'valid_from':base,
            'source_order':s['order'],'target_order':t['order'],'coefficients':[encode_rat(c) for c in g],
            'operator_denominator_guards':guards,'zero_residual':[encode_rat(c) for c in rem],
            'initial_equalities':seeds,'rational_state_recovery':det_receipt,
            'evidence':'conditional_exact_affine_lane_intertwiner','admission':'conditional_overlay_only',
            'domain':'all integer n >= valid_from; no prefix, OEIS truth, integrality of inverse, or speedup implied'}


def discover(source,target,m,r,max_degree=MAX_DEGREE):
    """Complete for each polynomial-degree ansatz within the fixed lane/state.

    No numerical guess is needed: construct exact rational residual equations,
    clear their denominators, and append the target initial conditions.
    """
    if not 0<=max_degree<=MAX_DEGREE:raise ValueError('degree budget')
    if any(p['status']!='conditional_source_definition' for p in (source,target)):return None
    s,t=source['definitions'][0],target['definitions'][0];d=s['order'];e=t['order']
    base=lane_base(s,t,m,r);v=state_rows(s,t,m,r)
    # Work in powers of n-base to control coefficient growth.
    for deg in range(max_degree+1):
        basis=[];coordinates=[]
        for j in range(d):
            for k in range(deg+1):
                p=affine(tuple([Q(0)]*k+[Q(1)]),1,-base)
                g=[Z]*d;g[j]=Rational(p,(Q(1),));basis.append(g);coordinates.append((j,k))
        residues=[residual(s,t,m,r,g,v) for g in basis];N=len(basis)
        rows=[]
        for h in range(d):rows.extend(clear_columns([a[h] for a in residues]))
        rhs=[Q(0)]*len(rows)
        for n in range(base,base+e):
            rows.append([Q(n-base)**k*terms_at(s,m*n+r+j) for j,k in coordinates]);rhs.append(terms_at(t,n))
        solved=solve(rows,rhs,N)
        if solved is None:continue
        weights,rank=solved;g=[sumrat(const(w).times(b[j]) for w,b in zip(weights,basis)) for j in range(d)]
        result=certificate(source,target,m,r,g)
        if result is None:continue
        result['discovery']={'basis':'polynomials in n-valid_from','degree':deg,'unknowns':N,'rank':rank,'nullity':N-rank}
        return result
    return None


def verify_certificate(edge,source,target):
    """Replay the algebra/guards/seeds independently of the search algorithm."""
    try:
        got=certificate(source,target,edge['stride'],edge['residue_or_offset'],list(map(decode_rat,edge['coefficients'])))
        return got is not None and got=={k:v for k,v in edge.items() if k!='discovery'}
    except (ValueError,KeyError,TypeError,OverflowError,ZeroDivisionError):return False


def inverse_operator(source,target,edge):
    """Recover a stride-one inverse from the proved square state matrix.

    Compute its first adjugate row, not a finite fit; the reversed recurrence
    obligations and its own seeds must still pass the independent checker.
    """
    if edge['stride']!=1 or edge['rational_state_recovery'] is None:return None
    s,t=source['definitions'][0],target['definitions'][0];r=edge['residue_or_offset'];d=s['order']
    g=list(map(decode_rat,edge['coefficients']));v=state_rows(s,t,1,r)
    A=[output_row(g,v,1,k) for k in range(d)];det=determinant(A)
    inv=[]
    for j in range(d):
        minor=[[A[i][k] for k in range(1,d)] for i in range(d) if i!=j]
        inv.append(compose(const((-1)**j).times(determinant(minor)).over(det),1,-r))
    result=certificate(target,source,1,-r,inv)
    if result is not None:result['discovery']={'basis':'exact_state_matrix_inverse','forward_source':source['id'],
                                               'forward_target':target['id'],'forward_offset':r}
    return result


def plan_from_queue(root,queue,max_leads=40):
    """Convert ranked lexical leads into a bounded, deterministic proof plan.

    Missing records are retained as acquisition gaps. Neither queue priority
    nor mere source availability is evidence of an identity.
    """
    if not 1<=max_leads<=64:raise ValueError('lead budget')
    pairs=[];ids=set();missing=[];seen=set();used=0
    for bucket in ('cross_component','new_id_frontier','outside_to_network','in_component'):
        rows=queue.get('queues',{}).get(bucket,[])
        for row in sorted(rows,key=lambda r:(-r['priority_score'],-r['mentions'],r['from'],r['to'])):
            a,b=row['from'],row['to']
            if not all(re.fullmatch(r'A\d{6}',v) for v in (a,b)) or a==b:continue
            key=tuple(sorted((a,b)))
            if key in seen:continue
            seen.add(key)
            absent=[v for v in key if not (root/'seq'/v[:4]/(v+'.seq')).is_file()]
            if absent:
                missing.append({'pair':list(key),'missing_ids':absent,'bucket':bucket});continue
            ids.update(key);pairs.extend([[a,b],[b,a]]);used+=1
            if used>=max_leads:break
        if used>=max_leads:break
    return {'schema':1,'records':[{'id':v} for v in sorted(ids)],'pairs':pairs,
            'lanes':[[1,0],[2,0],[2,1]],'max_degree':2,'queue_metadata':{
                'source_queue_sha256':sha256(json.dumps(queue,sort_keys=True).encode()).hexdigest(),
                'selected_undirected_leads':used,'missing_source_leads':missing,
                'status':'lexical_leads_only'}}


def valuation(x,p):
    if not x:return None
    a,b=abs(x.numerator),x.denominator;v=0
    while a%p==0:a//=p;v+=1
    while b%p==0:b//=p;v-=1
    return v


def local_precision(source,target,edge,n,p,k):
    """Exact local Smith exponents over Z_p at one certified index.

    Assumes arbitrary p-adically integral input state. A rational matrix need
    not define a map modulo p^k; reject coefficients with negative valuation.
    This is a state-information bound, not a runtime or sequence-wide claim.
    """
    from math import isqrt
    if not 2<=p<=10000 or any(p%i==0 for i in range(2,isqrt(p)+1)) or not 1<=k<=10000:
        raise ValueError('prime/precision budget')
    if n<edge['valid_from'] or abs(n)>1000000 or not verify_certificate(edge,source,target):
        raise ValueError('invalid certified index or edge')
    s,t=source['definitions'][0],target['definitions'][0];m=edge['stride'];r=edge['residue_or_offset']
    g=list(map(decode_rat,edge['coefficients']));v=state_rows(s,t,m,r)
    M=[[ratio_evaluate(x,n) for x in output_row(g,v,m,j)] for j in range(t['order'])]
    A=[row[:] for row in M];a,b=t['order'],s['order']
    if any(x and valuation(x,p)<0 for row in A for x in row):raise ValueError('matrix not p-integral')
    exponents=[]
    for j in range(min(a,b)):
        candidates=[(valuation(A[u][w],p),u,w) for u in range(j,a) for w in range(j,b) if A[u][w]]
        if not candidates:break
        e,u,w=min(candidates);A[j],A[u]=A[u],A[j]
        for row in A:row[j],row[w]=row[w],row[j]
        pivot=A[j][j]
        # All row/column multipliers are p-integral by minimum valuation.
        for u in range(j+1,a):
            c=A[u][j]/pivot
            for w in range(j,b):A[u][w]-=c*A[j][w]
        for w in range(j+1,b):
            c=A[j][w]/pivot
            for u in range(j,a):A[u][w]-=c*A[u][j]
        exponents.append(e)
    rank=len(exponents);loss=sum(min(x,k) for x in exponents)+(b-rank)*k
    return {'source':edge['source'],'target':edge['target'],'index':n,'prime':p,'precision':k,
            'matrix':[[ff(x) for x in row] for row in M],'smith_exponents':exponents,
            'input_dimension':b,'output_dimension':a,'rank':rank,'kernel_fiber_log_p':loss,
            'full_input_recovery_possible':rank==b,
            'minimum_output_precision_for_input_mod_p_to_k':k+max(exponents,default=0) if rank==b else None,
            'scope':'arbitrary Z_p input state at this index; no sequence-specific or uniform-in-index precision claim'}


def audit(root,manifest):
    """Bounded plan from cross-reference candidates, or all selected pairs."""
    if manifest.get('schema')!=1:raise ValueError('plan schema')
    records=manifest['records'];lanes=manifest.get('lanes',[[1,0],[2,0],[2,1]])
    if len(records)>128 or len(lanes)>12:raise ValueError('record/lane budget')
    profiles={}
    for row in records:
        id_=row['id']
        if not re.fullmatch(r'A\d{6}',id_) or id_ in profiles:raise ValueError('duplicate or invalid ID')
        path=root/'seq'/id_[:4]/(id_+'.seq');rec=parse_record(path,root)
        if 'git_blob_sha1' in row:
            from hashlib import sha1
            raw=path.read_bytes();h=sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
            if h!=row['git_blob_sha1']:raise ValueError('pinned Git blob mismatch: '+id_)
        if 'git_blob_sha1' in row and 'original_formula_line' in row:
            if (row['original_formula_line'],row.get('statement')) not in rec.formulas:
                raise ValueError('pinned formula line mismatch: '+id_)
        profiles[id_]=definitions(rec,row.get('statement'))
    pairs=manifest.get('pairs',[[a,b] for a in profiles for b in profiles if a!=b]);edges=[];blocked=[];tried=0
    if len(pairs)*len(lanes)>2000:raise ValueError('pair budget')
    for a,b in pairs:
        if a==b:continue
        for m,r in lanes:
            tried+=1
            try:
                e=discover(profiles[a],profiles[b],m,r,manifest.get('max_degree',2))
                if e is not None:edges.append(e)
            except (ValueError,ZeroDivisionError,OverflowError) as ex:blocked.append({'source':a,'target':b,'lane':[m,r],'reason':str(ex)})
    # Rational inverses may lie outside the polynomial discovery ansatz. Only
    # add missing directions, and only for an explicitly allowed plan lane/pair.
    keys={(x['source'],x['target'],x['stride'],x['residue_or_offset']) for x in edges}
    allowed_pairs={tuple(p) for p in pairs};allowed_lanes={tuple(l) for l in lanes}
    for e in list(edges):
        key=(e['target'],e['source'],1,-e['residue_or_offset'])
        if key in keys or key[:2] not in allowed_pairs or key[2:] not in allowed_lanes:continue
        try:
            inv=inverse_operator(profiles[e['source']],profiles[e['target']],e)
            if inv is not None:edges.append(inv);keys.add(key)
        except (ValueError,ZeroDivisionError,OverflowError) as ex:
            blocked.append({'source':key[0],'target':key[1],'lane':list(key[2:]),'reason':'inverse: '+str(ex)})
    if any(not verify_certificate(e,profiles[e['source']],profiles[e['target']]) for e in edges):
        raise ArithmeticError('independent certificate replay failed')
    return {'schema':1,'author':'Komorebi P.','scope':'source-bound conditional certificates, never graph promotion',
            'plan_sha256':sha256(json.dumps(manifest,sort_keys=True).encode()).hexdigest(),
            'corpus_kind':manifest.get('corpus_kind','synthetic_or_local_source_records'),
            'source_origin':manifest.get('origin'),
            'summary':{'records':len(profiles),'status_counts':dict(Counter(p['status'] for p in profiles.values())),
                       'candidate_lane_pairs':tried,'conditional_certificates':len(edges),
                       'polyphase_certificates':sum(x['stride']>1 for x in edges),
                       'nonconstant_coefficients':sum(any(len(c['num'])>1 or len(c['den'])>1 for c in x['coefficients']) for x in edges),
                       'recoverable_state_certificates':sum(x['rational_state_recovery'] is not None for x in edges),
                       'inverse_derived_certificates':sum(x['discovery']['basis']=='exact_state_matrix_inverse' for x in edges),
                       'budget_blocked':len(blocked),'unconditional_OEIS_identifications':0},
            'profiles':profiles,'edges':edges,'blocked':blocked}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--oeis-root',type=Path,required=True)
    choose=ap.add_mutually_exclusive_group(required=True);choose.add_argument('--plan',type=Path);choose.add_argument('--queue',type=Path)
    ap.add_argument('--max-leads',type=int,default=40);ap.add_argument('--save-plan',type=Path)
    ap.add_argument('--output',type=Path,required=True);ap.add_argument('--verify-report',action='store_true');a=ap.parse_args()
    plan=json.loads(a.plan.read_text()) if a.plan else plan_from_queue(a.oeis_root,json.loads(a.queue.read_text()),a.max_leads)
    if a.save_plan:write_json(a.save_plan,plan)
    out=audit(a.oeis_root,plan)
    if a.verify_report:
        if json.loads(a.output.read_text())!=out:raise SystemExit('source-bound exact replay mismatch')
    else:write_json(a.output,out)
    print(json.dumps(out['summary'],indent=2))

if __name__=='__main__':main()
