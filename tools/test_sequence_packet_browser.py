"""Exact certificate atlas static HTML checks."""
from pathlib import Path
import json
import re
import tempfile
import unittest
from render_sequence_packet_atlas import build

ROOT=Path(__file__).resolve().parents[1]

class AtlasTest(unittest.TestCase):
    def test_render_includes_only_grounded_certificates(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'packet.html'
            result=build(ROOT,path)
            self.assertEqual(result['phase_count'],1155)
            self.assertEqual(result['transfer_count'],58)
            self.assertEqual(result['basis_size'],9)
            text=path.read_text()
            match=re.search(r'<script id="embedded" type="application/json">(.*?)</script>',text,re.S)
            self.assertIsNotNone(match)
            payload=json.loads(match.group(1))
            self.assertEqual(len(payload['phases']),1155)
            self.assertEqual(len(payload['links']),58)
            self.assertIn('OEIS identification',text)
            self.assertTrue(all(x['scope'].startswith('all n>=0') for x in payload['links']))

if __name__=='__main__':unittest.main()
