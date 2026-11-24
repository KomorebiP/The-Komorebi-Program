"""Tests for OEIS term normalization, safeguards, and source changes."""
import json
import tempfile
import unittest
from pathlib import Path

from oeis_formula_database import connect, ingest_oeis, ingest_curated, statistics, inspect
from oeis_formula_discovery import compile_simple_term, extract_simple_terms, normalize_oeis, UnsupportedFormula

ROOT = Path(__file__).resolve().parents[1]
SEEDS = ROOT / 'research/oeis-formulas/seeds.json'


class FormulaDiscoveryTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.db = connect(self.root / 'test.sqlite3')
        self.addCleanup(self.db.close)

    def _source(self, sid, name, terms, extra=()):
        p = self.root / (sid + '.seq')
        chunks = [','.join(map(str,terms[i:i+12])) for i in range(0,len(terms),12)]
        payload = [f'%I {sid}', f'%N {sid} {name}', f'%O {sid} 0,2']
        payload.extend(f'%{f} {sid} {chunk}{"," if i < len(chunks)-1 else ""}' for i,(f,chunk) in enumerate(zip('STU',chunks)))
        payload += [f'%F {sid} {line}' for line in extra]
        p.write_text('\n'.join(payload)+'\n',encoding='utf-8')
        return p

    def test_safe_integer_expressions(self):
        spec = compile_simple_term('binomial(2*n,n)/(n+1)')
        self.assertEqual(spec['op'], 'exact_div')
        self.assertEqual(compile_simple_term('n^2')['op'],'pow')
        self.assertEqual(compile_simple_term('factorial(n)')['op'],'factorial')
        for expr in ('__import__("os").system("echo bad")', 'sqrt(n)',
                     '[n for n in range(4)]', 'a(n-1)+a(n-2)',
                     'n/2.0', 'x*n', 'n if n>1 else 0'):
            with self.subTest(expr=expr), self.assertRaises(UnsupportedFormula):
                compile_simple_term(expr)

    def test_from_names_and_formula_fields(self):
        self._source('A999990', 'The squares: a(n)=n^2.', [n*n for n in range(20)],
                    extra=['a(n)=n^2. - _Author_, Nov 22 2026',
                           'a(n)=binomial(n,2).', 'a(n) = n^2 + 1 for n > 5.'])
        result = ingest_oeis(self.db,self.root)
        self.assertEqual(result['inserted'],1)
        report = normalize_oeis(self.db)
        self.assertEqual(report['finite_checked'],1)
        self.assertEqual(report['rejected'],1)
        self.assertEqual(report['parsed_candidates'],2)
        self.assertEqual(len([x for x in inspect(self.db,'A999990')['formulas'] if x['origin']=='oeis_normalized']),2)
        self.assertEqual(normalize_oeis(self.db)['parsed_candidates'],2)
        self.assertEqual(statistics(self.db)['raw_oeis_formula_lines'],3)

    def test_insufficient_reference_terms(self):
        self._source('A999991','a(n) = n^3.', [n**3 for n in range(7)])
        ingest_oeis(self.db,self.root)
        report=normalize_oeis(self.db)
        self.assertEqual(report['insufficient_terms'],1)
        self.assertEqual(report['finite_checked'],0)

    def test_failed_source_reevaluation(self):
        ingest_curated(self.db,SEEDS)
        self._source('A000290','Squares a(n)=n^2.', [n*n for n in range(20)])
        ingest_oeis(self.db,self.root)
        normalize_oeis(self.db)
        self.assertGreaterEqual(statistics(self.db)['curated_finite_checked'],1)

    def test_negative_offset_is_preserved_without_false_normalization(self):
        p = self.root / 'A999993.seq'
        p.write_text('%I A999993\n%N A999993 a(n)=n^2.\n%O A999993 -3,2\n%S A999993 9,4,1,0,1,4,9,16,25,36,49,64\n', encoding='utf-8')
        self.assertEqual(ingest_oeis(self.db,p)['inserted'], 1)
        info = inspect(self.db,'A999993')
        self.assertEqual(info['offset'], -3)
        r=normalize_oeis(self.db)
        self.assertEqual(r['negative_offset_skipped'], 1)
        self.assertEqual(r['parsed_candidates'], 0)

    def test_restricts_prose_and_code(self):
        cases = ('a(n) = n^2 if n>0', 'a(n)=n^2; for n>7',
                 'a(n) = sum(k=0..n,k^2)', 'a(n) = 2**n + unknown(n)',
                 'a(n) = eval(n)', 'a(n)=__import__(os)',
                 'a(n)=n^2. See related terms.')
        for text in cases[:-1]:
            with self.subTest(text=text):
                self.assertFalse(extract_simple_terms(text))
        self.assertEqual(len(extract_simple_terms(cases[-1])),1)

if __name__ == '__main__':
    unittest.main()
