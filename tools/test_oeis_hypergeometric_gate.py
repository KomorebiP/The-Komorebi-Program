"""Independent and adversarial tests for conditional P-recursive/Pochhammer gate.

Author: Komorebi P.
"""
from __future__ import annotations

import json
from fractions import Fraction as Q
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from oeis_gap_automation import Rational
from oeis_identification_proofs import parse_record, profile_record
from oeis_hypergeometric_gate import (
    parse_first_order, profile, audit, sign_certificate, ratio_evaluate,
    terms_from_ratio, shift, root_decomposition, pochhammer_certificate,
    discover_gauge, verify_gauge_cert, report_files, verify_report,
    _ratio_ast_safe, _rref_nullspace)

ROOT=Path(__file__).resolve().parents[1]
FIX=ROOT/'fixtures/oeis_hypergeom'


class HypergeometricGateTests(unittest.TestCase):
    def rec(self,id):return parse_record(FIX/'seq'/id[:4]/(id+'.seq'),FIX)
    def proof(self,id):return profile(self.rec(id))

    def test_three_real_oeis_excerpt_recurrences(self):
        for seq in ('A000108','A000142','A000984'):
            p=self.proof(seq)
            self.assertEqual(p['status'],'conditional_first_order_definition',seq)
            self.assertEqual(p['definition']['matched_source_terms'],15)
            self.assertEqual(p['definition']['base_index'],0)
            self.assertIsNotNone(p['definition']['pochhammer'])

    def test_catalan_and_central_binomial_gauges(self):
        central=self.proof('A000984');catalan=self.proof('A000108')
        e=discover_gauge(central,catalan)
        self.assertIsNotNone(e)
        self.assertEqual(e['gauge'],{'num':['1'],'den':['1','1']})
        self.assertEqual(e['evidence'],'conditional_exact_hypergeometric_gauge')
        self.assertTrue(verify_gauge_cert(e,{central['oeis_id']:central,catalan['oeis_id']:catalan}))
        self.assertFalse(verify_gauge_cert({**e,'base_index':1},{central['oeis_id']:central,catalan['oeis_id']:catalan}))
        e2=discover_gauge(catalan,central)
        self.assertEqual(e2['gauge'],{'num':['1','1'],'den':['1']})

    def test_factorial_and_shifted_factorial(self):
        source=self.proof('A000142');target=self.proof('A987110')
        e=discover_gauge(source,target)
        self.assertEqual(e['gauge'],{'num':['1','1'],'den':['1']})
        self.assertEqual(discover_gauge(target,source)['gauge'],{'num':['1'],'den':['1','1']})

    def test_pochhammer_certificates(self):
        def p(id):return self.proof(id)['definition']['pochhammer']
        self.assertEqual((p('A000142')['geometric_factor'],p('A000142')['numerator_parameters']),('1',['1']))
        self.assertEqual((p('A000984')['geometric_factor'],p('A000984')['numerator_parameters'],p('A000984')['denominator_parameters']),('4',['1/2'],['1']))
        self.assertEqual((p('A000108')['geometric_factor'],p('A000108')['numerator_parameters'],p('A000108')['denominator_parameters']),('4',['1/2'],['2']))
        self.assertEqual(p('A987116')['numerator_parameters'],['3'])

    def test_native_nonzero_offset(self):
        p=self.proof('A987116')
        self.assertEqual(p['status'],'conditional_first_order_definition')
        self.assertEqual(p['definition']['base_index'],2)
        self.assertEqual(p['definition']['initial'],'2')
        self.assertEqual(p['definition']['matched_source_terms'],9)
        # a(n)=n! for n>=2, with anchor a(2)=2.
        poly=profile_record(parse_record(ROOT/'fixtures/oeis_identification/seq/A987/A987001.seq'))
        self.assertEqual(poly['status'],'unsupported_nonzero_or_missing_offset')

    def test_reject_bad_premises(self):
        self.assertEqual(self.proof('A987111')['status'],'quarantined_inconsistent_source_recurrence')
        for id in ('A987112','A987113','A987114','A987115'):
            self.assertEqual(self.proof(id)['status'],'no_supported_first_order_recurrence')

    def test_guard_exact_sign(self):
        self.assertIsNotNone(sign_certificate((Q(2),Q(3),Q(1)),0))
        self.assertIsNotNone(sign_certificate((Q(-1),Q(-2)),0))
        self.assertIsNone(sign_certificate((Q(-3),Q(1)),0))
        self.assertIsNotNone(sign_certificate((Q(-3),Q(1)),4))
        self.assertIsNone(sign_certificate((Q(0),Q(1)),0))
        self.assertIsNotNone(sign_certificate((Q(0),Q(1)),1))

    def test_safe_ratio_parser(self):
        self.assertIsNone(_ratio_ast_safe('a(n)*a(n)'))
        self.assertIsNone(_ratio_ast_safe('1/a(n)'))
        self.assertIsNone(_ratio_ast_safe('a(n)**2'))
        self.assertIsNone(_ratio_ast_safe('__import__("os").system("touch pwn")*a(n)'))
        self.assertIsNotNone(_ratio_ast_safe('2*(2*n-1)*a(n)/(n+1)'))
        self.assertIsNone(parse_first_order('a(n+1)= a(n)*a(n).',offset=0))
        self.assertIsNone(parse_first_order('a(n+1)= a(n)/(n-3).',offset=0))
        self.assertIsNone(parse_first_order('a(n+1)= (n+1)*a(n), n odd.',offset=0))
        self.assertIsNone(parse_first_order('a(n+2)=(n+2)*a(n+1)+a(n).',offset=0))
        self.assertIsNone(parse_first_order('a(n+1) = a(n)**2.',offset=0))

    def test_explicit_lhs_index_guard(self):
        x=parse_first_order('a(n)=n*a(n-1), n>=1.',offset=0)
        self.assertEqual(x['base_index'],0)
        self.assertEqual(ratio_evaluate(x['ratio'],2),Q(3))
        y=parse_first_order('a(n)=n*a(n-1), n>=5.',offset=0)
        self.assertEqual(y['base_index'],4)
        z=parse_first_order('a(n+1)=(n+1)*a(n), n>=5.',offset=0)
        self.assertEqual(z['base_index'],5)
        a=parse_first_order('a(n)=n*a(n-1), n>=2.',offset=2)
        self.assertEqual(a['base_index'],2)

    def test_exact_root_and_identity_controls(self):
        self.assertEqual(root_decomposition((Q(2),Q(4))),(Q(4),[Q(-1,2)]))
        self.assertIsNone(root_decomposition((Q(1),Q(0),Q(1))))
        p=Rational((Q(2),Q(4)),(Q(1),Q(1))).reduce()
        r=pochhammer_certificate(p,0)
        self.assertEqual(r['geometric_factor'],'4')
        self.assertEqual(r['numerator_parameters'],['1/2'])
        self.assertEqual(r['denominator_parameters'],['1'])
        self.assertTrue(shift(p,1).minus(Rational((Q(6),Q(4)),(Q(2),Q(1)))).is_zero())

    def test_rank_and_decoding_control(self):
        self.assertIsNone(_rref_nullspace([[Q(0),Q(0)]],2))
        self.assertEqual(_rref_nullspace([[Q(1),Q(1)]],2),[Q(-1),Q(1)])
        self.assertIsNone(_rref_nullspace([[Q(1),Q(0)],[Q(0),Q(1)]],2))

    def test_report_tamper_and_replay(self):
        r=audit(FIX)
        self.assertEqual(r['summary']['conditional_gauge_edges'],8)
        self.assertEqual(r['summary']['Pochhammer_normal_forms'],5)
        self.assertEqual(r['summary']['independently_established_OEIS_identifications'],0)
        with TemporaryDirectory() as tmp:
            d=Path(tmp)
            for name,obj in report_files(r).items():
                (d/name).write_text(json.dumps(obj,indent=2)+'\n')
            v=verify_report(FIX,d)
            self.assertEqual(v['conditional_gauges_reproved'],8)
            raw=json.loads((d/'hypergeom_profiles.json').read_text())
            raw[0]['definition']['pochhammer']['geometric_factor']='99'
            (d/'hypergeom_profiles.json').write_text(json.dumps(raw))
            with self.assertRaisesRegex(ValueError,'proof replay'):
                verify_report(FIX,d)

    def test_externally_pinned_subset_replay(self):
        ids={'A000108','A000984'} if True else {'A987200','A987201'}
        data=audit(FIX,ids=ids)
        with TemporaryDirectory() as folder:
            path=Path(folder)
            for name, obj in report_files(data).items(): (path/name).write_text(json.dumps(obj))
            self.assertEqual(verify_report(FIX,path,ids=ids)['status'],'passed')
            with self.assertRaisesRegex(ValueError,'proof replay'):
                verify_report(FIX,path)

    def test_batch_budget_fail_closed(self):
        with self.assertRaisesRegex(ValueError,'budget'):
            audit(FIX,max_pairs=1)

if __name__=='__main__':unittest.main()
