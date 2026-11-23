"""Measured sparse computation strategies; source formula correctness is audited separately.

Author: Komorebi P.  Exact equality checked on every timed run.
No speedup against optimal algorithms is asserted.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import statistics
import time
from sequence_archive_v08_bridge import quadratic_pair,quadratic_binomial_even,quadratic_binomial_odd
from sequence_sparse_packets import shared_sparse_terms
from sequence_recurrence_packets import nth_term
from sequence_sparse_index import integer_sha256


def _measure(fn,expected,runs):
    timings=[]
    for _ in range(runs):
        start=time.perf_counter();out=fn();elapsed=time.perf_counter()-start
        if out!=expected:raise AssertionError('benchmark outputs are not identical')
        timings.append(elapsed)
    return {'median_seconds':statistics.median(timings),'seconds':timings}


def benchmark(runs=5):
    if type(runs) is not int or not 1<=runs<=20:raise ValueError('runs outside 1..20')
    c,q,n=1,2,900
    expected=quadratic_pair(c,q,n)
    independent=lambda:(quadratic_binomial_even(c,q,n),quadratic_binomial_odd(c,q,n))
    shared=lambda:quadratic_pair(c,q,n)
    if independent()!=expected:raise AssertionError('quadratic pair does not equal binomial sums')
    a=_measure(independent,expected,runs);b=_measure(shared,expected,runs)
    indices=(3000,3001,3002,3003,3004,3100,3101,5000,5001,5002)
    sequences={'Fibonacci':([0,1],[1,1]),'Lucas':([2,1],[1,1])}
    request={sid:indices for sid in sequences}
    direct=lambda:{(sid,k):nth_term(iv,c,k)
                   for sid,(iv,c) in sequences.items() for k in indices}
    packed=lambda:shared_sparse_terms(sequences,request)[0]
    check=direct()
    if packed()!=check:raise AssertionError('sparse packet bank mismatch')
    a2=_measure(direct,check,runs);b2=_measure(packed,check,runs)
    receipt=shared_sparse_terms(sequences,request)[1]
    return {'schema':1,'author':'Komorebi P.','runs':runs,
            'quadratic':{'parameters':{'c':c,'q':q,'n':n},'independent_two_binomial_sums':a,
                         'paired_quadratic_jump':b,
                         'direct_over_jump_ratio':a['median_seconds']/b['median_seconds'],
                         'exact_output_hashes':[integer_sha256(v) for v in expected],
                         'comparison_scope':'naive exact binomial sums vs archived quadratic binary powering, not optimal Pell software'},
            'shared_packets':{'sequences':list(sequences),'requested_indices':list(indices),
                              'independent_recursion_packets':a2,
                              'shared_packet_bank':b2,
                              'independent_over_shared_ratio':a2['median_seconds']/b2['median_seconds'],
                              'terms_checked':len(check),'packet_bank':receipt,
                              'comparison_scope':'same Python exact recurrence kernel; shared binary powers across sequences/indices'},
            'nonclaims':['No benchmark guarantees on another machine','Proof checking is excluded from kernel timing',
                         'Source OEIS identification remains finitely checked']}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--runs',type=int,default=5)
    a=p.parse_args();result=benchmark(a.runs)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:{'ratio':v.get('direct_over_jump_ratio',v.get('independent_over_shared_ratio'))} for k,v in result.items() if k in ('quadratic','shared_packets')},indent=2))

if __name__=='__main__':main()
