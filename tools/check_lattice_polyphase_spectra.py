# Author: Komorebi P.
# Exact characteristic-polynomial and trace verification; requires SymPy.
import sympy as s
x=s.symbols('x')
Ds=[2,3,5,8,13]
H2=[];H4=[];T2=[];T4=[]
for w,d in enumerate(Ds,1):
    rows=[i for i in range(2**w) if not i&(i<<1)]
    M=s.Matrix([[int(not (i&j or (i<<1)&j)) for j in rows] for i in rows])
    p=M.charpoly(x).as_poly()
    assert M.rows==d and p.gcd(p.diff()).degree()==0 and p.TC()!=0
    t=[s.trace(M**k) for k in range(1,5)]
    assert t[0]==1 and t[1]==(2**(w+2)-(-1)**w)//3
    h=[s.Integer(1)]
    for j in range(1,5):
        h.append(sum(t[k-1]*h[j-k] for k in range(1,j+1))/j)
    H2.append(h[2]);H4.append(h[4]);T2.append(t[1]);T4.append(t[3])
    if w==3: assert p.rem(s.Poly((x+1)*(x**4-2*x**3-3*x**2-x+1),x)).is_zero
    if w==5:
        f=x**4+2*x**3-2*x+1
        assert p.rem(s.Poly(f,x)).is_zero
        assert s.expand((x*x+(1+s.I)*x-1)*(x*x+(1-s.I)*x-1)-f)==0
    print(w,d,s.factor(p.as_expr()),'traces',t,'h2,h4',h[2],h[4])
for W in range(3,11):
    w=W//2-1
    if W%2: v=2*H2[w]*H2[w+1]-T2[w]*T2[w+1]
    else: v=2*H4[w]-T4[w]
    if W==6: v-=1
    if W==9: v+=2*H2[3]
    if W==10: v+=2*H2[4]
    assert v==[-3,5,-19,10,-99,13,-397,59][W-3]
    print('width',W,'trace2',v)
