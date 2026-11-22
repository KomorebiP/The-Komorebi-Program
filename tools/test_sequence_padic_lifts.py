"""Independent exact and p-adic congruence checks on digit lift towers."""
import random
import unittest
from sequence_padic_lifts import lift_tower
from sequence_recurrence_packets import nth_term

class PadicLiftTest(unittest.TestCase):
    def test_random_digit_lifts(self):
        rng=random.Random(431)
        for c,a in [([1,1],[0,1]),([2,1],[0,1]),([1,1,1],[0,0,1]),
                    ([0,1],[1,2]),([4,-6,4,-1],[1,3,6,10])]:
            for p,digits in [(2,[1,0,1,1]),(3,[2,1,0]),(5,[1,2,0])]:
                tower=lift_tower(a,c,p,digits,padic_precision=4)
                self.assertEqual(tower[-1]['modulus'],p**len(digits))
                for level in tower:
                    m=level['modulus'];r=level['residue']
                    self.assertTrue(0<=r<m)
                    self.assertEqual(level['first_phase_terms'],
                                     [nth_term(a,c,m*n+r) for n in range(4)])
                    modulus=p**4
                    state=level['state_mod_p_power'][:]
                    matrix=level['shift_matrix_mod_p_power']
                    for n in range(8):
                        self.assertEqual(sum(x*y for x,y in zip(a,state))%modulus,
                                         nth_term(a,c,m*n+r)%modulus)
                        state=[sum(x*y for x,y in zip(row,state))%modulus for row in matrix]
    def test_bad_towers(self):
        for p,d in [(4,[1]),(1,[0]),(2,[2]),(3,[]),(3,[-1]),(3,[0]*9)]:
            if p==3 and len(d)==9:continue
            with self.assertRaises(ValueError):lift_tower([0,1],[1,1],p,d)
        with self.assertRaises(ValueError):lift_tower([0,1],[1,1],7,[1,1,1,1,1])

if __name__=='__main__':unittest.main()
