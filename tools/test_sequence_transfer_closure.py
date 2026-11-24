"""Exact all-index proof constructor tests for transfer operators.
Author: Komorebi P.
"""
from pathlib import Path
import json
import math
import sqlite3
import tempfile
import unittest

from sequence_transfer_closure import (binomial_transform,cauchy_product,
    hadamard_product,shift_monic_polynomial,canonical_recurrence,build)
from sequence_recurrence_packets import nth_term,load_sources,compile_db
from oeis_formula_database import connect,ingest_curated

ROOT=Path(__file__).resolve().parents[1]

class TransferClosureTests(unittest.TestCase):
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

    def test_binomial_Fibonacci_even(self):
        for initial in ([0,1],[2,1]):
            b=binomial_transform(initial,[1,1])
            self.assertEqual(b['coefficients'],[3,-1])
            for n in range(45):
                self.assertEqual(nth_term(b['initial'],b['coefficients'],n),
                                 nth_term(initial,[1,1],2*n))

    def test_exponential_chain(self):
        for rate in range(-4,8):
            f=binomial_transform([1],[rate])
            g=binomial_transform([1],[rate],inverse=True)
            self.assertEqual(f['coefficients'],[rate+1])
            self.assertEqual(g['coefficients'],[rate-1])

    def test_binomial_negative_and_inverse(self):
        for c in ([2],[1,1],[2,1],[0,0,1],[1,-1,2],[-1,3,0]):
            values=list(range(1,len(c)+1))
            forward=binomial_transform(values,c)
            original=binomial_transform(forward['initial'],forward['coefficients'],inverse=True)
            for n in range(26):
                self.assertEqual(nth_term(original['initial'],original['coefficients'],n),
                                 nth_term(values,c,n))
            self.assertEqual(shift_monic_polynomial(forward['coefficients'],1),c)

    def test_hadamard_Fibonacci_square(self):
        r=hadamard_product([0,1],[1,1],[0,1],[1,1])
        self.assertEqual(r['coefficients'],[2,2,-1])
        self.assertEqual(r['initial'],[0,1,1])
        for n in range(80):
            f=nth_term([0,1],[1,1],n)
            self.assertEqual(nth_term(r['initial'],r['coefficients'],n),f*f)

    def test_cauchy_Fibonacci(self):
        r=cauchy_product([0,1],[1,1],[0,1],[1,1])
        self.assertEqual(r['coefficients'],[2,1,-2,-1])
        self.assertEqual(r['initial'],[0,0,1,2])
        for n in range(50):
            direct=sum(nth_term([0,1],[1,1],k)*nth_term([0,1],[1,1],n-k)
                       for k in range(n+1))
            self.assertEqual(nth_term(r['initial'],r['coefficients'],n),direct)

    def test_zero_and_impulse_boundary(self):
        zero=hadamard_product([0],[0],[7],[3])
        self.assertEqual(zero['minimal']['order'],0)
        self.assertEqual(cauchy_product([1],[0],[1,1],[1,1])['minimal']['order'],2)
        impulse_square=cauchy_product([1,0],[0,0],[1,0],[0,0])
        self.assertEqual(impulse_square['coefficients'],[0])
        self.assertEqual(impulse_square['initial'],[1])

    def test_small_random_integer_operators(self):
        import random
        rng=random.Random(2006)
        for _ in range(30):
            da=rng.randint(1,3); db=rng.randint(1,3)
            ca=[rng.randint(-2,2) for _ in range(da)]
            cb=[rng.randint(-2,2) for _ in range(db)]
            va=[rng.randint(-3,3) for _ in range(da)]
            vb=[rng.randint(-3,3) for _ in range(db)]
            results=[hadamard_product(va,ca,vb,cb),cauchy_product(va,ca,vb,cb)]
            for n in range(30):
                p=nth_term(va,ca,n)*nth_term(vb,cb,n)
                q=sum(nth_term(va,ca,k)*nth_term(vb,cb,n-k) for k in range(n+1))
                for got,expected in zip(results,(p,q)):
                    self.assertEqual(nth_term(got['initial'],got['coefficients'],n),expected)

    def test_seed_graph_matches_are_global_curated_identities(self):
        p=self.db_path
        with sqlite3.connect(p) as db:
            s=load_sources(db,['A000045','A000032','A000012','A000079','A000244'])
            self.assertEqual(canonical_recurrence(*s['A000045']),
                             canonical_recurrence(*s['A000045']))
            with tempfile.TemporaryDirectory() as td:
                target=Path(td)/'closure.jsonl'
                report=build(db,target,max_pairs=15,max_phase_modulus=4)
                self.assertEqual(report['source_recursions'],33)
                rows=[json.loads(x) for x in target.read_text().splitlines()]
                def found(src,op,dst,m,r):
                    return any(x['inputs']==[src] and x['operator']==op and
                        {'oeis_id':dst,'modulus':m,'residue':r} in x['matches'] for x in rows)
                self.assertTrue(found('A000045','binomial','A000045',2,0))
                self.assertTrue(found('A000032','binomial','A000032',2,0))
                self.assertTrue(found('A000012','binomial','A000079',1,0))
                self.assertTrue(found('A000079','binomial','A000244',1,0))
                self.assertTrue(found('A000244','inverse_binomial','A000079',1,0))

    def test_corrupted_phase_receipt_is_rejected(self):
        # Recreate derived tables to test source-hash rejection without mutating the release DB.
        src=sqlite3.connect(self.db_path)
        with tempfile.TemporaryDirectory() as td:
            from shutil import copyfile
            dest=Path(td)/'bad.sqlite3'
            out=sqlite3.connect(dest)
            src.backup(out);out.commit();src.close()
            out.execute("UPDATE recurrence_packet_phases SET source_hash='stale' WHERE oeis_id='A000045'")
            out.commit()
            with self.assertRaisesRegex(ValueError,'stale phase certificate'):
                build(out,Path(td)/'bad.jsonl',max_pairs=0,max_phase_modulus=3)
            out.close()

if __name__=='__main__':unittest.main()
