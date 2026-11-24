"""Offline browser release integrity and hostile-title escaping tests.

Author: Komorebi P. Browser is static and never executes OEIS source text.
"""
import json
import re
import sqlite3
import tempfile
import unittest
from pathlib import Path

from render_oeis_v08_atlas import build


class OfflineAtlasTests(unittest.TestCase):
    def test_exact_payload_is_safe_and_self_contained(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            db=sqlite3.connect(':memory:')
            db.execute('CREATE TABLE sequences (oeis_id TEXT PRIMARY KEY, name TEXT)')
            db.executemany('INSERT INTO sequences VALUES (?, ?)', [
                ('A000001','a \\u003c/script\\u003e and <img src=x onerror=alert(1)>'),
                ('A000002','second & "quoted" <sequence>'),
            ])
            edge={'source':'A000001','target':'A000002','operator':'shift', 'parameters':{'shift':1},'was_finite_mined':False}
            projection={'target':'A000002','linear_combination':[{'source':'A000001','coefficient':'-2/3'}]}
            basis={'basis_rank':1,'source_count':2,'basis_sequences':['A000001']}
            (root/'edges.jsonl').write_text(json.dumps(edge)+'\n')
            (root/'basis.jsonl').write_text(json.dumps(projection)+'\n')
            (root/'summary.json').write_text(json.dumps(basis))
            report=build(db,root/'edges.jsonl',root/'basis.jsonl',root/'summary.json',root/'atlas.html')
            self.assertEqual((report['edges'], report['basis_projections'],report['basis_rank']),(1,1,1))
            page=(root/'atlas.html').read_text()
            payload=re.search(r'<script id="dataPayload" type="application/json">(.*?)</script>',page,re.S)
            self.assertIsNotNone(payload)
            obj=json.loads(payload.group(1))
            self.assertEqual(obj['names']['A000001'], 'a \\u003c/script\\u003e and <img src=x onerror=alert(1)>')
            self.assertEqual(obj['names']['A000002'], 'second & "quoted" <sequence>')
            self.assertNotIn('<img src=x', page)
            self.assertEqual(page.count('</script>'),2)
            self.assertIn("a.textContent=id",page)
            self.assertIn('rel=\'noopener noreferrer\'',page)
            db.close()


if __name__=='__main__': unittest.main()
