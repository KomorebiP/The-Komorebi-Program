"""Adversarial replay tests for proof-carrying transfer path composition.

Author: Komorebi P.
No real OEIS DB is needed; synthetic formulas are exact symbolic controls.
"""
import copy
import json
import unittest
from fractions import Fraction as F
from sequence_hypergeometric_gauges import certify_pair, source_model
from sequence_holonomic_compiler import fraction_eval
from sequence_v10_path_compiler import compose, oriented_edge, gauge_rat, composite_factors

N={'op':'n'}
def linear(a,b):
    return {'op':'add','args':[{'op':'mul','args':[a,N]},b]}

def model(sid,spec,offset=0):
    raw=json.dumps([str(fraction_eval(spec,j+offset)) for j in range(30)])
    return source_model('formula_'+sid,sid,spec,offset,raw,'sha_'+sid)


class TestGaugePath(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.models={}
        specs={'X':1,'Y':linear(1,1),'Z':{'op':'mul','args':[linear(1,1),linear(2,1)]}}
        for k,s in specs.items():
            cls.models[k]=model(k,s)
        cls.first=certify_pair(cls.models['X'],cls.models['Y'])
        cls.second=certify_pair(cls.models['Y'],cls.models['Z'])

    def test_exact_composition(self):
        cert=compose(self.models,self.first,self.second)
        self.assertEqual([cert[k] for k in ('source','via','target')],['X','Y','Z'])
        self.assertEqual(cert['gauge_linear_factors'],[{'a':1,'b':1,'power':1},{'a':2,'b':1,'power':1}])
        self.assertEqual(cert['exponential_factor'],'1')
        self.assertEqual(cert['base_ratio'],'1')
        for n in range(50):
            self.assertEqual(fraction_eval(self.models['Z']['ast'],n),
                fraction_eval(self.models['X']['ast'],n)*gauge_rat(cert['gauge_linear_factors']).at(n))

    def test_inverse_edges(self):
        e1=oriented_edge(self.second,True)
        e2=oriented_edge(self.first,True)
        cert=compose(self.models,e1,e2)
        self.assertEqual((cert['source'],cert['via'],cert['target']),('Z','Y','X'))
        self.assertEqual(sum(f['power'] for f in cert['gauge_linear_factors']),-2)

    def test_no_join_without_matching_middle(self):
        with self.assertRaises(ValueError):compose(self.models,self.first,self.first)

    def test_fake_intermediate_formula_sha_rejected(self):
        e=copy.deepcopy(self.first);e['target_evaluator_sha256']='0'*64
        with self.assertRaises(ValueError):compose(self.models,e,self.second)

    def test_tampered_initial_constant_rejected(self):
        e=copy.deepcopy(self.first);e['base_ratio']='100'
        with self.assertRaisesRegex(ValueError,'tampered'):
            compose(self.models,e,self.second)

    def test_tampered_shift_factors_rejected(self):
        e=copy.deepcopy(self.first);e['gauge_linear_factors'][0]['b']+=2
        with self.assertRaisesRegex(ValueError,'tampered'):
            compose(self.models,e,self.second)

    def test_changed_source_sha_rejected(self):
        e=copy.deepcopy(self.second);e['source_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'stale'):
            compose(self.models,self.first,e)

    def test_forged_ends_rejected(self):
        e=copy.deepcopy(self.second);e['target']='X'
        with self.assertRaises(ValueError):compose(self.models,self.first,e)

    def test_composite_factor_cancellation(self):
        e=oriented_edge(self.first,True)
        self.assertEqual(composite_factors([self.first,e]),[])

    def test_fraction_exponential(self):
        specs={'A':{'op':'pow','base':2,'exp':N},
               'B':{'op':'mul','args':[{'op':'pow','base':3,'exp':N},linear(1,1)]},
               'C':{'op':'mul','args':[{'op':'pow','base':6,'exp':N},linear(1,1)]}}
        models={k:model(k,v) for k,v in specs.items()}
        xy=certify_pair(models['A'],models['B'])
        yz=certify_pair(models['B'],models['C'])
        cert=compose(models,xy,yz)
        self.assertEqual(cert['exponential_factor'],'3')
        for n in range(10):
            self.assertEqual(fraction_eval(models['C']['ast'],n),F(3)**n*(n+1)*fraction_eval(models['A']['ast'],n))

if __name__=='__main__':unittest.main()
