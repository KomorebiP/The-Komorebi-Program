"""Deterministic negative and positive controls for OEIS source-bound automation."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from fractions import Fraction as Q

from oeis_gap_automation import (Rational, affine_certificate, audit, safe_csv_cell,
    components, formula_rows, ingest, load_network, parse_safe_rhs,
    parse_seq_file, parse_term_formula, scanner)


def tiny_network():
    return {"schema":1, "oeis":{"license":"CC-BY-SA-4.0","snapshot_sha256":"fixture-sha"},
            "counts":{"hyperedge":1},
            "records":[{"id":s} for s in ("A000001","A000002","A000003","A000004")],
            "edges":[{"key":"one","kind":"hyperedge","target":"A000001",
                      "inputs":["A000002"],"evidence":"all_index_formula_identity"}]}


class TestExactFormulaAlgebra(unittest.TestCase):
    def test_rational_identity(self):
        self.assertTrue(parse_safe_rhs('n*(n+1)/2').minus(parse_safe_rhs('binomial(n+1, 2)')).is_zero())
        self.assertTrue(parse_safe_rhs('((n+1)**2-1)/n').minus(parse_safe_rhs('n+2')).is_zero())
        self.assertEqual(parse_safe_rhs('(2*n+2)/(n+1)').expr_data(),Rational.constant(Q(2)).expr_data())
        self.assertTrue(parse_safe_rhs('n^2+2*n+1').minus(parse_safe_rhs('(n+1)**2')).is_zero())

    def test_affine_exact(self):
        c=affine_certificate(parse_safe_rhs('3*n*(n+1)/2-2*n'), parse_safe_rhs('n*(n+1)/2'))
        self.assertEqual(c['c'],'3')
        self.assertEqual(c['b'],'-2')
        self.assertEqual(c['a'],'0')
        self.assertIsNone(affine_certificate(parse_safe_rhs('n'),parse_safe_rhs('n')))

    def test_parser_rejects_execution_and_unsupported(self):
        bad=['__import__("os").system("ls")','open("/etc/passwd").read()',
             'n.__class__','lambda n: n','sum(range(n))','2**n','n//2','n%2',
             'binomial(n,n)','(0/0)','10**100','n**99','n < 5']
        for code in bad:
            with self.subTest(code=code), self.assertRaises((ValueError,SyntaxError,ZeroDivisionError,TypeError)):
                parse_safe_rhs(code)

    def test_csv_source_text_is_not_spreadsheet_code(self):
        self.assertTrue(safe_csv_cell('=HYPERLINK(\"x\")').startswith("'="))
        self.assertTrue(safe_csv_cell(' @SUM(1)').startswith("'"))
        self.assertEqual(safe_csv_cell('a(n)=n**2'), 'a(n)=n**2')

    def test_source_only_grammar(self):
        poly, rhs=parse_term_formula('a(n) = n*(n+1)/2. - _A Contributor_')
        self.assertTrue(poly.minus(parse_safe_rhs('binomial(n+1,2)')).is_zero())
        self.assertEqual(rhs,'n*(n+1)/2')
        with self.assertRaises(ValueError):
            parse_term_formula('a(n)=A000045(n)')


class TestGraphAndScanner(unittest.TestCase):
    def test_components(self):
        cid, groups=components(tiny_network())
        self.assertEqual(len(groups),3)
        self.assertEqual(cid['A000001'],cid['A000002'])
        self.assertNotEqual(cid['A000001'],cid['A000003'])

    def test_bridge_and_frontier_are_unproved(self):
        rows=[
          {'source':'A000001','field':'F','kind':'term_candidate','text':'a(n) = n*(n+1)/2','source_line':1},
          {'source':'A000003','field':'F','kind':'term_candidate','text':'a(n) = binomial(n+1,2)','source_line':2},
          {'source':'A000001','field':'F','kind':'unclassified','text':'Also A000003, A999999','source_line':3},
          {'source':'A000001','field':'F','kind':'unclassified','text':'Cf. A000002','source_line':4},
          {'source':'A000003','field':'Y','kind':'unclassified','text':'See A000001','source_line':5},
        ]
        report=scanner(tiny_network(),rows)
        self.assertEqual(report['network']['components'],3)
        self.assertEqual(report['queue_counts']['cross_component'],2)
        self.assertEqual(report['queue_counts']['new_id_frontier'],1)
        bridge=report['queues']['cross_component'][0]
        self.assertEqual(bridge['triage_status'],'lexical_lead_not_a_transfer')
        self.assertEqual(report['scan']['rational_formulas_parsed'],2)
        self.assertTrue(any(x.get('formal_expression_certificates') for x in report['queues']['cross_component']))

    def test_rejects_tampered_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'manifest.json'
            data=tiny_network()
            data['edges'][0]['evidence']='finite_match_falsely_promoted'
            p.write_text(json.dumps(data))
            with self.assertRaises(ValueError):load_network(p)

    def test_snapshot_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            d=Path(d)
            (d/'network.json').write_text(json.dumps(tiny_network()))
            (d/'formulas.json').write_text(json.dumps({"schema":1,"evidence":"unreviewed_source_text",
                       "license":"CC-BY-SA-4.0","snapshot_sha256":"tampered","entries":{}}))
            with self.assertRaises(ValueError):audit(d/'network.json',d/'formulas.json',None,d/'out')


class TestOEISIngest(unittest.TestCase):
    def test_seq_parser_revision_and_incremental(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); f=root/'seq/A000/A000001.seq';f.parent.mkdir(parents=True)
            f.write_text('%I A000001 M0000\n%N A000001 A test sequence\n'
                         '%O A000001 1,3\n%F A000001 a(n)=n*(n+1)/2.\n'
                         '%F A000001 Cf. A000002\n%Y A000001 A000003\n')
            parsed=parse_seq_file(f)
            self.assertEqual(parsed['offset_raw'],'1,3')
            self.assertEqual(len(parsed['formulas']),2)
            db=root/'snap.sqlite'
            first=ingest(root,db,'0123456789abcdef')
            self.assertEqual(first['entries_changed'],1)
            self.assertEqual(ingest(root,db,'0123456789abcdef')['entries_changed'],0)
            rows=list(formula_rows(None,db))
            self.assertEqual(len(rows),3)
            self.assertEqual(rows[0]['field'],'F')
            self.assertEqual(rows[-1]['field'],'Y')
            f.write_text(f.read_text().replace('Cf. A000002','Cf. A000004'))
            self.assertEqual(ingest(root,db,'0123456789abcdef')['entries_changed'],1)
            self.assertEqual(len(list(formula_rows(None,db))),3)


if __name__=='__main__':unittest.main()
