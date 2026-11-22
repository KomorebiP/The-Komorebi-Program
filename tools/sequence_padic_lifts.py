"""Exact dyadic/odd-adic phase lifts of recurrence packets.

Author: Komorebi P.

For T the quotient-ring shift matrix and w the residue state, a digit d at
prime p updates
    (m,r,T_m,w) -> (mp, r+md, T_m^p, T_m^d w).
This is an exact composition identity, before any modular reduction. Reducing
both sides modulo p^h supplies an auditable congruence witness. Nothing here
implies a novel p-adic valuation theorem or solves a global conjecture.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sqlite3
from sequence_recurrence_packets import (companion,mat_pow,mat_vec,characteristic,
                                          load_sources,nth_term)


def isprime(n):
    if type(n) is not int or n<2:return False
    return all(n%k for k in range(2,int(n**0.5)+1))


def lift_tower(initial,c,prime,digits,*,padic_precision=3,max_exact_modulus=4096):
    if not isprime(prime):raise ValueError('prime required')
    if not isinstance(digits,(list,tuple)) or not digits or len(digits)>10:
        raise ValueError('nonempty digit list of length at most ten required')
    if any(type(d) is not int or d<0 or d>=prime for d in digits):
        raise ValueError('digit outside 0..p-1')
    if type(padic_precision) is not int or not 1<=padic_precision<=12:
        raise ValueError('p-adic precision out of bounds')
    m=1;r=0
    state=[1]+[0]*(len(c)-1)
    power=companion(c)
    items=[]
    for level,digit in enumerate(digits,1):
        if m*prime>max_exact_modulus:
            raise ValueError('exact lift modulus too large; use a modular-only extension')
        # Compute new shift from the old shift, never recompute from a term prefix.
        state=mat_vec(mat_pow(power,digit),state)
        power=mat_pow(power,prime)
        r+=digit*m;m*=prime
        # Independent algebraic state witness: X^r mod P, T^m.
        expected_state=mat_vec(mat_pow(companion(c),r),[1]+[0]*(len(c)-1))
        if expected_state!=state or mat_pow(companion(c),m)!=power:
            raise ArithmeticError('lift composition failed')
        modulus=prime**padic_precision
        items.append({'level':level,'prime':prime,'digit':digit,'modulus':m,'residue':r,
                      'recurrence':[-v for v in characteristic(power)[1:]],
                      'state_mod_p_power':[v%modulus for v in state],
                      'shift_matrix_mod_p_power':[[v%modulus for v in row] for row in power],
                      'precision':padic_precision,
                      'first_phase_terms':[nth_term(initial,c,m*n+r) for n in range(4)],
                      'proof':'exact phase composition followed by homomorphic reduction mod p^h'})
    return items


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True)
    p.add_argument('--id',required=True)
    p.add_argument('--prime',type=int,default=2)
    p.add_argument('--digits',required=True,help='comma separated base-p digits, least significant first')
    p.add_argument('--precision',type=int,default=3)
    p.add_argument('--output',type=Path)
    args=p.parse_args(argv)
    digits=[int(x) for x in args.digits.split(',')]
    with sqlite3.connect(args.db) as db:initial,c=load_sources(db,[args.id])[args.id]
    entries=lift_tower(initial,c,args.prime,digits,padic_precision=args.precision)
    out={'oeis_id':args.id,'prime':args.prime,'digits':digits,'lifts':entries,
         'scope':'exact curated recurrence definition; original OEIS equality only finite checked'}
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
