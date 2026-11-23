"""Context-aware exact arithmetic benchmarks, not universal speed claims.
Author: Komorebi P. Reports medians and verifies exact outputs.
"""
from __future__ import annotations
import argparse,json,statistics,time
from math import comb
from pathlib import Path
from sequence_euler_fibonacci_bridge import bridge_series,native_euler


def catalog(n):return comb(2*n,n)//(n+1)

def prefix_direct(n):return [catalog(k) for k in range(n+1)]

def prefix_recurrence(n):
    a=[1]
    for k in range(n):
        numer=(4*k+2)*a[-1]
        if numer%(k+2):raise AssertionError('Catalan recurrence not exact')
        a.append(numer//(k+2))
    return a


def measure(fn,runs=5):
    vals=[];answer=None
    for _ in range(runs):
        start=time.perf_counter();x=fn();dt=time.perf_counter()-start
        if answer is not None and x!=answer:raise AssertionError('unstable exact output')
        answer=x;vals.append(dt)
    return statistics.median(vals),answer


def benchmark(n=2500,runs=5):
    direct,b=measure(lambda:catalog(n),runs)
    # Cached central binomial coefficient: its production cost is excluded.
    central=comb(2*n,n)
    cached,c=measure(lambda:central//(n+1),runs)
    assert b==c
    pref_direct,seqA=measure(lambda:prefix_direct(n),runs)
    pref_recur,seqB=measure(lambda:prefix_recurrence(n),runs)
    assert seqA==seqB
    euler_direct,egf=measure(lambda:native_euler(34),runs)
    euler_bridge,transfer=measure(lambda:bridge_series(34),runs)
    assert egf==transfer
    return {'date':'2026-11-22','author':'Komorebi P.','exact_terms_verified':n+1,
       'method':'wall-clock median of same-process Python runs on one machine',
       'results':{
          'catalan_single_n':{'n':n,'direct_seconds':direct,'cached_central_division_seconds':cached,
             'cached_qualification':'central binomial coefficient must already be available; its production cost is excluded'},
          'catalan_prefix':{'n':n,'independent_binomial_seconds':pref_direct,
             'recurrence_seconds':pref_recur},
          'euler_34_terms':{'native_egf_quotient_seconds':euler_direct,
             'fibonacci_composition_seconds':euler_bridge}},
       'caveat':'Machine-dependent, fixed workload. Algebraic transfer is not automatically a faster computation.'}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--n',type=int,default=2500);p.add_argument('--runs',type=int,default=5)
    a=p.parse_args(argv)
    result=benchmark(a.n,a.runs)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
