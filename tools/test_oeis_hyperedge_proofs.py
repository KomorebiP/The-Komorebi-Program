"""Exact multi-input proof ledger, offsets and adversarial mismatch tests.

Author: Komorebi P.
"""
import ast,hashlib,json,sqlite3,tempfile,unittest
from pathlib import Path
from sequence_oeis_hyperedge_proofs import prove,replay,symbolic,UnsupportedFormula
from sequence_oeis_symbolic_network import load_formulas,formal_eval

class HyperedgeProofTests(unittest.TestCase):
    def setUp(self):
        self.db=sqlite3.connect(':memory:')
        self.db.execute('CREATE TABLE sequences (oeis_id TEXT,offset INTEGER,source_sha256 TEXT)')
        self.db.execute('CREATE TABLE formulas (oeis_id TEXT,formula_id TEXT,evaluator_json TEXT,checked_terms INTEGER,origin TEXT,verification TEXT,expression TEXT)')
        formulas={
          'A000578':{'op':'pow','base':{'op':'n'},'exp':3},
          'A000244':{'op':'pow','base':3,'exp':{'op':'n'}},
          'A062074':{'op':'mul','args':[{'op':'pow','base':{'op':'n'},'exp':3},{'op':'pow','base':3,'exp':{'op':'n'}}]},
        }
        for sid,x in formulas.items():
            self.db.execute('INSERT INTO sequences VALUES (?,?,?)',(sid,0,sid*2))
            self.db.execute("INSERT INTO formulas VALUES (?,?,?,?,?,?,?)",(sid,sid+'-f',json.dumps(x),24,'oeis_normalized','finite_checked',None))
    def tearDown(self):self.db.close()
    def test_multi_input_identity_and_counterexample(self):
        good={'formula_id':'entry-1','oeis_id':'A062074','references':['A000578','A000244'],
          'source_text_sha256':'abc','candidate_rhs':'A000578(n)*A000244(n)',
          'status':'finite_checked_formula_hyperedge','checked_terms':24}
        bad=dict(good,formula_id='entry-2',candidate_rhs='A000578(n)*A000244(n)+1')
        malicious=dict(good,formula_id='entry-3',candidate_rhs='A000578(n)+__import__("os")')
        raw='a(n) = A000578(n)*A000244(n)'
        good['source_text_sha256']=hashlib.sha256(raw.encode()).hexdigest()
        self.db.execute("INSERT INTO formulas VALUES (?,?,?,?,?,?,?)",('A062074','entry-1',None,0,'oeis_formula','unverified',raw))
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)
            (p/'leads.jsonl').write_text('\n'.join(json.dumps(x) for x in [good,bad,malicious])+'\n')
            stats=prove(self.db,p/'leads.jsonl',p/'proofs.jsonl',p/'summary.json')
            self.assertEqual(stats['proved_formula_hyperedges'],1)
            self.assertEqual(stats['proved_multi_input_hyperedges'],1)
            self.assertEqual(stats['symbolic_inequality'],1)
            cert=json.loads((p/'proofs.jsonl').read_text().strip())
            self.assertEqual(cert['input_sequences'],['A000578','A000244'])
            self.assertEqual(cert['oeis_identification'].split(';')[0],'Finite OEIS prefix agreement only')
            self.assertEqual(replay(self.db,p/'proofs.jsonl')['passed'],1)
            cert['source_text_sha256']='0'*64
            (p/'proofs.jsonl').write_text(json.dumps(cert)+'\n')
            self.assertEqual(replay(self.db,p/'proofs.jsonl')['failed'],1)
    def test_symbolic_certain_and_rejects_undefined(self):
        records,_=load_formulas(self.db)
        tree=ast.parse('A000578(n)*A000244(n)',mode='eval')
        value=symbolic(tree,0,records)
        for n in range(13):self.assertEqual(formal_eval(value,n),n**3*3**n)
        with self.assertRaises(UnsupportedFormula):symbolic(ast.parse('A000578(n-1)',mode='eval'),0,records)
        with self.assertRaises(UnsupportedFormula):symbolic(ast.parse('A000578(n)//2',mode='eval'),0,records)

if __name__=='__main__':unittest.main()
