"""Exact three-sequence shared-transfer benchmark for the OEIS formulas.

Author: Komorebi P. Compare identical integer outputs, repeated runs.
The benchmark is a measured workload, not a universal speedup theorem.
"""
from __future__ import annotations
import argparse, json,statistics,time
from math import comb
from pathlib import Path


def independent_prefix(N):
    # Three separately evaluated exact mathematical formula expressions.
    catalan=[comb(2*n,n)//(n+1) for n in range(N+1)]
    central=[comb(2*n,n) for n in range(N+1)]
    target=[(n+1)**2*comb(2*n+1,n) for n in range(N+1)]
    return catalan,central,target


def shared_prefix(N):
    # A000108 formula -> A000984 expression -> A002544 expression.
    # One integer recurrence plus two exact multiplicative gauges.
    catalan=[1]
    for n in range(N):
        num=2*(2*n+1)*catalan[-1]
        assert num%(n+2)==0
        catalan.append(num//(n+2))
    central=[(n+1)*catalan[n] for n in range(N+1)]
    target=[(n+1)*(2*n+1)*central[n] for n in range(N+1)]
    return catalan,central,target


def compare(N=2000,runs=5):
    a=independent_prefix(N);b=shared_prefix(N)
    assert a==b
    timing={}
    for label,fn in [('independent',independent_prefix),('shared',shared_prefix)]:
        periods=[]
        for _ in range(runs):
            t=time.perf_counter();result=fn(N);periods.append(time.perf_counter()-t)
            assert result==a
        timing[label]=dict(median_seconds=statistics.median(periods),sample_seconds=periods)
    return dict(author='Komorebi P.',nmax=N,exact_comparisons=3*(N+1),
        source_formula_relations=['A000108: C_n=binomial(2n,n)/(n+1)',
            'A000984: B_n=(n+1)C_n',
            'A002544: T_n=(n+1)(2n+1)B_n'],
        timings=timing,
        observed_ratio=timing['independent']['median_seconds']/timing['shared']['median_seconds'],
        caveat='Three independent binomial-expression prefixes vs one recurrence prefix with shared integer gauge products; no caching in the independent run; actual speed is hardware/workload-dependent; source OEIS identifications separately finite-checked')


def main():
    p=argparse.ArgumentParser();p.add_argument('--nmax',type=int,default=2000);p.add_argument('--runs',type=int,default=5)
    p.add_argument('--output',type=Path);a=p.parse_args()
    o=compare(a.nmax,a.runs)
    if a.output:a.output.write_text(json.dumps(o,indent=2)+'\n',encoding='utf8')
    print(json.dumps({key:o[key] for key in ('nmax','exact_comparisons','observed_ratio')},indent=2))
if __name__=='__main__':main()
