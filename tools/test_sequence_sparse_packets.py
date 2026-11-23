"""Independent sparse C-finite packet-bank tests."""
import random
import unittest
from sequence_sparse_packets import SparsePacketBank,shared_sparse_terms
from sequence_recurrence_packets import nth_term,x_packet


class SparsePacketTests(unittest.TestCase):
    def test_randomized_recursions(self):
        rng=random.Random(1217)
        for _ in range(90):
            d=rng.randrange(1,6)
            coeff=[rng.randrange(-3,4) for _ in range(d)]
            init=[rng.randrange(-3,4) for _ in range(d)]
            bank=SparsePacketBank(coeff)
            for n in [0,1,2,3,5,8,31,32,33,65,127,128,129,1000,1023,1024,1025]:
                self.assertEqual(list(bank.packet(n)),x_packet(n,coeff))
                self.assertEqual(bank.terms(init,[n])[n],nth_term(init,coeff,n))

    def test_shared_kernel_across_fib_and_lucas(self):
        C=[1,1];seq={'fib':([0,1],C),'lucas':([2,1],C)}
        indices=[1000,1001,1002,1003,1024,2000,2001]
        value,receipt=shared_sparse_terms(seq,{'fib':indices,'lucas':indices})
        self.assertEqual(len(value),14)
        for sid in seq:
            for n in indices:
                self.assertEqual(value[sid,n],nth_term(seq[sid][0],C,n))
        self.assertEqual(receipt['reused_recurrence_kernels'],1)
        self.assertLess(receipt['banks']['1,1']['ring_multiplications'],80)

    def test_index_guard_and_noninvertible_root(self):
        bank=SparsePacketBank([0,0])
        self.assertEqual(bank.packet(100), (0,0))
        with self.assertRaises(ValueError):bank.packet(-1)
        with self.assertRaises(ValueError):SparsePacketBank([])
        with self.assertRaises(ValueError):shared_sparse_terms({'a':([1],[2])},{'a':[-1]})

    def test_gap_reuses(self):
        bank=SparsePacketBank([1,1])
        for n in range(2000,2020):bank.packet(n)
        self.assertGreater(bank.receipt()['shift_reuses'],0)

if __name__=='__main__':unittest.main()
