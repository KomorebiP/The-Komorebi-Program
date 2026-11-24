"""Exact higher-order polynomial-coefficient recurrence audit tests.

Author: Komorebi P.
"""
from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from fractions import Fraction as Q

from oeis_identification_proofs import parse_record
from oeis_precursive_gate import (
    parse_operator,profile,term_values,decode_rat,prove_gauge,verify_edge,audit,
    report_files,verify_report,_defs_operator)

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'fixtures/oeis_precursive'

class PRecursiveGaugeTests(unittest.TestCase):
    def rec(self,i):return parse_record(DATA/'seq'/i[:4]/(i+'.seq'),DATA)
    def prof(self,i):return profile(self.rec(i))

    def test_parse_exact_operators(self):
        x=parse_operator('a(n+2)=(n+2)*a(n+1)+a(n).',offset=0)
        self.assertEqual(x['order'],2)
        self.assertEqual(x['base_index'],0)
        self.assertEqual([decode_rat({'num':[str(y) for y in z.num],'den':[str(y) for y in z.den]}) for z in x['coefficients']],x['coefficients'])
        self.assertEqual([z.num for z in x['coefficients']],[(Q(1),),(Q(2),Q(1))])

    def test_exact_second_order_all_index_gauge(self):
        a=self.prof('A987200');b=self.prof('A987201')
        self.assertEqual(a['status'],'conditional_higher_order_definition')
        self.assertEqual(b['status'],'conditional_higher_order_definition')
        e=prove_gauge(a,b)
        self.assertIsNotNone(e)
        self.assertEqual(e['gauge'],{'num':['1','1'],'den':['1']})
        self.assertEqual(e['order'],2)
        self.assertTrue(verify_edge(e,{a['oeis_id']:a,b['oeis_id']:b}))
        self.assertFalse(verify_edge({**e,'order':3},{a['oeis_id']:a,b['oeis_id']:b}))
        reverse=prove_gauge(b,a)
        self.assertEqual(reverse['gauge'],{'num':['1'],'den':['1','1']})

    def test_recurrence_values_independent_seed(self):
        a=self.prof('A987200')['definition']
        op={'base_index':a['base_index'],'order':a['order'],
            'coefficients':[decode_rat(x) for x in a['coefficients']]}
        self.assertEqual(term_values(op,[Q(1),Q(1)],6),[Q(v) for v in [1,1,3,10,43,225]])

    def test_offset_normalization(self):
        a=self.prof('A987205')
        self.assertEqual(a['status'],'conditional_higher_order_definition')
        self.assertEqual(a['definition']['base_index'],1)
        self.assertEqual(a['definition']['initial'],['1','3'])
        self.assertEqual(a['definition']['matched_source_terms'],17)

    def test_negative_recurrence_rejections(self):
        self.assertEqual(self.prof('A987202')['status'],'quarantined_inconsistent_source_operator')
        self.assertEqual(self.prof('A987203')['status'],'no_supported_P_recurrence')
        self.assertEqual(self.prof('A987204')['status'],'no_supported_P_recurrence')
        self.assertIsNone(parse_operator('a(n+2)=a(n+1)*a(n).',offset=0))
        self.assertIsNone(parse_operator('a(n+2)=1/a(n+1)+a(n).',offset=0))
        self.assertIsNone(parse_operator('a(n+2)=a(n+1)/(n-1)+a(n).',offset=0))
        self.assertIsNone(parse_operator('a(n+2)=__import__("os").system("true")*a(n+1)+a(n).',offset=0))
        self.assertIsNone(parse_operator('a(n+6)=a(n+5)+a(n).',offset=0))

    def test_tail_guard(self):
        a=parse_operator('a(n+2)=a(n+1)+a(n), n>=7.',offset=2)
        self.assertEqual(a['base_index'],7)
        b=parse_operator('a(n+2)=a(n+1)/(n-1)+a(n), n>=2.',offset=0)
        self.assertEqual(b['base_index'],2)
        self.assertTrue(b['denominator_nonzero'][1]['sign']=='strict_positive')

    def test_certificate_replay(self):
        r=audit(DATA)
        self.assertEqual(r['summary']['conditional_higher_order_gauges'],6)
        with TemporaryDirectory() as folder:
            d=Path(folder)
            for k,v in report_files(r).items(): (d/k).write_text(json.dumps(v))
            self.assertEqual(verify_report(DATA,d)['gauges_reproved'],6)
            raw=json.loads((d/'conditional_P_recursive_gauges.json').read_text())
            raw['edges'][0]['gauge']['num']=['999']
            (d/'conditional_P_recursive_gauges.json').write_text(json.dumps(raw))
            with self.assertRaisesRegex(ValueError,'proof replay'):
                verify_report(DATA,d)

    def test_externally_pinned_subset_replay(self):
        ids={'A000108','A000984'} if False else {'A987200','A987201'}
        data=audit(DATA,ids=ids)
        with TemporaryDirectory() as folder:
            path=Path(folder)
            for name, obj in report_files(data).items(): (path/name).write_text(json.dumps(obj))
            self.assertEqual(verify_report(DATA,path,ids=ids)['status'],'passed')
            with self.assertRaisesRegex(ValueError,'proof replay'):
                verify_report(DATA,path)

    def test_budget_fail_closed(self):
        with self.assertRaisesRegex(ValueError,'budget'):audit(DATA,max_pairs=1)

if __name__=='__main__':unittest.main()
