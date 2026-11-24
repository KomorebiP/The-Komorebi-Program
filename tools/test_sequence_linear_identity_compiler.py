"""Cross-sequence, all-index algebra and 10-term coincidence rejection."""
import json
from fractions import Fraction as Q
from pathlib import Path
import tempfile
import unittest
from oeis_formula_database import connect,ingest_curated,evaluate
from sequence_exponential_polynomial import symbolic
from sequence_linear_identity_compiler import (
    discover,normalized,key,validate_identity_record
)

ROOT=Path(__file__).resolve().parents[1]

class LinearIdentityCompilerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp=tempfile.TemporaryDirectory()
        cls.db=connect(Path(cls._tmp.name)/'identities.sqlite3')
        ingest_curated(cls.db,ROOT/'research/oeis-formulas/seeds.json')
        ingest_curated(cls.db,ROOT/'research/oeis-formulas/seeds-extended.json')
        cls.result=discover(cls.db)

    @classmethod
    def tearDownClass(cls):
        cls.db.close();cls._tmp.cleanup()

    def test_basis_and_identity_counts(self):
        self.assertEqual(self.result['source_expressions'],21)
        self.assertEqual(self.result['basis']['basis_size'],9)
        self.assertEqual(self.result['exact_identities'],58)
        self.assertEqual(self.result['by_operator'],dict(shift_difference=7,pointwise_product=5,integer_linear_combination=46))

    def test_every_certificate_rechecks_independently(self):
        for record in self.result['links']:
            self.assertTrue(validate_identity_record(self.db,record),record)
            ids=set(record['sources']+[record['target']])
            specs={}
            for sid in ids:
                fid=record['formula_ids'][sid]
                raw,offset=self.db.execute('''SELECT f.evaluator_json,s.offset FROM formulas f
                    JOIN sequences s ON f.oeis_id=s.oeis_id WHERE f.formula_id=?''',(fid,)).fetchone()
                specs[sid]=(json.loads(raw),offset)
            for n in (0,1,2,5,11,23,64,115):
                value=lambda s,k=n:evaluate(specs[s][0],specs[s][1]+k)
                src=record['sources'];op=record['operator'];p=record['parameters']
                if op=='shift_difference':expected=value(src[0],n+p['shift'])-value(src[0])
                elif op=='pointwise_product':expected=value(src[0])*value(src[1])
                else:expected=p['left']*value(src[0])+p['right']*value(src[1])
                self.assertEqual(value(record['target']),expected,(record,n))

    def test_basis_projection_high_indices(self):
        basis=self.result['basis']
        for r in basis['projections']:
            sid=r['target']
            targets={sid}
            targets.update(x['source'] for x in r['coefficients'])
            for n in (0,3,21,87):
                values={}
                for x in targets:
                    fid=self.db.execute('SELECT formula_id FROM formulas WHERE oeis_id=? AND origin="komorebi_curated" ORDER BY length(evaluator_json) LIMIT 1',(x,)).fetchone()[0]
                    raw,offset=self.db.execute('''SELECT f.evaluator_json,s.offset FROM formulas f
                         JOIN sequences s ON s.oeis_id=f.oeis_id WHERE f.formula_id=?''',(fid,)).fetchone()
                    values[x]=evaluate(json.loads(raw),offset+n)
                got=sum(Q(y['weight'])*values[y['source']] for y in r['coefficients'])
                self.assertEqual(got,values[sid],(sid,n))

    def test_finite_coincidence_does_not_create_identity(self):
        n={'op':'n'}
        term={'op':'mul','args':[{'op':'sub','args':[n,j]} for j in range(10)]}
        self.assertNotEqual(key(normalized(term,0)),key(normalized(0,0)))
        for j in range(10):self.assertEqual(evaluate(term,j),0)
        self.assertNotEqual(evaluate(term,10),0)

    def test_changed_terms_invalidate_certificates(self):
        item=self.result['links'][0]
        sid=item['target'];old=self.db.execute('SELECT terms_json FROM sequences WHERE oeis_id=?',(sid,)).fetchone()[0]
        self.db.execute("UPDATE sequences SET terms_json='[7,8,9]' WHERE oeis_id=?",(sid,))
        self.assertFalse(validate_identity_record(self.db,item))
        self.db.execute('UPDATE sequences SET terms_json=? WHERE oeis_id=?',(old,sid))
        self.assertTrue(validate_identity_record(self.db,item))

if __name__=='__main__':unittest.main()
