"""Exact, adversarial tests of proof-gated multi-sequence work planning.

Author: Komorebi P.
"""
import hashlib
import itertools
import json
import tempfile
import unittest
from collections import deque
from pathlib import Path

from sequence_hypergeometric_gauges import certify_pair,source_model
from sequence_holonomic_compiler import fraction_eval
from sequence_workload_planner import (
    ROOT, WorkEdge, verified_gauges, plan_gauge_prefix,
    minimum_work_tree, independent_plan, direct_choice, run_plan,
    select_measured_strategy, apply_gauge, evaluate_prefix, make_cache_snapshot, valid_cache_snapshot, freeze_cache_snapshot
)

N={'op':'n'}
def mul(*args):return {'op':'mul','args':list(args)}
def add(*args):return {'op':'add','args':list(args)}
def model(sid,ast):
    vals=[str(int(fraction_eval(ast,n))) for n in range(30)]
    fingerprint=hashlib.sha256(sid.encode()).hexdigest()
    rec=source_model('F-'+sid,sid,ast,0,json.dumps(vals),fingerprint)
    assert rec is not None and rec['tail']==0
    return rec

class TestSteinerTheory(unittest.TestCase):
    def brute(self,names,links,rootcost,targets):
        es=[(ROOT,u,c) for u,(c,_) in rootcost.items()]
        es += [(e.u,e.v,e.cost) for e in links]
        best=10**9
        for r in range(1<<len(es)):
            cost=sum(edge[2] for i,edge in enumerate(es) if r&(1<<i))
            if cost>=best:continue
            graph={u:set() for u in names|{ROOT}}
            for i,(u,v,c) in enumerate(es):
                if r&(1<<i):graph[u].add(v);graph[v].add(u)
            visit={ROOT};queue=deque([ROOT])
            while queue:
                for v in graph[queue.popleft()]:
                    if v not in visit:visit.add(v);queue.append(v)
            if set(targets)<=visit:best=cost
        return best

    def test_optimum_agrees_with_exhaustive_edge_enumeration(self):
        nodes={'A','B','C','D'}
        base={'A':(6,'direct_ratio'),'B':(9,'direct_ast'),'C':(7,'direct_ratio'),'D':(5,'direct_ast')}
        edges=[WorkEdge('A','B',2,'gauge',{}),WorkEdge('B','C',2,'gauge',{}),WorkEdge('C','D',3,'gauge',{}),WorkEdge('A','D',7,'gauge',{})]
        for count in (1,2,3,4):
            for targets in itertools.combinations(sorted(nodes),count):
                expected=self.brute(nodes,edges,base,targets)
                result=minimum_work_tree(nodes,edges,base,targets)
                self.assertEqual(result['abstract_cost'],expected)
                self.assertTrue(result['exact_within_model'])

    def test_sharing_can_require_steiner_intermediate(self):
        nodes={'A','B','C'}
        direct={s:(100,'direct_ast') for s in nodes}
        links=[WorkEdge('A','B',1,'gauge',{}),WorkEdge('B','C',1,'gauge',{})]
        plan=minimum_work_tree(nodes,links,direct,['A','C'])
        self.assertEqual(plan['abstract_cost'],102)
        self.assertIn('B',[r['node'] for r in plan['recipes']])

    def test_deduplicates_targets_and_limits_exact_search(self):
        d={'A':(2,'direct_ast')}
        self.assertEqual(minimum_work_tree({'A'},[],d,['A','A'])['abstract_cost'],2)
        with self.assertRaises(ValueError):minimum_work_tree({'A'},[],d,[])
        with self.assertRaises(ValueError):minimum_work_tree(set('ABCDEFG'),[],{k:(1,'direct_ast') for k in 'ABCDEFG'},list('ABCDEFG'))

class TestRealFormulaGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        catalan={'op':'exact_div','num':{'op':'binomial','n':mul(2,N),'k':N},'den':add(N,1)}
        central={'op':'binomial','n':mul(2,N),'k':N}
        cubic={'op':'mul','args':[central,add(N,1)]}
        cls.models={x['oeis_id']:x for x in [model('A000108',catalan),model('A000984',central),model('A098765',cubic)]}
        cls.edges=[certify_pair(cls.models['A000108'],cls.models['A000984']),
                   certify_pair(cls.models['A000984'],cls.models['A098765'])]
        assert all(cls.edges)

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.ledger=Path(self.temp.name)/'proofs.jsonl'
        self.ledger.write_text(''.join(json.dumps(e)+'\n' for e in self.edges),encoding='utf8')

    def test_actual_formula_prefixes_match_direct_calculations(self):
        targets=list(self.models)
        plan=plan_gauge_prefix(self.models,self.ledger,targets,40)
        out=run_plan(plan,self.models)
        for id in targets:
            formula=[int(fraction_eval(self.models[id]['ast'],i)) for i in range(41)]
            self.assertEqual(out[id],formula)
        self.assertEqual(plan['verified_gauge_ledger']['accepted'],2)
        self.assertLess(plan['abstract_cost'],plan['direct_only_cost'])

    def test_gauge_inverse_is_exact(self):
        for e in self.edges:
            original=e['source'];target=e['target']
            a=evaluate_prefix(self.models[original],45,'direct_ratio')
            b=apply_gauge(a,e,True,45)
            self.assertEqual(b,evaluate_prefix(self.models[target],45,'direct_ratio'))
            self.assertEqual(a,apply_gauge(b,e,False,45))

    def test_tampered_normalizer_is_rejected_before_planning(self):
        cases=[('base_ratio','999/17'),('source_sha256','f'*64),('target_evaluator_sha256','0'*64),('support',99)]
        for field,value in cases:
            with self.subTest(field=field):
                entries=[dict(x) for x in self.edges]
                entries[0][field]=value
                self.ledger.write_text(''.join(json.dumps(e)+'\n' for e in entries),encoding='utf8')
                with self.assertRaises(ValueError):
                    plan_gauge_prefix(self.models,self.ledger,['A000108','A000984'],20)
        self.ledger.write_text(''.join(json.dumps(e)+'\n' for e in self.edges),encoding='utf8')

    def test_direct_computation_remains_legal_and_measured(self):
        targets=['A000108','A000984','A098765']
        plan=plan_gauge_prefix(self.models,self.ledger,targets,70)
        independ=independent_plan(self.models,targets,70)
        self.assertEqual(run_plan(plan,self.models),run_plan(independ,self.models))
        result=select_measured_strategy(self.models,plan,runs=2)
        self.assertEqual(result['status'],'exact_values_agree')
        self.assertEqual(result['outputs_checked'],213)
        self.assertIn(result['winner'],('shared_transfer','independent_direct'))

    def test_cached_prefix_reuses_verified_intermediary(self):
        src='A000108'
        values=evaluate_prefix(self.models[src],60,'direct_ratio')
        snap=make_cache_snapshot(self.models[src],values)
        cache={src:freeze_cache_snapshot(self.models[src],snap)}
        targets=['A000984','A098765']
        plan=plan_gauge_prefix(self.models,self.ledger,targets,60,cache=cache)
        self.assertTrue(any(x['method']=='cached' for x in plan['recipes']))
        outputs=run_plan(plan,self.models,cache=cache)
        direct=run_plan(independent_plan(self.models,targets,60),self.models)
        self.assertEqual(outputs,direct)
        self.assertTrue(valid_cache_snapshot(self.models[src],cache[src],60))
        self.assertFalse(valid_cache_snapshot(self.models[src],snap,61))

    def test_modified_cache_is_rejected_before_execution(self):
        source='A000108'
        snap=make_cache_snapshot(self.models[source],evaluate_prefix(self.models[source],20,'direct_ratio'))
        snap['values'][8]+=1
        self.assertFalse(valid_cache_snapshot(self.models[source],snap,20))
        with self.assertRaises(ValueError):
            run_plan({'targets':[source],'nmax':20,'recipes':[{'node':source,'method':'cached'}]},
                     self.models,cache={source:snap})

    def test_nonproof_matches_are_not_admitted(self):
        bad=dict(self.edges[0]);bad['base_ratio']='1/3'
        self.ledger.write_text(json.dumps(bad)+'\n',encoding='utf8')
        with self.assertRaises(ValueError):verified_gauges(self.models,self.ledger)

if __name__=='__main__':unittest.main()
