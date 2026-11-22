"""Exact sparse quotient-ring powers produce global multinomial transfer operators.

Author: Komorebi P.

For a_n=L(T^n e_0) with P(T)=0, define Q_m(T)=T^m mod P(T).
Then for every n,r >= 0,
 a_(m*n+r)=sum_{k_0+...+k_(d-1)=n} multinomial(n;k_0,...,k_(d-1))
                 *product_j q_j**k_j * a_(r+sum_j j*k_j).
This is all-index identity for every recurrence solution of P(S)a=0,
not a fit to finite OEIS terms. Numeric controls are separate.
"""
from __future__ import annotations
import argparse
from collections import Counter
import json
from math import comb
from pathlib import Path
import sqlite3

from sequence_recurrence_packets import x_packet,nth_term,load_sources


def sparse_lifts(coefficients,max_modulus=24,max_support=3,coefficient_bound=1000):
    if max_modulus<2 or max_support<1:raise ValueError('invalid lift bounds')
    out=[]
    for m in range(max(2,len(coefficients)),max_modulus+1):
        poly=x_packet(m,coefficients)
        terms=[(j,v) for j,v in enumerate(poly) if v]
        if not terms or len(terms)>max_support or max(abs(v) for _,v in terms)>coefficient_bound:
            continue
        out.append({'modulus':m,'polynomial':poly,
                    'terms':[{'shift':j,'weight':v} for j,v in terms],
                    'support':len(terms),'largest_coefficient':max(abs(v) for _,v in terms),
                    'proof':'X^m congruent to the recorded polynomial modulo the monic shift annihilator P(X)'} )
    return out


def _compositions(total,number):
    if number==1:
        yield (total,)
    else:
        for x in range(total+1):
            for tail in _compositions(total-x,number-1):yield (x,)+tail


def multinomial_evaluate(initial,coefficients,lift,n,residue=0,max_expansion=50000):
    """Direct exact multinomial expansion for a small independently checked n."""
    if n<0 or residue<0:raise ValueError('negative index or phase')
    entries=[(t['shift'],t['weight']) for t in lift['terms']]
    if comb(n+len(entries)-1,len(entries)-1)>max_expansion:
        raise ValueError('explicit multinomial sum exceeds verification budget')
    total=0
    for counts in _compositions(n,len(entries)):
        coefficient=1
        remain=n
        for k,(_,weight) in zip(counts,entries):
            coefficient*=comb(remain,k)*weight**k
            remain-=k
        shift=residue+sum(k*j for k,(j,_) in zip(counts,entries))
        total+=coefficient*nth_term(initial,coefficients,shift)
    return total


def certify(initial,coefficients,lift,checks=9,residues=(0,1)):
    expected=x_packet(lift['modulus'],coefficients)
    if expected!=lift['polynomial']:
        raise ArithmeticError('quotient-ring polynomial mismatch')
    for r in residues:
        for n in range(checks):
            lhs=nth_term(initial,coefficients,lift['modulus']*n+r)
            rhs=multinomial_evaluate(initial,coefficients,lift,n,r)
            if lhs!=rhs:raise AssertionError('multinomial direct control failed')
    return {'proof_type':'polynomial_quotient_ring_identity',
            'checks_per_residue':checks,'residues':list(residues),
            'scope':'every solution of supplied recurrence for every nonnegative n and residue'}


def discover(db,output,*,max_modulus=12,max_support=3,max_coefficient=20):
    ids=[r[0] for r in db.execute('SELECT oeis_id FROM recurrence_packet_sources ORDER BY oeis_id')]
    sources=load_sources(db,ids)  # hashes verified against current seed records
    by_kernel={};counts=Counter();selected=[]
    for sid,(iv,c) in sources.items():
        coeffs=tuple(c)
        if coeffs not in by_kernel:
            by_kernel[coeffs]=sparse_lifts(c,max_modulus,max_support,max_coefficient)
        for lift in by_kernel[coeffs]:
            record={'source_oeis_id':sid,'recurrence':c,'initial':iv,
                    'lift':lift,'proof_type':'ring_power_multinomial_transfer',
                    'scope':'identity for supplied recurrence; OEIS mapping finite checked'}
            if lift['modulus']<=6:
                record['controls']=certify(iv,c,lift,checks=6)
            selected.append(record)
            counts['certified_sequence_lifts']+=1
            if lift['support']<=2:counts['binomial_or_monomial_lifts']+=1
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('w',encoding='utf-8') as f:
        for item in selected:f.write(json.dumps(item,ensure_ascii=False,separators=(',',':'))+'\n')
    examples=[]
    for sid in ('A000045','A000032','A000129','A001045','A000931','A000073'):
        for item in selected:
            if item['source_oeis_id']==sid:
                examples.append({'source':sid,'modulus':item['lift']['modulus'],
                                 'polynomial':item['lift']['polynomial']})
                break
    return {'recurrence_sources':len(sources),'distinct_recurrence_kernels':len(by_kernel),
            **dict(counts),'examples':examples,
            'statement':'Universal quotient-ring transfer identities. The OEIS source connection is only finitely checked.'}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True)
    p.add_argument('--export',type=Path,required=True)
    p.add_argument('--max-modulus',type=int,default=12)
    p.add_argument('--max-support',type=int,default=3)
    p.add_argument('--max-coefficient',type=int,default=20)
    a=p.parse_args(argv)
    with sqlite3.connect(a.db) as db:
        r=discover(db,a.export,max_modulus=a.max_modulus,max_support=a.max_support,
                   max_coefficient=a.max_coefficient)
    print(json.dumps(r,indent=2))

if __name__=='__main__':main()
