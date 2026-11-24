"""Reproducible adversarial and exact-transfer tests for v0.8. Author: Komorebi P."""
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from fractions import Fraction as Q
from math import comb

from oeis_formula_database import connect,fingerprint
from sequence_transfer_miner import ensure_miner_schema
from sequence_oeis_proof_promotion import (
    apply_operator,direct_operator,maximum_source_index,sequence,
    promote,replay_all,replay_certificate,times_s_minus_one,
)
from sequence_oeis_symbolic_network import (
    prefix_sum,binomial,phase,shifted,formal_eval,
    transform,load_formulas,candidates,key,
)
from sequence_oeis_basis import shared_basis


class ExactOperatorTests(unittest.TestCase):
    def test_recursion_operator_vs_independent_direct(self):
        initial=[2,3]          # 2^n+1
        recurrence=[3,-2]      # (X-1)(X-2)
        cases=[('shift',{'shift':3}),('polyphase',{'modulus':5,'residue':3}),
               ('add_constant',{'constant':7}),('multiply_constant',{'constant':-5}),
               ('adjacent_difference',{}),('prefix_sum',{}),
               ('binomial_transform',{}),('inverse_binomial_transform',{})]
        for op,params in cases:
            with self.subTest(op=op):
                coeff,iv,_=apply_operator(recurrence,initial,op,params)
                D=len(coeff)+17
                source=sequence(initial,recurrence,maximum_source_index(op,params,D))
                result=sequence(iv,coeff,D)
                for n in range(D):
                    self.assertEqual(result[n],direct_operator(source,op,params,n))

    def test_prefix_powers_and_polynomials(self):
        expr={1:[Q(2),Q(1),Q(2)],2:[Q(3),Q(-1),Q(2)],-1:[Q(1),Q(4)]}
        output=prefix_sum(expr)
        for n in range(0,40):
            self.assertEqual(formal_eval(output,n),sum(formal_eval(expr,k) for k in range(n+1)))

    def test_constant_rate_antidifference(self):
        for r in (-4,-2,-1,1,2,3,7):
            for degree in (0,1,2,4):
                expr={r:[Q(j+1) for j in range(degree+1)]}
                result=prefix_sum(expr)
                for n in (0,1,2,5,11,31):
                    self.assertEqual(formal_eval(result,n),sum(formal_eval(expr,k) for k in range(n+1)),(r,degree,n))

    def test_binomial_and_inverse_non_singular(self):
        expr={2:[Q(1),Q(3),Q(2)],3:[Q(0),Q(-2),Q(1)],-2:[Q(2)]}
        for inverse in (False,True):
            out=binomial(expr,inverse=inverse)
            self.assertIsNotNone(out)
            for n in (0,1,2,4,6,12,25):
                expected=sum(comb(n,k)*formal_eval(expr,k)*((-1)**(n-k) if inverse else 1)
                             for k in range(n+1))
                self.assertEqual(formal_eval(out,n),expected)

    def test_singular_rates_not_misrepresented(self):
        self.assertIsNone(binomial({-1:[Q(1)]}))
        self.assertIsNone(binomial({1:[Q(1)]},inverse=True))

    def test_polyphase_symbolic(self):
        expr={-2:[Q(2),Q(3)],1:[Q(1),Q(0),Q(2)]}
        for modulus in (2,3,5,9):
            for residue in range(modulus):
                ans=phase(expr,modulus,residue)
                for n in (0,1,5,13):
                    self.assertEqual(formal_eval(ans,n),formal_eval(expr,modulus*n+residue))

    def test_basis_projection_example(self):
        rows={}
        definitions={
            'a':{1:[Q(1)]},
            'b':{1:[Q(0),Q(1)]},
            'c':{1:[Q(1),Q(1)]},
            'd':{2:[Q(1)]},
            'e':{2:[Q(1)],1:[Q(3),Q(2)]},
        }
        for sid,expr in definitions.items():rows[sid]={'oeis_id':sid,'expression':expr}
        axes,vectors,basis,proj=shared_basis(rows)
        self.assertEqual(len(basis),3)
        for sid,m in proj.items():
            for n in range(15):
                self.assertEqual(formal_eval(definitions[sid],n),
                                 sum(coef*formal_eval(definitions[base],n) for base,coef in m.items()))

    def test_sum_operator_extra_annihilator_degree(self):
        self.assertEqual(times_s_minus_one([2]),[3,-2])
        self.assertEqual(times_s_minus_one([3,-2]),[4,-5,2])


class CandidateSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.db=connect(Path(self.temp.name)/'tiny.sqlite3')
        ensure_miner_schema(self.db)
        self.seqids={}

    def tearDown(self):
        self.db.close();self.temp.cleanup()

    def add(self,sid,formula,offset,terms,formula_id=None):
        fid=formula_id or fingerprint(sid,formula)
        self.db.execute('''INSERT INTO sequences VALUES (?,?,?,?,?,?,?,?,?)''',
            (sid,sid,offset,None,json.dumps([str(x) for x in terms]),'',fingerprint(terms),
             f'https://oeis.org/{sid}','CC-BY-SA-4.0'))
        self.db.execute('''INSERT INTO formulas
           (formula_id,oeis_id,origin,field,ordinal,kind,expression,evaluator_json,
            source_url,license,proof_status,verification,checked_terms)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',
            (fid,sid,'oeis_normalized','N',0,'term_candidate','a(n)=test',json.dumps(formula),
             f'https://oeis.org/{sid}','CC-BY-SA-4.0','unassessed','finite_checked',len(terms)))
        self.seqids[sid]=fid
        return fid

    def candidate(self,source,target,op,parameters,checked=12):
        cid=fingerprint(source,target,op,parameters)[:24]
        self.db.execute('''INSERT INTO transfer_candidates VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
            (cid,target,json.dumps([source]),op,json.dumps(parameters,sort_keys=True),
             checked,10,max(0,checked-10),'finite candidate','finite_candidate','test',json.dumps({source:'a',target:'b'})))
        return cid

    def test_promote_replay_stale_reject(self):
        two={'op':'pow','base':2,'exp':{'op':'n'}}
        three={'op':'pow','base':3,'exp':{'op':'n'}}
        self.add('A000079',two,0,[2**n for n in range(18)])
        self.add('A000244',three,0,[3**n for n in range(18)])
        cid=self.candidate('A000079','A000244','binomial_transform',{},18)
        stats=promote(self.db)
        self.assertEqual(stats['formula_identities_certified'],1)
        self.assertEqual(replay_all(self.db)['replay_failed'],0)
        self.assertEqual(self.db.execute('SELECT status FROM transfer_candidates').fetchone()[0],'finite_candidate')
        self.db.execute("UPDATE sequences SET source_sha256='modified' WHERE oeis_id='A000079'")
        with self.assertRaisesRegex(ValueError,'changed|revoked'):
            replay_certificate(self.db,cid)

    def test_misleading_prefix_rejected(self):
        two={'op':'pow','base':2,'exp':{'op':'n'}}
        three={'op':'pow','base':3,'exp':{'op':'n'}}
        binomial10={'op':'binomial','n':{'op':'n'},'k':10}
        forged={'op':'add','args':[three,binomial10]}
        self.add('A000079',two,0,[2**n for n in range(10)])
        self.add('A000244',forged,0,[3**n for n in range(10)])
        self.candidate('A000079','A000244','binomial_transform',{},10)
        stats=promote(self.db)
        self.assertEqual(stats.get('formula_identities_certified',0),0)
        self.assertEqual(stats['all_index_equality_rejected'],1)

    def test_offsets_are_semantically_used(self):
        n={'op':'n'}
        minusone={'op':'sub','args':[n,1]}
        self.add('A000027',n,1,[1,2,3,4,5,6,7,8,9,10,11,12])
        self.add('A001477',minusone,1,list(range(12)))
        cid=self.candidate('A000027','A001477','add_constant',{'constant':-1},12)
        stats=promote(self.db)
        self.assertEqual(stats['formula_identities_certified'],1)
        self.assertEqual(replay_certificate(self.db,cid)['replayed'],True)

    def test_symbolic_exact_discovery_without_finite_miner(self):
        self.add('A000079',{'op':'pow','base':2,'exp':{'op':'n'}},0,[2**n for n in range(18)])
        self.add('A001018',{'op':'pow','base':8,'exp':{'op':'n'}},0,[8**n for n in range(18)])
        rec,conf=load_formulas(self.db)
        self.assertEqual(conf,[])
        spec=rec['A000079']['expression']
        matches=[(op,p) for op,p,t in candidates(spec,max_modulus=5)
                 if key(t)==key(rec['A001018']['expression'])]
        self.assertIn(('polyphase',{'modulus':3,'residue':0}),matches)

if __name__=='__main__':unittest.main()
