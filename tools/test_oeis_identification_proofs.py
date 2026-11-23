"""Adversarial exact OEIS identification proof gate controls.

Author: Komorebi P.
"""
from __future__ import annotations
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from fractions import Fraction as Q

from oeis_identification_proofs import (parse_record, profile_record, gf_parse,
  recurrence_parse, poly_shift, series, audit, transfer, verify_transfer_cert,
  build_overlay, verify_report)

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'fixtures/oeis_identification'

class ParsingAndFormalProofTests(unittest.TestCase):
    def record(self,ID):return parse_record(SRC/'seq'/ID[:4]/(ID+'.seq'),SRC)
    def profile(self,ID):return profile_record(self.record(ID))

    def test_offset_and_source_provenance(self):
        a=self.record('A000045')
        self.assertEqual(a.offset,0)
        self.assertEqual(a.terms[:7],(0,1,1,2,3,5,8))
        self.assertEqual(len(a.source_sha256),64)
        self.assertEqual(a.formulas[0][0],4)

    def test_GF_to_recurrence_and_initial_identification(self):
        p=self.profile('A000045')
        self.assertEqual(p['status'],'oeis_name_definition_equivalence_proved')
        self.assertEqual(p['definitions'][0]['coefficients'],['1','1'])
        self.assertEqual(p['definitions'][0]['initial'],['0','1'])
        self.assertEqual(p['definitions'][0]['matched_source_terms'],18)
        self.assertEqual(p['definitions'][0]['recurrence_valid_from'],2)
        self.assertEqual(p['definitions'][0]['name_definition_checked']['type'],'name_recurrence')
        self.assertNotIn('unconditional', p['status'])

    def test_polynomial_and_GF_same_definition(self):
        p=self.profile('A000290')
        self.assertEqual(p['status'],'oeis_name_definition_equivalence_proved')
        self.assertEqual(p['definitions'][0]['coefficients'],['3','-3','1'])
        self.assertEqual(p['definitions'][0]['initial'],['0','1','4'])
        self.assertEqual(p['definitions'][0]['name_definition_checked']['type'],'name_polynomial')

    def test_integer_recursion_parsing(self):
        self.assertEqual(recurrence_parse('a(n+2)= a(n+1) + a(n).'),([Q(1),Q(1)],2))
        self.assertEqual(recurrence_parse('a(n)= 2*a(n-1) - a(n-2), n>=4.'),([Q(2),Q(-1)],4))
        self.assertEqual(recurrence_parse('a(n)=(a(n-1)+a(n-2))/2.'),([Q(1,2),Q(1,2)],2))
        self.assertIsNone(recurrence_parse('a(n)=a(n-1)*a(n-2).'))
        self.assertIsNone(recurrence_parse('a(n)=a(n-1)+1, for odd n.'))
        self.assertIsNone(recurrence_parse('a(n) = __import__("os").system("x").'))

    def test_finite_recurrence_claim_not_a_proof(self):
        p=self.profile('A987003')
        self.assertEqual(p['status'],'finite_consistency_only')
        self.assertEqual(p['definitions'],[])

    def test_reject_inconsistent_terms_and_recurrence(self):
        p=self.profile('A987002')
        self.assertEqual(p['status'],'quarantined_inconsistent_source_premises')
        self.assertTrue(any('disagrees_with_reported_terms' in q['quarantine'] for q in p['quarantined']))

    def test_nonzero_offset_never_silently_rebased(self):
        p=self.profile('A987001')
        self.assertEqual(p['status'],'unsupported_nonzero_or_missing_offset')

    def test_conflicting_generating_functions_are_not_admitted(self):
        p=self.profile('A987004')
        self.assertEqual(p['status'],'quarantined_inconsistent_source_premises')
        self.assertEqual(len(p['quarantined']),1)
        self.assertEqual(p['definitions'],[])

    def test_eventual_recurrence_guarded_by_domain(self):
        p=self.profile('A987005')
        self.assertEqual(p['status'],'source_premise_exactly_rederived')
        d=p['definitions'][0]
        self.assertEqual(d['base_index'],6)
        self.assertEqual(d['recurrence_valid_from'],7)

    def test_ogf_not_e_gf(self):
        self.assertIsNone(gf_parse('E.g.f.: x/(1-x-x^2).'))
        self.assertIsNone(gf_parse('G.f.: 1/(1-x^100).'))
        self.assertIsNone(gf_parse('G.f.: __import__("os").system("anything")'))

    def test_finite_difference_polynomial(self):
        self.assertEqual(poly_shift((Q(1),Q(2),Q(1)),-1),(Q(0),Q(0),Q(1)))

    def test_verified_conditional_transfers_and_tamper_rejection(self):
        data=audit(SRC)
        ov=data['overlay']
        self.assertEqual(ov['conditional_edge_count'],4)
        self.assertEqual(data['summary']['unconditional_oeis_identifications'],0)
        edges={(x['source'],x['target']):x for x in ov['edges']}
        e=edges['A000045','A000032']
        self.assertEqual(e['shift_coefficients'],['-1','2'])
        profiles={x['oeis_id']:x for x in data['profiles']}
        self.assertTrue(verify_transfer_cert(e,profiles))
        self.assertFalse(verify_transfer_cert({**e,'shift_coefficients':['1','0']},profiles))
        self.assertFalse(verify_transfer_cert({**e,'source_sha256':'0'*64},profiles))

    def test_untrusted_mixed_ids_rejected(self):
        with TemporaryDirectory() as d:
            p=Path(d)/'A123456.seq'
            p.write_text('%I A123456\n%O A654321 0,1\n')
            with self.assertRaises(ValueError):parse_record(p)

    def test_report_replay_and_fail_closed_tamper(self):
        with TemporaryDirectory() as tmp:
            target=Path(tmp)
            r=audit(SRC)
            for name, data in [('identification_report.json',r['summary']),
              ('sequence_profiles.json',r['profiles']),
              ('conditional_transfer_overlay.json',r['overlay']),
              ('quarantine.json',r['quarantine'])]:
                (target/name).write_text(json.dumps(data))
            out=verify_report(SRC,target)
            self.assertEqual(out['conditional_edges_reproved'],4)
            p=target/'conditional_transfer_overlay.json'
            d=json.loads(p.read_text())
            d['edges'][0]['shift_coefficients']=['1','1']
            p.write_text(json.dumps(d))
            with self.assertRaisesRegex(ValueError,'proof replay'):
                verify_report(SRC,target)

    def test_name_conflict_must_quarantine_entire_record(self):
        for id in ('A987006','A987007'):
            p=self.profile(id)
            self.assertEqual(p['status'],'quarantined_name_definition_conflict')
            self.assertEqual(p['definitions'],[])
            self.assertTrue(p['quarantined'])

    def test_offset_one_polynomial_is_not_rebased(self):
        p=self.profile('A987008')
        self.assertEqual(p['status'],'oeis_name_definition_equivalence_proved')
        d=p['definitions'][0]
        self.assertEqual(d['base_index'],1)
        self.assertEqual(d['initial'],['1','4','9'])
        self.assertEqual(d['recurrence_valid_from'],4)

    def test_full_named_lucas_definition_is_checked(self):
        p=self.profile('A000032')
        self.assertEqual(p['status'],'oeis_name_definition_equivalence_proved')
        self.assertEqual(p['definitions'][0]['name_definition_checked']['type'],'name_recurrence')

    def test_externally_pinned_source_selection_not_report_controlled(self):
        chosen={'A000045','A000032'}
        with TemporaryDirectory() as folder:
            dest=Path(folder)
            r=audit(SRC,ids=chosen)
            for name, obj in [('identification_report.json',r['summary']),
              ('sequence_profiles.json',r['profiles']),
              ('conditional_transfer_overlay.json',r['overlay']),
              ('quarantine.json',r['quarantine'])]:
                (dest/name).write_text(json.dumps(obj))
            self.assertEqual(verify_report(SRC,dest,ids=chosen)['pinned_source_records_rechecked'],2)
            with self.assertRaisesRegex(ValueError,'proof replay'):
                verify_report(SRC,dest)

    def test_empty_and_excess_budget(self):
        with self.assertRaises(ValueError):audit(Path('/no/oeis/here'))
        with self.assertRaises(ValueError):audit(SRC,max_pairs=1)

if __name__=='__main__':unittest.main()
