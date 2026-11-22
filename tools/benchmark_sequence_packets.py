"""Reproducible exact integer benchmark of shared recurrence packets vs stepping.

Author: Komorebi P. No asymptotic claims about bit complexity or other machines.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sqlite3
from statistics import median
from time import perf_counter
import platform
from sequence_recurrence_packets import load_sources,batch_term


def step(initial,c,n):
    if n<len(initial):return initial[n]
    a=list(initial)
    d=len(c)
    for k in range(d,n+1):
        a.append(sum(c[j]*a[k-1-j] for j in range(d)))
        # Store only the rolling d-value state, not O(n) sequence memory.
        if len(a)>d+1:a.pop(0)
    return a[-1]


def step_rolling(initial,c,n):
    """Independent fixed-memory recurrence stepping using direct numeric loops."""
    if n<len(initial):return initial[n]
    a=list(initial);d=len(c)
    for k in range(d,n+1):
        nextvalue=sum(c[j]*a[-1-j] for j in range(d))
        a=a[1:]+[nextvalue]
    return a[-1]


def fingerprint_results(results):
    h=hashlib.sha256()
    for key,value in sorted(results.items()):
        raw=value.to_bytes((value.bit_length()+8)//8,'big',signed=True)
        h.update(key.encode()+b'\0')
        h.update(len(raw).to_bytes(8,'big'))
        h.update(raw)
    return h.hexdigest()


def run(db_path,n=10000,repeat=3):
    with sqlite3.connect(db_path) as db:
        sid=[row[0] for row in db.execute('SELECT oeis_id FROM recurrence_packet_sources ORDER BY oeis_id')]
        entries=load_sources(db,sid)
    def naive():return {s:step_rolling(v,c,n) for s,(v,c) in entries.items()}
    def compiled():return batch_term(entries,n)
    baseline=naive();actual,counts=compiled()
    if baseline!=actual:raise AssertionError('exact benchmark results differ')
    t0=[];t1=[]
    for i in range(repeat):
        a=perf_counter();naive();t0.append(perf_counter()-a)
        a=perf_counter();compiled();t1.append(perf_counter()-a)
    report={'n':n,'repeat':repeat,'sequences':len(entries),
      'kernels':counts['recurrence_kernels'],
      'packet_exponentiations':counts['packet_exponentiations'],
      'results_agree':True,
      'median_independent_step_seconds':round(median(t0),6),
      'median_shared_packet_seconds':round(median(t1),6),
      'observed_speed_ratio':round(median(t0)/median(t1),2) if median(t1) else None,
      'machine':{'python':platform.python_version(),'platform':platform.platform(),
                 'processor':platform.processor()},
      'scope':'one specific exact workload; not a universal performance guarantee',
      'result_sha256':fingerprint_results(actual)}
    return report


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True)
    p.add_argument('--n',type=int,default=10000)
    p.add_argument('--repeat',type=int,default=3)
    p.add_argument('--output',type=Path)
    args=p.parse_args(argv)
    if args.n<0 or args.n>500000 or not 1<=args.repeat<=20:
        p.error('invalid n/repeat for bounded performance benchmark')
    report=run(args.db,args.n,args.repeat)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
