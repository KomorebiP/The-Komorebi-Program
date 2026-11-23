"""Cycle consistency and canonical chart tests. Author: Komorebi P."""
import hashlib,json,tempfile,unittest
from pathlib import Path
from fractions import Fraction
from sequence_hypergeometric_gauges import certify_pair,source_model
from sequence_holonomic_compiler import fraction_eval
from sequence_gauge_atlas import make_gauge_atlas,normalize_cycle
from sequence_v10_path_compiler import oriented_edge

N={'op':'n'}
def add(*xs):return dict(op='add',args=list(xs))
def mul(*xs):return dict(op='mul',args=list(xs))
def mod(sid,ast):
    terms=[str(fraction_eval(ast,n)) for n in range(24)]
    m=source_model('m-'+sid,sid,ast,0,json.dumps(terms),hashlib.sha256(sid.encode()).hexdigest())
    assert m is not None and m['tail']==0
    return m

class TestGaugeAtlas(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.file=Path(self.tmp.name)/'gauge.jsonl'
        f= {'op':'binomial','n':mul(2,N),'k':N}
        g= {'op':'exact_div','num':f,'den':add(N,1)}
        h=mul(f,add(N,1))
        models=[mod('A100001',f),mod('A100002',g),mod('A100003',h)]
        self.models={m['oeis_id']:m for m in models}
        self.edges=[]
        for a,b in (('A100001','A100002'),('A100002','A100003'),('A100001','A100003')):
            edge=certify_pair(self.models[a],self.models[b],max_support=5)
            self.assertIsNotNone(edge)
            self.edges.append(edge)
        self.file.write_text(''.join(json.dumps(r)+'\n' for r in self.edges),encoding='utf8')

    def test_triangle_cycle_flatness_and_two_charts(self):
        atlas=make_gauge_atlas(self.models,self.file)
        stats=atlas['summary']
        self.assertEqual(stats['accepted_full_prefix_gauges'],3)
        self.assertEqual(stats['connected_formula_models'],3)
        self.assertEqual(stats['component_count'],1)
        self.assertEqual(stats['fundamental_cycles'],1)
        self.assertEqual(stats['flat_cycles'],1)
        self.assertEqual(stats['chart_count'],2)
        self.assertTrue(atlas['cycles'][0]['flat'])

    def test_ledger_order_does_not_change_cycle_rank(self):
        one=make_gauge_atlas(self.models,self.file)
        self.file.write_text(''.join(json.dumps(e)+'\n' for e in reversed(self.edges)),encoding='utf8')
        other=make_gauge_atlas(self.models,self.file)
        self.assertEqual(one['summary']['fundamental_cycles'],other['summary']['fundamental_cycles'])
        self.assertEqual(one['summary']['nontrivial_holonomy'],other['summary']['nontrivial_holonomy'])

    def test_normalizer_rejects_fake_holonomy(self):
        fake=dict(self.edges[0]);fake['base_ratio']='2'
        self.assertFalse(normalize_cycle([fake,oriented_edge(self.edges[0],True)])['flat'])
        fake=dict(self.edges[0]);fake['exponential_factor']='3'
        self.assertFalse(normalize_cycle([fake,oriented_edge(self.edges[0],True)])['flat'])

    def test_certificate_tampering_rejected(self):
        altered=[dict(x) for x in self.edges];altered[-1]['target_sha256']='bad'
        self.file.write_text(''.join(json.dumps(e)+'\n' for e in altered),encoding='utf8')
        with self.assertRaises(ValueError):make_gauge_atlas(self.models,self.file)

if __name__=='__main__':unittest.main()
