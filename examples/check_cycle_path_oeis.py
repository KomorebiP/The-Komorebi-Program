from math import comb
# First 10 source terms from the retrieved OEIS entries. All offsets are original.
# (cycle ID, first index, bisection?, cycle terms, path ID, first index, n-to-entry shift, path terms)
rows = [
(3,'A078008',0,False,[1,0,2,2,6,10,22,42,86,170],'A000012',0,0,[1]*10),
(4,'A199573',0,False,[1,0,2,0,8,0,32,0,128,0],'A000079',0,0,[2**i for i in range(10)]),
(5,'A054877',0,False,[1,0,2,0,6,2,20,14,70,72],'A001906',0,1,[0,1,3,8,21,55,144,377,987,2584]),
(6,'A047849',0,True,[1,2,6,22,86,342,1366,5462,21846,87382],'A003462',0,1,[0,1,4,13,40,121,364,1093,3280,9841]),
(7,'A094659',0,False,[1,0,2,0,6,0,20,2,70,18],'A005021',0,0,[1,5,19,66,221,728,2380,7753,25213,81927]),
(8,'A063376',-1,True,[1,2,6,20,72,272,1056,4160,16512,65792],'A005022',0,0,[1,6,26,100,364,1288,4488,15504,53296,182688]),
(9,'A094233',0,False,[1,0,2,0,6,0,20,0,70,2,252,22,924,156,3432,910,12870,4760,48622,23256,184796,108528,705894,490314,2708204,2163150,10430500,9373652,40313160,40060078,156305070,169345560,607812102,709645552,2369918628,2952780320],'A005023',1,0,[7,34,143,560,2108,7752,28101,100947,360526,1282735,4552624,16131656,57099056,201962057,714012495,2523515514,8916942687,31504028992,111295205284,393151913464,1388758662221,4905479957435,17327203698086,61202661233823,216176614077600]),
]
def walk(size,k,cycle):
    a=[1]+[0]*(size-1)
    for _ in range(k):
        a=[(a[(j-1)%size] if cycle or j else 0)+(a[(j+1)%size] if cycle or j+1<size else 0) for j in range(size)]
    return a[0 if cycle else -1]
def A(m,k):return walk(m,k,True)
def B(m,n):return walk(m-1,2*n+m-2,False) if n>=0 else 0
c=p=t=0
for m,aid,off,half,av,bid,boff,shift,bv in rows:
    # A063376's first index -1 is the zeroth even moment.
    for i,v in enumerate(av):
        k=2*i if half else i
        assert A(m,k)==v,(aid,i,v,A(m,k));c+=1
    for i,v in enumerate(bv):
        n=i+boff-shift
        assert B(m,n)==v,(bid,i,v,B(m,n));p+=1
        if n>=0:
            L=2*n+m-2
            h=lambda r:sum(comb(r,j)*2**(r-j)*A(m,j) for j in range(r+1))
            d2=(h(L//2+1)-4*h(L//2)) if L%2==0 else 0
            assert 2*v==A(m,L+2)-4*A(m,L)-d2,(m,n,v);t+=1
    print(aid,bid,'PASS',len(av),len(bv))
q=[16,-24,-64,-6,21];av=rows[-1][4];bv=rows[-1][-1]
nseed=0
for n in range(min((len(av)-5)//2+1,len(bv))):
    assert sum(q[j]*av[2*n+j] for j in range(5))==2*bv[n]
    nseed+=1
print('cycle terms',c,'path terms',p,'transfer terms',t,'seed using only source records',nseed,'total',c+p+t+nseed)
# General table check: A259475 row r=p-1 via reciprocal determinant.
from fractions import Fraction
for m in range(3,31):
    psize=m-1
    q=[(-1)**j*comb(psize-j,j) for j in range(psize//2+1)]
    v=[1]
    for n in range(1,21):v.append(-sum(q[j]*v[n-j] for j in range(1,min(n,len(q)-1)+1)))
    for n,b in enumerate(v):assert B(m,n)==b
print('General generating function 588 checks passed')
