"""Regression tests for the OEIS formula database. Run from any directory."""
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from oeis_formula_database import (
    canonical, classify_formula, connect, evaluate, ingest_curated,
    ingest_komorebi, ingest_oeis, inspect, parse_seq, statistics,
    verify_formula,
)

ROOT = Path(__file__).resolve().parents[1]
SEEDS = ROOT / 'research/oeis-formulas/seeds.json'


class FormulaDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.db = connect(Path(self.temp.name) / 'test.sqlite3')
        self.addCleanup(self.db.close)

    def test_curated_seed_all_exact(self):
        outcomes = ingest_curated(self.db, SEEDS)
        self.assertEqual(len(outcomes), 32)
        self.assertTrue(all(x['verification']=='finite_checked' and x['checked_terms']>=8 for x in outcomes))
        self.assertEqual(statistics(self.db)['curated_finite_checked'], 32)
        ingest_curated(self.db, SEEDS)
        self.assertEqual(statistics(self.db)['curated_evaluator_formulas'], 32)
        self.assertEqual(inspect(self.db,'A000108')['formulas'][0]['verification'],'finite_checked')

    def test_parser_offsets_and_source_fields(self):
        raw = '''%I A999999 #4
%S A999999 1,2,
%T A999999 3,5,
%U A999999 8,13
%N A999999 Test Fibonacci analogue
%O A999999 1,2
%F A999999 a(n) = a(n-1)+a(n-2).
%F A999999 G.f.: 1/(1-x-x^2).
%o A999999 (PARI) a(n)=fibonacci(n)
%K A999999 nonn
'''
        r = parse_seq(raw)
        self.assertEqual(r['offset'], 1)
        self.assertEqual(r['offset_second'], 2)
        self.assertEqual(r['terms'], ['1','2','3','5','8','13'])
        self.assertEqual(classify_formula(r['formulas'][0]), 'recurrence')
        self.assertEqual(classify_formula(r['formulas'][1]), 'generating_function')
        file = Path(self.temp.name) / 'A999999.seq'
        file.write_text(raw, encoding='utf-8')
        status = ingest_oeis(self.db, file)
        self.assertEqual(status['inserted'], 1)
        self.assertEqual(statistics(self.db)['raw_oeis_formula_lines'], 2)
        self.assertEqual(statistics(self.db)['raw_oeis_program_blocks'], 1)
        self.assertEqual(ingest_oeis(self.db,file)['unchanged'], 1)
        self.assertEqual(statistics(self.db)['raw_oeis_formula_lines'], 2)
        self.assertEqual({x['verification'] for x in inspect(self.db,'A999999')['formulas']}, {'unreviewed','not_executed'})

    def test_update_retains_curated_formula(self):
        ingest_curated(self.db, SEEDS)
        first=statistics(self.db)['curated_finite_checked']
        raw = '''%I A000045 #5
%S A000045 0,1,1,2,3,5,8,13,21,
%U A000045 34,55,89,144,233,377,610,987,1597
%N A000045 Fibonacci numbers
%O A000045 0,4
%F A000045 a(n)=a(n-1)+a(n-2)
'''
        f=Path(self.temp.name)/'A000045.seq'
        f.write_text(raw,encoding='utf-8')
        out=ingest_oeis(self.db,f)
        self.assertEqual(out['updated'],1)
        self.assertEqual(statistics(self.db)['curated_finite_checked'],first)
        self.assertEqual(statistics(self.db)['raw_oeis_formula_lines'],1)
        self.assertEqual(len(inspect(self.db,'A000045')['terms']),18)

    def test_failed_curated_formula_rejected_not_promoted(self):
        ingest_curated(self.db, SEEDS)
        with self.db:
            row = self.db.execute("SELECT formula_id FROM formulas WHERE oeis_id='A000108' AND origin='komorebi_curated'").fetchone()
            self.db.execute("UPDATE formulas SET evaluator_json=? WHERE formula_id=?", (json.dumps({'op':'n'}),row[0]))
            r=verify_formula(self.db,row[0])
        self.assertEqual(r['verification'],'rejected')
        self.assertIn('expected',r['failure'])
        self.assertEqual(statistics(self.db)['curated_rejected'],1)

    def test_dangerous_text_never_executed(self):
        with self.assertRaises(ValueError):
            evaluate({'op':'__import__','args':['os']},3)
        with self.assertRaises(ValueError):
            evaluate({'op':'pow','base':2,'exp':100001},1)
        with self.assertRaises(ValueError):
            evaluate({'op':'exact_div','num':5,'den':2},1)
        self.assertEqual(evaluate({'op':'linear_recurrence','coefficients':[2,1],'initial':[0,1]},6),70)

    def test_local_import_distinguishes_matches_from_identity(self):
        sample={'entries':[{'id':'KSEQ-001','title':'Sample source','terms':['1','1','2','3','5','8','13','21'],
                  'offset':0,'source':'https://example.org/source','oeis':'A000045',
                  'matches':[{'id':'A000045','position':3,'matched_terms':8}],
                  'formulas':[{'kind':'term formula','expression':'hypothetical formula',
                               'source':'https://example.org/source'}]}]}
        f=Path(self.temp.name)/'komorebi.json'
        f.write_text(json.dumps(sample),encoding='utf-8')
        stats=ingest_komorebi(self.db,f)
        self.assertEqual(stats['records'],1)
        self.assertEqual(stats['representations'],1)
        self.assertEqual(stats['finite_crosswalks'],1)
        self.assertEqual(stats['claimed_crosswalks'],1)
        self.assertEqual(statistics(self.db)['curated_finite_checked'],0)
        ingest_komorebi(self.db,f)
        self.assertEqual(statistics(self.db)['local_formula_representations'],1)

    def test_invalid_files_do_not_create_fake_records(self):
        f=Path(self.temp.name)/'A123456.seq'
        f.write_text('%I A123456\n%S A123456 1,2,3\n',encoding='utf-8')
        result=ingest_oeis(self.db,f)
        self.assertEqual(result['errors'],1)
        self.assertEqual(statistics(self.db)['oeis_sequences_stored'],0)
        with self.assertRaises(ValueError):
            canonical('not a number')

if __name__=='__main__':
    unittest.main()
