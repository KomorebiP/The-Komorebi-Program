"""Exact transfer quotient-ring verification and negative controls. Author: Komorebi P."""
import json
import random
from pathlib import Path
import sqlite3
import tempfile
import unittest

from sequence_recurrence_packets import nth_term,x_packet,load_sources,compile_db
from oeis_formula_database import connect,ingest_curated
from sequence_sparse_lifts import sparse_lifts,certify,multinomial_evaluate,discover

ROOT=Path(__file__).resolve().parents[1]

class SparseLiftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._temp=tempfile.TemporaryDirectory()
        cls.db_path=Path(cls._temp.name)/'rebuild.sqlite3'
        db=connect(cls.db_path)
        try:
            ingest_curated(db,ROOT/'research/oeis-formulas/seeds.json')
            ingest_curated(db,ROOT/'research/oeis-formulas/seeds-extended.json')
            compile_db(db,max_modulus=4)
        finally:db.close()

    @classmethod
    def tearDownClass(cls):cls._temp.cleanup()

    def test_fibonacci_lucas_Pell_Jacobsthal_Padovan_Tribonacci(self):
        with sqlite3.connect(self.db_path) as db:
            sources=load_sources(db,['A000045','A000032','A000129','A001045','A000931','A000073'])
        expected={
            'A000045':(2,[1,1]),'A000032':(2,[1,1]),
            'A000129':(2,[1,2]),'A001045':(2,[2,1]),
            'A000931':(3,[1,1,0]),'A000073':(3,[1,1,1]),
        }
        for sid,(initial,c) in sources.items():
            m,poly=expected[sid]
            lifts={r['modulus']:r for r in sparse_lifts(c,12,3,50)}
            self.assertEqual(lifts[m]['polynomial'],poly)
            certify(initial,c,lifts[m],checks=8,residues=(0,1,2))
            for n in range(16):
                for r in range(3):
                    actual=nth_term(initial,c,m*n+r)
                    expected_value=multinomial_evaluate(initial,c,lifts[m],n,r)
                    self.assertEqual(actual,expected_value)

    def test_padovan_works_for_arbitrary_initial_conditions(self):
        rng=random.Random(2011)
        for _ in range(12):
            initial=[rng.randint(-10,10) for _ in range(3)]
            c=[0,1,1]
            lift=next(x for x in sparse_lifts(c,3,2,2) if x['modulus']==3)
            for n in range(20):
                self.assertEqual(multinomial_evaluate(initial,c,lift,n),
                                 nth_term(initial,c,3*n))

    def test_arbitrary_recurrence_polynomial_certificate(self):
        rng=random.Random(2026)
        for _ in range(25):
            d=rng.randint(1,4)
            c=[rng.randint(-2,2) for _ in range(d)]
            ini=[rng.randint(-2,2) for _ in range(d)]
            for m in range(max(2,d),8):
                poly=x_packet(m,c)
                selected=[{'shift':j,'weight':v} for j,v in enumerate(poly) if v]
                if not selected:continue
                lift={'modulus':m,'polynomial':poly,'terms':selected}
                for r in (0,1):
                    for n in range(5):
                        self.assertEqual(multinomial_evaluate(ini,c,lift,n,r),nth_term(ini,c,m*n+r))

    def test_negative_controls(self):
        v=[0,1];c=[1,1]
        lift=sparse_lifts(c,3,2,20)[0]
        mutated=dict(lift,polynomial=[2,1])
        with self.assertRaises(ArithmeticError):certify(v,c,mutated)
        with self.assertRaisesRegex(ValueError,'budget'):
            multinomial_evaluate([0,0,1],[1,1,1],
                {'modulus':3,'polynomial':[1,1,1],'terms':[{'shift':j,'weight':1} for j in range(3)]},
                80,max_expansion=400)

    def test_db_export_has_nontrivial_power_congruences(self):
        with sqlite3.connect(self.db_path) as db:
            with tempfile.TemporaryDirectory() as temp:
                output=Path(temp)/'lifts.jsonl'
                report=discover(db,output,max_modulus=12,max_support=3,max_coefficient=20)
                self.assertEqual(report['recurrence_sources'],33)
                rows=[json.loads(r) for r in output.read_text().splitlines()]
                self.assertEqual(report['certified_sequence_lifts'],len(rows))
                self.assertEqual(report['binomial_or_monomial_lifts'],
                    sum(r['lift']['support']<=2 for r in rows))
                self.assertTrue(any(r['source_oeis_id']=='A000931' and
                    r['lift']['modulus']==3 and r['lift']['polynomial']==[1,1,0] for r in rows))
                self.assertTrue(all(r['lift']['modulus']>=len(r['recurrence']) for r in rows))

if __name__=='__main__':unittest.main()
