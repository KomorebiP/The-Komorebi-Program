"""Integrity controls for the formula dependency hypergraph browser.

Author: Komorebi P.
"""
import json,sqlite3,tempfile,re,unittest
from pathlib import Path
from render_oeis_dependency_atlas import build

class DependencyBrowserTests(unittest.TestCase):
    def test_escaping_and_counts(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            db=sqlite3.connect(':memory:')
            db.execute('CREATE TABLE sequences (oeis_id TEXT, name TEXT)')
            db.execute('INSERT INTO sequences VALUES (?,?)',('A000011','<img src=x onerror=alert(1)>'))
            x={'oeis_id':'A000010','references':['A000011','A000012'],
               'status':'finite_checked_formula_hyperedge','checked_terms':29,
               'candidate_rhs':'A000011(n) + A000012(n)','source_text_sha256':'ff'*32}
            (p/'data.jsonl').write_text(json.dumps(x)+'\n')
            (p/'summary.json').write_text(json.dumps({'reference_occurrences':2,'multi_input_lines':1,'finite_checked_lines':1}))
            stats=build(db,p/'data.jsonl',p/'summary.json',p/'browser.html')
            self.assertEqual(stats['finite_checked'],1)
            source=(p/'browser.html').read_text()
            m=re.search(r'<script id="dataPayload" type="application/json">(.*?)</script>',source,re.S)
            self.assertIsNotNone(m)
            payload=json.loads(m.group(1))
            self.assertEqual(payload['rows'][0]['references'],['A000011','A000012'])
            self.assertEqual(payload['names']['A000011'],'<img src=x onerror=alert(1)>')
            self.assertNotIn('<img src=x',source)
            self.assertEqual(source.count('</script>'),2)
            db.close()

if __name__=='__main__':unittest.main()
