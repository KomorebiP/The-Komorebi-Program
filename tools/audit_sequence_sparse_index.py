"""Real OEIS (99,999 record) sparse-index replay; no source mutation.

Author: Komorebi P.  All-index results concern extracted formula definitions;
OEIS sequence identification remains finite-term checked.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sqlite3
import statistics
import time

from sequence_hypergraph_workload import load_formula_models,certify_hyperedges
from sequence_sparse_index import (
    prepare_sparse_tasks, shortest_sparse_plan, execute_sparse_plan,
    source_requirements,direct_value,
)


def audit(db_path,ledger,*,limit=24):
    db_path=Path(db_path)
    sha=hashlib.sha256(db_path.read_bytes()).hexdigest()
    with sqlite3.connect(f'file:{db_path}?mode=ro',uri=True) as db:
        db.execute('PRAGMA query_only=ON')
        integrity=db.execute('PRAGMA integrity_check').fetchone()[0]
        if integrity!='ok':raise ValueError('SQLite source integrity failure')
        models,model_info=load_formula_models(db)
        certs,stats=certify_hyperedges(db,ledger,models,require_multi=False,allow_indexed=True)
        indexed=[]
        for c in certs:
            maps=[tuple(x) for coords in c['index_maps'].values() for x in coords]
            if not maps or all(v==(1,0) for v in maps):continue
            if max(m for m,r in maps)>5 or max(r for m,r in maps)>12:continue
            if len(maps)>5:continue
            indexed.append(c)
        # Deterministic complete/index-truncated sample with no duplicate certificates.
        indexed.sort(key=lambda x:(x['target'],x['formula_id']))
        chosen=indexed[:limit]
        audits=[];costs=[]
        for cert in chosen:
            n=37 if len(cert['inputs'])<2 else 23
            target=cert['target']
            graph=prepare_sparse_tasks(models,[cert],[(target,n)],max_index=5000,
                max_tasks=24,depth=1,allow_packets=False,db=db,
                direct_score=lambda sid,index: 800 if sid==target else 6,
                hyperedge_score=lambda c,index: 2)
            plan=shortest_sparse_plan(graph,max_states=60000)
            outputs,receipts=execute_sparse_plan(graph,plan,models,db=db)
            expected=direct_value(models[target],n)
            if outputs[(target,n)]!=expected:
                raise AssertionError('real OEIS formula evaluation mismatch '+target)
            if not any(a.kind=='hyperedge' for a in plan['steps']):
                raise AssertionError('cost-controlled plan did not select certified transfer')
            direct_cost=800
            savings=direct_cost/plan['cost']
            costs.append(savings)
            audits.append({'target':target,'requested_index':n,'inputs':list(cert['inputs']),
                           'index_maps':cert['index_maps'],'source_indices':[[sid,k] for sid,k in source_requirements(cert,[n])],
                           'computed_term_count':len(plan['steps']),
                           'full_source_prefix_horizon':max((k for _,k in source_requirements(cert,[n])),default=0),
                           'exact_match':True,'cost_score':plan['cost'],
                           'chosen_methods':[a.kind for a in plan['steps']],
                           'certified_formula_id':cert['formula_id'],
                           'output_sha256':hashlib.sha256(str(expected).encode()).hexdigest(),
                           'replay_term_hashes':[v['value_sha256'] for v in receipts]})
    return {'schema':1,'author':'Komorebi P.','source_database_sha256':sha,
            'integrity_check':integrity,'source_sequence_models':model_info['combined_models'],
            'source_certificates_recertified':len(certs),'indexed_eligible':len(indexed),
            'indexed_sample_replayed':len(audits),'exact_outputs':len(audits),
            'transfer_cost_reductions_heuristic_median':statistics.median(costs) if costs else None,
            'cost_scope':'Explicit demonstrator operation scores, not runtime or bit complexity',
            'source_scope':'Exact extracted formula identities; OEIS identification remains finite term checked',
            'samples':audits}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',required=True,type=Path)
    p.add_argument('--ledger',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--limit',type=int,default=24)
    a=p.parse_args()
    result=audit(a.db,a.ledger,limit=a.limit)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='samples'},indent=2))

if __name__=='__main__':main()
