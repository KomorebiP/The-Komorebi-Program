"""Tests for finite candidate discovery, rational-ratio fitting and provenance."""
import json
import sqlite3
import tempfile
import unittest
from fractions import Fraction as Q
from pathlib import Path

from oeis_formula_database import connect, ingest_curated
from sequence_transfer_graph import create_graph, path_query
from sequence_transfer_miner import (
    infer_ratio, mine_transfers, mine_rational_ratios, candidates,
    materialize_candidates, export_candidates, _solve_unique,
)

BASE=Path(__file__).resolve().parents[1]
SEED=BASE/'research/oeis-formulas/seeds.json'
MORE=BASE/'research/oeis-formulas/seeds-extended.json'

class TransferMinerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        cls.db=connect(Path(cls.tmp.name)/'specimen.db')
        ingest_curated(cls.db,SEED)
        ingest_curated(cls.db,MORE)
        cls.transfers=mine_transfers(cls.db)
        cls.ratios=mine_rational_ratios(cls.db)

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        cls.tmp.cleanup()

    def test_discovery_count_and_provenance(self):
        self.assertGreaterEqual(self.transfers['candidate_edges'],40)
        self.assertGreaterEqual(self.ratios['candidates'],14)
        self.assertEqual(self.db.execute('''SELECT COUNT(*) FROM transfer_candidates
                            WHERE holdout_terms<=0''').fetchone()[0],0)
        self.assertEqual(self.db.execute('''SELECT COUNT(*) FROM transfer_candidates
                            WHERE status!='finite_candidate' ''').fetchone()[0],0)

    def test_binomial_transform_discoveries_are_candidate_only(self):
        entries=candidates(self.db,operator='binomial_transform',limit=100)
        found={(r['inputs'][0],r['output']) for r in entries}
        self.assertTrue({('A000012','A000079'),('A000079','A000244'),
                         ('A000244','A000302'),('A000166','A000142')} <= found)
        self.assertTrue(all(r['status']=='finite_candidate' for r in entries))

    def test_square_differences_preserve_real_offsets(self):
        entries=candidates(self.db,oeis_id='A005408',operator='adjacent_difference')
        row=next(r for r in entries if r['inputs']==['A000290'])
        self.assertIn('A005408[0+j]',row['statement'])
        self.assertIn('A000290[0+j+1]',row['statement'])
        a=candidates(self.db,oeis_id='A000027',operator='adjacent_difference')
        self.assertTrue(any(r['statement'].startswith('A000027[1+j]') for r in a))

    def test_rational_ratio_catalan_and_central_binomial(self):
        for sid,expect in [('A000108',['4','1/2','2']),
                           ('A000984',['4','1/2','1'])]:
            row=self.db.execute('SELECT pochhammer_json,holdout_ratios,status FROM rational_ratio_candidates WHERE oeis_id=?',(sid,)).fetchone()
            self.assertIsNotNone(row)
            f=json.loads(row[0])
            self.assertEqual([f['multiplier'],f['upper'][0],f['lower'][0]],expect)
            self.assertGreaterEqual(row[1],4)
            self.assertEqual(row[2],'finite_candidate')

    def test_no_spurious_fibonacci_hypergeometric(self):
        self.assertIsNone(self.db.execute('SELECT oeis_id FROM rational_ratio_candidates WHERE oeis_id=?',('A000045',)).fetchone())
        fib=[0,1,1,2,3,5,8,13,21,34,55,89,144,233,377,610,987]
        self.assertIsNone(infer_ratio(fib,0))

    def test_rational_solver_singular_and_inconsistent(self):
        self.assertIsNone(_solve_unique([[1,1],[2,2]],[2,4]))
        self.assertIsNone(_solve_unique([[1],[1]],[1,2]))
        self.assertEqual(_solve_unique([[1,0],[0,1]],[Q(1,2),Q(3,4)]),[Q(1,2),Q(3,4)])

    def test_false_late_term_rejected(self):
        factorial=[1]
        for n in range(1,30):factorial.append(factorial[-1]*n)
        factorial[-1]+=1
        self.assertIsNone(infer_ratio(factorial,0))

    def test_proof_paths_exclude_candidate_edges(self):
        create_graph(self.db)
        materialize_candidates(self.db)
        row=self.db.execute('''SELECT status FROM transfer_edges
                       WHERE operator='candidate_binomial_transform'
                         AND source_node='A000012' AND target_node='A000079' ''').fetchone()
        self.assertEqual(row,('finite_candidate',))
        self.assertEqual(path_query(self.db,'A000012','A000079')[0]['status'],'algebraic_identity')
        # A prefix-sum candidate has not been promoted to a proved route.
        self.assertIsNone(path_query(self.db,'A000012','A000027'))
        row=self.db.execute('SELECT COUNT(*) FROM transfer_nodes WHERE type=?',('candidate_hyperedge',)).fetchone()
        self.assertGreater(row[0],0)

    def test_stale_candidate_not_materialized(self):
        with tempfile.TemporaryDirectory() as td:
            db=connect(Path(td)/'stale.sqlite3')
            try:
                ingest_curated(db,SEED)
                mine_transfers(db)
                mine_rational_ratios(db)
                create_graph(db)  # Build existing proof edges before mutation.
                # Tamper source without regenerating the candidate relation.
                old=db.execute('SELECT terms_json FROM sequences WHERE oeis_id=?',('A000079',)).fetchone()[0]
                values=json.loads(old); values[5]='1000000001'
                db.execute('UPDATE sequences SET terms_json=? WHERE oeis_id=?', (json.dumps(values),'A000079'))
                materialize_candidates(db)
                hits=db.execute('''SELECT COUNT(*) FROM transfer_edges WHERE status='finite_candidate'
                       AND (source_node='A000079' OR target_node='A000079')''').fetchone()[0]
                self.assertEqual(hits,0)
                self.assertIsNone(db.execute('SELECT 1 FROM transfer_nodes WHERE node_id=?',('RATIO:A000079',)).fetchone())
            finally:db.close()

    def test_export_reproducibility(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'c.jsonl'
            r=export_candidates(self.db,path)
            self.assertEqual(r['records']['transfer'],self.transfers['candidate_edges'])
            self.assertEqual(r['records']['ratio'],self.ratios['candidates'])
            assert path.exists()
            for line in path.read_text().splitlines():
                item=json.loads(line)
                self.assertEqual(item['status'],'finite_candidate')

if __name__=='__main__':unittest.main()

class LocalKomorebiGraphTest(unittest.TestCase):
    def test_local_formulas_are_separate_and_crosswalks_not_proofs(self):
        from oeis_formula_database import ingest_komorebi
        from sequence_transfer_graph import create_graph,path_query
        with tempfile.TemporaryDirectory() as td:
            base=Path(td)
            db=connect(base/'local.db')
            try:
                ingest_curated(db,SEED)
                fixture={'entries':[{'id':'KFOR-TEST-1','title':'example',
                    'offset':2,'terms':['1','2','3','4'],
                    'source':'https://example.org/source',
                    'formulas':[{'kind':'finite_sum','expression':'a(n)=n-1',
                                  'source':'https://example.org/source'}],
                    'matches':[{'id':'A000045','matched_terms':4,'position':0}],
                    'oeis':'A000032'}]}
                file=base/'entries.json';file.write_text(json.dumps(fixture))
                ingest_komorebi(db,file)
                result=create_graph(db)
                self.assertGreaterEqual(result['statuses']['crosswalk_reference'],2)
                self.assertEqual(db.execute('SELECT type FROM transfer_nodes WHERE node_id=?',('KFOR-TEST-1',)).fetchone(),('komorebi_sequence',))
                self.assertEqual(db.execute('''SELECT count(*) FROM transfer_edges WHERE operator='formula_representation' AND target_node='KFOR-TEST-1' ''').fetchone()[0],1)
                self.assertIsNone(path_query(db,'KFOR-TEST-1','A000045'))
            finally:db.close()
