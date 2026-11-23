"""Exact algebra and adversarial checks for sparse-index planning and v0.8 bridge."""
from __future__ import annotations
import copy
import hashlib
import json
import random
import unittest
from fractions import Fraction as Q

from sequence_archive_v08_bridge import (
    quadratic_pair, quadratic_sparse, quadratic_certificate,
    quadratic_binomial_even,quadratic_binomial_odd,
    riordan_nth,riordan_sparse,riordan_requirements,
)
from sequence_sparse_index import (
    certify_sparse_edge,cache_record,direct_value,packet_from_ep,packet_nth,
    prepare_sparse_tasks,shortest_sparse_plan,execute_sparse_plan,plan_and_run,
    source_requirements,
)
from sequence_linear_identity_compiler import key as formal_key
from sequence_hypergraph_workload import formula_fingerprint,PlanningBudgetExceeded


def sample_models_and_edges():
    expressions={
        'A000217':{1:[Q(0),Q(1,2),Q(1,2)]},
        'A005449':{1:[Q(0),Q(1,2),Q(3,2)]},
        'A016789':{1:[Q(2),Q(3)]},
    }
    models={}
    for sid,expr in expressions.items():
        models[sid]={'oeis_id':sid,'source_sha256':hashlib.sha256((sid+'-formula-source').encode()).hexdigest(),
                     'offset':0,'terms_sha256':hashlib.sha256((sid+'-terms').encode()).hexdigest(),
                     'ep':{'expression':expr,'key':formal_key(expr),'formula_id':sid+'-ep','offset':0},
                     'gauge':None}
    rules=[('A005449',['A000217'],'A000217(2*n)-A000217(n)',{'A000217':[[2,0],[1,0]]}),
           ('A016789',['A005449'],'A005449(n+1)-A005449(n)',{'A005449':[[1,1],[1,0]]})]
    certs=[]
    for ix,(target,inputs,rhs,maps) in enumerate(rules):
        certs.append({'target':target,'inputs':inputs,'rhs':rhs,'formula_id':'example-'+str(ix),
                      'index_maps':maps,'bindings':{sid:{'source_sha256':models[sid]['source_sha256'],
                                    'formula_fingerprint':formula_fingerprint(models[sid])}
                                    for sid in (target,*inputs)},
                      'status':'all_index_extracted_formula_identity',
                      'oeis_identification':'finite_prefix_only'})
    return models,certs


class SparseOperatorTests(unittest.TestCase):
    def setUp(self):self.models,self.certs=sample_models_and_edges()

    def test_all_index_algebra_and_affine_composition(self):
        for c in self.certs:certify_sparse_edge(c,self.models)
        self.assertEqual(source_requirements(self.certs[0],[2,5]),
                         (('A000217',2),('A000217',4),('A000217',5),('A000217',10)))
        self.assertEqual(source_requirements(self.certs[1],[3,6]),
                         (('A005449',3),('A005449',4),('A005449',6),('A005449',7)))
        self.assertEqual(3*17+2,53)

    def test_sparse_two_hop_without_full_prefix(self):
        requested=[('A016789',11)]
        graph=prepare_sparse_tasks(self.models,self.certs,requested,
            direct_score=lambda sid,n:5 if sid=='A000217' else 1000,
            hyperedge_score=lambda c,n:1,allow_packets=False,max_tasks=24)
        plan=shortest_sparse_plan(graph)
        self.assertEqual(plan['cost'],23)  # 4 triangular values + 2 intermediates + target
        outputs,receipts=execute_sparse_plan(graph,plan,self.models)
        self.assertEqual(outputs[('A016789',11)],35)
        selected={a.target for a in plan['steps']}
        self.assertEqual(selected,{('A016789',11),('A005449',11),('A005449',12),
                                   ('A000217',11),('A000217',12),('A000217',22),('A000217',24)})
        self.assertEqual(len(receipts),7)

    def test_shared_requests_reuse_term(self):
        queries=[('A016789',11),('A016789',12)]
        graph=prepare_sparse_tasks(self.models,self.certs,queries,direct_score=lambda sid,n:
                                 5 if sid=='A000217' else 1000,
                                 hyperedge_score=lambda c,n:1,allow_packets=False,max_tasks=24)
        plan=shortest_sparse_plan(graph)
        output,_=execute_sparse_plan(graph,plan,self.models)
        self.assertEqual(output,{('A016789',11):35,('A016789',12):38})
        self.assertEqual(len([a for a in plan['steps'] if a.target[0]=='A005449']),3)
        self.assertLess(plan['cost'],2*23)

    def test_optimizer_selects_direct_for_linear(self):
        g=prepare_sparse_tasks(self.models,self.certs,[('A016789',300)],
                               direct_score=lambda sid,n:1 if sid=='A016789' else 20,
                               hyperedge_score=lambda c,n:20,allow_packets=False)
        p=shortest_sparse_plan(g)
        self.assertEqual(p['cost'],1)
        self.assertEqual(len(p['steps']),1)
        self.assertEqual(p['steps'][0].kind,'direct')

    def test_symbolic_forgery_rejected(self):
        invalid=copy.deepcopy(self.certs[0]);invalid['rhs']='A000217(2*n)+A000217(n)'
        with self.assertRaises(ValueError):certify_sparse_edge(invalid,self.models)
        invalid=copy.deepcopy(self.certs[0]);invalid['index_maps']['A000217']=[[2,1],[1,0]]
        with self.assertRaises(ValueError):certify_sparse_edge(invalid,self.models)
        invalid=copy.deepcopy(self.certs[0]);invalid['bindings']['A000217']['source_sha256']='wrong'
        with self.assertRaises(ValueError):certify_sparse_edge(invalid,self.models)
        invalid=copy.deepcopy(self.certs[0]);invalid['rhs']='__import__("os").system("x")'
        with self.assertRaises(ValueError):certify_sparse_edge(invalid,self.models)

    def test_modified_source_rejected_before_execution(self):
        g=prepare_sparse_tasks(self.models,self.certs,[('A016789',3)])
        p=shortest_sparse_plan(g)
        changed=copy.deepcopy(self.models);changed['A000217']['source_sha256']='changed'
        with self.assertRaises(ValueError):execute_sparse_plan(g,p,changed)

    def test_cache_authenticated_and_value_checked(self):
        task=('A000217',4)
        legit=cache_record(task,10,self.models['A000217'])
        g=prepare_sparse_tasks(self.models,self.certs,[task])
        p=shortest_sparse_plan(g,cache={task:legit})
        self.assertEqual(p['cost'],0)
        self.assertEqual(execute_sparse_plan(g,p,self.models,cache={task:legit})[0][task],10)
        forged=dict(legit,value=11)
        with self.assertRaises(ValueError):execute_sparse_plan(g,p,self.models,cache={task:forged})

    def test_all_indices_packet_equality(self):
        for sid,model in self.models.items():
            packet=packet_from_ep(model)
            self.assertIsNotNone(packet)
            for n in [0,1,2,3,11,100,1000,10001]:
                self.assertEqual(packet_nth(packet,n),direct_value(model,n))

    def test_demand_caps_fail_closed(self):
        with self.assertRaises(ValueError):
            prepare_sparse_tasks(self.models,self.certs,[('A016789',-1)])
        with self.assertRaises(PlanningBudgetExceeded):
            prepare_sparse_tasks(self.models,self.certs,[('A016789',5)],max_tasks=2)
        g=prepare_sparse_tasks(self.models,self.certs,[('A016789',5)])
        with self.assertRaises(PlanningBudgetExceeded):shortest_sparse_plan(g,max_states=0)


class ArchiveBridgeTests(unittest.TestCase):
    def test_quad_binomial_identity_and_norm(self):
        for c,q in [(-2,0),(0,2),(1,2),(2,3),(3,5),(-1,7)]:
            for n in range(32):
                b,d=quadratic_pair(c,q,n)
                self.assertEqual(b,quadratic_binomial_even(c,q,n))
                self.assertEqual(d,quadratic_binomial_odd(c,q,n))
                self.assertEqual(b*b-q*d*d,(c*c-q)**n)
        self.assertEqual(quadratic_pair(1,2,0),(1,0))

    def test_quad_sparse_reuse(self):
        vals,receipt=quadratic_sparse(1,2,[0,1,7,20,7,300,5000])
        self.assertEqual(len(vals),6)
        self.assertEqual(vals[5000],quadratic_pair(1,2,5000))
        self.assertEqual(receipt['queries'],6)
        self.assertLess(receipt['ring_multiplications'],100)
        self.assertTrue(quadratic_certificate(2,3,90)['norm_verified'])

    def test_riordan_quadratic_from_power_source(self):
        for q,c in [(2,1),(3,2),(0,-3),(5,0)]:
            for n in range(30):
                src=lambda k:q**k
                b=riordan_nth(src,n,c=c,s=1,r=2,t=2)
                d=riordan_nth(src,n-1,c=c,s=2,r=2,t=2) if n else 0
                self.assertEqual((b,d),quadratic_pair(c,q,n))

    def test_riordan_inverse_unramified(self):
        rng=random.Random(230)
        for _ in range(22):
            length=18;c=rng.randint(-3,3);s=rng.randint(0,3)
            a=[rng.randint(-5,5) for _ in range(length)]
            b=[riordan_nth(a.__getitem__,n,c=c,s=s,r=1,t=1) for n in range(length)]
            recovered=[riordan_nth(b.__getitem__,n,c=-c,s=s,r=1,t=1) for n in range(length)]
            self.assertEqual(recovered,a)

    def test_riordan_sparse_and_support_pruning(self):
        called=[]
        def source(k):called.append(k);return 7*k+1
        result=riordan_sparse(source,[0,2,8,13,2],c=0,s=1,r=2,t=1)
        self.assertEqual(result,{0:1,2:8,8:29,13:0})
        self.assertEqual(called,[0,1,4])
        self.assertEqual(riordan_requirements(13,c=0,s=1,r=2,t=1),())
        self.assertEqual(riordan_requirements(0,c=0,s=0,r=2,t=2),(0,))

    def test_archive_input_guards(self):
        for f in [lambda:quadratic_pair(True,2,3),
                  lambda:quadratic_pair(1,-2,3),
                  lambda:quadratic_sparse(1,2,[3,-1]),
                  lambda:riordan_nth(lambda k:1,3,c=1,s=0,r=0,t=1),
                  lambda:riordan_requirements(4,c=1,s=0,r=2,t=0)]:
            with self.assertRaises(ValueError):f()

if __name__=='__main__':unittest.main()
