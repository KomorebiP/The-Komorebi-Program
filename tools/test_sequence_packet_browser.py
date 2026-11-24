"""Rebuild the exact certificate atlas without relying on committed generated files.

Author: Komorebi P.
"""
from pathlib import Path
import json
import re
import tempfile
import unittest

from oeis_formula_database import connect, ingest_curated
from sequence_recurrence_packets import compile_db
from sequence_packet_atlas import build as build_phases
from sequence_linear_identity_compiler import discover
from render_sequence_packet_atlas import build as render_atlas

ROOT=Path(__file__).resolve().parents[1]


class AtlasTest(unittest.TestCase):
    def test_render_includes_only_grounded_certificates(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            folder=root/'research/oeis-formulas'
            folder.mkdir(parents=True)
            db=connect(root/'scratch.sqlite3')
            try:
                ingest_curated(db,ROOT/'research/oeis-formulas/seeds.json')
                ingest_curated(db,ROOT/'research/oeis-formulas/seeds-extended.json')
                packet=compile_db(db,max_modulus=8)
                index=build_phases(db,folder/'phase-formulas.jsonl',folder/'packet-atlas-index.json')
                exact=discover(db)
            finally:db.close()
            self.assertEqual(packet['certified_polyphase_formulas'],1155)
            self.assertEqual(index['denominator_modules'],72)
            self.assertEqual(exact['exact_identities'],58)
            (folder/'exact-linear-identities.jsonl').write_text(''.join(json.dumps(x,sort_keys=True)+'\n' for x in exact['links']),encoding='utf-8')
            (folder/'EXACT_BASIS.json').write_text(json.dumps(exact['basis']),encoding='utf-8')
            path=root/'packet.html'
            counts=render_atlas(root,path)
            self.assertEqual(counts['phase_count'],1155)
            self.assertEqual(counts['transfer_count'],58)
            self.assertEqual(counts['basis_size'],9)
            doc=path.read_text(encoding='utf-8')
            match=re.search(r'<script id="embedded" type="application/json">(.*?)</script>',doc,re.S)
            self.assertIsNotNone(match)
            data=json.loads(match.group(1))
            self.assertEqual(len(data['phases']),1155)
            self.assertEqual(len(data['links']),58)
            self.assertIn('OEIS identification',doc)
            self.assertTrue(all(x['scope'].startswith('all n>=0') for x in data['links']))


if __name__=='__main__':unittest.main()
