# Author: Komorebi P.
# Standard-library exact checks for the direct cyclic graph and lattice transfers.
from collections import Counter, defaultdict
from itertools import combinations_with_replacement, product
from math import comb, gcd
import json


def masks(w):
    return [i for i in range(1 << w) if not i & (i << 1)]


def strip_edges(w, z=1):
    R = masks(w)
    return [{j: z ** b.bit_count() for j, b in enumerate(R)
             if not (a & b or (a << 1) & b) and z ** b.bit_count()}
            for a in R]


def advance(v, edges):
    out = defaultdict(int)
    for i, c in v.items():
        for j, e in edges[i].items():
            out[j] += c * e
    return dict(out)


def strip_counts(w, H, z=1):
    E = strip_edges(w, z)
    v, out = {0: 1}, [1]
    for _ in range(H):
        v = advance(v, E)
        out.append(sum(v.values()))
    return out


def sym_edges(E, k):
    # Ordered assignments from any representative tuple, then sort the targets.
    # The quotient weights are independent of the chosen representative.
    states = list(combinations_with_replacement(range(len(E)), k))
    ind = {a: i for i, a in enumerate(states)}
    adj = []
    for a in states:
        r = Counter()
        for dest in product(*(E[i].items() for i in a)):
            b = tuple(sorted(j for j, c in dest))
            weight = 1
            for j, c in dest:
                weight *= c
            r[ind[b]] += weight
        adj.append(dict(r))
    return adj


def row_group(W, q, z=1):
    w, b = divmod(W, q)
    A = sym_edges(strip_edges(w, z), q-b)
    B = sym_edges(strip_edges(w+1, z), b)
    d = len(B)
    E = [{j*d+k: a*c for j, a in row.items() for k, c in col.items()}
         for row in A for col in B]
    assert len(E) == comb(len(masks(w))+q-b-1, q-b)*comb(len(masks(w+1))+b-1, b)
    return E


def direct_counts(W, q, H, z=1):
    E = row_group(W, q, z)
    D = len(E)
    # Vertices are q-tuples, plus one terminal. Advance the first coordinate
    # and rotate it to the end. The terminal is reached by one final unit arc.
    v, out = {(0,)*q: 1}, [1]
    for _ in range(H):
        nxt = defaultdict(int)
        for a, c in v.items():
            for j, weight in E[a[0]].items():
                nxt[a[1:]+(j,)] += c*weight
        v = dict(nxt)
        out.append(sum(v.values()))
    return out, dict(row_states=D, vertices=D**q+1,
                     distinct_arcs=D**(q-1)*sum(map(len,E))+D**q,
                     max_weight=max(1,max((v for row in E for v in row.values()),default=0)))


def formula(H, W, q, z=1):
    h, a = divmod(H,q)
    w, b = divmod(W,q)
    A, B = strip_counts(w,h+1,z), strip_counts(w+1,h+1,z)
    return A[h]**((q-a)*(q-b))*A[h+1]**(a*(q-b))*B[h]**((q-a)*b)*B[h+1]**(a*b)


def brute(H, W, q, z=1):
    edges=[]
    for i in range(H):
        for j in range(W):
            for a,b in ((q,0),(0,q),(q,q)):
                if i+a<H and j+b<W:
                    edges.append((1<<(i*W+j))|(1<<((i+a)*W+j+b)))
    return sum(z**v.bit_count() for v in range(1<<(H*W)) if all(v&e!=e for e in edges))


def matrix_mul(A,B):
    return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]


def traces(w, H):
    E=strip_edges(w)
    d=len(E)
    M=[[row.get(j,0) for j in range(d)] for row in E]
    X=[[int(i==j) for j in range(d)] for i in range(d)]
    t=[d]
    for _ in range(H):
        X=matrix_mul(X,M)
        t.append(sum(X[i][i] for i in range(d)))
    return t


def homogeneous(t,j,k):
    h=[1]
    for a in range(1,k+1):
        v=sum(t[i*j]*h[a-i] for i in range(1,a+1))
        assert v%a==0
        h.append(v//a)
    return h[-1]


def spectral_moment(W,n,T):
    a,b=T[W//2],T[(W+1)//2]
    if n%2:
        v=a[n]*b[n] if W%2 else a[2*n]
    elif W%2:
        j=n//2
        v=2*homogeneous(a,j,2)*homogeneous(b,j,2)-a[n]*b[n]
    else:
        j=n//2
        v=2*homogeneous(a,j,4)-a[2*n]
    if W==6:
        v-=1
    if W in (9,10) and n%2==0:
        v-=2*(-1)**(n//2)*homogeneous(a,n//2,2)
    return v


def run():
    direct, interp, exhaustive=0,0,0
    sizes=[]
    for q in (2,3,4):
        for W in (range(3,11) if q==2 else range(2,6)):
            for z in (1,2):
                got,info=direct_counts(W,q,12,z)
                assert got==[formula(H,W,q,z) for H in range(13)]
                direct+=13
                if q==2 and z==1:
                    sizes.append(dict(width=W,**info))
        for H in range(7):
            for W in range(7):
                h,a=divmod(H,q);w,b=divmod(W,q)
                for z in (0,1,2):
                    corner=1
                    for i,j in product((0,1),repeat=2):
                        corner*=formula(q*(h+i),q*(w+j),q,z)**((a if i else q-a)*(b if j else q-b))
                    assert formula(H,W,q,z)**(q*q)==corner
                    interp+=1
                    if H*W<=12:
                        assert formula(H,W,q,z)==brute(H,W,q,z)
                        exhaustive+=1
    T={w:traces(w,128) for w in range(1,6)}
    results=[]
    for W,r in zip(range(3,11),(30,27,165,134,1040,652,6376,3445)):
        s=[0]+[spectral_moment(W,n,T) for n in range(1,65)]
        # Primitive periodic orbit counts, without factoring large integers.
        prim=[0]
        for n in range(1,65):
            v=s[n]-sum(d*prim[d] for d in range(1,n) if n%d==0)
            assert v%n==0
            prim.append(v//n)
        obstruction=next((n for n in range(1,65) if prim[n]<0),None)
        results.append(dict(width=W,order=r,trace1=s[1],trace2=s[2],
                            primitive_orbit2=prim[2],first_negative_primitive=obstruction,
                            minimum_vertices=[r+1,r+1] if obstruction else [r,r+1]))
    assert results[5]['primitive_orbit2']==-4 and results[5]['minimum_vertices']==[653,653]
    assert [r['width'] for r in results if r['first_negative_primitive'] is None]==[4,6,10]
    return dict(direct_walk_checks=direct,interpolation_checks=interp,
                brute_force_checks=exhaustive,trace_orbit_checks=8*64,
                direct_graph_sizes=sizes,minimum_graph_sizes=results)


if __name__=='__main__':
    print(json.dumps(run(),indent=2))
