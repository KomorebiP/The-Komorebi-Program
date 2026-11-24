"""Adversarial and exact tests for proof-gated variable-horizon computation.
Author: Komorebi P.
"""
from fractions import Fraction as Q
import heapq
import hashlib
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from sequence_linear_identity_compiler import key
from sequence_hypergraph_workload import (
    PlanningBudgetExceeded, cache_snapshot, formula_fingerprint,
    load_formula_models, certify_hyperedges,
)
from sequence_variable_horizon import (
    HorizonAction, candidate_horizons, make_horizon_actions, shortest_horizon_derivation,
    plan_variable_horizon, run_variable_plan, apply_certified_indexed_hyperedge,
    measured_variable_strategy,
)

A,B,C,D='A111111','A222222','A333333','A444444'


def ep_model(sid,poly):
    expression={1:[Q(x) for x in poly]}
    ep={'oeis_id':sid,'formula_id':sid+'_formula','record_sha256':sid+'_sha',
        'offset':0,'expression':expression,'key':key(expression)}
    return {'oeis_id':sid,'source_sha256':sid+'_sha','offset':0,'ep':ep,'gauge':None}


def four_models():
    return {A:ep_model(A,[0,1]), B:ep_model(B,[0,0,1]),
            C:ep_model(C,[1,4,1]), D:ep_model(D,[8,9,1])}


def cert(models,target,inputs,rhs,maps):
    return {'target':target,'inputs':inputs,'rhs':rhs,'formula_id':target+'_source',
        'index_maps':maps,
        'bindings':{s:{'source_sha256':models[s]['source_sha256'],
                       'formula_fingerprint':formula_fingerprint(models[s])}
                    for s in (target,*inputs)}}


def chain():
    models=four_models()
    c=cert(models,C,[A,B],f'{A}(2*n) + {B}(n+1)',{A:[[2,0]],B:[[1,1]]})
    d=cert(models,D,[A,C],f'{C}(n+1) + {A}(3*n+2)',{C:[[1,1]],A:[[3,2]]})
    return models,c,d


class HorizonSearch(unittest.TestCase):
    def setUp(self):
        self.models,self.c,self.d=chain()

    def test_backward_horizon_exact_composition(self):
        tiers,detail=candidate_horizons([A,B,C,D],[],[self.c,self.d],[D],5,depth=2,cap=40)
        self.assertEqual(tiers[D],(5,))
        self.assertEqual(tiers[C],(6,))
        self.assertEqual(tiers[A],(12,17))
        self.assertEqual(tiers[B],(7,))
        self.assertEqual(detail['tier_count'],5)

    def test_repeated_source_calls_take_max_not_sum(self):
        models=self.models
        changed={**models,C:ep_model(C,[3,3])}
        both=cert(changed,C,[A],f'{A}(2*n)+{A}(n+3)',{A:[[2,0],[1,3]]})
        tiers,_=candidate_horizons([A,C],[],[both],[C],6,depth=1)
        self.assertEqual(tiers[A],(12,))
        result=apply_certified_indexed_hyperedge({A:list(range(13))},both,changed,6)
        self.assertEqual(result,[3*n+3 for n in range(7)])

    def test_multi_level_global_optimum_against_exhaustive_states(self):
        tiers={A:(6,11,17), B:(7,), C:(5,6), D:(5,)}
        actions=[HorizonAction(A,6,(),(),8,'direct'),HorizonAction(A,11,(),(),13,'direct'),
                 HorizonAction(A,17,(),(),18,'direct'),HorizonAction(B,7,(),(),7,'direct'),
                 HorizonAction(C,5,(),(),70,'direct'),HorizonAction(C,6,(),(),72,'direct'),
                 HorizonAction(D,5,(),(),90,'direct'),
                 HorizonAction(C,6,(A,B),(12,7),3,'hyperedge'),
                 HorizonAction(D,5,(C,A),(6,17),4,'hyperedge')]
        # High A horizon 17 serves both consumers, with no duplicate charge.
        result=shortest_horizon_derivation(tiers,actions,[D],5)
        self.assertEqual(result['score'],18+7+3+4)
        self.assertEqual(result['actions'][-1].target,D)
        # Independent exhaustive DP in a differently structured state search.
        nodes=sorted(tiers);levels={s:(-1,*tiers[s]) for s in nodes}
        start=tuple([-1]*len(nodes));best={start:0}
        q=[(0,start)]
        while q:
            cost,st=heapq.heappop(q)
            if cost!=best[st]:continue
            for act in actions:
                ti=nodes.index(act.target)
                if st[ti]>=act.horizon:continue
                if any(st[nodes.index(s)]<h for s,h in zip(act.inputs,act.needs)):continue
                nxt=list(st);nxt[ti]=act.horizon;nxt=tuple(nxt)
                cand=cost+act.cost
                if cand<best.get(nxt,10**9):best[nxt]=cand;heapq.heappush(q,(cand,nxt))
        exact=min(cost for state,cost in best.items() if state[nodes.index(D)]>=5)
        self.assertEqual(result['score'],exact)

    def test_missing_prerequisite_cannot_be_skipped(self):
        tiers={A:(3,),C:(3,)}
        actions=[HorizonAction(A,3,(),(),11,'direct'),
                 HorizonAction(C,3,(A,),(6,),1,'hyperedge'),
                 HorizonAction(C,3,(),(),20,'direct')]
        out=shortest_horizon_derivation(tiers,actions,[C],3)
        self.assertEqual(out['score'],20)
        self.assertEqual(out['actions'][0].kind,'direct')

    def test_longer_source_prefix_than_target(self):
        tiers,_=candidate_horizons([A,B,C],[],[self.c],[C],10,depth=1)
        acts,info=make_horizon_actions(self.models,[],[self.c],tiers)
        edge=[a for a in acts if a.kind=='hyperedge'][0]
        self.assertEqual(edge.needs,(20,11))
        self.assertEqual(edge.horizon,10)
        self.assertEqual(info['hyperedge_actions'],1)

    def test_bounded_graph_excludes_beyond_cap(self):
        tiers,info=candidate_horizons([A,B,C],[],[self.c],[C],10,depth=1,cap=19)
        self.assertEqual(tiers[A],())
        self.assertGreater(info['omitted_over_cap'],0)
        acts,_=make_horizon_actions(self.models,[],[self.c],tiers)
        self.assertFalse(any(a.kind=='hyperedge' for a in acts))
        plan=plan_variable_horizon(self.models,[],[self.c],[C],10,scope=[A,B,C],cap=19)
        self.assertEqual(plan['steps'][0]['kind'],'direct')

    def test_state_and_tier_budgets_fail_explicitly(self):
        tiers={A:(1,2,3),B:(1,2,3)}
        actions=[HorizonAction(A,1,(),(),1,'direct'),HorizonAction(B,1,(),(),1,'direct'),
                 HorizonAction(A,2,(),(),1,'direct'),HorizonAction(B,2,(),(),1,'direct'),
                 HorizonAction(A,3,(),(),1,'direct'),HorizonAction(B,3,(),(),1,'direct')]
        with self.assertRaises(PlanningBudgetExceeded):
            shortest_horizon_derivation(tiers,actions,[A,B],3,max_states=1)
        cert2=cert(self.models,C,[A],f'{A}(2*n)',{A:[[2,0]]})
        with self.assertRaises(PlanningBudgetExceeded):
            candidate_horizons([A,C],[],[cert2,cert(self.models,A,[C],f'{C}(2*n)',{C:[[2,0]]})],[C],1,depth=8,max_levels=2)

    def test_provenance_mutation_rejected_at_execution(self):
        p=plan_variable_horizon(self.models,[],[self.c],[C],5,scope=[A,B,C])
        altered={**self.models, A:{**self.models[A],'source_sha256':'changed'}}
        with self.assertRaises(ValueError):run_variable_plan(p,altered)

    def test_cached_prefix_is_validated(self):
        snap=cache_snapshot(self.models[A],list(range(25)))
        p=plan_variable_horizon(self.models,[],[self.c],[C],8,
                                 scope=[A,B,C],cache={A:snap})
        self.assertEqual(p['cached_prefix_horizons'][A],24)
        out,_=run_variable_plan(p,self.models,cache={A:snap})
        self.assertEqual(out[C], [n*n+4*n+1 for n in range(9)])
        corrupt={**snap,'values':[0,999]+list(range(2,25))}
        with self.assertRaises(ValueError):run_variable_plan(p,self.models,cache={A:corrupt})

    def test_exact_indexed_output_independent_of_planner_choice(self):
        inputs={A:list(range(18)),B:[n*n for n in range(9)]}
        vals=apply_certified_indexed_hyperedge(inputs,self.c,self.models,7)
        self.assertEqual(vals,[n*n+4*n+1 for n in range(8)])
        with self.assertRaises(ValueError):
            apply_certified_indexed_hyperedge({A:inputs[A][:-5],B:inputs[B]},self.c,self.models,7)

    def test_tampered_rhs_rejected_algebraically(self):
        inputs={A:list(range(18)),B:[n*n for n in range(9)]}
        forged={**self.c,'rhs':f'{A}(2*n) + {B}(n+2)'}
        with self.assertRaises(ValueError):apply_certified_indexed_hyperedge(inputs,forged,self.models,7)

    def test_stale_record_binding_rejected(self):
        inputs={A:list(range(18)),B:[n*n for n in range(9)]}
        forged={**self.c,'bindings':{**self.c['bindings'], A:{**self.c['bindings'][A], 'source_sha256':'old'}}}
        with self.assertRaises(ValueError):apply_certified_indexed_hyperedge(inputs,forged,self.models,7)

    def test_multihorizon_manual_two_hop_execution(self):
        # Explicit certified path; the optimizer is not forced to select this
        # when a cheaper direct source formula exists.
        p=plan_variable_horizon(self.models,[],[self.c,self.d],[D],5,
                                scope=[A,B,C,D],max_depth=2)
        p['steps']=[
          {'target':A,'horizon':17,'inputs':[],'required_horizons':{},
           'cost':None,'kind':'direct','record':None,'method':None},
          {'target':B,'horizon':7,'inputs':[],'required_horizons':{},
           'cost':None,'kind':'direct','record':None,'method':None},
          {'target':C,'horizon':6,'inputs':[A,B],'required_horizons':{A:12,B:7},
           'cost':None,'kind':'hyperedge','record':self.c,'method':None},
          {'target':D,'horizon':5,'inputs':[A,C],'required_horizons':{A:17,C:6},
           'cost':None,'kind':'hyperedge','record':self.d,'method':None},
        ]
        from sequence_hypergraph_workload import direct_cost,hyperedge_score
        for step in p['steps']:
            if step['kind']=='direct':
                step['cost'],step['method']=direct_cost(self.models[step['target']],step['horizon'])
            else:step['cost']=hyperedge_score(step['record'],step['horizon'])
        out,receipt=run_variable_plan(p,self.models)
        self.assertEqual(out[D],[n*n+9*n+8 for n in range(6)])
        self.assertEqual([x['horizon'] for x in receipt],[17,7,6,5])

    def test_forged_but_internally_consistent_cache_is_not_trusted(self):
        vals=list(range(20))
        snap=cache_snapshot(self.models[A],vals)
        hacked=[0,1,2,999]+list(range(4,20))
        snap['values']=hacked
        snap['values_sha256']=hashlib.sha256(json.dumps(hacked,separators=(',',':')).encode()).hexdigest()
        # A checksummed cache is not an authenticated cache. By default,
        # every cached value is rechecked against the exact formula.
        plan=plan_variable_horizon(self.models,[],[self.c],[C],7,
                                  scope=[A,B,C],cache={A:snap})
        with self.assertRaises(ValueError):run_variable_plan(plan,self.models,cache={A:snap})

    def test_modified_horizon_map_cannot_understate_required_prefix(self):
        prefixes={A:list(range(18)),B:[n*n for n in range(9)]}
        wrong={**self.c,'index_maps':{A:[[1,0]],B:[[1,1]]}}
        with self.assertRaises(ValueError):
            apply_certified_indexed_hyperedge(prefixes,wrong,self.models,7)

    def test_mathematical_offsets_are_converted_to_local_coordinates(self):
        base=ep_model(A,[1,1]);base['offset']=1;base['ep']={**base['ep'],'offset':1}
        end=ep_model(C,[3,2])
        models={A:base,C:end}
        evidence=cert(models,C,[A],f'{A}(2*n+3)',{A:[[2,2]]})
        self.assertEqual(apply_certified_indexed_hyperedge(
            {A:[i+1 for i in range(11)]},evidence,models,4),[3,5,7,9,11])
        tiers,_=candidate_horizons([A,C],[],[evidence],[C],4,depth=1)
        self.assertEqual(tiers[A],(10,))

    def test_empirical_selector_verifies_both_strategies(self):
        plan=plan_variable_horizon(self.models,[],[self.c],[C],9,scope=[A,B,C])
        report=measured_variable_strategy(plan,self.models,runs=2)
        self.assertEqual(report['values_compared'],10)
        self.assertIn(report['winner'],('variable_horizon_dag','independent'))
        self.assertEqual(report['runs'],2)

    def test_horizon_tier_zero_is_allowed(self):
        p=plan_variable_horizon(self.models,[],[self.c],[C],0,scope=[A,B,C],max_depth=1)
        out,_=run_variable_plan(p,self.models)
        self.assertEqual(out[C],[1])


if __name__=='__main__':unittest.main()
