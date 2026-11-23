"""Exact affine-lane and singular-domain regression controls.
Author: Komorebi P.
"""
import json
import unittest
from fractions import Fraction as Q
from pathlib import Path
from oeis_identification_proofs import parse_record
from oeis_hypergeometric_gate import parse_first_order
from oeis_precursive_gate import parse_operator, decode_rat
from oeis_shift_operator_gate import (audit, definitions, equation, integer_guard,
    certificate, verify_certificate, discover, inverse_operator, ratio_evaluate, terms_at, plan_from_queue, local_precision)

ROOT=Path(__file__).resolve().parents[1]
SYN=ROOT/'fixtures/oeis_shift_operator'
OFF=ROOT/'fixtures/oeis_shift_official_excerpts'

def run(root):return audit(root,json.loads((root/'plan.json').read_text()))

class ShiftOperatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.syn=run(SYN);cls.off=run(OFF)
        cls.edges={(e['source'],e['target'],e['stride'],e['residue_or_offset']):e for e in cls.syn['edges']+cls.off['edges']}
    def test_counts(self):
        self.assertEqual(self.syn['summary']['conditional_certificates'],10)
        self.assertEqual(self.off['summary']['conditional_certificates'],24)
        self.assertEqual(self.off['summary']['polyphase_certificates'],18)
        self.assertEqual(self.off['summary']['records'],7)
    def test_polynomial_shift_not_scalar(self):
        e=self.edges['A987300','A987302',1,0]
        self.assertEqual(e['coefficients'],[{'num':['1','1'],'den':['1']},{'num':['1'],'den':['1']}])
        self.assertEqual(e['discovery']['degree'],1)
    def test_inverse_outside_polynomial_search(self):
        e=self.edges['A987302','A987300',1,0]
        self.assertEqual(e['discovery']['basis'],'exact_state_matrix_inverse')
        for n in (0,1,8):
            self.assertEqual(ratio_evaluate(decode_rat(e['coefficients'][0]),n),Q(2*(n+2),2*n*n+6*n+3))
            self.assertEqual(ratio_evaluate(decode_rat(e['coefficients'][1]),n),Q(-1,2*n*n+6*n+3))
    def test_guard_uncancelled_pole(self):
        for key in ('A987303','A987304'):
            d=self.syn['profiles'][key]['definitions'][0]
            self.assertEqual(d['base'],2)
            self.assertTrue(any(g['excluded_integer_roots']==[1] for g in d['guards']))
            self.assertEqual(self.edges[key,'A987305',1,0]['valid_from'],2)
    def test_backward_index_normalization(self):
        d=equation('a(n)=a(n-1)+a(n-2), n>=5.',1)
        self.assertEqual(d['natural_from'],3)
        self.assertEqual(d['original_min_shift'],-2)
    def test_integer_guard_not_just_real_sign(self):
        self.assertEqual(integer_guard((Q(-1),Q(2)),0)['safe_from'],0)
        self.assertEqual(integer_guard((Q(-1),Q(1)),0)['safe_from'],2)
        with self.assertRaises(ValueError):integer_guard((Q(0),),0)
    def test_legacy_cancelled_pole_rejection(self):
        self.assertIsNone(parse_first_order('a(n+1)=(n-1)/(n-1)*a(n).',offset=0))
        self.assertIsNone(parse_operator('a(n+2)=(n-1)/(n-1)*a(n+1)+a(n).',offset=0))
        self.assertIsNotNone(parse_first_order('a(n+1)=(n-1)/(n-1)*a(n), n>=2.',offset=0))
    def test_different_order(self):
        e=self.edges['A987306','A987307',1,0]
        self.assertEqual((e['source_order'],e['target_order']),(2,3))
        self.assertIsNone(e['rational_state_recovery'])
    def test_loss_of_state(self):
        e=self.edges['A987308','A987309',1,0]
        self.assertIsNone(e['rational_state_recovery'])
        self.assertNotIn(('A987309','A987308',1,0),self.edges)
    def test_quarantine_and_unsafe_formula(self):
        self.assertEqual(self.syn['profiles']['A987310']['status'],'quarantined_contradiction')
        self.assertEqual(self.syn['profiles']['A987311']['status'],'unsupported')
        for expr in ('a(n+2)=a(n)*a(n+1).','a(n+2)=__import__("os").system("echo bad")*a(n).','a(n+2)=a(n+1)/a(n).','a(n+2)=a(n+1)+a(n), n>=0 if n odd.'):
            self.assertIsNone(equation(expr,0))
    def test_fibonacci_lane_and_inverse_state(self):
        e=self.edges['A000045','A001906',2,0]
        self.assertEqual(e['coefficients'],[{'num':['1'],'den':['1']},{'num':['0'],'den':['1']}])
        self.assertEqual(e['rational_state_recovery']['inverse_matrix'],[[{'num':['1'],'den':['1']},{'num':['0'],'den':['1']}],[{'num':['-1'],'den':['1']},{'num':['1'],'den':['1']}]])
        odd=self.edges['A000045','A001519',2,0]
        self.assertEqual(odd['coefficients'],[{'num':['-1'],'den':['1']},{'num':['1'],'den':['1']}])
    def test_tampering(self):
        e=self.edges['A987300','A987302',1,0];p=self.syn['profiles'];a,b=p[e['source']],p[e['target']]
        self.assertTrue(verify_certificate(e,a,b))
        self.assertFalse(verify_certificate({**e,'valid_from':1},a,b))
        self.assertFalse(verify_certificate({**e,'source_sha256':'fake'},a,b))
        self.assertFalse(verify_certificate({**e,'coefficients':[{'num':['99'],'den':['1']},e['coefficients'][1]]},a,b))
    def test_full_source_pin_rejects_excerpt(self):
        with self.assertRaisesRegex(ValueError,'blob mismatch'):
            audit(OFF,json.loads((OFF/'full_source_plan.json').read_text()))
    def test_precision_state_fibers(self):
        e=self.edges['A000045','A001906',2,0];p=self.off['profiles']
        receipt=local_precision(p[e['source']],p[e['target']],e,0,2,6)
        self.assertEqual(receipt['smith_exponents'],[0,0]);self.assertEqual(receipt['kernel_fiber_log_p'],0)
        e=self.edges['A987300','A987302',1,0];p=self.syn['profiles']
        receipt=local_precision(p[e['source']],p[e['target']],e,0,3,4)
        self.assertEqual(receipt['smith_exponents'],[0,1]);self.assertEqual(receipt['kernel_fiber_log_p'],1)
        self.assertEqual(receipt['minimum_output_precision_for_input_mod_p_to_k'],5)
        e=self.edges['A987308','A987309',1,0]
        receipt=local_precision(p[e['source']],p[e['target']],e,0,2,4)
        self.assertEqual(receipt['rank'],1);self.assertEqual(receipt['kernel_fiber_log_p'],4)
        self.assertFalse(receipt['full_input_recovery_possible'])
        with self.assertRaises(ValueError):local_precision(p[e['source']],p[e['target']],e,0,4,4)
    def test_queue_automation(self):
        def lead(a,b,priority):return {'from':a,'to':b,'priority_score':priority,'mentions':1}
        q={'queues':{'cross_component':[lead('A000045','A000032',10),lead('A000032','A000045',8),lead('A000045','A999999',12)]}}
        plan=plan_from_queue(OFF,q,1)
        self.assertEqual(plan['pairs'],[['A000045','A000032'],['A000032','A000045']])
        self.assertEqual(plan['queue_metadata']['missing_source_leads'][0]['missing_ids'],['A999999'])
        self.assertEqual(audit(OFF,plan)['summary']['conditional_certificates'],2)
    def test_budget(self):
        plan=json.loads((OFF/'plan.json').read_text());plan['lanes']=[[1,0]]*13
        with self.assertRaisesRegex(ValueError,'budget'):audit(OFF,plan)

if __name__=='__main__':unittest.main()
