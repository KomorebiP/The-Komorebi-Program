"""Tests for exact-source receipts, lexical semantics, offsets and stale raw text."""
from __future__ import annotations
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from oeis_formula_database import connect,parse_seq,store_seq
from sequence_formula_retrieval import classify,index_formulas,search


FIXTURE='''%I A300001
%S A300001 1,2,3,4,5,6,7,8,9,10,11,12,
%N A300001 Synthetic test sequence (not an actual OEIS claim)
%O A300001 1,2
%F A300001 a(n) = binomial(n,1). Compare A000027.
%F A300001 g.f. = x/(1-x)^2; Pochhammer(n,1).
%p A300001 program_to_preserve_not_execute()
'''


class FormulaRetrievalTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.db=connect(Path(self.tmp.name)/'unit.sqlite3')
        store_seq(self.db,parse_seq(FIXTURE),FIXTURE)
        self.db.commit()

    def tearDown(self):
        self.db.close();self.tmp.cleanup()

    def test_index_search_and_source_boundaries(self):
        result=index_formulas(self.db)
        self.assertEqual(result['indexed'],3)
        self.assertEqual(result['unproved_lexical_leads'],1)
        self.assertEqual(index_formulas(self.db)['unchanged'],3)
        answers=search(self.db,'binomial')
        self.assertEqual(len(answers),1)
        self.assertEqual(answers[0]['oeis_id'],'A300001')
        self.assertEqual(answers[0]['verification'],'unreviewed')
        self.assertIn('binomial',answers[0]['tags'])
        self.assertEqual(search(self.db,'program_to_preserve_not_execute')[0]['origin'],'oeis_program')
        self.assertEqual(search(self.db,'binomial',verified_only=True),[])
        self.assertEqual(search(self.db,'binomial',required_tag='pochhammer'),[])

    def test_delete_update_and_rowid_reuse(self):
        index_formulas(self.db)
        self.db.execute("DELETE FROM formulas WHERE origin='oeis_program'")
        self.assertEqual(index_formulas(self.db)['removed'],1)
        self.assertEqual(search(self.db,'program_to_preserve_not_execute'),[])
        self.db.execute("UPDATE formulas SET expression='a(n)=binomial(n,2)' WHERE expression LIKE '%binomial(n,1)%'")
        updated=index_formulas(self.db)
        self.assertEqual(updated['updated'],1)
        self.assertEqual(len(search(self.db,'binomial')),1)
        changed=FIXTURE.replace('binomial(n,1)','binomial(n,2)')
        store_seq(self.db,parse_seq(changed),changed)
        refreshed=index_formulas(self.db)
        self.assertGreaterEqual(refreshed['inserted']+refreshed['updated'],1)
        self.assertEqual(len(search(self.db,'binomial')),1)

    def test_lexical_only_and_sanitized_results(self):
        self.assertIn('multisection',classify('polyphase residue-class transform'))
        self.assertIn('binomial',classify('a(n)=binomial(n,2)'))
        with self.assertRaises(ValueError):search(self.db,'anything',required_tag='invented')
        with self.assertRaises(ValueError):search(self.db,'anything',limit=101)

    def test_fts_scales_to_many_raw_records(self):
        row=[]
        for k in range(10000):
            fid=f'fixture-{k:06d}'
            expr=f'a(n) = binomial(n,{k%8}); compare A000045; source note {k}'
            row.append((fid,'A300001','oeis_formula','F',k,'term_candidate',expr,
                'https://oeis.org/A300001','CC-BY-SA-4.0','unassessed','unreviewed'))
        self.db.executemany('''INSERT INTO formulas
          (formula_id,oeis_id,origin,field,ordinal,kind,expression,source_url,license,proof_status,verification)
          VALUES (?,?,?,?,?,?,?,?,?,?,?)''',row)
        report=index_formulas(self.db,batch_size=300)
        self.assertEqual(report['indexed'],10003)
        self.assertEqual(report['unproved_lexical_leads'],10001)
        self.assertTrue(search(self.db,'binomial',limit=100))
        self.assertEqual(index_formulas(self.db)['unchanged'],10003)


if __name__=='__main__':unittest.main()
