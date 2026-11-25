"""Unified cycle–path transfers, exact integer and rational checks. Author: Komorebi P."""
from math import comb
from fractions import Fraction
from check_cycle_path import walks, recurrence_poly, apply, odd_remainder
from check_cycle_path_triangular import forward, inverse


def rem(p, q):
    p = list(p)
    assert q[-1] == 1
    while len(p) >= len(q):
        a = len(p) - len(q)
        lead = p[-1]
        for j, c in enumerate(q):
            p[a+j] -= lead*c
        p.pop()
    while len(p)>1 and p[-1] == 0:
        p.pop()
    return p


def mul(p, q):
    out = [0]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):
            out[i+j] += a*b
    return out


def shift(p, a):
    return [sum(p[j]*comb(j,i)*a**(j-i) for j in range(i,len(p))) for i in range(len(p))]


def cycle_minimal(m):
    r=m//2
    if m%2:
        u=recurrence_poly(r,1)
        v=recurrence_poly(r-1,1)
        return mul([-2,1],[c+(v[i] if i<len(v) else 0) for i,c in enumerate(u)])
    return mul([-4,0,1],recurrence_poly(r-1,1))


def uniform_filter(m):
    p=recurrence_poly(m-2,2)
    q=recurrence_poly(m,2)
    d=[(p[i] if i<len(p) else 0)-v for i,v in enumerate(q)]
    r=[0]*(m-2)+d
    assert all(v==0 for v in r[1::2])
    return rem(r[::2],shift(cycle_minimal(m),-2))


def lift(a):
    return [sum(comb(n,j)*2**(n-j)*a[j] for j in range(n+1)) for n in range(len(a))]


def matrix_row(k,i,j):
    p=recurrence_poly(abs(i-j),2)
    q=recurrence_poly(i+j,2)
    row=[0]*((k+i+j)//2+1)
    for s,v in enumerate(q):
        d=(p[s] if s<len(p) else 0)-v
        if (k+s)%2==0:
            h=(k+s)//2
            for r in range(h+1):
                row[r]+=d*comb(h,r)*2**(h-r)
    return row


def partition_formula(g,n,k=1):
    if n==0:
        return Fraction(1)
    if k>n:
        return Fraction(0)
    total=Fraction(0)
    power=Fraction(1)
    for r in range(n//k+1):
        if r:
            power*=Fraction(g[k],2*k*r)
        total+=power*partition_formula(g,n-k*r,k+1)
    return total


FILTERS={3:[4,-1],4:[0,4,-1],5:[-4,9,-2],6:[0,-12,11,-2],
         7:[8,-46,31,-5],8:[0,32,-72,36,-5],9:[-20,197,-272,112,-14],
         10:[0,-100,385,-370,126,-14],11:[56,-834,1873,-1401,414,-42],
         12:[0,336,-1924,2944,-1773,456,-42],
         13:[-168,3514,-11472,13255,-6743,1551,-132]}


def main():
    if not __debug__:
        raise RuntimeError('Do not use -O.')
    counts=dict(cycle_binomial=0,uniform=0,coefficients=0,matrix=0,partitions=0,mixed_7_8=0)
    for m in range(3,101):
        N=30
        a=[r[0] for r in walks(m,N+m,0,True)]
        h=lift(a)
        b=[r[-1] for r in walks(m-1,2*N+m-2,0)][m-2::2]
        for k in range(N+1):
            assert a[k]==sum(comb(k,j) for j in range(k+1) if (2*j-k)%m==0),(m,k)
            counts['cycle_binomial']+=1
        R=uniform_filter(m)
        assert len(R)-1<=m//2
        if m in FILTERS:
            assert R==FILTERS[m],(m,R)
            counts['coefficients']+=1
        for n in range(N+1):
            assert apply(R,h,n)==2*b[n],(m,n,R)
            counts['uniform']+=1
        g=[m*v-4**n for n,v in enumerate(h)]
        for n in range(9):
            assert partition_formula(g,n)==b[n],(m,n)
            counts['partitions']+=1
        if m<=16:
            for i in range(1,m):
                direct=walks(m-1,8,i-1)
                for j in range(1,m):
                    for k in range(9):
                        row=matrix_row(k,i,j)
                        assert sum(c*a[r] for r,c in enumerate(row))==2*direct[k][j-1],(m,k,i,j)
                        counts['matrix']+=1
    a=lambda n:2**n+4**n
    b=[r[-1] for r in walks(7,2*82+6,0)][6::2]
    D=lambda n:b[n+2]-4*b[n+1]+2*b[n]
    for n in range(41):
        assert 2*b[n]==sum(comb(n+2,2*j)*(4*a(n+1-j)-a(n+2-j)) for j in range(1,(n+2)//2+1)),n
        assert 4*a(n)==D(n)+D(2*n),n
        counts['mixed_7_8']+=2
    print(counts)
    print('PASS:',sum(counts.values()),'explicit exact comparisons')

if __name__=='__main__':
    main()
