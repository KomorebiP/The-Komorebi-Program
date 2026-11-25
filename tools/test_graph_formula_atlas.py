"""Author: Komorebi P. Static source, arithmetic and route checks."""
import unittest
import tempfile
from pathlib import Path
from graph_formula_atlas import load, evaluate, build, PreviewSite, FAMILIES

ROOT=Path(__file__).resolve().parents[1]
class GraphFormulaAtlasTests(unittest.TestCase):
    def test_inventory_and_exact_evaluation(self):
        *_, records, counts=load(ROOT)
        self.assertEqual(sum(counts.values()),462)
        self.assertEqual(len(counts),15)
        core={r['id']:r['data'] for r in records if 'data' in r}
        self.assertEqual(len(core),288)
        self.assertEqual(evaluate(core['G01'],8),1)
        self.assertEqual(evaluate(core['C01'],8),5)
        self.assertEqual(evaluate(core['R03'],4),1)
    def test_generated_pages(self):
        with tempfile.TemporaryDirectory() as out:
            site=PreviewSite(ROOT,Path(out))
            result=build(site)
            self.assertEqual(result['formula_records'],462)
            self.assertEqual((Path(out)/'graph-formulas.html').read_text().count('data-gfa-record '),462)
            for slug,_,_,count,_ in FAMILIES:
                body=(Path(out)/'graph-formulas'/f'{slug}.html').read_text()
                self.assertEqual(body.count('<details class="gfa-record"'),count)

if __name__=='__main__':unittest.main()
