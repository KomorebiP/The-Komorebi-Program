"""Direct-sum recurrence-state transfer discovery and exact certificate replay.
Author: Komorebi P.
"""
from fractions import Fraction as Q
from oeis_shift_operator_gate import (Z,const,sumrat,affine,lane_base,state_rows,residual,
    clear_columns,solve,terms_at,integer_guard,ratio_evaluate)
from oeis_gap_automation import Rational
from oeis_precursive_gate import encode_rat,decode_rat
from oeis_identification_proofs import ff


def prepare(sources,target,lanes):
    if not 2<=len(sources)<=4 or len(sources)!=len(lanes):raise ValueError('joint arity budget')
    if len({(s['id'],tuple(l)) for s,l in zip(sources,lanes)})!=len(sources):raise ValueError('duplicate input lane')
    if any(p['status']!='conditional_source_definition' for p in [*sources,target]):return None
    s=[p['definitions'][0] for p in sources];t=target['definitions'][0]
    if sum(p['order'] for p in s)>12:raise ValueError('state dimension budget')
    base=max(lane_base(p,t,m,r) for p,(m,r) in zip(s,lanes))
    return s,t,base


def joint_certificate(sources,target,lanes,gs):
    q=prepare(sources,target,lanes)
    if q is None:return None
    s,t,base=q
    if len(gs)!=len(s) or any(len(g)!=p['order'] for p,g in zip(s,gs)):return None
    if any(all(c.is_zero() for c in g) for g in gs):return None # truly uses every supplied lane
    guards=[integer_guard(c.den,base) for g in gs for c in g];base=max([base]+[p['safe_from'] for p in guards])
    rr=[residual(p,t,m,r,g) for p,(m,r),g in zip(s,lanes,gs)]
    if any(not z.is_zero() for row in rr for z in row):return None
    seeds=[]
    for n in range(base,base+t['order']):
        parts=[sum((ratio_evaluate(c,n)*terms_at(p,m*n+r+j) for j,c in enumerate(g)),Q(0)) for p,(m,r),g in zip(s,lanes,gs)]
        v=terms_at(t,n)
        if sum(parts,Q(0))!=v:return None
        seeds.append({'n':n,'summands':list(map(ff,parts)),'target':ff(v)})
    return {'sources':[{'id':p['id'],'sha256':p['sha256'],'line':v['line'],'lane':list(l),'coefficients':[encode_rat(c) for c in g]} for p,v,l,g in zip(sources,s,lanes,gs)],
            'target':target['id'],'target_sha256':target['sha256'],'target_line':t['line'],'valid_from':base,'guards':guards,
            'residuals':[[encode_rat(v) for v in row] for row in rr],'initial_equalities':seeds,'evidence':'conditional_exact_joint_direct_sum_intertwiner','admission':'conditional_overlay_only'}


def discover_joint(sources,target,lanes,max_degree=2):
    """Complete linear ansatz for direct-sum residual plus target initial state.
    Activate zero input blocks by moving along the exact homogeneous nullspace.
    Completeness is restricted to the specified direct-sum polynomial ansatz.
    """
    if not 0<=max_degree<=3:raise ValueError('degree budget')
    q=prepare(sources,target,lanes)
    if q is None:return None
    s,t,base=q;vs=[state_rows(p,t,m,r) for p,(m,r) in zip(s,lanes)]
    for deg in range(max_degree+1):
        cols=[];coordinates=[]
        for i,(p,(m,r),v) in enumerate(zip(s,lanes,vs)):
            for j in range(p['order']):
                for k in range(deg+1):
                    g=[Z]*p['order'];g[j]=Rational(affine(tuple([Q(0)]*k+[Q(1)]),1,-base),(Q(1),))
                    col=[([Z]*q['order']) for q in s];col[i]=residual(p,t,m,r,g,v);cols.append(col);coordinates.append((i,j,k,g[j]))
        N=len(cols);rows=[]
        for i,p in enumerate(s):
            for h in range(p['order']):rows.extend(clear_columns([c[i][h] for c in cols]))
        rhs=[Q(0)]*len(rows)
        for n in range(base,base+t['order']):
            rows.append([Q(n-base)**k*terms_at(s[i],lanes[i][0]*n+lanes[i][1]+j) for i,j,k,g in coordinates]);rhs.append(terms_at(t,n))
        sol=solve(rows,rhs,N)
        if sol is None:continue
        weights,rank=sol
        groups=[[h for h,(j,_,_,_) in enumerate(coordinates) if j==i] for i in range(len(s))]
        feasible=True
        for group in groups:
            if any(weights[h] for h in group):continue
            direction=None
            for h in group:
                unit=[Q(int(j==h)) for j in range(N)]
                z=solve(rows+[unit],[Q(0)]*len(rows)+[Q(1)],N)
                if z is not None:direction=z[0];break
            if direction is None:feasible=False;break
            active=[g for g in groups if any(weights[h] for h in g)]+[group]
            # A nonzero block can be cancelled by at most one scalar. At most
            # len(active) values are forbidden; len(active)+1 trials suffice.
            for a in range(1,len(active)+2):
                w=[u+a*v for u,v in zip(weights,direction)]
                if all(any(w[h] for h in g) for g in active):weights=w;break
            else:raise ArithmeticError('activation counting invariant')
        if not feasible:continue
        gs=[[Z]*p['order'] for p in s]
        for w,(i,j,k,g) in zip(weights,coordinates):gs[i][j]=gs[i][j].plus(const(w).times(g))
        e=joint_certificate(sources,target,lanes,gs)
        if e:
            e['discovery']={'basis':'direct_sum_polynomial_ansatz','degree':deg,'rank':rank,'unknowns':N,'nullity':N-rank}
            return e
    return None


def verify_joint(e,sources,target):
    try:
        got=joint_certificate(sources,target,[v['lane'] for v in e['sources']],[[decode_rat(c) for c in v['coefficients']] for v in e['sources']])
        return got is not None and got=={k:v for k,v in e.items() if k!='discovery'}
    except (ValueError,KeyError,TypeError,ZeroDivisionError,OverflowError):return False


def minimal_constant_characteristic(profile):
    """Exact cyclic-state minimal annihilator, not recurrence guessing.

    For the supplied seed v and companion matrix A, find the least k with
    A^k v in span(v,...,A^(k-1)v). Applying A^j proves all later instances.
    Return None outside constant recurrence class.
    """
    if profile['status']!='conditional_source_definition':return None
    p=profile['definitions'][0];d=p['order'];c=list(map(decode_rat,p['coefficients']))
    if any(len(v.num)>1 or len(v.den)>1 for v in c):return None
    c=[ratio_evaluate(v,0) for v in c];v=list(map(Q,p['initial']))
    if not any(v):return (Q(1),)
    cols=[v]
    for k in range(1,d+1):
        v=v[1:]+[sum((a*b for a,b in zip(c,v)),Q(0))]
        z=solve(list(map(list,zip(*cols))),v,k)
        if z is not None:return tuple(-a for a in z[0])+(Q(1),)
        cols.append(v)
    raise ArithmeticError('cyclic-state dimension bound violated')


def spectral_cover_jobs(profiles, max_sources=3, max_per_target=12, max_candidates=24):
    """Bounded, exact spectral cover prefilter for genuinely joint C-finite jobs.

    A finite list of source recurrence states spans the sum of their cyclic
    shift modules. Their combined annihilator is the LCM of the minimal
    characteristic polynomials. A target's minimal polynomial must divide it.
    The filter requires every source to contribute a necessary factor/power.
    Actual identities still need the independent direct-sum certificate.
    """
    import itertools
    from oeis_gap_automation import pgcd,mul,divmod_poly
    if not 2<=max_sources<=4 or not 1<=max_per_target<=64 or not 1<=max_candidates<=64:raise ValueError('cover budget')
    def divides(a,b):return not any(divmod_poly(b,a)[1])
    def lcm(a,b):return mul(divmod_poly(a,pgcd(a,b))[0],b)
    def cover(rows):
        p=(Q(1),)
        for _,g in rows:p=lcm(p,g)
        return p
    polynomials={k:p for k,v in profiles.items() if (p:=minimal_constant_characteristic(v)) is not None and len(p)>1}
    jobs=[]
    for target,t in sorted(polynomials.items()):
        if len(t)<3:continue
        candidates=[]
        for source,s in sorted(polynomials.items()):
            if target==source:continue
            g=pgcd(s,t)
            if len(g)>1 and not divides(t,g):candidates.append((source,g))
        candidates=sorted(candidates,key=lambda z:(-len(z[1]),z[0]))[:max_candidates]
        count=0
        for arity in range(2,max_sources+1):
            for rows in itertools.combinations(candidates,arity):
                if not divides(t,cover(rows)):continue
                if any(divides(t,cover(rows[:i]+rows[i+1:])) for i in range(arity)):continue
                jobs.append({'sources':[k for k,_ in rows],'target':target,'lanes':[[1,0] for _ in rows],'max_degree':0,
                             'prefilter':'exact_minimal_characteristic_lcm_cover','target_minimal_characteristic':list(map(ff,t)),
                             'source_minimal_characteristics':[list(map(ff,polynomials[k])) for k,_ in rows]})
                count+=1
                if count>=max_per_target:break
            if count>=max_per_target:break
    return jobs
