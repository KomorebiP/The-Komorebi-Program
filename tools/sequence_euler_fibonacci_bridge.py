"""Exact nonholonomic Euler-zigzag / Fibonacci generating-function bridge.

Author: Komorebi P. Pure formal power series over Q, with independent
integer recurrence and OEIS term checks. No numerical square roots or
floating-point approximations.

E(z)=sec(z)+tan(z)=(1+sin(z))/cos(z)
    =(1+sin(z))*sum_(k>=0) F_(k+1)*u(z)^k,
u(z)=(sqrt(5-4*cos(z))-1)/2.
The algebraic substitution is exact in Q[[z]], because u(0)=0 and
1-u-u**2=cos(z). It is a representation transfer, not a speed claim.
"""
from __future__ import annotations
import argparse,json,sqlite3
from fractions import Fraction as F
from math import comb,factorial
from pathlib import Path


def mul(a,b,terms):
    out=[F(0)]*terms
    for i,x in enumerate(a[:terms]):
        if not x:continue
        for j,y in enumerate(b[:terms-i]):out[i+j]+=x*y
    return out


def cos_sin(terms):
    c=[F(0)]*terms;s=[F(0)]*terms
    for n in range(terms):
        if n%2==0:c[n]=F((-1)**(n//2),factorial(n))
        else:s[n]=F((-1)**((n-1)//2),factorial(n))
    return c,s


def fibonacci(n):
    x,y=0,1
    for _ in range(n):x,y=y,x+y
    return x


def bridge_series(terms):
    if terms<1:raise ValueError('positive truncation length required')
    cosine,sine=cos_sin(terms)
    rad=[F(5 if n==0 else 0)-4*cosine[n] for n in range(terms)]
    root=[F(1)]+[F(0)]*(terms-1)
    for n in range(1,terms):
        root[n]=(rad[n]-sum(root[j]*root[n-j] for j in range(1,n)))/2
    u=[F(0)]+[root[n]/2 for n in range(1,terms)]
    # Exact verification of the defining quadratic; no transcendental CAS.
    square=mul(u,u,terms)
    assert all((F(1) if n==0 else F(0))-u[n]-square[n]==cosine[n] for n in range(terms))
    power=[F(1)]+[F(0)]*(terms-1)
    total=[F(0)]*terms
    for k in range((terms-1)//2+1):
        f=fibonacci(k+1)
        for n in range(terms):total[n]+=f*power[n]
        power=mul(power,u,terms)
    one_plus_sin=sine[:];one_plus_sin[0]+=1
    E=mul(one_plus_sin,total,terms)
    return [e*factorial(i) for i,e in enumerate(E)]


def native_euler(terms):
    """Euler numbers from the independent formal quotient cos(z) E(z)=1+sin(z)."""
    c,s=cos_sin(terms)
    a=[]
    for n in range(terms):
        rhs=F(1 if n==0 else 0)+s[n]
        # Exponential coefficients E_n, with cos coefficients c_j.
        val=rhs*factorial(n)-sum(comb(n,j)*c[j]*factorial(j)*a[n-j]
                                  for j in range(1,n+1) if j%2==0)
        a.append(val)
    return a


def verify(db,terms=28):
    derived=bridge_series(terms)
    native=native_euler(terms)
    if derived!=native:raise AssertionError('Fibonacci transfer coefficients do not match Euler quotient')
    if any(x.denominator!=1 for x in derived):raise AssertionError('zigzag coefficients not integral')
    report={'tested_formal_coefficients':terms,'formal_identity':'1-u-u^2=cos(z), u=(sqrt(5-4cos(z))-1)/2',
        'exact_bridge':'(1+sin z) * sum_(k>=0) F_(k+1) u(z)^k = sec z + tan z',
        'independent_euler_recurrence':'cos(z)*E(z)=1+sin(z)',
        'formal_oeis_identification':'Classical defining generating functions; check OEIS finite reference terms separately'}
    for sid,values in [('A000111',derived),('A000364',derived[::2])]:
        row=db.execute('SELECT offset,terms_json FROM sequences WHERE oeis_id=?',(sid,)).fetchone()
        if not row:continue
        off,stored=row
        if off!=0:raise ValueError('unexpected OEIS index convention for '+sid)
        ref=[int(x) for x in json.loads(stored)];n=min(len(ref),len(values))
        if values[:n]!=ref[:n]:raise AssertionError('OEIS reference values disagree for '+sid)
        report[sid+'_reference_terms_matched']=n
    report['exact_values']=[str(v) for v in derived[:18]]
    return report


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--db',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args(argv)
    with sqlite3.connect(a.db) as db:report=verify(db)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf8')
    print(json.dumps(report,indent=2,sort_keys=True))
if __name__=='__main__':main()
