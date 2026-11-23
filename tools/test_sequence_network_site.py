"""Offline static-site proof-boundary and handoff tests."""
import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from sequence_network_site import read_index, read_formula_text, build_site_assets,local_network_link,network_section
ROOT=Path(__file__).resolve().parents[1]

class DummySite:
    def __init__(self,root,output):self.root=root;self.output=output
    def write(self,name,content):
        target=self.output/name;target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(content,encoding='utf-8')

class NetworkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.fixture=read_index(ROOT/'manifests/sequence-transfer-network.json')
    def test_counts_and_attribution(self):
        index=self.fixture
        self.assertEqual(index['counts'],{'hyperedge':539,'gauge':975,'riordan':41,'quadratic':4})
        self.assertEqual(len(index['edges']),1559)
        self.assertEqual(index['oeis']['license'],'CC-BY-SA-4.0')
        self.assertGreaterEqual(len(index['records']),900)
    def test_pinned_formula_source_is_unreviewed_and_complete(self):
        source=read_formula_text(ROOT/'manifests/sequence-network-formula-text.json',self.fixture)
        self.assertEqual(source['counts'],{'network_ids':916,'ids_with_formulas':845,'formula_lines':8853})
        self.assertEqual(source['evidence'],'unreviewed_source_text')
        self.assertEqual(source['snapshot_sha256'],self.fixture['oeis']['snapshot_sha256'])
        self.assertTrue(any('binomial' in row['text'].lower()
                            for row in source['entries']['A000108']['formulas']))
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'source.json'
            for key,value in [('evidence','all_index_formula_identity'),('snapshot_sha256','forged')]:
                corrupted=copy.deepcopy(source);corrupted[key]=value
                p.write_text(json.dumps(corrupted),encoding='utf-8')
                with self.subTest(field=key),self.assertRaises(ValueError):
                    read_formula_text(p,self.fixture)
            corrupted=copy.deepcopy(source)
            corrupted['entries']['A000108']['source']='javascript:alert(1)'
            p.write_text(json.dumps(corrupted),encoding='utf-8')
            with self.assertRaises(ValueError):read_formula_text(p,self.fixture)

    def test_invalid_proof_status_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            for alteration in ('evidence','key','counts','id'):
                data=copy.deepcopy(self.fixture)
                if alteration=='evidence':data['edges'][0]['evidence']='finite_candidate'
                if alteration=='key':data['edges'][0]['key']=data['edges'][1]['key']
                if alteration=='counts':data['counts']['hyperedge']=1
                if alteration=='id':data['records'][0]['id']='https://evil.example/'
                p=Path(temporary)/'bad.json';p.write_text(json.dumps(data),encoding='utf-8')
                with self.subTest(alteration=alteration),self.assertRaises(ValueError):read_index(p)
    def test_local_handoff_never_promoted(self):
        with tempfile.TemporaryDirectory() as temporary:
            r=Path(temporary)/'repo';o=Path(temporary)/'site';(r/'manifests').mkdir(parents=True)
            (r/'website/assets').mkdir(parents=True)
            shutil.copy(ROOT/'manifests/sequence-transfer-network.json',r/'manifests/sequence-transfer-network.json')
            shutil.copy(ROOT/'manifests/sequence-network-formula-text.json',r/'manifests/sequence-network-formula-text.json')
            for name in ('sequence-network.css','sequence-network-ui.mjs','sequence-network-format.mjs'):
                shutil.copy(ROOT/'website/assets'/name,r/'website/assets'/name)
            entries=[{'id':'KSEQ-TEST','oeis_checked':True,'matches':[{'id':'A000108','matched_terms':24},
                {'id':'A000217','matched_terms':7}]},{'id':'KSEQ-NOCHECK','oeis_checked':False,
                 'matches':[{'id':'A000129','matched_terms':30}]}]
            meta=build_site_assets(DummySite(r,o),entries)
            self.assertEqual(meta['edge_count'],1559)
            formula_out=json.loads((o/'assets/sequence-network-formulas.json').read_text())
            self.assertEqual(formula_out['counts']['formula_lines'],8853)
            self.assertEqual(meta['handoffs'],1)
            handoff=json.loads((o/'assets/sequence-network-handoffs.json').read_text())
            self.assertEqual(handoff['matches']['KSEQ-TEST'],[{'id':'A000108','terms':24}])
            self.assertNotIn('KSEQ-NOCHECK',handoff['matches'])
            self.assertIn('finite',handoff['scope'].lower())
            self.assertIn('sequence-network.html?q=KSEQ-TEST',local_network_link(entries[0]))
            self.assertIn('sequence-network',network_section(meta))
    def test_quadratic_channels_are_shifted_transfers(self):
        quad=[e for e in self.fixture['edges'] if e['kind']=='quadratic']
        self.assertEqual(len(quad),4)
        for c,q,B,D in ((1,2,'A001333','A000129'),(2,3,'A001075','A001353')):
            rows={x['target']:x for x in quad if x['proof_ref']==f'quadratic-channel:{c}:{q}'}
            self.assertEqual(set(rows),{B,D})
            self.assertEqual(rows[B]['inputs'],[D])
            self.assertEqual(rows[D]['inputs'],[B])
            self.assertEqual(rows[B]['index_maps'][D],[[1,0],[1,1]])
            self.assertEqual(rows[D]['index_maps'][B],[[1,0],[1,1]])
            bn,dn=1,0
            for n in range(30):
                next_b,next_d=c*bn+q*dn,bn+c*dn
                self.assertEqual(bn,next_d-c*dn)
                self.assertEqual(dn,(next_b-c*bn)//q)
                bn,dn=next_b,next_d

    def test_gauge_states_initial_normalization_and_domain(self):
        gauges=[e for e in self.fixture['edges'] if e['kind']=='gauge']
        self.assertEqual(len(gauges),975)
        for e in gauges:
            self.assertIn('L(t)/L(t0)',e['expression'])
            self.assertIn('c^(t-t0)',e['expression'])
            self.assertIn(f"t0={e['valid_from']}",e['expression'])
            self.assertIn(f"n>={e['valid_from']}",e['domain'])

    def test_untrusted_local_id_escaped_or_rejected(self):
        with self.assertRaises(ValueError):local_network_link({'id':'KSEQ"<script>'})
if __name__=='__main__':unittest.main()
