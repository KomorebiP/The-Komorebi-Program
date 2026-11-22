"""Independent exact generating-function replay and structural transfer checks."""
from __future__ import annotations
from fractions import Fraction as Q
import json
from contextlib import closing
from pathlib import Path
import sqlite3
import tempfile
import unittest

from oeis_formula_database import connect, ingest_curated
from sequence_packet_atlas import build, reduced_rational
from sequence_recurrence_packets import compile_db
from sequence_recurrence_packets import load_sources, nth_term

ROOT=Path(__file__).resolve().parents[1]


def coefficient_replay(num,den,count):
    num,den=[Q(x) for x in num],[Q(x) for x in den]
    assert den[0]==1
    out=[]
    for k in range(count):
        value=(num[k] if k<len(num) else Q(0)) - sum(den[j]*out[k-j] for j in range(1,min(k,len(den)-1)+1))
        out.append(value)
    return out


class PacketAtlasTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp=tempfile.TemporaryDirectory()
        cls.dbpath=Path(cls._tmp.name)/'reconstructed.sqlite3'
        db=connect(cls.dbpath)
        ingest_curated(db,ROOT/'research/oeis-formulas/seeds.json')
        ingest_curated(db,ROOT/'research/oeis-formulas/seeds-extended.json')
        compile_db(db,max_modulus=8)
        db.close()

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_exact_ogfs_all_1155(self):
        with closing(sqlite3.connect(self.dbpath)) as db:
            source_ids=[r[0] for r in db.execute('SELECT oeis_id FROM recurrence_packet_sources')]
            c=load_sources(db,source_ids)
            rows=db.execute('''SELECT oeis_id,modulus,residue,minimal_initial_json,minimal_recurrence_json
                FROM recurrence_packet_phases ORDER BY oeis_id,modulus,residue''').fetchall()
            self.assertEqual(len(rows),1155)
            for sid,m,r,initial_raw,coeff_raw in rows:
                gf=reduced_rational(json.loads(initial_raw),json.loads(coeff_raw))
                actual=coefficient_replay(gf['P'],gf['Q'],12)
                expected=[nth_term(*c[sid],m*n+r) for n in range(12)]
                self.assertEqual(actual,expected,(sid,m,r))

    def test_exact_quotient_links_all(self):
        with tempfile.TemporaryDirectory() as tmp:
            with closing(sqlite3.connect(self.dbpath)) as db:
                out=build(db,Path(tmp)/'f.jsonl',Path(tmp)/'i.json')
            self.assertEqual(out['phase_formulas'],1155)
            payload=json.loads((Path(tmp)/'i.json').read_text())
            formula={(r['source'],r['modulus'],r['residue']):r for r in map(json.loads,(Path(tmp)/'f.jsonl').read_text().splitlines())}
            for link in payload['links']:
                s=link['source'];t=link['target'];flt=link['filter']
                source=formula[(s['source'],s['modulus'],s['residue'])]
                target=formula[(t['source'],t['modulus'],t['residue'])]
                P=[Q(x) for x in source['ogf']['numerator']];Q1=[Q(x) for x in source['ogf']['denominator']]
                R=[Q(x) for x in target['ogf']['numerator']];Q2=[Q(x) for x in target['ogf']['denominator']]
                N=[Q(x) for x in flt['numerator']];D=[Q(x) for x in flt['denominator']]
                # B(z) / A(z) = z^shift * N(z)/D(z), after cross multiplying.
                def mul(a,b):
                    out=[Q(0)]*(len(a)+len(b)-1)
                    for i,x in enumerate(a):
                        for j,y in enumerate(b):out[i+j]+=x*y
                    return out
                lhs=mul(mul(R,D),Q1)
                rhs=mul(mul(P,N),Q2)
                shift=flt['shift']
                if shift>=0:rhs=[Q(0)]*shift+rhs
                else:lhs=[Q(0)]*(-shift)+lhs
                width=max(len(lhs),len(rhs));lhs+=[Q(0)]*(width-len(lhs));rhs+=[Q(0)]*(width-len(rhs))
                self.assertEqual(lhs,rhs,(s,t,flt))

    def test_known_fibonacci_subsequence(self):
        self.assertEqual(reduced_rational([0,1],[3,-1]), {'P':[Q(0),Q(1)],'Q':[Q(1),Q(-3),Q(1)]})
        self.assertEqual(reduced_rational([1,2],[3,-1]), {'P':[Q(1),Q(-1)],'Q':[Q(1),Q(-3),Q(1)]})


if __name__=='__main__':unittest.main()
