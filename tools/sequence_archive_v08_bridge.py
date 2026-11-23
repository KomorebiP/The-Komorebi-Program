"""Exact sparse-index operators recovered from the user's v0.8 OEIS archive.

Author: Komorebi P.

The archived source is ``Komorebi_OEIS_All_Versions_Through_v0_8.zip``:
  current/komorebi_oeis_v08/EXACT_RESULTS_V08.md
  current/komorebi_oeis_v08/transfer_engines_v08.py
  current/komorebi_oeis_v08/quadratic_polyphase_v08.py

These are *formal operator theorems*, not standalone proofs of every OEIS
identification in the archive. No original OEIS formula text is executed.
"""
from __future__ import annotations
from functools import lru_cache
import hashlib
from math import comb
from typing import Callable, Iterable


def _integer(value, label, *, minimum=None):
    if type(value) is not int or (minimum is not None and value < minimum):
        raise ValueError(f'{label} must be an integer >= {minimum}' if minimum is not None else
                         f'{label} must be an integer')


def binomial_generalized(power: int, k: int) -> int:
    """Coefficient [x^k](1-x)^(-power), including the power=0 endpoint."""
    _integer(power, 'power', minimum=0)
    _integer(k, 'k', minimum=0)
    return int(k == 0) if power == 0 else comb(power+k-1,k)


def riordan_requirements(n: int, *, c: int, s: int, r: int, t: int) -> tuple[int, ...]:
    """Exact source indices needed for one output term, excluding zero weights."""
    for name,value,low in [('n',n,0),('c',c,None),('s',s,0),('r',r,1),('t',t,1)]:
        _integer(value,name,minimum=low)
    return tuple(k for k in range(n//r+1)
                 if (not (c == 0 and n != r*k)) and
                    (s+t*k > 0 or n == r*k))


def riordan_nth(source: Callable[[int],int], n: int, *, c: int, s: int, r: int, t: int) -> int:
    """[x^n](1-cx)^(-s) A(x^r/(1-cx)^t), with A(x)=sum a_k x^k.

    Only the exact source-index set returned by riordan_requirements is read.
    The proof is a formal binomial expansion of each a_k term; no sample fit.
    """
    needed=riordan_requirements(n,c=c,s=s,r=r,t=t)
    result=0
    for k in needed:
        value=source(k)
        if type(value) is not int:
            raise TypeError('Riordan source must supply exact integers')
        degree=n-r*k
        result += value * c**degree * binomial_generalized(s+t*k,degree)
    return result


def riordan_sparse(source: Callable[[int],int], indices: Iterable[int],
                   *, c: int, s: int, r: int, t: int) -> dict[int,int]:
    """Evaluate sparse target indices while reusing only necessary a_k values."""
    target=tuple(dict.fromkeys(indices))
    needed={k for n in target for k in riordan_requirements(n,c=c,s=s,r=r,t=t)}
    values={k:source(k) for k in sorted(needed)}
    return {n:riordan_nth(values.__getitem__,n,c=c,s=s,r=r,t=t) for n in target}


def quadratic_multiply(v: tuple[int,int], w: tuple[int,int], q: int) -> tuple[int,int]:
    """Multiplication in Z[sqrt(q)]: (a+b√q)(c+d√q)."""
    _integer(q,'q',minimum=0)
    if any(type(x) is not int for x in v+w) or len(v)!=2 or len(w)!=2:
        raise ValueError('quadratic operands must contain two integers')
    a,b=v; c,d=w
    return (a*c+q*b*d,a*d+b*c)


def quadratic_pair(c: int, q: int, n: int) -> tuple[int,int]:
    """Return exact B_n,D_n for (c+sqrt(q))^n=B_n+sqrt(q) D_n.

    Binary powering takes O(log(n+1)) quadratic-ring operations. n=0 -> (1,0).
    """
    _integer(c,'c');_integer(q,'q',minimum=0);_integer(n,'n',minimum=0)
    pair=(1,0); base=(c,1)
    while n:
        if n & 1:pair=quadratic_multiply(pair,base,q)
        n >>= 1
        if n:base=quadratic_multiply(base,base,q)
    return pair


def quadratic_sparse(c: int, q: int, indices: Iterable[int]) -> tuple[dict[int,tuple[int,int]],dict]:
    """Compute paired channels at requested n only, sharing powers of two.

    Results include an exact operation counter (not an elapsed-time estimate).
    """
    _integer(c,'c');_integer(q,'q',minimum=0)
    ns=tuple(sorted(set(indices)))
    for n in ns:_integer(n,'n',minimum=0)
    if not ns:return {},{'queries':0,'ring_multiplications':0,'precomputed_powers':0}
    powers=[(c,1)]
    multiplies=0
    while len(powers)<max(ns).bit_length():
        powers.append(quadratic_multiply(powers[-1],powers[-1],q));multiplies+=1
    output={}
    for n in ns:
        state=(1,0)
        for bit in range(n.bit_length()):
            if n>>bit & 1:
                state=quadratic_multiply(state,powers[bit],q);multiplies+=1
        output[n]=state
    return output,{'queries':len(ns),'ring_multiplications':multiplies,
                   'precomputed_powers':len(powers)}


def quadratic_binomial_even(c:int,q:int,n:int)->int:
    for k in (c,q,n):_integer(k,'argument')
    _integer(q,'q',minimum=0);_integer(n,'n',minimum=0)
    return sum(comb(n,2*k)*c**(n-2*k)*q**k for k in range(n//2+1))


def quadratic_binomial_odd(c:int,q:int,n:int)->int:
    for k in (c,q,n):_integer(k,'argument')
    _integer(q,'q',minimum=0);_integer(n,'n',minimum=0)
    return sum(comb(n,2*k+1)*c**(n-2*k-1)*q**k
               for k in range((n+1)//2))


def quadratic_certificate(c:int,q:int,n:int)->dict:
    """Check the algebraic norm without decimal-converting enormous integers."""
    b,d=quadratic_pair(c,q,n)
    def summary(v):
        raw=abs(v).to_bytes(max(1,(abs(v).bit_length()+7)//8),'big')
        return {'bits':v.bit_length(),'sign':-1 if v<0 else (1 if v else 0),
                'binary_sha256':hashlib.sha256((b'-' if v<0 else b'+')+raw).hexdigest(),
                'decimal':str(v) if v.bit_length()<=12000 else None}
    norm=b*b-q*d*d
    expected=(c*c-q)**n
    return {'index':n,'B':summary(b),'D':summary(d),
            'norm':summary(norm),'norm_expected':summary(expected),
            'norm_verified':norm==expected,
            'scope':'exact quadratic-extension identity; OEIS labels separate'}
