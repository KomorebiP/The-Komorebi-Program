"""Controls for algebraic certificates, offsets and no false OEIS proofs."""
import json
import sqlite3
import tempfile
import unittest
from fractions import Fraction as Q
from pathlib import Path

from oeis_formula_database import connect, ingest_curated
from sequence_transfer_miner import mine_rational_ratios
from sequence_ratio_certificates import certify as certify_ratio,derive_ratio,affine,ratio_polynomials
from sequence_kernel_transfers import term_form,discover as discover_kernel
from sequence_recurrence_transfers import (
    ogf_from_recurrence, rational_ogf_filter, same_kernel_projection,
    certify as certify_recurrence,load_filter,pmul,
)
from sequence_transfer_graph import create_graph,path_query

BASE=Path(__file__).resolve().parents[1]


class SymbolicProofTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work=tempfile.TemporaryDirectory()
        cls.db=connect(Path(cls.work.name)/'symbolic.db')
        for file in ('seeds.json','seeds-extended.json'):
            ingest_curated(cls.db,BASE/'research/oeis-formulas'/file)
        mine_rational_ratios(cls.db)
        cls.ratio=certify_ratio(cls.db)
        cls.kernel=discover_kernel(cls.db)
        cls.recurrence=certify_recurrence(cls.db)

    @classmethod
    def tearDownClass(cls):
        cls.db.close();cls.work.cleanup()

    def test_symbolic_certifications_not_equated_to_oeis_theorems(self):
        self.assertEqual(self.ratio['certified_formula_identities'],21)
        self.assertEqual(self.ratio['fitted_ratios_confirmed'],17)
        self.assertEqual(self.db.execute('SELECT count(*) FROM certified_formula_ratios').fetchone()[0],21)
        self.assertEqual(self.db.execute("SELECT count(*) FROM certified_formula_ratios WHERE scope!='symbolic_identity_of_curated_evaluator'").fetchone()[0],0)
        self.assertEqual(self.db.execute("SELECT count(*) FROM formulas WHERE verification='finite_checked'").fetchone()[0],61)

    def test_catalan_exact_ratio_and_pochhammer(self):
        row=self.db.execute("SELECT pochhammer_json,matches_inferred_ratio FROM certified_formula_ratios WHERE oeis_id='A000108'").fetchone()
        self.assertIsNotNone(row)
        data=json.loads(row[0])
        self.assertEqual((data['multiplier'],data['upper'],data['lower']),('4',['1/2'],['2']))
        self.assertEqual(row[1],1)

    def test_non_hypergeometric_forms_explicitly_declined(self):
        rows=[r[0] for r in self.db.execute('SELECT oeis_id FROM certified_formula_ratios')]
        for sid in ('A000045','A000111','A000041','A000040'):
            self.assertNotIn(sid,rows)
        self.assertIsNone(derive_ratio({'op':'pow','base':{'op':'n'},'exp':{'op':'n'}},start=1))
        self.assertIsNone(derive_ratio({'op':'factorial','arg':{'op':'sub','args':[1,{'op':'n'}]}},start=1))
        self.assertIsNone(derive_ratio({'op':'sum','from':0,'to':{'op':'n'},'body':1},start=0))

    def test_identity_of_binomial_formula_not_inferred_by_point_matching(self):
        spec={'op':'binomial','n':{'op':'mul','args':[2,{'op':'n'}]},'k':{'op':'n'}}
        r=derive_ratio(spec,0)
        self.assertEqual(r.ratio_at(0),2)
        self.assertEqual(r.ratio_at(10),Q(2*(2*10+1),11))
        # Proof works by identities for affine factorials, no numeric fitting.
        num,den=ratio_polynomials(r)
        self.assertTrue(num and den)

    def test_kernel_normalization_proves_catalan_quotient(self):
        self.assertEqual(self.kernel['symbolic_transfers'],14)
        row=self.db.execute('''SELECT quotient_json FROM certified_formula_transfers
            WHERE source_oeis_id='A000984' AND target_oeis_id='A000108' ''').fetchone()
        self.assertIsNotNone(row)
        q=json.loads(row[0])
        self.assertEqual(q['scalar'],'1')
        self.assertEqual(q['factors'],[{'a':1,'b':1,'power':-1}])

    def test_rational_ogf_and_laurent_transfer(self):
        self.assertEqual(self.recurrence['certified_ogf_formulas'],8)
        self.assertEqual(self.recurrence['certified_shared_state_projections'],4)
        pell=load_filter(self.db,'A000045','A000129')
        self.assertEqual(pell['shift'],0)
        self.assertEqual(pell['numerator'],['1','-1','-1'])
        self.assertEqual(pell['denominator'],['1','-2','-1'])
        lucas=load_filter(self.db,'A000045','A000032')
        self.assertEqual(lucas['shift'],-1)
        self.assertEqual(lucas['numerator'],['2','-1'])
        self.assertEqual(lucas['denominator'],['1'])

    def test_shared_recurrence_shift_operator_is_globally_proved(self):
        pairs={(a,b):json.loads(c) for a,b,c in self.db.execute(
            'SELECT source_oeis_id,target_oeis_id,coefficients_json FROM certified_recurrence_projections')}
        self.assertEqual(pairs['A000045','A000032'],['-1','2'])
        self.assertEqual(pairs['A000129','A001333'],['-1','1'])

    def test_composition_of_filters_is_exact_rational_identity(self):
        ab=load_filter(self.db,'A000045','A000129')
        bc=load_filter(self.db,'A000129','A001045')
        ac=load_filter(self.db,'A000045','A001045')
        self.assertEqual(ab['shift']+bc['shift'],ac['shift'])
        left_num=pmul([Q(x) for x in ab['numerator']],[Q(x) for x in bc['numerator']])
        left_den=pmul([Q(x) for x in ab['denominator']],[Q(x) for x in bc['denominator']])
        target_num=[Q(x) for x in ac['numerator']]
        target_den=[Q(x) for x in ac['denominator']]
        self.assertEqual(pmul(left_num,target_den),pmul(left_den,target_num))

    def test_proof_graph_keeps_symbolic_links_out_of_oeis_proof_paths(self):
        stats=create_graph(self.db)
        self.assertGreaterEqual(stats['statuses']['formula_algebra'],39)
        count=self.db.execute("SELECT count(*) FROM transfer_edges WHERE status='algebraic_identity'").fetchone()[0]
        self.assertEqual(count,17)
        # The exact rational filter F->Pell is available by query, but must not
        # be promoted into an OEIS sequence proof edge without independent
        # review of OEIS identifications and transfer semantics.
        self.assertIsNone(path_query(self.db,'A000045','A000129'))
        self.assertIsNone(path_query(self.db,'A000984','A000290'))


if __name__=='__main__':unittest.main()
