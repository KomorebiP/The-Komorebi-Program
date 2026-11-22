"""Self-contained display contract for the exact closure atlas. Author: Komorebi P."""
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from oeis_formula_database import connect,ingest_curated
from sequence_recurrence_packets import compile_db
from sequence_transfer_closure import build as compile_closure
from sequence_sparse_lifts import discover
from render_sequence_closure_atlas import build

ROOT=Path(__file__).resolve().parents[1]

class ClosureAtlasTests(unittest.TestCase):
    def test_portable_html_no_script_execution_or_remote_assets(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td)
            db=connect(base/'test.sqlite3')
            try:
                ingest_curated(db,ROOT/'research/oeis-formulas/seeds.json')
                ingest_curated(db,ROOT/'research/oeis-formulas/seeds-extended.json')
                compile_db(db,max_modulus=4)
                a=base/'closure.jsonl';b=base/'sparse.jsonl';page=base/'atlas.html'
                compile_closure(db,a,max_pairs=10,max_phase_modulus=4)
                discover(db,b,max_modulus=5,max_support=3,max_coefficient=20)
                output=build(db,a,b,page)
                html=page.read_text(encoding='utf-8')
                self.assertGreater(output['display_records'],50)
                self.assertIn('A000931',html)
                self.assertIn('A000045',html)
                self.assertIn('sparse_polyphase',html)
                self.assertIn('Proof boundary',html)
                self.assertNotIn('<script src=',html)
                self.assertNotIn('eval(',html)
                self.assertNotIn('__PAYLOAD__',html)
            finally:db.close()

if __name__=='__main__':unittest.main()
