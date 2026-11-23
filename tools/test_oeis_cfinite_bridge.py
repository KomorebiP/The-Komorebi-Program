"""Exact all-index recurrence transfer controls, including known OEIS pairs."""
from fractions import Fraction as Q
import json
from pathlib import Path
import unittest

from oeis_cfinite_bridge import build, recurrence_transfer, terms, sequence_terms
from oeis_gap_automation import components,load_network

HERE=Path(__file__).resolve().parents[1]

class CFiniteBridgeTests(unittest.TestCase):
    def setUp(self):
        self.reg=json.loads((HERE/'manifests/oeis-cfinite-recurrence-seeds.json').read_text())
        self.seeds={x['id']:x for x in self.reg['sequences']}

    def test_fibonacci_to_lucas_all_index_certificate(self):
        fib,luc=self.seeds['A000045'],self.seeds['A000032']
        f=recurrence_transfer(fib,luc);r=recurrence_transfer(luc,fib)
        self.assertEqual((f['alpha'],f['beta']),('-1','2'))
        self.assertEqual((r['alpha'],r['beta']),('-1/5','2/5'))
        a=terms(1,1,[0,1],120);b=terms(1,1,[2,1],120)
        for n in range(119):
            self.assertEqual(b[n],-a[n]+2*a[n+1])
            self.assertEqual(5*a[n],-b[n]+2*b[n+1])

    def test_pell_companion(self):
        pell,pellcomp=self.seeds['A000129'],self.seeds['A001333']
        f=recurrence_transfer(pell,pellcomp);r=recurrence_transfer(pellcomp,pell)
        self.assertEqual((f['alpha'],f['beta']),('-1','1'))
        self.assertEqual((r['alpha'],r['beta']),('-1/2','1/2'))
        a=terms(2,1,[0,1],120);b=terms(2,1,[1,1],120)
        for n in range(119):
            self.assertEqual(b[n],a[n+1]-a[n])
            self.assertEqual(2*a[n],b[n+1]-b[n])

    def test_adversarial_seed(self):
        with self.assertRaises(ValueError):
            wrong={**self.reg,'sequences':self.reg['sequences']+[self.reg['sequences'][0]]}
            build(wrong,set(),{})
        x=dict(self.seeds['A000045'])
        x['initial']=[0,0]
        self.assertIsNone(recurrence_transfer(x,self.seeds['A000032']))

    def test_singular_but_compatible_shift_orbit(self):
        source={'id':'A123450','recurrence':[2,-1],'initial':[1,1],'source':'https://oeis.org/A123450'}
        target={'id':'A123451','recurrence':[2,-1],'initial':[3,3],'source':'https://oeis.org/A123451'}
        c=recurrence_transfer(source,target)
        self.assertFalse(c['coefficients_unique'])
        self.assertEqual(c['source_shift_rank'],1)
        self.assertEqual(c['shift_coefficients'],['3','0'])

    def test_higher_order_polynomial_bridges(self):
        for src,dst in [('A000290','A000217'),('A000578','A000330'),('A000583','A000537')]:
            source,target=self.seeds[src],self.seeds[dst]
            proof=recurrence_transfer(source,target)
            self.assertIsNotNone(proof)
            coeff=[Q(x) for x in proof['shift_coefficients']]
            terms_a=sequence_terms(source['recurrence'],source['initial'],100)
            terms_b=sequence_terms(target['recurrence'],target['initial'],100)
            for n in range(100-len(coeff)+1):
                self.assertEqual(terms_b[n],sum(coeff[i]*terms_a[n+i] for i in range(len(coeff))))

    def test_network_cross_component(self):
        net=HERE/'manifests/sequence-transfer-network.json'
        if not net.exists():net=HERE/'fixtures/existing_sequence_network_v15.json'
        n=load_network(net)
        c,_=components(n)
        report=build(self.reg,set(c),c)
        self.assertEqual(report['certificate_count'],10)
        self.assertEqual(report['cross_component_certificate_count'],2)
        self.assertEqual(len(report['rank_deficient_pairs_unresolved']),0)
        self.assertEqual(report['certificates'][0]['formal_abstract_identity'],'proved')

if __name__=='__main__':unittest.main()
