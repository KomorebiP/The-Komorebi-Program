#!/usr/bin/env python3
"""Exact rational generating functions and certified algebraic transforms.
Author: Komorebi P.
Only Fraction arithmetic is used. A rational OGF is a formal power series,
requiring Q(0) != 0. No arbitrary OEIS formula text is evaluated.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from math import comb
from itertools import product
from typing import Iterable


def trim(a):
    a = [F(x) for x in a]
    while len(a)>1 and a[-1]==0: a.pop()
    return a or [F(0)]

def add(a,b):
    c=[F(0)]*max(len(a),len(b))
    for i,v in enumerate(a): c[i]+=v
    for i,v in enumerate(b): c[i]+=v
    return trim(c)

def neg(a): return [-F(t) for t in a]

def sub(a,b): return add(a,neg(b))

def mul(a,b):
    c=[F(0)]*(len(a)+len(b)-1)
    for i,u in enumerate(a):
        for j,v in enumerate(b): c[i+j]+=F(u)*F(v)
    return trim(c)

def pow_poly(a,n):
    if n<0: raise ValueError('negative polynomial power')
    result=[F(1)]
    for _ in range(n):result=mul(result,a)
    return result

def divmod_poly(a,b):
    a=trim(a);b=trim(b)
    if b==[0]:raise ZeroDivisionError('polynomial zero divisor')
    if len(a)<len(b):return [F(0)],a
    q=[F(0)]*(len(a)-len(b)+1)
    while len(a)>=len(b) and a!=[0]:
        d=len(a)-len(b);t=a[-1]/b[-1];q[d]+=t
        for j in range(len(b)):a[d+j]-=t*b[j]
        a=trim(a)
    return trim(q),a

def gcd_poly(a,b):
    a=trim(a);b=trim(b)
    while b!=[0]: _,r=divmod_poly(a,b);a,b=b,r
    return trim([x/a[-1] for x in a]) if a!=[0] else [F(1)]


def poly_shift(a,k):
    if k<0:raise ValueError('negative polynomial shift')
    return ([F(0)]*k+list(a)) if a!=[0] else [F(0)]


def subst_scale(a,c): return trim([F(v)*F(c)**i for i,v in enumerate(a)])

def homogenize(a,power,c):
    """(1-cx)^power * a(x/(1-cx)), where power >= deg(a)."""
    a=trim(a)
    if power<len(a)-1:raise ValueError('homogenization power too small')
    base=[F(1),-F(c)];z=[F(0)]
    for i,v in enumerate(a):
        z=add(z,[F(v)*q for q in poly_shift(pow_poly(base,power-i),i)])
    return z


def display_poly(a,variable='x'):
    parts=[]
    for i,coef in enumerate(a):
        if not coef:continue
        val=abs(coef)
        atom=(str(val) if i==0 else (variable if i==1 else f'{variable}^{i}'))
        if i>0 and val!=1: atom=str(val)+'*'+atom
        parts.append((coef<0,atom))
    if not parts:return '0'
    s='-'+parts[0][1] if parts[0][0] else parts[0][1]
    for negative,atom in parts[1:]:s+=(' - ' if negative else ' + ')+atom
    return s


@dataclass(frozen=True)
class RatOGF:
    num: tuple
    den: tuple

    def __post_init__(self):
        p=trim(self.num);q=trim(self.den)
        if q[0]==0:raise ValueError('Q(0) must be nonzero for formal power series')
        factor=gcd_poly(p,q)
        if factor!=[1]:
            p,r=divmod_poly(p,factor)
            if r!=[0]:raise ArithmeticError('failed exact numerator division')
            q,r=divmod_poly(q,factor)
            if r!=[0]:raise ArithmeticError('failed exact denominator division')
        z=q[0]
        p=trim([u/z for u in p]);q=trim([u/z for u in q])
        object.__setattr__(self,'num',tuple(p))
        object.__setattr__(self,'den',tuple(q))

    def __str__(self):return '('+display_poly(self.num)+')/('+display_poly(self.den)+')'

    @property
    def order(self):return len(self.den)-1

    def to_json(self):return {'numerator':[str(c) for c in self.num], 'denominator':[str(c) for c in self.den]}

    @classmethod
    def from_json(cls,d):return cls(tuple(F(v) for v in d['numerator']),tuple(F(v) for v in d['denominator']))

    def terms(self,n):
        if n<0:raise ValueError('negative term count')
        result=[]
        for j in range(n):
            z=self.num[j] if j<len(self.num) else F(0)
            for k in range(1,min(len(self.den)-1,j)+1):z-=self.den[k]*result[j-k]
            result.append(z/self.den[0])
        return result

    def mul(self,other):return RatOGF(tuple(mul(self.num,other.num)),tuple(mul(self.den,other.den)))

    def add(self,other):
        return RatOGF(tuple(add(mul(self.num,other.den),mul(other.num,self.den))),tuple(mul(self.den,other.den)))

    def inflate(self,m):
        """Substitution x->x^m, m>=1."""
        if not isinstance(m,int) or m<1:raise ValueError('m must be >=1')
        def expansion(a):
            z=[F(0)]*(m*(len(a)-1)+1)
            for i,coef in enumerate(a):z[m*i]=coef
            return tuple(z)
        return RatOGF(expansion(self.num),expansion(self.den))

    def multiply_x_power(self,n):
        if not isinstance(n,int) or n<0:raise ValueError('n>=0')
        return RatOGF(tuple(poly_shift(self.num,n)),self.den)

    def partial_sums(self):return RatOGF(self.num,tuple(mul(self.den,[1,-1])))

    def alternating(self):return RatOGF(tuple(subst_scale(self.num,-1)),tuple(subst_scale(self.den,-1)))

    def shifted(self):
        a0=self.terms(1)[0]
        numerator=sub(self.num,[a0*q for q in self.den])
        if numerator[0]!=0:raise ArithmeticError('constant term must cancel')
        return RatOGF(tuple(trim(numerator[1:])),self.den)

    def binomial_shear(self,c=1):
        """B_c: b_n=Σ_{k=0}^n binom(n,k)*c^(n-k)*a_k.
        B_c(A)(x)=A(x/(1-cx))/(1-cx). Works for any rational A.
        """
        d=max(len(self.den)-1,len(self.num))
        pn=homogenize(self.num,d-1,c)
        qn=homogenize(self.den,d,c)
        return RatOGF(tuple(pn),tuple(qn))

    @classmethod
    def recurrence(cls,initial,coefficients):
        """a_n=Σ_(i=1)^d c_i a_(n-i), n>=d, with d initial terms."""
        c=tuple(F(v) for v in coefficients)
        if not c:raise ValueError('recurrence order must be >=1')
        if len(initial)!=len(c):raise ValueError('d initial terms needed for order d recurrence')
        q=[F(1)]+[-v for v in c]
        p=mul(q,list(initial))[:len(c)]
        return cls(tuple(trim(p)),tuple(q))

    def polyphase(self,m,j):
        """Root-free rational projection: b_k=a_(m*k+j).
        For a proper rational OGF, Cayley-Hamilton on T^m certifies Q_b.
        """
        if not isinstance(m,int) or m<1 or not 0<=j<m: raise ValueError('m >=1 and 0<=j<m')
        if self.order==0:
            # Polynomial series has finite support: direct finite extraction.
            return RatOGF(tuple(self.terms((len(self.num)-1)//m*m + j + m + 2)[j::m]),(F(1),))
        if len(self.num)>=len(self.den):
            # Separate a polynomial transient, avoiding false CH certificate.
            polynomial,rest=divmod_poly(self.num,self.den)
            proper=RatOGF(tuple(rest),self.den)
            projected=proper.polyphase(m,j)
            trans=[polynomial[j+m*k] for k in range((len(polynomial)-1-j)//m+1)] if j<len(polynomial) else []
            return projected.add(RatOGF(tuple(trans or [F(0)]),(F(1),)))
        d=self.order
        M=[[F(0) for _ in range(d)] for __ in range(d)]
        for i in range(d):M[0][i]=-self.den[i+1]
        for i in range(1,d):M[i][i-1]=1
        T=mat_pow(M,m)
        q=[F(1)]+charpoly_coeffs(T)
        full_prefix=self.terms(m*(d-1)+j+1)
        initial=[full_prefix[m*k+j] for k in range(d)]
        p=mul(q,initial)[:d]
        return RatOGF(tuple(trim(p)),tuple(q))


def mat_mul(A,B):
    n=len(A);k=len(B);p=len(B[0]);out=[[F(0)]*p for _ in range(n)]
    for i in range(n):
        for h in range(k):
            if A[i][h]:
                for j in range(p):out[i][j]+=A[i][h]*B[h][j]
    return out

def mat_pow(M,m):
    n=len(M);res=[[F(int(i==j)) for j in range(n)] for i in range(n)];cur=M
    while m:
        if m&1:res=mat_mul(res,cur)
        cur=mat_mul(cur,cur);m>>=1
    return res

def charpoly_coeffs(A):
    """Det(λI-A)=λ^d+c1 λ^(d-1)+...+cd, exact Leverrier."""
    d=len(A);identity=[[F(int(i==j)) for j in range(d)] for i in range(d)]
    B=[r[:] for r in identity];cs=[]
    for k in range(1,d+1):
        B=mat_mul(A,B)
        coef=-sum(B[i][i] for i in range(d))/k
        cs.append(coef)
        for i in range(d):B[i][i]+=coef
    return cs


def binomial_sum(terms,n,c=1):
    return sum(F(comb(n,k))*F(c)**(n-k)*terms[k] for k in range(n+1))


def is_integral(xs):return all(F(v).denominator==1 for v in xs)


def interlace(polyphase_parts):
    """Exact inverse polyphase reconstruction: sum_j x^j B_j(x^m)."""
    m=len(polyphase_parts)
    if m<1:raise ValueError('need at least one polyphase channel')
    out=RatOGF((F(0),),(F(1),))
    for j,part in enumerate(polyphase_parts):
        out=out.add(part.inflate(m).multiply_x_power(j))
    return out
