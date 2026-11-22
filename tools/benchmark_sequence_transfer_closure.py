"""Benchmark an exact compiled binomial transform against direct summation.

Author: Komorebi P.
Report only this workload's timings; the full OEIS identifications are not
established by these finite calculations. Python 3.10+ stdlib.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from statistics import median
from time import perf_counter

from sequence_transfer_closure import binomial_transform
from sequence_recurrence_packets import nth_term


def direct_fibonacci_binomial(n):
    """Single exact O(n) traversal with updated Fibonacci and binomial terms."""
    if n<0:raise ValueError('n must be nonnegative')
    coefficient=1
    f,g=0,1
    result=0
    for k in range(n+1):
        result+=coefficient*f
        f,g=g,f+g
        if k<n:coefficient=coefficient*(n-k)//(k+1)
    return result


def benchmark(n=5000,repeat=5):
    if n<1 or n>20000 or repeat<1 or repeat>30:raise ValueError('n or repeat outside supported limit')
    formula=binomial_transform([0,1],[1,1])
    checks=[]
    for _ in range(repeat):
        t=perf_counter();slow=direct_fibonacci_binomial(n);t1=perf_counter()-t
        t=perf_counter();fast=nth_term(formula['initial'],formula['coefficients'],n);t2=perf_counter()-t
        if fast!=slow or fast!=nth_term([0,1],[1,1],2*n):
            raise ArithmeticError('computed transformed Fibonacci terms differ')
        checks.append([t1,t2])
    measured_slow=median(row[0] for row in checks)
    measured_fast=median(row[1] for row in checks)
    return dict(n=n,repeats=repeat,benchmarked_case='binomial transform of Fibonacci at index n',
        exact_equality=True,slow_method='single-pass exact Fibonacci and binomial coefficient accumulation',
        fast_method='compiled order-2 shift recurrence evaluated using modular polynomial powers',
        slow_median_seconds=measured_slow,fast_median_seconds=measured_fast,
        measured_speed_ratio=measured_slow/measured_fast if measured_fast else None,
        result_decimal_digits=len(str(fast)),result_sha256=hashlib.sha256(str(fast).encode()).hexdigest(),
        scope='specific Python implementation and workload, not universal performance claim')


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--n',type=int,default=5000)
    p.add_argument('--repeat',type=int,default=5)
    p.add_argument('--output',type=Path)
    args=p.parse_args(argv)
    report=benchmark(n=args.n,repeat=args.repeat)
    content=json.dumps(report,indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(content,encoding='utf-8')
    print(content)

if __name__=='__main__':main()
