"""Renderer smoke tests; browser interaction checked separately when Chromium exists."""
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from oeis_formula_database import connect, ingest_curated
from sequence_transfer_graph import create_graph
from sequence_transfer_miner import mine_transfers,mine_rational_ratios
from render_sequence_transfer_atlas import render
BASE=Path(__file__).resolve().parents[1]

class AtlasRenderTests(unittest.TestCase):
    def test_render_is_standalone_and_marks_provenance(self):
        with tempfile.TemporaryDirectory() as d:
            db=connect(Path(d)/'d.sqlite3')
            try:
                ingest_curated(db,BASE/'research/oeis-formulas/seeds.json')
                ingest_curated(db,BASE/'research/oeis-formulas/seeds-extended.json')
                mine_transfers(db);mine_rational_ratios(db);create_graph(db)
                r=render(db,Path(d)/'atlas.html')
                html=Path(r['html']).read_text()
                self.assertIn('A000045',html)
                self.assertIn('finite_candidate',html)
                self.assertIn('algebraic_identity',html)
                self.assertIn('Not a theorem' if False else 'not a global theorem',html)
                self.assertNotIn('<script src=',html)
                self.assertGreater(r['nodes'],150)
            finally:db.close()
if __name__=='__main__':unittest.main()
