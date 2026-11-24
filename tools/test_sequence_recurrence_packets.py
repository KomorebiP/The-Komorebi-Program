"""Adversarial correctness and all-index certificate tests for C-finite packets."""
from __future__ import annotations
import json
from pathlib import Path
import random
import sqlite3
import tempfile
import unittest

from oeis_formula_database import connect, ingest_curated
from sequence_recurrence_packets import (
    x_packet,multiply_mod,nth_term,batch_term,companion,characteristic,
    mat_pow,phase_certificate,minimal_scalar_phase,compile_db,load_sources,
)

ROOT=Path(__file__).resolve().parents[1]


def slow(initial,c,n):
    d=len(c);a=list(initial)
    for k in range(d,n+1):a.append(sum(c[j]*a[k-1-j] for j in range(d)))
    return a[n]


class RecurrencePacketsTest(unittest.TestCase):
    def test_packet_regression_all_orders_and_degenerate_kernels(self):
        rng=random.Random(267654)
        for d in range(1,7):
            for trial in range(22):
                c=[rng.randrange(-3,4) for _ in range(d)]
                a=[rng.randrange(-5,6) for _ in range(d)]
                for n in [0,1,d-1,d,2*d,10,17,41,99,201]:
                    self.assertEqual(nth_term(a,c,n),slow(a,c,n),(d,trial,n))
                    self.assertEqual(sum(x*y for x,y in zip(x_packet(n,c),a)),slow(a,c,n))

    def test_proved_polyphase_characteristics(self):
        rng=random.Random(711)
        for d in range(1,6):
            for trial in range(9):
                c=[rng.randrange(-2,3) for _ in range(d)]
                a=[rng.randrange(-3,4) for _ in range(d)]
                for m in (2,3,4,7):
                    char=characteristic(mat_pow(companion(c),m))
                    self.assertEqual(len(char),d+1)
                    for residue in (0,m-1):
                        proof=phase_certificate(a,c,m,residue)
                        b=[slow(a,c,m*n+residue) for n in range(25)]
                        for coefficients, initial in [
                            (proof['general_recurrence'],b[:d]),
                            (proof['minimal']['coefficients'],proof['minimal']['initial'])]:
                            k=len(coefficients)
                            self.assertEqual(k, len(initial))
                            if k==0:self.assertTrue(all(v==0 for v in b));continue
                            for n in range(k,24):
                                self.assertEqual(b[n],sum(coefficients[j]*b[n-1-j] for j in range(k)),
                                                 (c,a,m,residue,proof))
                        self.assertLessEqual(proof['minimal']['order'],d)

    def test_order_reductions_are_not_spurious(self):
        # Under X^2 mod (X^2-1), every even or odd phase is constant.
        for residue in (0,1):
            a=[2,7]; c=[0,1]
            cert=phase_certificate(a,c,2,residue)
            self.assertEqual(cert['minimal']['order'],1)
            self.assertEqual(cert['minimal']['coefficients'],[1])
        self.assertEqual(phase_certificate([0,0],[1,1],5,0)['minimal']['order'],0)

    def test_shared_kernel_multi_output(self):
        shared={'A000045':([0,1],[1,1]),'A000032':([2,1],[1,1]),
                'A000129':([0,1],[2,1]),'A001333':([1,1],[2,1]),
                'A000073':([0,0,1],[1,1,1])}
        for n in (0,1,2,10,50,333,4096):
            out,cost=batch_term(shared,n)
            self.assertEqual(cost['recurrence_kernels'],3)
            self.assertEqual(cost['packet_exponentiations'],3)
            self.assertEqual(cost['outputs'],5)
            for sid,(a,c) in shared.items():self.assertEqual(out[sid],slow(a,c,n))

    def test_bad_inputs(self):
        for op in [lambda: x_packet(-1,[1,1]), lambda: x_packet(2,[]),
                   lambda: x_packet(2,[1.0,1]),lambda: phase_certificate([1,2],[1,1],0,0),
                   lambda: phase_certificate([1,2],[1,1],2,2),
                   lambda: nth_term([0],[1,1],3),lambda: multiply_mod([1],[1],[1,1])]:
            with self.assertRaises(ValueError):op()

    def test_replay_from_full_local_db_and_idempotent(self):
        # Make a private DB clone so tests cannot alter the distributed reference artifact.
        with tempfile.TemporaryDirectory() as td:
            dst=Path(td)/'data.sqlite3'
            target=connect(dst)
            ingest_curated(target,ROOT/'research/oeis-formulas/seeds.json')
            ingest_curated(target,ROOT/'research/oeis-formulas/seeds-extended.json')
            r=compile_db(target,max_modulus=8)
            self.assertEqual(r['verified_sequence_definitions'],33)
            self.assertEqual(r['certified_polyphase_formulas'],1155)
            self.assertGreaterEqual(r['shared_kernels'],6)
            self.assertGreaterEqual(r['reused_recursions'],2)
            self.assertEqual(compile_db(target,max_modulus=8),r)
            src=load_sources(target,['A000045','A000032','A000129','A001333'])
            outputs,counts=batch_term(src,1000)
            self.assertEqual(counts['packet_exponentiations'],2)
            self.assertEqual(outputs['A000032'],2*nth_term([0,1],[1,1],1001)-outputs['A000045'])
            # A changed OEIS prefix invalidates the source digest and refuses to compute.
            target.execute("UPDATE sequences SET terms_json='[0,1,99]' WHERE oeis_id='A000045'")
            with self.assertRaises(ValueError):load_sources(target,['A000045'])
            target.close()


if __name__=='__main__':unittest.main()
