"""Source-bound real-OEIS replay of indexed dependencies and composed horizon paths.
Author: Komorebi P.

This audit intentionally does NOT claim a global OEIS theorem. It checks exact
identities between extracted formula expressions, plus finite term receipts.
"""
from __future__ import annotations

import argparse
from collections import Counter
import statistics
import hashlib
import json
from pathlib import Path
import sqlite3

from sequence_hypergraph_workload import (
    load_formula_models, certify_hyperedges, verified_compatible_gauges, direct_cost, evaluate_model,
    hyperedge_score, required_input_horizons, integer_exact,
)
from sequence_oeis_symbolic_network import formal_eval
from sequence_workload_planner import verified_gauges
from sequence_hypergeometric_gauges import load_models
from sequence_variable_horizon import (
    apply_certified_indexed_hyperedge, plan_variable_horizon, run_variable_plan,
)


def audit(dbpath,ledger,extra,*,nmax=20,gauges_path=None):
    with sqlite3.connect(dbpath) as db:
        check=db.execute('PRAGMA integrity_check').fetchone()[0]
        if check!='ok':raise RuntimeError('source database failed integrity check')
        models,model_info=load_formula_models(db,extra)
        certs,cert_info=certify_hyperedges(db,ledger,models,require_multi=False,allow_indexed=True)
        seq_total=db.execute('SELECT COUNT(*) FROM sequences').fetchone()[0]
        formula_count=db.execute('SELECT COUNT(*) FROM formulas').fetchone()[0]
        gauge_models, _ = load_models(db,extra) if gauges_path else ({}, {})
    indexed=[c for c in certs if any(tuple(pair)!=(1,0) for pairs in c['index_maps'].values() for pair in pairs)]
    checked=0;max_required=0;operations=Counter();proof_digests=[]
    for cert in indexed:
        needed=required_input_horizons(cert,nmax)
        prefixes={sid:evaluate_model(models[sid],h,direct_cost(models[sid],h)[1]) for sid,h in needed.items()}
        computed=apply_certified_indexed_hyperedge(prefixes,cert,models,nmax)
        for k,value in enumerate(computed):
            expect=integer_exact(formal_eval(models[cert['target']]['ep']['expression'],k),cert['target'],k)
            if value!=expect:raise AssertionError('indexed source expression mismatch')
            checked+=1
        max_required=max(max_required,max(needed.values(),default=0))
        operations[('multisource' if len(cert['inputs'])>1 else 'single_source')]+=1
        proof_digests.append(hashlib.sha256(json.dumps([cert['target'],cert['rhs'],needed,computed],sort_keys=True,
                                                       separators=(',',':')).encode()).hexdigest())
    # Every one-input indexed edge can now participate in a query-local DAG.
    # Importantly, the cost planner is free to reject a valid transfer.
    selected=0;end_to_end_values=0;chosen_ratios=[];chosen_examples=[];all_plan_hashes=[];edge_detail=[]
    for cert in indexed:
        scope=list(dict.fromkeys((cert['target'],*cert['inputs'])))
        plan=plan_variable_horizon(models,[],[cert],[cert['target']],nmax,
                                   scope=scope,max_depth=1,cap=max(128,4*nmax+12))
        outputs,receipts=run_variable_plan(plan,models)
        expect=[integer_exact(formal_eval(models[cert['target']]['ep']['expression'],j),
                              cert['target'],j) for j in range(nmax+1)]
        if outputs[cert['target']]!=expect:raise AssertionError('optimized indexed plan mismatch')
        end_to_end_values+=len(expect)
        chosen=any(step['kind']=='hyperedge' for step in plan['steps'])
        if chosen:
            selected+=1
            chosen_ratios.append(plan['independent_direct_score']/plan['score'])
            if len(chosen_examples)<10:
                chosen_examples.append({'target':cert['target'], 'score':plan['score'],
                       'direct_score':plan['independent_direct_score'],
                       'steps':[(s['target'],s['horizon'],s['kind']) for s in plan['steps']]})
        edge_detail.append({'target':cert['target'],'inputs':cert['inputs'],
            'rhs':cert['rhs'],'index_maps':cert['index_maps'],
            'source_text_sha256':cert['source_text_sha256'],
            'required_input_horizons':required_input_horizons(cert,nmax),
            'cost_model_choice':'indexed_transfer' if chosen else 'direct',
            'score':plan['score'],'independent_direct_score':plan['independent_direct_score']})
        all_plan_hashes.append(hashlib.sha256(json.dumps([cert['target'],plan['steps'],expect],
                            sort_keys=True,default=str,separators=(',',':')).encode()).hexdigest())
    gauge_sanity=None
    if gauges_path:
        approved,review=verified_gauges(gauge_models,gauges_path)
        compatible=verified_compatible_gauges(models,approved)
        wanted=[r for r in compatible if {r['source'],r['target']}=={'A000108','A000984'}]
        if len(wanted)!=1:raise AssertionError('Catalan/central-binomial gauge admission failed')
        gauge_plan=plan_variable_horizon(models,wanted,[],['A000108','A000984'],nmax,
                                scope=['A000108','A000984'],max_depth=1)
        numbers,_=run_variable_plan(gauge_plan,models)
        if any(numbers['A000984'][k]!=(k+1)*numbers['A000108'][k] for k in range(nmax+1)):
            raise AssertionError('exact Catalan/central-binomial gauge values disagree')
        gauge_sanity={'pair':['A000108','A000984'],
             'gauge_certified':len(wanted),'ratio_identity':'A000984(n)=(n+1)*A000108(n)',
             'values_checked':2*(nmax+1),'chosen_steps':[(a['target'],a['kind']) for a in gauge_plan['steps']],
             'proof_status':'all-index formula identity; finite OEIS identification',
             'total_compatible_gauges':len(compatible),'gauge_ledger':review}
    # A real two-hop path: A016789(n) = A005449(n+1)-A005449(n)
    # A005449(n) = A000217(2n)-A000217(n).
    first=next(c for c in certs if c['target']=='A005449' and c['rhs']=='A000217(2*n) - A000217(n)')
    second=next(c for c in certs if c['target']=='A016789' and c['rhs']=='A005449(n+1) - A005449(n)')
    scope=['A000217','A005449','A016789']
    planned=plan_variable_horizon(models,[],[first,second],['A016789'],nmax,
                                   scope=scope,max_depth=2,cap=4*nmax+10)
    chosen,chosen_steps=run_variable_plan(planned,models)
    h_base=2*(nmax+1);h_mid=nmax+1
    forced=plan_variable_horizon(models,[],[first,second],['A016789'],nmax,
                                 scope=scope,max_depth=2,cap=4*nmax+10)
    manual=[
      {'target':'A000217','horizon':h_base,'inputs':[],'required_horizons':{},
       'kind':'direct','record':None,'method':None,'cost':0},
      {'target':'A005449','horizon':h_mid,'inputs':['A000217'],
       'required_horizons':required_input_horizons(first,h_mid),
       'kind':'hyperedge','record':first,'method':None,'cost':hyperedge_score(first,h_mid)},
      {'target':'A016789','horizon':nmax,'inputs':['A005449'],
       'required_horizons':required_input_horizons(second,nmax),
       'kind':'hyperedge','record':second,'method':None,'cost':hyperedge_score(second,nmax)},
    ]
    manual[0]['cost'],manual[0]['method']=direct_cost(models['A000217'],h_base)
    forced['steps']=manual
    via_chain,chain_steps=run_variable_plan(forced,models)
    if via_chain!=chosen:raise AssertionError('real source chain disagrees with selected optimizer plan')
    expected=[3*n+2 for n in range(nmax+1)]
    if chosen['A016789']!=expected:raise AssertionError('independent polynomial identity wrong')
    # Report the real planner's choice faithfully, even when it rejects
    # algebraically valid multihop paths as more expensive.
    with open(dbpath,'rb') as stream:
        db_sha256=hashlib.file_digest(stream,'sha256').hexdigest()
    return {
        'version':'1.3','author':'Komorebi P.','source':'official OEIS .seq snapshot',
        'source_db_sha256':db_sha256,
        'db_integrity':check,'source_sequence_records':seq_total,'source_formula_records':formula_count,
        'models_rechecked':model_info['finite_source_rechecked'],
        'all_index_formula_hyperedges':len(certs),'indexed_formula_hyperedges':len(indexed),
        'indexed_automated_replay_values':checked,'indexed_replay_failures':0,
        'query_plans_executed':len(indexed),'query_plan_values_checked':end_to_end_values,
        'query_plans_with_selected_indexed_edge':selected,
        'query_plans_with_direct_selection':len(indexed)-selected,
        'selected_indexed_heuristic_ratio_median':statistics.median(chosen_ratios) if chosen_ratios else None,
        'selected_indexed_heuristic_ratio_min':min(chosen_ratios) if chosen_ratios else None,
        'selected_indexed_examples':chosen_examples,'indexed_edge_detail':edge_detail,
        'query_plan_replay_sha256':hashlib.sha256('\n'.join(all_plan_hashes).encode()).hexdigest(),
        'indexed_max_source_local_index_at_nmax':max_required,'replay_target_horizon':nmax,
        'indexed_input_types':dict(operations),'indexed_replay_sha256':hashlib.sha256(
            '\n'.join(proof_digests).encode()).hexdigest(),
        'model_incompatibilities':model_info['incompatible_overlapping_models'],
        'gauge_sanity':gauge_sanity,
        'two_hop_real_example':{'formula_chain':[
            'A005449(n) = A000217(2*n)-A000217(n)',
            'A016789(n) = A005449(n+1)-A005449(n)'],
            'target_horizon':nmax,'middle_required_horizon':h_mid,
            'base_required_horizon':h_base,
            'direct_independent_output_values':len(expected),
            'planner_score':planned['score'],
            'planner_steps':[{'target':s['target'],'kind':s['kind'],'horizon':s['horizon'],
                              'required_horizons':s['required_horizons']} for s in planned['steps']],
            'explicit_two_hop_work_score':sum(x['cost'] for x in manual),
            'two_hop_values_checked':len(expected),
            'two_hop_step_digests':[x['sha256'] for x in chain_steps]},
        'claims_scope':'all-index formula expression identities and local finite OEIS term identification only',
        'optimization_scope':'finite horizon tiers, bounded nodes/depth, declared full-prefix operation-cost heuristic',
        'raw_source_certificate_replay':cert_info,
    }


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',required=True,type=Path)
    p.add_argument('--hyperedges',required=True,type=Path)
    p.add_argument('--extra',required=True,type=Path)
    p.add_argument('--gauges',type=Path)
    p.add_argument('--nmax',type=int,default=20)
    p.add_argument('--output',required=True,type=Path)
    args=p.parse_args(argv)
    result=audit(args.db,args.hyperedges,args.extra,nmax=args.nmax,gauges_path=args.gauges)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('model_incompatibilities','two_hop_real_example','indexed_edge_detail','selected_indexed_examples')},indent=2))

if __name__=='__main__':main()
