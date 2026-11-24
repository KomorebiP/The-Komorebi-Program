"""Independent/adversarial v1.0 tests, stdlib only. Author: Komorebi P."""
from __future__ import annotations
import json,math,random,sqlite3,tempfile,unittest
from fractions import Fraction as F
from pathlib import Path
from oeis_formula_discovery import compile_simple_term
from oeis_formula_database import evaluate
from sequence_holonomic_compiler import (
    Rat,pdivmod,pgcd,pshift,paffine,peval,normalize_operator,nullspace_operator,
    compile_formula,decompose,fraction_eval,start_and_components,compile_database,replay
)
from sequence_holonomic_ogfs import construct
from sequence_hypergeometric_gauges import Ratio,source_model,certify_pair,solve_gauge,difference_ratio
from sequence_hypergeom_polyphase import phase_ratio,lift,reduce_hypergeo
from sequence_oeis_chain_normalizer import extract_chain,verify
from sequence_euler_fibonacci_bridge import bridge_series,native_euler,fibonacci


def spec(rhs):return compile_simple_term(rhs)

def check_formula(rhs,offset=0,terms=32):
    s=spec(rhs)
    nums=[evaluate(s,n) for n in range(offset,offset+terms)]
    c=compile_formula('demo','A999999',s,offset,nums,'1234'*16)
    return s,c,nums

class RationalPolynomialTests(unittest.TestCase):
    def test_poly_exact_division(self):
        q,r=pdivmod((1,3,2),(1,1))
        self.assertEqual(q,(F(1),F(2)))
        self.assertEqual(r,(F(0),))
    def test_poly_shift(self):
        self.assertEqual(pshift((1,0,1),2),(F(5),F(4),F(1)))
        self.assertEqual(paffine((0,1,1),3,1),(F(2),F(9),F(9)))
    def test_rat_cancellation(self):
        x=Rat((1,3,2),(1,1))
        self.assertEqual(x,Rat((1,2)))
        self.assertEqual(x.shift(2).at(5),F(15))
    def test_rat_zero_divisor(self):
        with self.assertRaises(ZeroDivisionError):Rat((1,))/Rat((0,))
    def test_annihilate_two_distinct_geometric_terms(self):
        poly=nullspace_operator([Rat((2,)),Rat((3,))])
        for n in range(100):
            self.assertEqual(sum(peval(p,n)*(2**(n+j)+3**(n+j)) for j,p in enumerate(poly)),0)
        self.assertEqual(len(poly)-1,2)
    def test_annihilate_three_rational_terms(self):
        r=[Rat((1,2),(1,1)),Rat((2,3),(3,1)),Rat((2,))]
        polys=nullspace_operator(r)
        values=[F(1),F(1),F(1)]
        for n in range(50):
            predicted=[]
            for j in range(len(polys)):
                predicted.append(sum(values[i]*math.prod((r[i].at(n+k) for k in range(j)),start=F(1)) for i in range(3)))
            self.assertEqual(sum(peval(p,n)*predicted[j] for j,p in enumerate(polys)),0)
            values=[values[i]*r[i].at(n) for i in range(3)]
    def test_duplicate_ratios_collapse(self):
        out=nullspace_operator([Rat((2,)),Rat((2,))])
        self.assertEqual(len(out),2)

class HolonomicCertificates(unittest.TestCase):
    def test_catalan_order_one(self):
        a,c,terms=check_formula('binomial(2*n,n)/(n+1)')
        self.assertEqual(c['order'],1)
        for j in range(25):
            self.assertEqual(sum(peval(list(map(F,c['operator_coefficients'][k])),j)*terms[j+k] for k in range(2)),0)
    def test_central_binomial_order_one(self):
        _,c,_=check_formula('binomial(2*n,n)')
        self.assertEqual(c['order'],1)
    def test_factorial_order_one(self):
        _,c,_=check_formula('factorial(n)')
        self.assertEqual(c['order'],1)
    def test_franel_like_binomial_product(self):
        _,c,_=check_formula('binomial(3*n,n)*binomial(2*n,n)')
        self.assertEqual(c['order'],1)
    def test_sum_of_two_hypergeom(self):
        _,c,_=check_formula('2^(2*n+1)-binomial(2*n+1,n+1)')
        self.assertEqual(c['order'],2)
    def test_sum_of_three_hypergeom(self):
        _,c,_=check_formula('4^n+2^n+binomial(2*n,n)')
        self.assertEqual(c['order'],3)
    def test_n_factor_ordinary_offset(self):
        _,c,terms=check_formula('binomial(n,11)',offset=11)
        self.assertEqual(c['mathematical_start'],11)
        self.assertEqual(c['order'],1)
    def test_zero_tail_guard(self):
        _,c,_=check_formula('n*(n-1)',offset=0)
        self.assertGreaterEqual(c['mathematical_start'],1)
        self.assertTrue(c['checked_oeis_recursion_positions'] >= 20)
    def test_n_power_n_rejected(self):
        a=spec('n^n')
        terms=[evaluate(a,n) for n in range(30)]
        self.assertIsNone(compile_formula('x','test',a,0,terms,'x'))
    def test_wrong_oeis_prefix_rejected(self):
        a=spec('binomial(2*n,n)/(n+1)')
        terms=[evaluate(a,n) for n in range(30)];terms[16]+=1
        with self.assertRaises(ValueError):compile_formula('x','test',a,0,terms,'x')
    def test_ogf_theta_identity(self):
        ast,c,terms=check_formula('binomial(2*n,n)/(n+1)')
        ode=construct(c,ast,check=20)
        self.assertEqual(ode['order'],1)
        self.assertEqual(ode['tail_initial_values'],['1'])
        self.assertEqual(len(ode['operator_theta_terms']),2)
    def test_large_integer_coefficients(self):
        _,c,_=check_formula('factorial(3*n)/(factorial(n)^3)')
        self.assertEqual(c['order'],1)

class GaugeCertificates(unittest.TestCase):
    def test_exact_catalan_central_binomial(self):
        a=spec('binomial(2*n,n)');b=spec('binomial(2*n,n)/(n+1)')
        nums_a=[str(evaluate(a,n)) for n in range(30)]
        nums_b=[str(evaluate(b,n)) for n in range(30)]
        A=source_model('a','A000984',a,0,json.dumps(nums_a),'hashA')
        B=source_model('b','A000108',b,0,json.dumps(nums_b),'hashB')
        c=certify_pair(A,B)
        self.assertEqual(c['gauge_linear_factors'],[{'a':1,'b':1,'power':-1}])
        self.assertEqual(c['exponential_factor'],'1')
    def test_exact_polynomial_multiplier(self):
        a=spec('2^n');b=spec('(n+1)*2^n')
        A=source_model('a','A111111',a,0,json.dumps([str(evaluate(a,n)) for n in range(30)]),'sha')
        B=source_model('b','A222222',b,0,json.dumps([str(evaluate(b,n)) for n in range(30)]),'sha')
        c=certify_pair(A,B)
        self.assertEqual(c['gauge_linear_factors'],[{'a':1,'b':1,'power':1}])
    def test_nonrational_gauge_rejected(self):
        d=Ratio();d.factor(1,1,1)
        self.assertIsNone(solve_gauge(d))
    def test_ratio_exponential_twist(self):
        a=spec('2^n');b=spec('3^n')
        A=source_model('a','A000079',a,0,json.dumps([str(2**n) for n in range(25)]),'a')
        B=source_model('b','A000244',b,0,json.dumps([str(3**n) for n in range(25)]),'b')
        c=certify_pair(A,B)
        self.assertEqual(c['exponential_factor'],'3/2')
        self.assertEqual(c['support'],0)

class PhaseAndSourceTests(unittest.TestCase):
    def test_catalan_pochhammer(self):
        a=spec('binomial(2*n,n)/(n+1)')
        x=lift(a,'sha','fid','A000108',0,1,0)
        self.assertEqual(x['pochhammer']['multiplier'],'4')
        self.assertEqual(x['pochhammer']['upper'],['1/2'])
        self.assertEqual(x['pochhammer']['lower'],['2'])
        self.assertEqual(x['hypergeometric_ogf']['numerator_parameters'],['1/2','1'])
    def test_central_binomial_phase(self):
        a=spec('binomial(2*n,n)')
        for m in (2,3,5):
            for r in range(m):
                x=lift(a,'sha','fid','A000984',0,m,r)
                self.assertEqual(x['modulus'],m)
                self.assertEqual(x['residue'],r)
    def test_no_bad_negative_tail(self):
        a=spec('binomial(n,11)')
        with self.assertRaises(ValueError):lift(a,'sha','fid','A001288',0,2,0)
    def test_source_chain_extraction(self):
        s='a(n) = binomial(2*n,n)/(n+1) = (2*n)!/(n!*(n+1)!).'
        vals=list(extract_chain(s))
        self.assertEqual(len(vals),1)
        self.assertEqual(evaluate(vals[0][1],12),208012)
    def test_conditions_not_inferred(self):
        self.assertEqual(list(extract_chain('a(n)=n for odd n = 1')),[])
    def test_unsupported_code_not_executed(self):
        self.assertEqual(list(extract_chain('a(n)=__import__("os").system("bad") = 7')),[])

class EulerBridgeTests(unittest.TestCase):
    def test_euler_28_exact(self):
        self.assertEqual(bridge_series(28),native_euler(28))
    def test_euler_secant_subsequence(self):
        a=bridge_series(20)
        self.assertEqual(a[::2][:8],[1,1,5,61,1385,50521,2702765,199360981])
    def test_fibonacci_anchor(self):
        self.assertEqual([fibonacci(n) for n in range(11)],[0,1,1,2,3,5,8,13,21,34,55])
    def test_boundary(self):
        with self.assertRaises(ValueError):bridge_series(0)

if __name__=='__main__':unittest.main()
