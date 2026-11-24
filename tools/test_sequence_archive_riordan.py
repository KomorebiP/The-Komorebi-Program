"""Adversarial exact rational-OGF replay for the archived v0.8 operators."""
from __future__ import annotations
import csv
import json
import random
import sqlite3
import tempfile
import unittest
from pathlib import Path
from fractions import Fraction

from sequence_archive_rational_operators import RatOGF
from sequence_archive_v08_riordan import riordan_ogf,replay_riordan_archive
from sequence_archive_v08_bridge import riordan_nth,quadratic_pair,quadratic_certificate
from sequence_sparse_index import integer_sha256,prepare_sparse_tasks,execute_sparse_plan,shortest_sparse_plan
from test_sequence_sparse_index import sample_models_and_edges


class RiordanAlgebraTests(unittest.TestCase):
    def test_random_exact_rational_ogfs(self):
        rng=random.Random(32016)
        for _ in range(35):
            num=[rng.randint(-2,2) for k in range(rng.randint(1,3))]
            den=[1]+[rng.randint(-2,2) for k in range(rng.randint(1,3))]
            a=RatOGF(tuple(num),tuple(den))
            c=rng.randint(-2,2);s=rng.randint(0,3);r=rng.randint(1,3);t=rng.randint(1,3)
            b=riordan_ogf(a,c=c,s=s,r=r,t=t)
            left=a.terms(18);right=b.terms(18)
            out=[riordan_nth(lambda k:int(left[k]),n,c=c,s=s,r=r,t=t) for n in range(18)]
            self.assertEqual(out,right)

    def test_unramified_inverse_formal_power_series(self):
        rng=random.Random(22)
        for _ in range(22):
            a=RatOGF((rng.randint(0,4),rng.randint(-3,3)),
                     (1,rng.randint(-2,2),rng.randint(-2,2)))
            c=rng.randint(-4,4);s=rng.randint(0,4)
            b=riordan_ogf(a,c=c,s=s,r=1,t=1)
            inv=riordan_ogf(b,c=-c,s=s,r=1,t=1)
            self.assertEqual(inv.num,a.num)
            self.assertEqual(inv.den,a.den)

    def test_not_invertible_when_ramified(self):
        a=RatOGF((0,1),(1,))
        b=riordan_ogf(a,c=0,s=0,r=2,t=2)
        self.assertEqual(b.terms(6),[0,0,1,0,0,0])
        self.assertNotEqual(b.num,a.num)

    def test_wrong_target_rejected(self):
        source=RatOGF((1,),(1,-2))
        actual=riordan_ogf(source,c=1,s=1,r=2,t=2)
        false=RatOGF((1,),(1,-3))
        self.assertNotEqual((actual.num,actual.den),(false.num,false.den))

    def test_real_source_trial_in_minimal_sqlite(self):
        with tempfile.TemporaryDirectory() as td:
            dbfile=Path(td)/'mini.sqlite'
            arch=Path(td)/'riordan.csv'
            a=RatOGF((1,),(1,-2))
            b=riordan_ogf(a,c=1,s=1,r=2,t=2)
            with sqlite3.connect(dbfile) as db:
                db.execute('CREATE TABLE sequences(oeis_id TEXT,name TEXT,offset INT,terms_json TEXT,source_sha256 TEXT)')
                for sid,g in [('A000079',a),('A001333',b)]:
                    db.execute('INSERT INTO sequences VALUES(?,?,?,?,?)',
                               (sid,'example',0,json.dumps([str(x) for x in g.terms(30)]),sid+'hash'))
            original={'cert_key':'fixture','source_id':'A000079','target_id':'A001333',
                'c':'1','s':'1','r':'2','t':'2',
                'source_ogf_json':json.dumps(a.to_json()),
                'target_ogf_json':json.dumps(b.to_json()),
                'premise_state':'exact_Qx_from_two_classical_models'}
            def write(row):
                with arch.open('w',newline='',encoding='utf-8') as f:
                    w=csv.DictWriter(f,fieldnames=list(row));w.writeheader();w.writerow(row)
            write(original)
            result=replay_riordan_archive(arch,dbfile)
            self.assertEqual(result['exact_rational_identities'],1)
            self.assertEqual(result['cross_snapshot_riordan_output_comparisons'],25)
            tampered=dict(original,target_ogf_json=json.dumps(RatOGF((1,),(1,-3)).to_json()))
            write(tampered)
            with self.assertRaises(ArithmeticError):replay_riordan_archive(arch,dbfile)
            write(original)
            with sqlite3.connect(dbfile) as db:
                row=db.execute("SELECT terms_json FROM sequences WHERE oeis_id='A001333'").fetchone()
                values=json.loads(row[0]);values[18]='999999'
                db.execute("UPDATE sequences SET terms_json=? WHERE oeis_id='A001333'",(json.dumps(values),))
            with self.assertRaises(ArithmeticError):replay_riordan_archive(arch,dbfile)

    def test_huge_integer_receipts_avoid_decimal_limit(self):
        cert=quadratic_certificate(1,2,20000)
        self.assertTrue(cert['norm_verified'])
        self.assertGreater(cert['B']['bits'],12000)
        self.assertIsNone(cert['B']['decimal'])
        self.assertEqual(len(cert['D']['binary_sha256']),64)
        value=1<<50000
        self.assertEqual(len(integer_sha256(value)),64)

if __name__=='__main__':unittest.main()
