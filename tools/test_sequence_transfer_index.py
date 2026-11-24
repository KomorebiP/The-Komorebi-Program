"""Independent regression controls for SQLite streaming prefix matching."""
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from oeis_formula_database import connect, ingest_curated
from sequence_transfer_miner import mine_transfers
from sequence_transfer_index import (
    SINGLE_OPERATORS, build_prefix_index, mine_indexed,
)

ROOT=Path(__file__).resolve().parents[1]
SEEDS=[ROOT/'research/oeis-formulas'/name for name in ('seeds.json','seeds-extended.json')]


class StreamingIndexTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory()
        self.db=connect(Path(self.t.name)/'collection.sqlite3')
        for path in SEEDS:ingest_curated(self.db,path)

    def tearDown(self):
        self.db.close();self.t.cleanup()

    def subset(self):
        rows=self.db.execute('SELECT candidate_id,output_id,inputs_json,operator,parameters_json,checked_terms FROM transfer_candidates')
        return {(x[0],x[1],x[2],x[3],x[4],x[5]) for x in rows if x[3] in SINGLE_OPERATORS}

    def test_identical_to_original_56_sequence_miner(self):
        mine_transfers(self.db)
        baseline=self.subset()
        self.assertEqual(len(baseline),27)
        result=mine_indexed(self.db,reset_unary=True)
        self.assertEqual(result['exact_prefix_hits'],27)
        self.assertEqual(self.subset(),baseline)
        self.assertEqual(result['stale_index_hits'],0)
        self.assertEqual(self.db.execute('SELECT count(*) FROM transfer_candidates').fetchone()[0],52)

    def test_index_idempotence_and_hash_invalidation(self):
        counts=build_prefix_index(self.db)
        self.assertEqual(counts['stored'],56)
        self.assertEqual(build_prefix_index(self.db)['unchanged'],56)
        row=self.db.execute("SELECT terms_json FROM sequences WHERE oeis_id='A000079'").fetchone()
        terms=json.loads(row[0]);terms[-1]='999999999'
        self.db.execute("UPDATE sequences SET terms_json=? WHERE oeis_id='A000079'",(json.dumps(terms),))
        # Old index's full-row digest is stale even when the first ten terms
        # continue to match: no inference can use this stale target witness.
        hit=mine_indexed(self.db,auto_index=False)
        self.assertGreater(hit['stale_index_hits'],0)
        self.assertEqual(build_prefix_index(self.db)['updated'],1)
        self.assertEqual(mine_indexed(self.db,reset_unary=True,auto_index=False)['stale_index_hits'],0)

    def test_sharding_and_no_false_proof_edges(self):
        build_prefix_index(self.db)
        left=mine_indexed(self.db,through_id='A000300',reset_unary=True,auto_index=False)
        right=mine_indexed(self.db,from_id='A000301',auto_index=False)
        count=self.db.execute('SELECT count(*) FROM transfer_candidates').fetchone()[0]
        self.assertEqual(left['exact_prefix_hits']+right['exact_prefix_hits'],count)
        self.assertEqual(self.db.execute("SELECT count(*) FROM transfer_candidates WHERE status!='finite_candidate'").fetchone()[0],0)
        second=mine_indexed(self.db,auto_index=False)
        self.assertEqual(second['exact_prefix_hits'],count)
        self.assertEqual(self.db.execute('SELECT count(*) FROM transfer_candidates').fetchone()[0],count)

    def test_anomalous_shared_prefix_is_not_a_relation(self):
        # Emulates 10 agreeing terms followed by one incorrect coefficient.
        a=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16']
        b=[str(int(x)+1) for x in a]
        b[13]='123456'
        for sid,terms in (('A999980',a),('A999981',b)):
            self.db.execute('INSERT INTO sequences VALUES (?,?,?,?,?,?,?,?,?)',
                            (sid,sid,0,None,json.dumps(terms),'','fixture','https://oeis.org/'+sid,'CC-BY-SA-4.0'))
        mine_indexed(self.db,reset_unary=True)
        row=self.db.execute("SELECT count(*) FROM transfer_candidates WHERE output_id='A999981' AND operator='add_constant'").fetchone()[0]
        self.assertEqual(row,0)

    def test_large_collection_index_is_sql_backed(self):
        # 600 distinct synthetic records stress the index without any bulk
        # read of sequence terms. This is an implementation test, not OEIS data.
        for i in range(600):
            sequence=[str((i+7)*(n+1)**2+3*n**3) for n in range(22)]
            self.db.execute('INSERT INTO sequences VALUES (?,?,?,?,?,?,?,?,?)',
                            (f'A9{i:05d}',f'Synthetic {i}',0,None,json.dumps(sequence),
                             '','fixture','fixture://synthetic','CC-BY-SA-4.0'))
        result=build_prefix_index(self.db)
        self.assertEqual(result['stored'],656)
        self.assertGreaterEqual(result['indexed'],600)  # Some OEIS seed excerpts are constant/degenerate
        # In bounded range, only synthetic source rows are visited, while all
        # 656 records remain searchable as target candidates.
        result=mine_indexed(self.db,from_id='A900000',through_id='A900099',auto_index=False)
        self.assertEqual(result['sources_scanned'],100)


if __name__=='__main__':unittest.main()
