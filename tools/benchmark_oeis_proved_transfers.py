"""Benchmark exact direct transforms against compiled formula recurrences.

Author: Komorebi P. The figures are workload measurements, not complexity
claims for every formula, and source OEIS identities remain finitely checked.
"""
from __future__ import annotations
import argparse,json,platform,sqlite3,statistics,time
from math import comb
from pathlib import Path
from sequence_exponential_polynomial import infer
from sequence_recurrence_packets import nth_term


def target_recurrence(db,sid):
    row=db.execute('''SELECT f.evaluator_json,s.offset FROM formulas f
          JOIN sequences s ON s.oeis_id=f.oeis_id WHERE f.oeis_id=?
          AND f.origin='oeis_normalized' AND f.verification='finite_checked'
          ORDER BY f.formula_id LIMIT 1''',(sid,)).fetchone()
    if not row:raise ValueError('no finite-checked target formula '+sid)
    r=infer(json.loads(row[0]),row[1])
    if r is None:raise ValueError('target not C-finite '+sid)
    return r


def measure(fn,rounds):
    times=[];value=None
    for _ in range(rounds):
        start=time.perf_counter()
        current=fn()
        times.append(time.perf_counter()-start)
        if value is not None and current!=value:raise AssertionError('non-deterministic result')
        value=current
    return value,statistics.median(times),times


def benchmark(db, n=3000, rounds=5):
    if not 100<=n<=10000 or not 2<=rounds<=11:raise ValueError('unsupported benchmark bounds')
    cases=[
      ('A000051','A007689','binomial_transform',lambda:sum(comb(n,k)*(2**k+1) for k in range(n+1))),
      ('A000290','A000330','prefix_sum',lambda:sum(k*k for k in range(n+1))),
    ]
    runs=[]
    for source,target,operation,direct in cases:
        cert=db.execute('''SELECT 1 FROM oeis_formula_transfer_proofs
            WHERE source_id=? AND output_id=? AND operator=? LIMIT 1''',
            (source,target,operation)).fetchone()
        if cert is None:raise ValueError('no all-index formula transfer certificate for '+target)
        rec=target_recurrence(db,target)
        fast=lambda:nth_term(rec['initial'],rec['coefficients'],n)
        direct_value,t_direct,controls_direct=measure(direct,rounds)
        computed,t_fast,controls_compiled=measure(fast,rounds)
        if computed!=direct_value:raise AssertionError('compiled term and direct exact transform differ')
        runs.append({'source':source,'target':target,'operator':operation,'index':n,
                     'direct_median_s':t_direct,'compiled_median_s':t_fast,
                     'observed_speed_ratio':t_direct/t_fast if t_fast else None,
                     'exact_value_bits':computed.bit_length(),
                     'all_repetitions_agree':True,
                     'reference':'Exact Python integer arithmetic; compiled formula recurrence via quotient-ring modular exponentiation'})
    return {'author':'Komorebi P.','python':platform.python_version(),
            'python_implementation':platform.python_implementation(),
            'rounds':rounds,'trials':runs,
            'disclaimer':'Measured workload-specific runtime ratio, not proof of global speedup or a faster target than its simplest direct closed form. OEIS identification remains finite checked.'}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--index',type=int,default=3000)
    args=p.parse_args(argv)
    with sqlite3.connect(args.db) as db:report=benchmark(db,args.index)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,indent=2,sort_keys=True))

if __name__=='__main__':main()
