"""Independent reference-prefix controls for the expanded OEIS set and lifts."""
import json
import tempfile
import unittest
from pathlib import Path
from oeis_formula_database import connect, ingest_curated, statistics, evaluate, ingest_oeis, inspect
from oeis_formula_polyphase import compute, build_catalogue, lift

ROOT = Path(__file__).resolve().parents[1]
SEEDS = ROOT / 'research/oeis-formulas/seeds.json'
MORE = ROOT / 'research/oeis-formulas/seeds-extended.json'


class ExpandedFormulaTests(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root = Path(t.name)
        self.db = connect(self.root / 'test.sqlite3')
        self.addCleanup(self.db.close)
        ingest_curated(self.db,SEEDS)
        ingest_curated(self.db,MORE)

    def test_all_expanded_reference_terms(self):
        report = statistics(self.db)
        self.assertEqual(report['oeis_sequences_stored'],56)
        self.assertEqual(report['curated_finite_checked'],61)
        self.assertEqual(report['curated_rejected'],0)
        self.assertEqual(self.db.execute('SELECT SUM(checked_terms) FROM formulas WHERE verification="finite_checked"').fetchone()[0],61*18)

    def test_prime_and_combinatorial_oracles(self):
        for sid,n,expected in [('A000040',19,67),('A000720',30,10),('A001223',20,2),
                               ('A000172',8,739162),('A000111',8,1385),
                               ('A000364',8,19391512145),('A000009',30,296),
                               ('A000120',255,8),('A000073',10,81),('A000931',20,49)]:
            row=self.db.execute('SELECT evaluator_json FROM formulas WHERE oeis_id=? AND verification="finite_checked" ORDER BY ordinal LIMIT 1',(sid,)).fetchone()
            self.assertEqual(evaluate(json.loads(row[0]),n),expected,sid)

    def test_polyphase_lifts_all_entries(self):
        report=build_catalogue(self.db,self.root/'polyphase.jsonl')
        self.assertEqual(report['source_sequences'],56)
        self.assertEqual(report['parameterized_families'],56)
        self.assertEqual(report['source_value_mismatches'],0)
        self.assertGreater(report['preview_cases_checked'],1500)
        lines=(self.root/'polyphase.jsonl').read_text().splitlines()
        self.assertEqual(len(lines),56)
        self.assertEqual(len(json.loads(lines[0])['examples']),9)

    def test_polyphase_exact_prime_subsequence(self):
        out=compute(self.db,'A000040',2,0,3)
        self.assertEqual(out['source_index'],7)
        self.assertEqual(out['exact_value'],'17')
        self.assertTrue(out['reference_checked'])
        with self.assertRaises(ValueError):
            compute(self.db,'A000040',2,2,3)

    def test_changed_reference_invalidates_old_verified_state(self):
        path=self.root/'A000583.seq'
        path.write_text('%I A000583\n%N A000583 Wrong fourth powers\n%O A000583 0,3\n%S A000583 0,1,16,81,256,625,1296,2401,4096,6561,10000,14642,20736,28561,38416,50625,65536,83521\n',encoding='utf-8')
        report=ingest_oeis(self.db,path)
        self.assertEqual(report['updated'],1)
        state=self.db.execute("SELECT verification,checked_terms FROM formulas WHERE oeis_id='A000583' AND origin='komorebi_curated'").fetchone()
        self.assertEqual(state,('rejected',11))
        path.write_text(path.read_text().replace('14642','14641'),encoding='utf-8')
        self.assertEqual(ingest_oeis(self.db,path)['updated'],1)
        state=self.db.execute("SELECT verification,checked_terms FROM formulas WHERE oeis_id='A000583' AND origin='komorebi_curated'").fetchone()
        self.assertEqual(state,('finite_checked',18))

if __name__=='__main__':
    unittest.main()
