"""Author: Komorebi P. Static source, arithmetic and route checks."""
import unittest
import tempfile
import json
import subprocess
from pathlib import Path
from html.parser import HTMLParser
from graph_formula_atlas import load, evaluate, build, PreviewSite, FAMILIES
from graph_formula_atlas_transfers import ADDED_FAMILIES, TRANSFER_JSON, TRANSFER_PAGE

ROOT=Path(__file__).resolve().parents[1]

class Controls(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.labels=set()
        self.controls=[]
        self.ids=[]
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if a.get('id'):
            self.ids.append(a['id'])
        if tag=='label' and a.get('for'):
            self.labels.add(a['for'])
        if tag in ('input','select','textarea'):
            self.controls.append(a)

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
            self.assertEqual(result['formula_records'],537)
            self.assertEqual(result['families'],17)
            self.assertEqual(result['exact_calculators'],363)
            bundle=json.loads((Path(out)/TRANSFER_JSON).read_text())
            self.assertEqual(len(bundle['coreModels']),288)
            self.assertEqual(len(bundle['nonbipartiteModels']),75)
            self.assertEqual(len(bundle['transfers']),60)
            self.assertEqual(len(bundle['zeroComplements']),11)
            self.assertEqual(len(bundle['equivalenceGroups']),16)
            self.assertTrue((Path(out)/TRANSFER_PAGE).is_file())
            self.assertEqual((Path(out)/'graph-formulas.html').read_text().count('data-gfa-record '),537)
            controls=Controls((Path(out)/'graph-formulas.html').read_text())
            self.assertEqual(len(controls.controls),3)
            self.assertTrue(all(c.get('id') in controls.labels or c.get('aria-label') for c in controls.controls))
            self.assertEqual(len(controls.ids),len(set(controls.ids)))
            for slug,_,_,count,_ in FAMILIES+ADDED_FAMILIES:
                body=(Path(out)/'graph-formulas'/f'{slug}.html').read_text()
                self.assertEqual(body.count('<details class="gfa-record"'),count)
                controls=Controls(body)
                self.assertTrue(all(c.get('id') in controls.labels or c.get('aria-label') for c in controls.controls))
                self.assertEqual(len(controls.ids),len(set(controls.ids)))
                self.assertEqual(len(controls.controls),count if slug in {f[0] for f in FAMILIES[:8]+ADDED_FAMILIES} else 0)

    def test_all_index_audit_negative_control(self):
        p=subprocess.run(['node',str(ROOT/'tools/verify_graph_formula_atlas_exact.js')],
                         cwd=ROOT,check=True,capture_output=True,text=True)
        report=json.loads(p.stdout)
        self.assertEqual(report['identities'],288)
        self.assertEqual(report['lanes'],1752)
        self.assertTrue(report['negativeControlRejected'])

if __name__=='__main__':unittest.main()
