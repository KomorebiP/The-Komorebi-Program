"""All-index transfer closure for C-finite Komorebi sequence definitions.

Author: Komorebi P.

This produces exact recurrence certificates for three operators:
- binomial transform and its inverse, P(S) -> P(S-1) or P(S+1)
- Cauchy convolution, C(z) = A(z)B(z), reducing the rational OGF
- termwise (Hadamard) product, using a tensor state/observability proof.

All global claims concern the supplied curated recurrence definitions, whose
OEIS identifications have been compared only on finite term windows. Raw OEIS
formula text and program listings are not executed.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
from fractions import Fraction as Q
import hashlib
import itertools
import json
import math
from pathlib import Path
import sqlite3
from functools import lru_cache

from sequence_recurrence_packets import (nth_term,mat_vec,companion,
                                         minimal_scalar_phase,_solve,load_sources)
from sequence_recurrence_transfers import (ogf_from_recurrence,pmul,pdivmod,gcdpoly,trim)


def shift_monic_polynomial(coefficients, shift):
    """Coefficients of P(X+shift), where P(X)=X^d-sum c_j X^(d-j)."""
    if not coefficients or not all(type(v) is int for v in coefficients):
        raise ValueError('integer nonempty recurrence coefficients required')
    if type(shift) is not int:raise ValueError('integral shift required')
    p=list(reversed([1]+[-v for v in coefficients]))  # ascending
    out=[0]*len(p)
    for k,value in enumerate(p):
        for j in range(k+1):out[j]+=value*math.comb(k,j)*shift**(k-j)
    if out[-1]!=1:raise AssertionError('monic polynomial lost its leading coefficient')
    return [-v for v in reversed(out[:-1])]


def binomial_transform(initial,coefficients,inverse=False,checks=28):
    """Certified recurrence for B[a]_n=sum_k (-1)^(n-k) C(n,k)a_k (inverse sign)."""
    d=len(coefficients)
    if d<1 or len(initial)!=d:raise ValueError('recurrence and initial lengths differ')
    newc=shift_monic_polynomial(coefficients,1 if inverse else -1)
    def direct(n):
        return sum(math.comb(n,k)*((-1)**(n-k) if inverse else 1)*
                   nth_term(initial,coefficients,k) for k in range(n+1))
    newinit=[direct(n) for n in range(d)]
    for n in range(checks):
        if nth_term(newinit,newc,n)!=direct(n):
            raise AssertionError('exact binomial operator validation failed')
    reduced=minimal_scalar_phase(newinit,newc,1,0)
    return {'operation':'inverse_binomial' if inverse else 'binomial',
            'coefficients':newc,'initial':newinit,'minimal':reduced,
            'proof':'EGF B(x)=exp(±x) A(x). Therefore P(D∓1)B=0; initial values are exact binomial sums.',
            'checked_terms':checks,'scope':'all indices for supplied recurrence definition'}


def _rec_ogf(initial,coefficients):
    return ogf_from_recurrence({'op':'linear_recurrence',
                                'initial':initial,'coefficients':coefficients})


def cauchy_product(initial_a,c_a,initial_b,c_b,checks=25):
    """Certified recurrence for sum_{k=0}^n a_k b_(n-k), using rational OGFs."""
    fa,fb=_rec_ogf(initial_a,c_a),_rec_ogf(initial_b,c_b)
    if fa is None or fb is None:raise ValueError('invalid input recurrences')
    p,q=pmul(fa['P'],fb['P']),pmul(fa['Q'],fb['Q'])
    if p==[0]:
        return {'operation':'cauchy_product','coefficients':[0],'initial':[0],
                'numerator':['0'],'denominator':['1'],
                'minimal':{'order':0,'coefficients':[],'initial':[]},
                'proof':'The product of the two rational OGFs is identically zero',
                'checked_terms':checks,'scope':'all indices for supplied recurrence definitions'}
    g=gcdpoly(p,q);p,rp=pdivmod(p,g);q,rq=pdivmod(q,g)
    if rp!=[0] or rq!=[0]:raise ArithmeticError('gcd reduction failed')
    scale=q[0]
    if not scale:raise ArithmeticError('denominator constant term vanished')
    p,q=trim([v/scale for v in p]),trim([v/scale for v in q])
    d=max(1,len(q)-1,len(p))
    c=[-v for v in q[1:]]+[Q(0)]*(d-(len(q)-1))
    if any(v.denominator!=1 for v in c):
        raise ValueError('reduced Cauchy recurrence is not integral')
    c=[int(v) for v in c]
    def direct(n):return sum(nth_term(initial_a,c_a,k)*nth_term(initial_b,c_b,n-k)
                             for k in range(n+1))
    iv=[direct(i) for i in range(d)]
    for n in range(checks):
        if direct(n)!=nth_term(iv,c,n):raise AssertionError('convolution recurrence check failed')
    minimal=minimal_scalar_phase(iv,c,1,0)
    return {'operation':'cauchy_product','coefficients':c,'initial':iv,
            'numerator':[str(v) for v in p],'denominator':[str(v) for v in q],
            'minimal':minimal,
            'proof':'Cauchy product of two rational OGFs equals their exact rational product, whose reduced denominator supplies an all-index recurrence.',
            'checked_terms':checks,'scope':'all indices for supplied recurrence definitions'}


def kronecker(a,b):
    """Tensor matrix with index (i,k) mapped to i*dim_b+k."""
    m,n=len(a),len(b)
    return [[a[i][j]*b[k][l] for j in range(m) for l in range(n)]
            for i in range(m) for k in range(n)]


def hadamard_product(initial_a,c_a,initial_b,c_b,checks=25,max_state=24):
    """Minimal scalar recurrence for a_n*b_n with tensor observability witness."""
    da,db=len(c_a),len(c_b);D=da*db
    if da<1 or db<1 or D>max_state:raise ValueError('tensor-state dimension outside supported range')
    K=kronecker(companion(c_a),companion(c_b))
    output=[x*y for x in initial_a for y in initial_b]
    w=[1]+[0]*(D-1)
    states=[w]
    for _ in range(2*D):states.append(mat_vec(K,states[-1]))
    obs=[sum(a*b for a,b in zip(output,state)) for state in states]
    def direct(n):return nth_term(initial_a,c_a,n)*nth_term(initial_b,c_b,n)
    for n in range(min(checks,len(obs))):
        if obs[n]!=direct(n):raise AssertionError('tensor output is not the termwise product')
    if not any(obs[:D]):
        if any(obs[D:]):raise ArithmeticError('zero tensor outputs inconsistent')
        return {'operation':'hadamard_product','coefficients':[0], 'initial':[0],
                'minimal':{'order':0,'coefficients':[],'initial':[]},
                'tensor_dimension':D,'checked_terms':min(checks,len(obs)),
                'proof':'Zero first D output evaluations and Cayley-Hamilton imply identically zero output',
                'scope':'all indices for supplied recurrence definitions'}
    for degree in range(1,D+1):
        rows=[[obs[n+j] for j in range(degree)] for n in range(D)]
        target=[obs[n+degree] for n in range(D)]
        ans=_solve(rows,target,degree)
        if ans is None:continue
        if any(v.denominator!=1 for v in ans):
            raise ArithmeticError('minimal polynomial coefficient not integral')
        asc=[int(v) for v in ans]
        residual=[states[degree][i]-sum(asc[j]*states[j][i]
                     for j in range(degree)) for i in range(D)]
        for n in range(D):
            if sum(output[i]*residual[i] for i in range(D))!=0:
                raise AssertionError('observable residual is nonzero')
            residual=mat_vec(K,residual)
        c=asc[::-1];initial=obs[:degree]
        for n in range(checks):
            if nth_term(initial,c,n)!=direct(n):
                raise AssertionError('Hadamard recurrence check failed')
        return {'operation':'hadamard_product','coefficients':c,'initial':initial,
                'minimal':{'order':degree,'coefficients':c,'initial':initial},
                'tensor_dimension':D,'checked_terms':checks,
                'proof':'a_n b_n=(u_a⊗u_b)^T (T_a⊗T_b)^n (e_0⊗e_0); D zero observable residuals and Cayley-Hamilton establish the scalar recurrence for all n.',
                'scope':'all indices for supplied recurrence definitions'}
    raise AssertionError('Cayley-Hamilton tensor recurrence not found')


@lru_cache(maxsize=8192)
def _cached_canonical(initial,coefficients):
    m=minimal_scalar_phase(list(initial),list(coefficients),1,0)
    if m['order']==0:return ('zero',)
    return (tuple(m['coefficients']),tuple(m['initial']))


def canonical_recurrence(initial,coefficients):
    return _cached_canonical(tuple(initial),tuple(coefficients))


def build(db,export_path,*,max_pairs=170,max_phase_modulus=6):
    """Generate proof-scoped operators and prove collisions against phase targets.

    Sequence source receipts are checked with load_sources; no prefix matching
    is used to establish any edge. Candidate results are not confused with OEIS.
    """
    ids=[sid for (sid,) in db.execute('SELECT oeis_id FROM recurrence_packet_sources ORDER BY oeis_id')]
    sources=load_sources(db,ids)
    receipts={sid:record for sid,*record in db.execute(
        'SELECT oeis_id,formula_id,source_hash,evaluator_hash FROM recurrence_packet_sources')}
    matches=defaultdict(list)
    for sid,(iv,c) in sources.items():
        matches[canonical_recurrence(iv,c)].append({'oeis_id':sid,'modulus':1,'residue':0})
    if max_phase_modulus>1:
        for sid,m,r,rawc,rawiv,fid,digest in db.execute('''SELECT oeis_id,modulus,residue,
            minimal_recurrence_json,minimal_initial_json,formula_id,source_hash
            FROM recurrence_packet_phases WHERE modulus<=?''',(max_phase_modulus,)):
            if sid not in receipts or receipts[sid][0]!=fid or receipts[sid][1]!=digest:
                raise ValueError('stale phase certificate for '+sid)
            c,iv=json.loads(rawc),json.loads(rawiv)
            if not c:
                key=('zero',)
            else:
                key=canonical_recurrence(iv,c)
            matches[key].append({'oeis_id':sid,'modulus':m,'residue':r})
    out=[];by_kind=Counter();canonical_hits=[]
    for sid,(iv,c) in sources.items():
        for inverse in (False,True):
            cert=binomial_transform(iv,c,inverse)
            kind=cert['operation'];signature=canonical_recurrence(cert['initial'],cert['coefficients'])
            targets=[t for t in matches.get(signature,[]) if t['oeis_id']!=sid or t['modulus']!=1]
            for t in targets:
                canonical_hits.append({'source':sid,'operator':kind,'target':t,
                  'proof':'Both sequences satisfy the same exact minimal recurrence and the same complete initial vector; uniqueness gives equality for all indices of their curated definitions'})
            out.append({'operator':kind,'inputs':[sid],'source_receipts':{sid:receipts[sid]},
                        'certificate':cert,'matches':targets})
            by_kind[kind]+=1
    limited=list(itertools.islice(itertools.combinations_with_replacement(sorted(sources),2),max_pairs))
    for sa,sb in limited:
        va,ca=sources[sa];vb,cb=sources[sb]
        for kind,build_operator in [('cauchy_product',cauchy_product),('hadamard_product',hadamard_product)]:
            if kind=='hadamard_product' and len(ca)*len(cb)>24:continue
            cert=build_operator(va,ca,vb,cb)
            sig=canonical_recurrence(cert['initial'],cert['coefficients'])
            targets=[t for t in matches.get(sig,[]) if t['oeis_id'] not in (sa,sb) or t['modulus']!=1]
            for t in targets:
                canonical_hits.append({'source':[sa,sb],'operator':kind,'target':t,
                  'proof':'Exact recurrence generation plus unique minimal recurrence and initial vector certify the all-index identity for curated definitions'})
            out.append({'operator':kind,'inputs':[sa,sb],
                        'source_receipts':{s:receipts[s] for s in {sa,sb}},
                        'certificate':cert,'matches':targets})
            by_kind[kind]+=1
    export_path=Path(export_path);export_path.parent.mkdir(parents=True,exist_ok=True)
    with export_path.open('w',encoding='utf-8') as fh:
        for row in out:fh.write(json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n')
    meaningful=[t for t in canonical_hits if
                not (isinstance(t['source'],str) and t['source']=='A000004')]
    return {'source_recursions':len(ids),'operator_certificates':len(out),
            'by_operator':dict(by_kind),'exact_phase_or_sequence_matches':len(canonical_hits),
            'nonzero_source_matches':len(meaningful),
            'notable_matches':[hit for hit in meaningful if hit['source'] in
                ('A000045','A000032','A000079','A000244','A000012')][:22],
            'statement':'All-index proofs concern curated recurrence definitions; identification with OEIS is supported by finite term checks only.'}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db',type=Path,required=True)
    parser.add_argument('--export',type=Path,required=True)
    parser.add_argument('--max-pairs',type=int,default=170)
    parser.add_argument('--max-phase-modulus',type=int,default=6)
    args=parser.parse_args(argv)
    with sqlite3.connect(args.db) as db:
        report=build(db,args.export,max_pairs=args.max_pairs,max_phase_modulus=args.max_phase_modulus)
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
