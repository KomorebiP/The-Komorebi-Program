"""Positive, negative and exact replay tests for Stage 5. Author: Komorebi P."""
import copy,json,unittest
from pathlib import Path
from fractions import Fraction as Q
import sympy as sp
from oeis_algebraic_gate import (x,y,n,ast_polynomial,equation,branch,differential,coefficient_operator,
    algebraic_profile,load_records,audit,gf_transfer,verify_composition,family_normal_form,family_term,decode_poly,encode_poly)
from oeis_joint_transfer_gate import discover_joint,verify_joint,joint_certificate,minimal_constant_characteristic,spectral_cover_jobs
from oeis_shift_operator_gate import discover,terms_at,const
from oeis_identification_proofs import parse_record

ROOT=Path(__file__).resolve().parents[3]
FIX=ROOT/'fixtures/oeis_stage5'
PLAN=json.loads((FIX/'plan.json').read_text())

class Stage5(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=audit(FIX,PLAN);cls.p=cls.report['profiles']
    def test_summary(self):
        self.assertEqual(self.report['summary'],{'records':6,'conditional_profiles':6,'algebraic_profiles':3,'joint_certificates':1,'spectral_cover_jobs':1,'composition_certificates':2,'family_normal_forms':3,'finite_sum_normal_forms':3})
    def test_orders_and_bases(self):
        for id,d in [('A000108',1),('A001006',2),('A006318',2)]:
            v=self.p[id]['definitions'][0];self.assertEqual((v['order'],v['base']),(d,0))
    def test_formal_branch_and_recurrence_farther_than_source(self):
        for id in ('A000108','A001006','A006318'):
            p=self.p[id];a,_=branch(decode_poly(p['algebraic']['P']),1,50)
            self.assertEqual([terms_at(p['definitions'][0],k) for k in range(50)],a)
    def test_singular_branch_refused(self):
        for P,a0 in [(y**2-x,0),(y**2-1,0),((y-1)**2,1)]:
            with self.assertRaisesRegex(ValueError,'simple formal branch'):branch(P,a0,5)
    def test_multiple_branches_selected_by_seed(self):
        a,slope=branch(y**2-1-x,1,8);b,_=branch(y**2-1-x,-1,8)
        self.assertEqual(a,[-v for v in b]);self.assertEqual(slope,2)
    def test_unsafe_or_ambiguous_input(self):
        for s in ['__import__("os").system("echo no")','x/y','x**10000','x**(-1)','sqrt(x)','x if y else 1','(x+y)**8']:
            with self.assertRaises(ValueError):ast_polynomial(s)
        with self.assertRaises(ValueError):equation('E.g.f.: A(x)=1+x*A(x).')
    def test_algebraic_source_mismatch(self):
        from dataclasses import replace
        rec=parse_record(FIX/'seq/A000/A000108.seq',FIX);wrong=replace(rec,terms=(1,1,3,*rec.terms[3:]));st=PLAN['records'][0]['statement']
        self.assertEqual(algebraic_profile(wrong,st)['status'],'quarantined_contradiction')
        self.assertEqual(algebraic_profile(replace(rec,offset=1),st)['status'],'unsupported')
    def test_non_squarefree_quotient_refused(self):
        # A simple branch can coexist with a repeated unrelated factor; the
        # current quotient inversion conservatively refuses the full polynomial.
        with self.assertRaises(sp.NotInvertible):differential((y-1)*(y-2)**2-x*(y-2)**2)
    def test_composition_receipts_replay(self):
        for e in self.report['composition_edges']:
            self.assertTrue(verify_composition(e,self.p[e['source']],self.p[e['target']]))
            bad=copy.deepcopy(e);bad['branch_value']='2'
            self.assertFalse(verify_composition(bad,self.p[e['source']],self.p[e['target']]))
    def test_composition_rejects_pole_and_wrong_branch(self):
        a,b=self.p['A000108'],self.p['A001006']
        self.assertIsNone(gf_transfer(a,b,1/x,1,0))
        self.assertIsNone(gf_transfer(a,b,x**2/(1-x)**2,1/(1-x),1))
        self.assertIsNone(gf_transfer(a,b,x,1,0))
    def test_family_sums(self):
        for f in self.report['family_normal_forms']:
            a=self.p[f['target']]['definitions'][0]
            self.assertEqual([family_term(f['finite_sum_parameters'],k) for k in range(40)],[terms_at(a,k) for k in range(40)])
    def test_degree_three_general_family(self):
        p={'id':'synthetic','sha256':'synthetic','status':'conditional_source_definition','algebraic':{'P':encode_poly(y-1-2*x*y-3*x**2*y**3),'a0':'1'}}
        f=family_normal_form(p);self.assertEqual(f['finite_sum_parameters'],{'a':'2','b':'3','d':3,'s':2})
        a,_=branch(decode_poly(p['algebraic']['P']),1,25)
        self.assertEqual(a,[family_term(f['finite_sum_parameters'],k) for k in range(25)])
    def test_general_polynomial_family(self):
        p={'id':'synthetic','sha256':'synthetic','status':'conditional_source_definition','algebraic':{'P':encode_poly(y-1-(x+x*x)*y-(x**2+2*x**3)*y**3),'a0':'1'}}
        f=family_normal_form(p);self.assertIsNotNone(f);self.assertNotIn('finite_sum_parameters',f)
    def test_joint_jacobsthal(self):
        e=self.report['joint_edges'][0];s=[self.p[v['id']] for v in e['sources']];t=self.p[e['target']]
        self.assertEqual([r['coefficients'][0]['num'] for r in e['sources']],[['1/3'],['-1/3']]);self.assertTrue(verify_joint(e,s,t))
        for p in s:self.assertIsNone(discover(p,t,1,0,3))
        bad=copy.deepcopy(e);bad['sources'][0]['coefficients'][0]['num']=['1/2'];self.assertFalse(verify_joint(bad,s,t))
    def test_joint_nontrivial_free_variables(self):
        a=self.p['A000079'];b={**a,'id':'synthetic_duplicate','sha256':'synthetic'}
        e=discover_joint([a,b],a,[[1,0],[1,0]],0);self.assertIsNotNone(e)
        self.assertTrue(verify_joint(e,[a,b],a));self.assertEqual(e['discovery']['nullity'],1)
    def test_automatic_spectral_cover(self):
        j=self.report['spectral_cover_jobs'][0];self.assertEqual(j['sources'],['A000079','A033999']);self.assertEqual(j['target'],'A001045')
        self.assertEqual(j['target_minimal_characteristic'],['-2','-1','1'])
    def test_minimal_cyclic_annihilator_discards_unused_mode(self):
        p=copy.deepcopy(self.p['A001045']);p['definitions'][0]['initial']=['1','2']
        self.assertEqual(minimal_constant_characteristic(p),(Q(-2),Q(1)))
        self.assertIsNone(minimal_constant_characteristic(self.p['A000108']))
    def test_repeated_modes_not_additive_under_lcm(self):
        from oeis_precursive_gate import encode_rat
        a=copy.deepcopy(self.p['A000079']);b={**a,'id':'duplicate','sha256':'duplicate'}
        p=copy.deepcopy(a);p['id']='synthetic_target';v=p['definitions'][0];v.update(order=2,initial=['0','2'],coefficients=[encode_rat(const(-4)),encode_rat(const(4))])
        self.assertEqual(minimal_constant_characteristic(p),(Q(4),Q(-4),Q(1)))
        self.assertEqual(spectral_cover_jobs({'a':a,'b':b,'t':p}),[])
    def test_joint_missing_spectrum(self):
        a=self.p['A000079'];b={**a,'id':'synthetic_duplicate','sha256':'synthetic'};t=self.p['A001045']
        self.assertIsNone(discover_joint([a,b],t,[[1,0],[1,0]],2))
    def test_full_blob_pin_rejects_excerpt(self):
        with self.assertRaisesRegex(ValueError,'blob mismatch'):load_records(FIX,json.loads((FIX/'full_source_plan.json').read_text()))
    def test_seed_and_domain_tamper(self):
        e=self.report['joint_edges'][0];ss=[self.p[v['id']] for v in e['sources']];t=self.p[e['target']]
        self.assertFalse(verify_joint({**e,'valid_from':1},ss,t));self.assertFalse(verify_joint({**e,'target_sha256':'fake'},ss,t))

if __name__=='__main__':unittest.main()
