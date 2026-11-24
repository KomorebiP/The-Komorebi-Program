"""Reproducible exact multi-input DAG benchmarking. Author: Komorebi P."""
from __future__ import annotations
import argparse,hashlib,json,sqlite3,statistics,time,sys
from pathlib import Path
from sequence_hypergraph_workload import (
    load_formula_models,certify_hyperedges,verified_compatible_gauges,verified_gauges,
    load_models,plan_prefix,run_plan,direct_cost,evaluate_model,formula_fingerprint,
)


def independent(models,targets,nmax):
    return {sid:evaluate_model(models[sid],nmax,direct_cost(models[sid],nmax)[1]) for sid in targets}


def run(db:Path,ledger:Path,gauges:Path,extra:Path|None,*,nmax=300,runs=5):
    with sqlite3.connect(db) as con:
        models,info=load_formula_models(con,extra)
        all_hypers,proof_counts=certify_hyperedges(con,ledger,models,require_multi=False,allow_indexed=True)
        hypers=[c for c in all_hypers if all(v==[1,0] for maps in c['index_maps'].values() for v in maps)]
        rawg,_=load_models(con,extra)
    verified,vs=verified_gauges(rawg,gauges)
    approved=verified_compatible_gauges(models,verified)
    sample=[('subtraction',( 'A003222','A002943','A013730')),
            ('product',('A071237','A000217','A002522')),
            ('rational_combination',('A000290','A000326','A005449'))]
    results=[]
    for label,targets in sample:
        p=plan_prefix(models,approved,hypers,targets,nmax,max_nodes=13,max_states=100000)
        targetvals=run_plan(p,models)
        baseline=independent(models,targets,nmax)
        if targetvals!=baseline:raise AssertionError(f'competing plans disagree: {label}')
        times={}
        for name,fun in [('optimized',lambda:run_plan(p,models,spot_check=False)),
                         ('independent',lambda:independent(models,targets,nmax))]:
            observed=[]
            for _ in range(runs):
                start=time.perf_counter();found=fun();elapsed=time.perf_counter()-start
                if found!=baseline:raise AssertionError('timed run output changed')
                observed.append(elapsed)
            times[name]={'median_seconds':statistics.median(observed),'samples_seconds':observed}
        results.append({'label':label,'targets':targets,'nmax':nmax,
                        'abstract_cost':p['score'],'independent_cost':p['independent_direct_score'],
                        'operations':[{'kind':s['kind'],'node':s['target'],'inputs':s['inputs']} for s in p['steps']],
                        'states_expanded':p['states_expanded'], 'scope_nodes':p['scope_node_count'],
                        'exact_integers_compared':len(targets)*(nmax+1),
                        'measured_independent_to_optimized':times['independent']['median_seconds']/times['optimized']['median_seconds'],
                        'timings':times,'result_digest_sha256':hashlib.sha256(json.dumps(baseline,sort_keys=True).encode()).hexdigest()})
    return {'author':'Komorebi P.','status':'exact_value_agreement',
            'source_db':str(db.name),'validated_hyperedges':len(all_hypers),'optimizer_eligible_hyperedges':len(hypers),
            'validated_gauges':len(approved), 'models':len(models),
            'runs':runs,'nmax':nmax,'results':results,
            'scope':'Exact extracted-formula identities, not all-index OEIS identification',
            'cost_claim':'Exact lowest abstract score only within bounded local graph; benchmark is workload-and-machine-specific'}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True);p.add_argument('--hyperedges',type=Path,required=True)
    p.add_argument('--gauges',type=Path,required=True);p.add_argument('--extra',type=Path)
    p.add_argument('--nmax',type=int,default=300);p.add_argument('--runs',type=int,default=5)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args(argv);r=run(a.db,a.hyperedges,a.gauges,a.extra,nmax=a.nmax,runs=a.runs)
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(r,indent=2)+'\n')
    for entry in r['results']:
        print(entry['label'],entry['measured_independent_to_optimized'],entry['operations'])


if __name__=='__main__':main()
