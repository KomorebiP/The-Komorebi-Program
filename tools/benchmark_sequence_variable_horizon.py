"""Measured exact workload comparison for real indexed OEIS formula transfers.
Author: Komorebi P.

Separates proof and startup costs from execution-only timings; this is not a
cross-machine performance guarantee. Both routes return identical values.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sqlite3
import statistics
import time
from sequence_hypergraph_workload import load_formula_models, certify_hyperedges, direct_cost, evaluate_model
from sequence_variable_horizon import plan_variable_horizon, run_variable_plan


def benchmark(dbpath,ledger,extra,targets,nmax=300,runs=5):
    if type(runs) is not int or not 1<=runs<=10:raise ValueError('runs must be 1..10')
    with sqlite3.connect(dbpath) as db:
        models,info=load_formula_models(db,extra)
        certified,_=certify_hyperedges(db,ledger,models,require_multi=False,allow_indexed=True)
    rows=[]
    for target in targets:
        edges=[c for c in certified if c['target']==target and
            any(tuple(pair)!=(1,0) for pairs in c['index_maps'].values() for pair in pairs)]
        if not edges:raise ValueError('no certified indexed source formula for '+target)
        choices=[]
        for e in edges:
            scope=list(dict.fromkeys((target,*e['inputs'])))
            choices.append(plan_variable_horizon(models,[],[e],[target],nmax,
                scope=scope,max_depth=1,cap=3*nmax+60,max_states=30000))
        plan=min(choices,key=lambda p:p['score'])
        method=direct_cost(models[target],nmax)[1]
        def baseline():return evaluate_model(models[target],nmax,method)
        def shared():return run_variable_plan(plan,models,spot_check=False)[0][target]
        expected=baseline()
        if shared()!=expected:raise AssertionError('exact candidate and independent formula disagree')
        times={}
        for name,fn in [('shared',shared),('independent',baseline)]:
            batch=[]
            for _ in range(runs):
                start=time.perf_counter();actual=fn();elapsed=time.perf_counter()-start
                if actual!=expected:raise AssertionError('benchmark changed outputs')
                batch.append(elapsed)
            times[name]={'median_seconds':statistics.median(batch),'samples_seconds':batch}
        rows.append({'target':target,'nmax':nmax,'values_compared':nmax+1,
                     'planner_steps':[(s['target'],s['horizon'],s['kind']) for s in plan['steps']],
                     'planner_selected_indexed':any(s['kind']=='hyperedge' for s in plan['steps']),
                     'planner_score':plan['score'],'independent_score':plan['independent_direct_score'],
                     'median_seconds':{name:times[name]['median_seconds'] for name in times},
                     'independent_over_shared':times['independent']['median_seconds']/times['shared']['median_seconds'],
                     'measured_winner':min(times,key=lambda k:times[k]['median_seconds']),
                     'output_sha256':hashlib.sha256(json.dumps(expected,separators=(',',':')).encode()).hexdigest()})
    return {'version':'1.3','author':'Komorebi P.','baseline':'independent exact prefix evaluation',
            'timings_exclude':'SQLite load, source checks, proof ledger compilation, planning and initial validation',
            'runs':runs,'tasks':rows,'scope':'machine-specific execution times, formulas only; not OEIS all-index identifications'}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True)
    p.add_argument('--hyperedges',type=Path,required=True)
    p.add_argument('--extra',type=Path,required=True)
    p.add_argument('--targets',nargs='+',default=['A006331','A086653','A047732','A016789'])
    p.add_argument('--nmax',type=int,default=300)
    p.add_argument('--runs',type=int,default=5)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args(argv)
    result=benchmark(a.db,a.hyperedges,a.extra,a.targets,a.nmax,a.runs)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
