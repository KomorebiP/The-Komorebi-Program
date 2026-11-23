"""Offline atlas source integration and safe escaped JSON data tests.

Author: Komorebi P.
"""
import json,sqlite3,tempfile,unittest
from pathlib import Path
from render_oeis_holonomic_atlas import render


class TestV10Atlas(unittest.TestCase):
    def test_renderer_handles_empty_source_and_escapes_html(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp);(path/'outputs').mkdir()
            with sqlite3.connect(path/'min.sqlite3') as db:
                db.executescript('CREATE TABLE sequences (oeis_id TEXT PRIMARY KEY, name TEXT)')
                db.execute('INSERT INTO sequences VALUES (?,?)',('A000108','Catalan </script><script>alert(1)</script>'))
                db.commit()
            with (path/'outputs'/'holonomic-all-final.jsonl').open('w') as f:
                f.write(json.dumps({'oeis_id':'A000108','formula_id':'formula1','order':1,
                    'component_count':1,'operator_coefficients':[['-1'],['1']],
                    'mathematical_start':0,'checked_oeis_recursion_positions':10})+'\n')
            result=render(path/'min.sqlite3',path,path/'out.html')
            self.assertEqual(result['records'],1)
            source=(path/'out.html').read_text()
            self.assertIn('A000108',source)
            self.assertNotIn('Catalan </script><script>alert(1)',source)
            self.assertIn('Catalan <\\/script>',source)
            self.assertIn('textContent',source)
            self.assertIn('OEIS Foundation',source)

    def test_filter_kinds_and_routes_source_included(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp);(path/'outputs').mkdir()
            with sqlite3.connect(path/'min.sqlite3') as db:
                db.executescript('CREATE TABLE sequences (oeis_id TEXT PRIMARY KEY, name TEXT)')
                db.executemany('INSERT INTO sequences VALUES (?,?)',
                               [('A000108','Catalan'),('A000984','Central binomial')]);db.commit()
            cert={'source':'A000108','target':'A000984','source_formula':'f1',
                  'base_ratio':'1','exponential_factor':'1','gauge_linear_factors':[{'a':1,'b':1,'power':1}],
                  'tail_start_local':0,'support':1}
            (path/'outputs'/'structured-gauges.jsonl').write_text(json.dumps(cert)+'\n')
            result=render(path/'min.sqlite3',path,path/'out.html')
            self.assertEqual(result['categories']['Direct transfer'],1)
            self.assertIn('A000984',(path/'out.html').read_text())

if __name__=='__main__':unittest.main()
