"""Proof-kernel and transfer-graph tests, Python standard library only.

Author: Komorebi P.
"""
from fractions import Fraction as Q
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parent))
from sequence_transfer_graph import (
    create_graph, euler_via_fibonacci, exact_series_quotient, fib_resolvent,
    graph_stats, import_xrefs, path_query, sqrt_one, exact_series_mul,
)
from oeis_formula_database import connect, ingest_curated

ROOT=Path(__file__).resolve().parents[1]
SEEDS=ROOT/'research/oeis-formulas/seeds.json'
EXTENDED=ROOT/'research/oeis-formulas/seeds-extended.json'

class TransferGraphTests(unittest.TestCase):
    def test_generic_fibonacci_resolvent_is_exact(self):
        cases=[
            ([1],[1],14),
            ([1,3],[1,-1,-1],14),
            ([2,0,1],[1,Q(1,2),0,Q(-2,3)],14),
            ([0,1,1],[1,0,0,Q(7,4),Q(-1,3)],14),
            ([1,0,0,2],[1,-4,6,-4,1],14),
        ]
        for n,d,length in cases:
            with self.subTest(n=n,d=d):
                shifted,phi=fib_resolvent(n,d,length)
                expected=exact_series_quotient(n,d,length)
                self.assertEqual(shifted,expected)
                # Independently check the substitution equation.
                square=exact_series_mul(phi,phi,length)
                for j in range(length):
                    self.assertEqual(
                        (Q(1) if j==0 else Q(0))-phi[j]-square[j],
                        Q(d[j]) if j<len(d) else 0)

    def test_euler_fibonacci_bridge(self):
        e,phi=euler_via_fibonacci(18)
        self.assertEqual([int(x) for x in e],
            [1,1,1,2,5,16,61,272,1385,7936,50521,353792,
             2702765,22368256,199360981,1903757312,19391512145,
             209865342976])
        self.assertEqual(phi[0],0)
        self.assertEqual(phi[1],0)
        self.assertEqual(phi[2],Q(1,2))

    def test_reject_wrong_denominator(self):
        with self.assertRaises(ValueError):fib_resolvent([1],[2,1],8)
        with self.assertRaises(ValueError):sqrt_one([2,0,0],3)

    def test_graph_build_and_path(self):
        with tempfile.TemporaryDirectory() as directory:
            db=connect(Path(directory)/'test.sqlite3')
            try:
                ingest_curated(db,SEEDS)
                ingest_curated(db,EXTENDED)
                result=create_graph(db)
                self.assertEqual(result['statuses']['algebraic_identity'],17)
                self.assertGreaterEqual(result['nodes'],120)
                path=path_query(db,'A000045','A000111')
                self.assertEqual(len(path),1)
                self.assertEqual(path[0]['operator'],'fibonacci_resolvent')
                self.assertIsNone(path_query(db,'A000111','A000045'))
                self.assertEqual(path_query(db,'A000111','A000364')[0]['operator'],
                    'even_subsequence')
                self.assertEqual(len(path_query(db,'A000045','A000364')),2)
                self.assertEqual(graph_stats(db)['statuses']['recorded_representation'],61)
            finally:db.close()

    def test_crossrefs_are_unverified_and_persist(self):
        with tempfile.TemporaryDirectory() as directory:
            base=Path(directory)
            db=connect(base/'test.sqlite3')
            try:
                ingest_curated(db,SEEDS)
                ingest_curated(db,EXTENDED)
                create_graph(db)
                raw='''%I A000045 M0000
%Y A000045 Cf. A000032, A000111, A222222.
%Y A000045 Also A000032.
'''
                path=base/'A000045.seq';path.write_text(raw,encoding='utf-8')
                result=import_xrefs(db,path)
                self.assertEqual(result['staged'],4)
                self.assertEqual(result['links_to_imported_nodes'],3)
                evidence=db.execute('''SELECT status FROM transfer_edges
                  WHERE operator='oeis_cross_reference' AND source_node='A000045'
                  AND target_node='A000032' ''').fetchone()
                self.assertEqual(evidence[0],'reference_only')
                create_graph(db)
                self.assertEqual(db.execute('''SELECT count(*) FROM transfer_edges
                   WHERE operator='oeis_cross_reference' ''').fetchone()[0],2)
                # An updated OEIS entry must replace (not accumulate) the refs.
                path.write_text('''%I A000045 M0000
%Y A000045 Cf. A000111 only.
''',encoding='utf-8')
                result=import_xrefs(db,path)
                self.assertEqual(result['staged'],1)
                # Rebuild removes old materialized refs, preserving raw archive.
                create_graph(db)
                self.assertEqual(db.execute('''SELECT count(*) FROM transfer_edges
                   WHERE operator='oeis_cross_reference' ''').fetchone()[0],1)
            finally:db.close()

if __name__=='__main__':
    unittest.main()
