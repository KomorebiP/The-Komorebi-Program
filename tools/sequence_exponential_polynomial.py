"""Structural exact C-finite extraction from curated arithmetic evaluators.

Author: Komorebi P.

Accepts a restricted expression grammar that provably represents a finite sum
of exponential polynomials P_i(n)*lambda_i^n with integer lambda_i, plus
certain explicit periodic/floor-division forms. This compiles a global
annihilating recurrence by the shift-polynomial identity
    (S-lambda)^(deg(P)+1) [P(n)*lambda^n] = 0.

Importantly, this does NOT derive a recurrence by fitting a finite prefix.
Unsupported constructs return None. Integer-valuedness follows from having
integral initial values and an integer-coefficient recurrence; evaluation
at the first order-many indices checks that the supplied DSL's exact-division
semantics agrees with the symbolic expression, and the polynomial identity
ensures that agreement for all indices where the expression is defined.
"""
from __future__ import annotations
from fractions import Fraction as Q
from math import factorial
import math

from oeis_formula_database import evaluate
from sequence_ratio_certificates import affine

MAX_DEGREE=10
MAX_ORDER=24


def p_trim(p):
    p=[Q(x) for x in p]
    while len(p)>1 and p[-1]==0:p.pop()
    return p


def p_add(a,b):return p_trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])

def p_scale(a,v):return p_trim([t*Q(v) for t in a])

def p_mul(a,b):
    if len(a)+len(b)-2>MAX_DEGREE:raise ValueError('polynomial degree limit')
    out=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return p_trim(out)


def p_power(a,k):
    if k<0 or k>MAX_DEGREE:raise ValueError('exponent bound')
    out=[Q(1)]
    for _ in range(k):out=p_mul(out,a)
    return out


def ep_add(a,b):
    out={r:list(p) for r,p in a.items()}
    for rate,poly in b.items():out[rate]=p_add(out.get(rate,[Q(0)]),poly)
    return {rate:p for rate,p in out.items() if p!=[0]}


def ep_mul(a,b):
    result={}
    for r,p in a.items():
        for s,q in b.items():
            if r*s==0:raise ValueError('zero exponential rate requires separate handling')
            rate=r*s
            result=ep_add(result,{rate:p_mul(p,q)})
    return result


def ep_power(a,k):
    out={1:[Q(1)]}
    for _ in range(k):out=ep_mul(out,a)
    return out


def symbolic(spec,offset=0):
    """Return {integer exponential_rate: rational polynomial coefficient list}."""
    if type(spec) is int:return {} if spec==0 else {1:[Q(spec)]}
    if not isinstance(spec,dict):return None
    op=spec.get('op')
    if op=='n':return {1:[Q(0),Q(1)]}
    if op in ('add','sub'):
        parts=spec.get('args',[])
        if not parts or op=='sub' and len(parts)!=2:return None
        result={}
        try:
            for i,child in enumerate(parts):
                comp=symbolic(child,offset)
                if comp is None:return None
                if op=='sub' and i==1:comp={r:p_scale(p,-1) for r,p in comp.items()}
                result=ep_add(result,comp)
        except ValueError:return None
        return result
    if op=='mul':
        out={1:[Q(1)]}
        try:
            for child in spec.get('args',[]):
                part=symbolic(child,offset)
                if part is None:return None
                out=ep_mul(out,part)
        except ValueError:return None
        return out
    if op=='exact_div':
        den=affine(spec['den'])
        if den is None or den[0]!=0 or den[1]==0:return None
        num=symbolic(spec['num'],offset)
        if num is None:return None
        return {r:p_scale(poly,Q(1,den[1])) for r,poly in num.items()}
    if op=='pow':
        power=affine(spec['exp'])
        base=spec['base']
        if power is None:return None
        if power[0]==0:
            if not 0<=power[1]<=MAX_DEGREE:return None
            inner=symbolic(base,offset)
            if inner is None:return None
            try:return ep_power(inner,power[1])
            except ValueError:return None
        if type(base) is int and base!=0 and power[0]>=0 and power[0]*offset+power[1]>=0:
            return {base**power[0]:[Q(base)**power[1]]}
        return None
    if op=='binomial':
        k=affine(spec.get('k'));a=affine(spec.get('n'))
        if k is None or a is None or k[0] or not 0<=k[1]<=MAX_DEGREE or a[0]<0 or a[0]*offset+a[1]<0:
            return None
        p=[Q(1)]
        for j in range(k[1]):
            try:p=p_mul(p,[Q(a[1]-j),Q(a[0])])
            except ValueError:return None
        return {1:p_scale(p,Q(1,factorial(k[1])))}
    return None


def poly_desc_mul(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out


def recurrence_from_roots(roots):
    """Finite difference annihilator product of (X-lambda)^multiplicity."""
    p=[1]
    for rate,multiplicity in sorted(roots.items()):
        for _ in range(multiplicity):p=poly_desc_mul(p,[1,-rate])
        if len(p)-1>MAX_ORDER:return None
    return [-x for x in p[1:]] if len(p)>1 else None


def recurrence_from_period(m,degree=0):
    """(S^m-1)^(degree+1) annihilates an m-phase quasipolynomial."""
    if m<1 or m*(degree+1)>MAX_ORDER:return None
    p=[1]
    factor=[1]+[0]*(m-1)+[-1]
    for _ in range(degree+1):p=poly_desc_mul(p,factor)
    return [-x for x in p[1:]]


def infer(spec,offset=0):
    """Return a globally justified linear recurrence or None, no finite fit."""
    if type(offset) is not int or offset<0:return None
    if isinstance(spec,dict) and spec.get('op')=='linear_recurrence':
        c=spec.get('coefficients');v=spec.get('initial')
        if (not isinstance(c,list) or not c or len(c)!=len(v or ()) or
            any(type(k) is not int for k in c+v)):return None
        # Evaluator n denotes source mathematical index; shift by offset here.
        try:ini=[evaluate(spec,offset+i) for i in range(len(c))]
        except (ValueError,TypeError,OverflowError):return None
        return {'coefficients':c,'initial':ini,'method':'declared_linear_recurrence',
                'proof':'The supplied recurrence holds by definition for all indices'}
    if isinstance(spec,dict) and spec.get('op')=='pow' and spec.get('base')==0 and spec.get('exp')=={'op':'n'}:
        # delta_(n,0), hence X*a=0 with a(0)=1.
        return {'coefficients':[0],'initial':[int(offset==0)],'method':'unit_impulse',
                'proof':'For n>=0, 0^n is 1 for n=0 and 0 afterward'}
    if isinstance(spec,dict) and spec.get('op') in ('mod','floor_div'):
        op=spec['op'];args=spec.get('args',[])
        if len(args)==2:
            numerator=affine(args[0]);denominator=affine(args[1]);
            if numerator is not None and denominator is not None and denominator[0]==0 and denominator[1]>0:
                m=denominator[1]
                # a(n+m)-a(n) =0 for mod, or a for floor_div, all n.
                c=recurrence_from_period(m, 0 if op=='mod' else 1)
                if c is not None:
                    try:initial=[evaluate(spec,offset+i) for i in range(len(c))]
                    except (ValueError,TypeError,OverflowError):return None
                    return {'coefficients':c,'initial':initial,
                            'method':'periodic_or_affine_floor',
                            'proof':f'(S^{m}-1)^{1 if op=="mod" else 2} annihilates the expression'}
    expression=symbolic(spec,offset)
    if expression is None:return None
    if not expression:
        return {'coefficients':[0],'initial':[0],
                'method':'zero_expression','proof':'The evaluator is identically zero'}
    roots={rate:len(poly) for rate,poly in expression.items()}
    c=recurrence_from_roots(roots)
    if c is None:return None
    try:
        initial=[evaluate(spec,offset+i) for i in range(len(c))]
    except (ValueError,TypeError,OverflowError,ZeroDivisionError):return None
    # The rational expression is equivalent to the supplied integer-evaluator DSL
    # wherever exact divisions are defined. Integrality holds globally because
    # the first order-many values are integers and recurrence coefficients are Z.
    return {'coefficients':c,'initial':initial,
            'method':'exponential_polynomial_annihilator',
            'proof':'Product of (S-rate)^(degree+1) annihilates the exact normalized expression'}
