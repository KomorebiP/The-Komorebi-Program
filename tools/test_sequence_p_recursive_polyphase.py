"""Independent exact polyphase recurrence tests; no OEIS download required.

Author: Komorebi P.
"""
import unittest
from fractions import Fraction as F
from sequence_holonomic_compiler import compile_formula, fraction_eval, peval
from sequence_p_recursive_polyphase import safe_leader, lift, matmul, mat_identity, primitive_nullvector

N={'op':'n'}
def a(*args):return {'op':'add','args':list(args)}
def m(*args):return {'op':'mul','args':list(args)}
def exp(c):return {'op':'pow','base':c,'exp':N}
def bino():return {'op':'binomial','n':m(2,N),'k':N}


def comp(spec):
    terms=[int(fraction_eval(spec,t)) for t in range(36)]
    out=compile_formula('test','X999999',spec,0,terms,'sha')
    assert out is not None
    return out

class TestPrecursivePhase(unittest.TestCase):
    def test_leader_certificate_positive_and_negative(self):
        self.assertEqual(safe_leader([1,-2,1]),(2,1))
        self.assertEqual(safe_leader([-1,2,-1]),(2,-1))
        self.assertIsNone(safe_leader([-50,1],max_shift=40))

    def test_matrix_multiplication(self):
        x=mat_identity(2)
        self.assertEqual(matmul(x,x),x)

    def test_nullvector_hyperplane(self):
        R=__import__('sequence_holonomic_compiler').Rat
        poly=primitive_nullvector([[R(),R((2,)),R((3,))],[R((0,)),R(),R((2,))]])
        self.assertEqual(len(poly),3)
        for row in [[1,2,3],[0,1,2]]:
            self.assertEqual(sum(peval(poly[j],0)*row[j] for j in range(3)),0)

    def test_additive_hypergeometric_mod_2_and_3(self):
        spec=a(exp(4),bino())
        rec=comp(spec)
        self.assertEqual(rec['order'],2)
        for modulo in (2,3):
            for phase in range(modulo):
                p=lift(rec,spec,modulo,phase,checks=8)
                self.assertEqual(p['result_order'],2)
                coeff=[[F(x) for x in poly] for poly in p['operator_coefficients']]
                for k in range(20):
                    delta=sum(peval(coeff[j],k)*fraction_eval(spec,p['mathematical_base_start']+phase+modulo*(k+j))
                              for j in range(len(coeff)))
                    self.assertEqual(delta,0,(modulo,phase,k))

    def test_additive_polynomial_exponential(self):
        spec=a(m(N,N),exp(2))
        rec=comp(spec)
        for phase in (0,1):
            c=lift(rec,spec,2,phase,checks=8)
            self.assertLessEqual(c['result_order'],rec['order'])

    def test_mixed_factorial_exponential(self):
        spec=a({'op':'factorial','arg':N},exp(2))
        rec=comp(spec)
        c=lift(rec,spec,2,0)
        self.assertGreaterEqual(c['result_order'],1)

    def test_nonzero_tail(self):
        spec=a(m(N,{'op':'sub','args':[N,1]}),exp(3))
        rec=comp(spec)
        c=lift(rec,spec,2,1)
        self.assertGreaterEqual(c['mathematical_base_start'],rec['mathematical_start'])

    def test_invalid_parameters(self):
        spec=a(exp(4),bino());rec=comp(spec)
        with self.assertRaises(ValueError):lift(rec,spec,0,0)
        with self.assertRaises(ValueError):lift(rec,spec,2,2)
        with self.assertRaises(ValueError):lift(rec,spec,5,-1)

    def test_singular_input_leader_rejected(self):
        spec=exp(2);rec=comp(spec)
        rec['operator_coefficients']=[['50','-1'],['-50','1']]
        with self.assertRaises(ValueError):lift(rec,spec,2,0)

if __name__=='__main__':unittest.main()
