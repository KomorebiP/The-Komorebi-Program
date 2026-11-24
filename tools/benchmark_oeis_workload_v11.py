"""Reproducible exact shared-workload experiments on source-bound OEIS models.

Author: Komorebi P.
Compares the independently streamed hypergeometric recurrences against a
shared, proof-carrying Steiner tree. Does not assume that the tree is faster.
"""
from __future__ import annotations
import argparse,json,platform,hashlib,time
from pathlib import Path
from sequence_workload_planner import load_project,plan_gauge_prefix,select_measured_strategy

WORKLOADS=[
 ('catalan-family-3', ['A000108','A000984','A002544'],1000),
 ('catalan-family-3-large', ['A000108','A000984','A002544'],2500),
 ('binomial-family-5', ['A000108','A000984','A002544','A002457','A002738'],1000),
 ('binomial-family-5-large', ['A000108','A000984','A002544','A002457','A002738'],2500),
]

def execute(db,extras,gauges,runs):
    models,load=load_project(db,extras)
    results=[]
    for title,ids,nmax in WORKLOADS:
        plan=plan_gauge_prefix(models,gauges,ids,nmax)
        measurement=select_measured_strategy(models,plan,runs=runs)
        results.append(dict(name=title,targets=ids,nmax=nmax,
            abstract_work_score=plan['abstract_cost'],direct_only_score=plan['direct_only_cost'],
            modeled_savings_factor=plan['modeled_savings_factor'],
            recipe_summary=[{'node':r['node'],'method':r['method'],'depends_on':r['depends_on']} for r in plan['recipes']],
            measured=measurement))
    return dict(author='Komorebi P.',status='all_values_exact_and_independently_agree',
         python=platform.python_version(),platform=platform.platform(),
         source=Path(db).name,gauge_source=Path(gauges).name,
         gauge_ledger_sha256=hashlib.sha256(Path(gauges).read_bytes()).hexdigest(),
         model_load=load,workloads=results,
         caveats=['Formula identities proved conditional on extracted formula definitions, not global OEIS identification',
            'All-index transfer proof does not imply computation speedup',
            'Timing samples exclude one-off model loading and certificate graph validation',
            'Calibration itself evaluates multiple competing plans and has a cost',
            'Operation-count score is heuristic; observed runtimes choose the empirical winner',
            'The planner is exact only within a six-output, symmetric additive certified-gauge cost model'])

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--db',type=Path,required=True)
    p.add_argument('--extra',type=Path,required=True)
    p.add_argument('--gauges',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--runs',type=int,default=5)
    a=p.parse_args()
    result=execute(a.db,a.extra,a.gauges,a.runs)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    print(json.dumps([{k:v for k,v in x.items() if k in ('name','nmax','modeled_savings_factor')} |
        {'winner':x['measured']['winner'],'observed_direct_to_shared_ratio':x['measured']['observed_direct_to_shared_ratio']}
        for x in result['workloads']],indent=2))
if __name__=='__main__':main()
