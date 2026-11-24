"""OEIS formula dependency hypergraph: restricted AST and finite-evidence limits.

Author: Komorebi P.
"""
import json,sqlite3,tempfile,unittest
from fractions import Fraction
from pathlib import Path
from sequence_oeis_formula_dependencies import extract,safe_parse,eval_arithmetic,UnsupportedFormula

class DependencyTests(unittest.TestCase):
    def setUp(self):
        self.db=sqlite3.connect(':memory:')
        self.db.execute('CREATE TABLE sequences (oeis_id TEXT, offset INTEGER, terms_json TEXT)')
        self.db.execute('CREATE TABLE formulas (formula_id TEXT,oeis_id TEXT,expression TEXT,origin TEXT)')
        def add(i,offset,terms):self.db.execute('INSERT INTO sequences VALUES (?,?,?)',(i,offset,json.dumps(terms)))
        add('A000100',0,[n*n for n in range(30)])
        add('A000101',0,[2*n+1 for n in range(30)])
        add('A000102',0,[(n+1)**2+n*n for n in range(30)])
        add('A000103',0,[(n+1)**2-n*n for n in range(30)])
        add('A000104',0,[n*n+1 for n in range(30)])
        self.db.execute("INSERT INTO formulas VALUES ('f1','A000103','a(n) = A000100(n+1) - A000100(n). - _OEIS Author_','oeis_formula')")
        self.db.execute("INSERT INTO formulas VALUES ('f2','A000102','a(n) = A000100(n+1) + A000100(n)','oeis_formula')")
        self.db.execute("INSERT INTO formulas VALUES ('f3','A000104','a(n) = A000100(n+1)','oeis_formula')")
        self.db.execute("INSERT INTO formulas VALUES ('f4','A000104',\"a(n) = __import__('os').system('echo BAD') + A000100(n)\",'oeis_formula')")
    def tearDown(self):self.db.close()
    def test_cross_sequence_checked_and_rejected_differently(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'hyper.jsonl'; stats=extract(self.db,path,None,minimum=10,holdout=8)
            rows={r['formula_id']:r for r in map(json.loads,path.read_text().splitlines())}
            self.assertEqual(stats['source_formula_lines'],4)
            self.assertEqual(rows['f1']['status'],'finite_checked_formula_hyperedge')
            self.assertEqual(rows['f2']['status'],'finite_checked_formula_hyperedge')
            self.assertEqual(rows['f1']['checked_terms'],29) # shift +1 cannot evaluate last term
            self.assertEqual(rows['f3']['status'],'parsed_but_unverified')
            self.assertTrue(rows['f3']['first_failure'])
            self.assertEqual(rows['f4']['status'],'textual_dependency_unverified')
    def test_rational_arithmetic_only(self):
        expr=safe_parse('A000100(n+1)/2 + 3*n')
        r=eval_arithmetic(expr,4,lambda sid,n:n*n)
        self.assertEqual(r,Fraction(5*5,2)+12)
        for raw in ['__import__("os")','A000100.__class__','(lambda x:x)(n)','A000100(n).__class__','A000100(n, unsafe=True)','n if n>2 else 0','[A000100(n)]','A000100(n)**99999','A000100(n) + open("/etc/passwd")']:
            tree=safe_parse(raw)
            if tree:
                with self.assertRaises(UnsupportedFormula,msg=raw):eval_arithmetic(tree,1,lambda sid,n:n)
    def test_textual_citation_never_promoted(self):
        self.db.execute("INSERT INTO formulas VALUES ('f5','A000104','See A000101 for a related sequence.','oeis_formula')")
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'h.jsonl';extract(self.db,p,None,minimum=10,holdout=8)
            row=[json.loads(s) for s in p.read_text().splitlines() if json.loads(s)['formula_id']=='f5'][0]
            self.assertEqual(row['status'],'textual_dependency_unverified')
            self.assertEqual(row['references'],['A000101'])

if __name__=='__main__':unittest.main()
