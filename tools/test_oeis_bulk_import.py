"""Archive-based ingestion and transactional source replay tests."""
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest
import zipfile

from oeis_formula_database import connect,statistics
from oeis_bulk_import import import_archive,import_tree
from sequence_transfer_graph import import_xrefs,create_graph

SEQ1='''%I A000045 M1234 N1234
%S A000045 0,1,1,2,3,5,8,13,21,34,55,
%T A000045 89,144,233,377,610,987
%O A000045 0,4
%N A000045 Fibonacci numbers
%F A000045 a(n)=a(n-1)+a(n-2)
%Y A000045 Cf. A000032, A000111.
'''
SEQ2='''%I A000032 M1234 N1234
%S A000032 2,1,3,4,7,11,18,29,47,76,123,199,322,521
%O A000032 0,1
%N A000032 Lucas numbers
%Y A000032 See A000045.
'''
SEQ_BAD='''%I A000999
%S A000999 1,2,WRONG
%O A000999 0,2
'''

class ArchiveTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.directory=Path(self.tmp.name)
        self.db=connect(self.directory/'t.sqlite3')
        self.addCleanup(self.db.close)

    def items(self):
        return {'oeisdata-main/seq/A000/A000045.seq':SEQ1,
                'oeisdata-main/seq/A000/A000032.seq':SEQ2,
                'oeisdata-main/seq/A000/A000999.seq':SEQ_BAD,
                '../evil.txt':'ignored'}

    def build_zip(self):
        p=self.directory/'src.zip'
        with zipfile.ZipFile(p,'w') as z:
            for key,value in self.items().items():z.writestr(key,value)
        return p

    def build_tar(self):
        p=self.directory/'src.tar.gz'
        with tarfile.open(p,'w:gz') as t:
            for key,value in self.items().items():
                b=value.encode();i=tarfile.TarInfo(key);i.size=len(b)
                t.addfile(i,io.BytesIO(b))
        return p

    def check_file(self,p):
        r=import_archive(self.db,p,batch_size=1)
        self.assertEqual((r['scanned'],r['inserted'],r['failed']),(3,2,1))
        self.assertEqual(r['references_staged'],3)
        self.assertEqual(statistics(self.db)['oeis_sequences_stored'],2)
        self.assertEqual(statistics(self.db)['raw_oeis_formula_lines'],1)
        # Staged cross-references must be candidate edges, not identities.
        create_graph(self.db)
        rows=self.db.execute("SELECT status FROM transfer_edges WHERE operator='oeis_cross_reference'").fetchall()
        self.assertEqual(rows,[('reference_only',),('reference_only',)])
        new=import_archive(self.db,p,batch_size=1)
        self.assertEqual((new['unchanged'],new['failed']),(2,1))
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM oeis_xrefs').fetchone()[0],3)
        self.assertEqual(r['archive_sha256'],new['archive_sha256'])

    def test_zip(self):self.check_file(self.build_zip())
    def test_tar(self):self.check_file(self.build_tar())

    def test_tree_is_deterministic_and_stages_links(self):
        root=self.directory/'seq'
        a=root/'A000';a.mkdir(parents=True)
        for key,content in [("A000999",SEQ_BAD),("A000045",SEQ1),("A000032",SEQ2)]:
            (a/(key+'.seq')).write_text(content,encoding='utf-8')
        result=import_tree(self.db,root,limit=2,batch_size=1)
        self.assertEqual(result['inserted'],2)
        self.assertEqual(result['failed'],0)
        self.assertEqual(result['references_staged'],3)
        self.assertEqual(statistics(self.db)['oeis_sequences_stored'],2)
        self.assertEqual(import_tree(self.db,root,limit=2)['unchanged'],2)
        full=import_tree(self.db,root)
        self.assertEqual(full['failed'],1)
        self.assertEqual(full['unchanged'],2)
        self.assertEqual(self.db.execute('SELECT count(*) FROM oeis_xrefs').fetchone()[0],3)

    def test_tree_reimport_rolls_back_bad_changes(self):
        root=self.directory/'seq'; root.mkdir()
        p=root/'A000045.seq';p.write_text(SEQ1,encoding='utf-8')
        self.assertEqual(import_tree(self.db,root)['inserted'],1)
        old=self.db.execute('SELECT terms_json FROM sequences WHERE oeis_id=?',('A000045',)).fetchone()[0]
        p.write_text(SEQ_BAD.replace('A000999','A000045'),encoding='utf-8')
        result=import_tree(self.db,root)
        self.assertEqual(result['failed'],1)
        self.assertEqual(old,self.db.execute('SELECT terms_json FROM sequences WHERE oeis_id=?',('A000045',)).fetchone()[0])

    def test_limit_and_no_xrefs(self):
        r=import_archive(self.db,self.build_zip(),limit=1,with_xrefs=False)
        self.assertEqual(r['scanned'],1)
        self.assertEqual(r['references_staged'],0)
        self.assertEqual(statistics(self.db)['oeis_sequences_stored'],1)

if __name__=='__main__':unittest.main()
