"""Exact and adversarial checks for the real-OEIS atlas, without network or corpus."""
from __future__ import annotations
import json
import math
from pathlib import Path
import sqlite3
import tempfile
import unittest
from render_oeis_real_transfer_atlas import PROVED, build

class RealOEISAtlasTests(unittest.TestCase):
    def test_riordan_catalan_all_index_recurrence(self):
        # Independent integer recurrence and inverse-binomial evaluation.
        riordan=[1,0]
        for n in range(2,130):
            value=(n-1)*(2*riordan[-1]+3*riordan[-2])
            self.assertEqual(value%(n+1),0)
            riordan.append(value//(n+1))
        for n in range(130):
            inv=sum((-1)**(n-k)*math.comb(n,k)*(math.comb(2*k,k)//(k+1))
                    for k in range(n+1))
            # All summands are integers, and Catalan = exact integer quotient.
            self.assertEqual(inv,riordan[n],n)

    def test_minimal_atlas_fixture(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp=Path(tmp)
            with sqlite3.connect(':memory:') as db:
                db.executescript('''
                  CREATE TABLE sequences(oeis_id TEXT PRIMARY KEY,name TEXT NOT NULL);
                  CREATE TABLE formulas(origin TEXT,verification TEXT);
                  CREATE TABLE transfer_candidates(candidate_id TEXT,output_id TEXT,
                    inputs_json TEXT,operator TEXT,parameters_json TEXT,checked_terms INT,
                    holdout_terms INT,statement TEXT,status TEXT);
                ''')
                for idx,(src,tgt,op) in enumerate(PROVED):
                    db.execute('INSERT OR IGNORE INTO sequences VALUES (?,?)',(src,'Source '+src))
                    db.execute('INSERT OR IGNORE INTO sequences VALUES (?,?)',(tgt,'Target '+tgt))
                    db.execute('INSERT INTO transfer_candidates VALUES (?,?,?,?,?,?,?,?,?)',
                     (str(idx),tgt,json.dumps([src]),op,'{}',32,22,'Synthetic witness', 'finite_candidate'))
                db.execute("INSERT INTO formulas VALUES ('oeis_formula','raw_text')")
                db.execute("INSERT INTO formulas VALUES ('oeis_program','raw_text')")
                db.execute("INSERT INTO formulas VALUES ('oeis_normalized','finite_checked')")
                out=tmp/'index.html'; jsonl=tmp/'data.jsonl'; receipt=tmp/'receipt.json'
                summary=build(db,out,jsonl,receipt)
            self.assertEqual(summary['all_candidate_links'],5)
            self.assertEqual(summary['independently_proved_examples'],5)
            self.assertEqual(len(jsonl.read_text().splitlines()),5)
            self.assertIn('Real OEIS transfer atlas',out.read_text())
            self.assertIn('Catalog',out.read_text().replace('catalog','Catalog'))
            self.assertEqual(json.loads(receipt.read_text())['raw_program_blocks'],1)

    def test_missing_proof_example_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp,sqlite3.connect(':memory:') as db:
            db.executescript('''CREATE TABLE sequences(oeis_id TEXT,name TEXT);
              CREATE TABLE transfer_candidates(candidate_id TEXT,output_id TEXT,
                 inputs_json TEXT,operator TEXT,parameters_json TEXT,checked_terms INT,
                 holdout_terms INT,statement TEXT,status TEXT);
              CREATE TABLE formulas(origin TEXT,verification TEXT);''')
            root=Path(tmp)
            with self.assertRaisesRegex(ValueError,'Expected classical recovered identities absent'):
                build(db,root/'out.html',root/'data.jsonl',root/'receipt.json')

if __name__=='__main__': unittest.main()
