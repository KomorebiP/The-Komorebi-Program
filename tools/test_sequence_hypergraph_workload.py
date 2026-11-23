"""All-index hypergraph workload planner tests (offline, stdlib only).

Author: Komorebi P.
"""
from __future__ import annotations
import ast
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path
import random
import sqlite3
import tempfile
import unittest

from sequence_hypergraph_workload import (
    Action, PlanningBudgetExceeded, shortest_derivation, plan_prefix, run_plan,
    cache_snapshot, cache_valid, formula_fingerprint, load_formula_models,
    certify_hyperedges, hyperedge_score, choose_scope, apply_hyperedge, measured_strategy,
    required_input_horizons, run_indexed_hyperedge,
)
from sequence_linear_identity_compiler import key


A,B,C,D='A111111','A222222','A333333','A444444'


def fixture_model(sid,expr):
    ep={'oeis_id':sid,'formula_id':sid+'_formula','record_sha256':sid+'_source',
        'offset':0,'expression':expr,'key':key(expr)}
    return {'oeis_id':sid,'source_sha256':sid+'_source','offset':0,'ep':ep,'gauge':None}


def small_models():
    return {A:fixture_model(A,{1:[Q(0),Q(1)]}),
            B:fixture_model(B,{1:[Q(0),Q(0),Q(1)]}),
            C:fixture_model(C,{1:[Q(0),Q(1),Q(1)]}),
            D:fixture_model(D,{1:[Q(0),Q(0),Q(0),Q(1)]})}


def certificate(models,target,inputs,rhs):
    return {'target':target,'inputs':inputs,'rhs':rhs,'formula_id':'test-record',
        'bindings':{sid:{'source_sha256':models[sid]['source_sha256'],
                          'formula_fingerprint':formula_fingerprint(models[sid])}
                    for sid in [target,*inputs]}}


def fixture_db(db):
    db.executescript('''CREATE TABLE sequences(oeis_id TEXT,offset INTEGER,source_sha256 TEXT,terms_json TEXT);
       CREATE TABLE formulas(formula_id TEXT,oeis_id TEXT,evaluator_json TEXT,checked_terms INTEGER,
          origin TEXT,verification TEXT,expression TEXT);''')
    from sequence_hypergraph_workload import integer_exact
    from sequence_oeis_symbolic_network import formal_eval
    models=small_models()
    asts={A:{'op':'n'},B:{'op':'pow','base':{'op':'n'},'exp':2},
          C:{'op':'add','args':[{'op':'n'},{'op':'pow','base':{'op':'n'},'exp':2}]},
          D:{'op':'pow','base':{'op':'n'},'exp':3}}
    for sid,m in models.items():
        values=[integer_exact(formal_eval(m['ep']['expression'],i),sid,i) for i in range(24)]
        db.execute('INSERT INTO sequences VALUES(?,?,?,?)',(sid,0,m['source_sha256'],json.dumps(values)))
        db.execute('INSERT INTO formulas VALUES(?,?,?,?,?,?,?)',(
            sid+'_normal',sid,json.dumps(asts[sid]),24,'oeis_normalized','finite_checked',''))
    rows=[('formula_sum',C,f'a(n) = {A}(n) + {B}(n)'),
          ('formula_product',D,f'a(n) = {A}(n)*{B}(n)')]
    data=[]
    for fid,sid,raw in rows:
        db.execute('INSERT INTO formulas VALUES(?,?,?,?,?,?,?)',(
            fid,sid,None,24,'oeis_formula','unreviewed',raw))
        from sequence_oeis_formula_dependencies import rhs
        data.append({'target':sid,'inputs':[A,B],'rhs':rhs(raw),'formula_id':fid,
                    'source_text_sha256':hashlib.sha256(raw.encode()).hexdigest()})
    db.commit()
    return data


class TestExactPlanner(unittest.TestCase):
    def setUp(self):
        self.models=small_models()
        self.sum=certificate(self.models,C,[A,B],f'{A}(n) + {B}(n)')
        self.product=certificate(self.models,D,[A,B],f'{A}(n)*{B}(n)')

    def test_executable_two_input_hyperedge(self):
        p=plan_prefix(self.models,[],[self.sum,self.product],[A,B,C,D],14,scope=[A,B,C,D])
        self.assertEqual(p['optimality'],'exact_within_selected_scope')
        self.assertEqual(p['status'],'exact_cost_minimum_within_scope')
        computed=run_plan(p,self.models)
        self.assertEqual(computed[C], [i+i*i for i in range(15)])
        self.assertEqual(computed[D], [i**3 for i in range(15)])
        self.assertEqual(computed[A],list(range(15)))
        self.assertEqual(computed[B],[i*i for i in range(15)])

    def test_exact_brute_force_minimum(self):
        rng=random.Random(11222)
        nodes=(A,B,C,D)
        for _ in range(28):
            actions=[Action(node,(),rng.randint(2,16),'direct') for node in nodes]
            actions += [Action(C,(A,B),rng.randint(1,7),'hyperedge'),
                        Action(D,(B,C),rng.randint(1,7),'hyperedge'),
                        Action(A,(D,),rng.randint(1,7),'gauge')]
            out=shortest_derivation(nodes,actions,[C,D])
            # Independent exhaustive relaxation over all 2^4 availability states.
            dp={0:0}
            for count in range(4):
                for state,value in list(dp.items()):
                    for action in actions:
                        tbit=1<<nodes.index(action.target)
                        req=sum(1<<nodes.index(x) for x in action.inputs)
                        if state&tbit or (state&req)!=req:continue
                        nxt=state|tbit
                        dp[nxt]=min(dp.get(nxt,10**12),value+action.cost)
            exact=min(v for s,v in dp.items() if s&(1<<2) and s&(1<<3))
            self.assertEqual(out['score'],exact)
            self.assertEqual(sum(a.cost for a in out['steps']),exact)

    def test_cycle_not_usable_as_a_source(self):
        actions=[Action(B,(C,),1,'hyperedge'),Action(C,(B,),1,'hyperedge'),
                 Action(B,(),9,'direct'),Action(C,(),20,'direct')]
        p=shortest_derivation([B,C],actions,[B,C])
        self.assertEqual(p['score'],10)
        self.assertEqual(p['steps'][0].kind,'direct')

    def test_nonreversible_multiplication(self):
        actions=[Action(C,(A,B),1,'hyperedge'),Action(C,(),20,'direct'),
                 Action(A,(),7,'direct'),Action(B,(),7,'direct')]
        p=shortest_derivation([A,B,C],actions,[A,C])
        self.assertNotIn('inversion',str(p))
        self.assertTrue(any(a.target==A and a.kind=='direct' for a in p['steps']))

    def test_budget_failure_is_explicit(self):
        acts=[Action(x,(),1,'direct') for x in [A,B,C,D]]
        with self.assertRaises(PlanningBudgetExceeded):
            shortest_derivation([A,B,C,D],acts,[A,B,C,D],max_states=1)

    def test_mutated_cache_rejected(self):
        v=[0,1,2,3,4]
        snap=cache_snapshot(self.models[A],v)
        self.assertTrue(cache_valid(self.models[A],snap,4))
        hacked={**snap,'values':[0,1,99,3,4]}
        self.assertFalse(cache_valid(self.models[A],hacked,4))
        changed={**self.models[A],'source_sha256':'new-source'}
        self.assertFalse(cache_valid(changed,snap,4))
        p=plan_prefix(self.models,[],[self.sum],[A,B,C],4,scope=[A,B,C],cache={A:snap})
        self.assertIn(A,p['cached_nodes'])
        self.assertEqual(run_plan(p,self.models,cache={A:snap})[C][-1],20)
        with self.assertRaises(ValueError):run_plan(p,self.models,cache={A:hacked})

    def test_mutated_runtime_identity_detected(self):
        p=plan_prefix(self.models,[],[self.sum],[A,B,C],3,scope=[A,B,C])
        changed=dict(self.models)
        changed[A]={**self.models[A],'source_sha256':'tampered'}
        with self.assertRaises(ValueError):run_plan(p,changed)

    def test_measured_selector_checks_exact_results(self):
        models=self.models
        p=plan_prefix(models,[],[self.sum],[A,B,C],14,scope=[A,B,C])
        result=measured_strategy(models,p,runs=2)
        self.assertEqual(result['status'],'exact_value_agreement')
        self.assertIn(result['winner'],('shared_dag','independent'))
        self.assertEqual(result['output_values_compared'],45)
        self.assertGreater(result['calibration_elapsed_seconds'],0)

    def test_all_inputs_must_fit_scope(self):
        scope=choose_scope([C],self.models,[],[self.sum],max_nodes=2,max_depth=2)
        self.assertEqual(scope,(C,))
        scope=choose_scope([C],self.models,[],[self.sum],max_nodes=3,max_depth=2)
        self.assertEqual(set(scope),{A,B,C})


class TestSourceBoundHyperedges(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.dbpath=Path(self.temp.name)/'mini.sqlite3'
        self.db=sqlite3.connect(self.dbpath)
        self.entries=fixture_db(self.db)
        self.ledger=Path(self.temp.name)/'ledger.json'
        self.ledger.write_text(json.dumps({'admissible_edges':self.entries}))
        self.models,_=load_formula_models(self.db)

    def tearDown(self):
        self.db.close();self.temp.cleanup()

    def test_replay_two_hyperedges(self):
        edges,receipt=certify_hyperedges(self.db,self.ledger,self.models)
        self.assertEqual(receipt['certified'],2)
        self.assertEqual(len(edges),2)
        result=plan_prefix(self.models,[],edges,[A,B,C,D],11,scope=[A,B,C,D])
        found=run_plan(result,self.models)
        self.assertEqual(found[D][11],1331)
        self.assertEqual(found[C][11],132)

    def test_changed_raw_text_rejected(self):
        self.db.execute('UPDATE formulas SET expression=expression||" + 0" WHERE formula_id=?',('formula_sum',))
        self.db.commit()
        with self.assertRaises(ValueError):certify_hyperedges(self.db,self.ledger,self.models)

    def test_altered_rhs_rejected(self):
        data=json.loads(self.ledger.read_text())
        data['admissible_edges'][0]['rhs']=f'{A}(n) + {A}(n)'
        self.ledger.write_text(json.dumps(data))
        with self.assertRaises(ValueError):certify_hyperedges(self.db,self.ledger,self.models)

    def test_silent_offset_changes_rejected(self):
        data=json.loads(self.ledger.read_text())
        data['admissible_edges'][0]['rhs']=f'{A}(n+1) + {B}(n)'
        self.ledger.write_text(json.dumps(data))
        with self.assertRaises(ValueError):certify_hyperedges(self.db,self.ledger,self.models)

    def test_current_source_terms_are_rechecked(self):
        changed=json.dumps([500]+list(range(1,24)))
        self.db.execute('UPDATE sequences SET terms_json=? WHERE oeis_id=?',(changed,A))
        self.db.commit()
        models,info=load_formula_models(self.db)
        self.assertIn(A,info['rejected_stale_or_inconsistent_models'])
        self.assertNotIn(A,models)
        with self.assertRaises(ValueError):certify_hyperedges(self.db,self.ledger,models)

    def test_term_fingerprint_changes_without_source_sha_mutation(self):
        from sequence_hypergraph_workload import cache_snapshot,cache_valid
        before=cache_snapshot(self.models[A],[0,1,2])
        changed=json.dumps([0,1,2,3]+[i for i in range(4,24)])
        # Formally same values, but source's stored term representation changed.
        self.db.execute('UPDATE sequences SET terms_json=? WHERE oeis_id=?',(changed,A))
        self.db.commit()
        # A JSON representation change is still a change of the retained data.
        models,_=load_formula_models(self.db)
        self.assertTrue(cache_valid(models[A],before,2))  # unchanged bytes exactly
        changed=json.dumps([0,1,2,3]+[i for i in range(4,24)],indent=1)
        self.db.execute('UPDATE sequences SET terms_json=? WHERE oeis_id=?',(changed,A))
        self.db.commit()
        models,_=load_formula_models(self.db)
        self.assertFalse(cache_valid(models[A],before,2))

    def test_shifted_input_horizon(self):
        new_text=f'a(n) = {A}(n+1) + {B}(n) - 1'
        fid='shifted_sum'
        self.db.execute('INSERT INTO formulas VALUES(?,?,?,?,?,?,?)',(
            fid,C,None,24,'oeis_formula','unreviewed',new_text))
        self.db.commit()
        cert={'target':C,'inputs':[A,B],'rhs':new_text.split('=',1)[1].strip(),
              'formula_id':fid,'source_text_sha256':hashlib.sha256(new_text.encode()).hexdigest()}
        self.ledger.write_text(json.dumps({'admissible_edges':[cert]}))
        with self.assertRaises(ValueError):
            certify_hyperedges(self.db,self.ledger,self.models,allow_indexed=False)
        edges,stats=certify_hyperedges(self.db,self.ledger,self.models,allow_indexed=True)
        self.assertEqual(stats['certified'],1)
        self.assertEqual(required_input_horizons(edges[0],10),{A:11,B:10})
        self.assertEqual(run_indexed_hyperedge(edges[0],self.models,10),
                         [n+n*n for n in range(11)])

    def test_polyphase_input_horizon(self):
        sid='A555555'
        exp={1:[Q(0),Q(0),Q(4)]}
        norm={'op':'mul','args':[4,{'op':'pow','base':{'op':'n'},'exp':2}]}
        values=[4*n*n for n in range(24)]
        self.db.execute('INSERT INTO sequences VALUES(?,?,?,?)',(
             sid,0,sid+'_source',json.dumps(values)))
        self.db.execute('INSERT INTO formulas VALUES(?,?,?,?,?,?,?)',(
            sid+'_normalized',sid,json.dumps(norm),24,'oeis_normalized','finite_checked',''))
        text=f'a(n) = {A}(2*n)^2'
        self.db.execute('INSERT INTO formulas VALUES(?,?,?,?,?,?,?)',(
            'polyphase_squares',sid,None,24,'oeis_formula','unreviewed',text))
        self.db.commit()
        models,_=load_formula_models(self.db)
        cert={'target':sid,'inputs':[A],'rhs':f'{A}(2*n)**2',
              'formula_id':'polyphase_squares','source_text_sha256':hashlib.sha256(text.encode()).hexdigest()}
        self.ledger.write_text(json.dumps({'admissible_edges':[cert]}))
        edges,stats=certify_hyperedges(self.db,self.ledger,models,
                                      require_multi=False,allow_indexed=True)
        self.assertEqual(len(edges),1)
        self.assertEqual(edges[0]['index_maps'],{A:[[2,0]]})
        self.assertEqual(required_input_horizons(edges[0],10),{A:20})
        self.assertEqual(run_indexed_hyperedge(edges[0],models,10),[4*n*n for n in range(11)])

    def test_unsafe_program_never_executed(self):
        data=json.loads(self.ledger.read_text())
        data['admissible_edges'][0]['rhs']='__import__("os").system("echo never")'
        self.ledger.write_text(json.dumps(data))
        with self.assertRaises(ValueError):certify_hyperedges(self.db,self.ledger,self.models)


if __name__=='__main__':unittest.main()
