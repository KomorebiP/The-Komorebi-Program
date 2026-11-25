# Structural-core graph formula catalogue — v31–v32

**Author: Komorebi P.**

288 individually written rational model records, 262 distinct rational functions. Index `n` is the vertex count, starting at zero. There are 196 v32 records and 92 v31 records; some classes overlap. Only ten inherited rooted-tree records are OEIS-bound in this collection. No new OEIS admissions or literature-priority claims.

## Common explicit a(n) formula

Every entry specifies the integers $s,b$, the polynomial $R$, and the normalized denominator $Q$, such that $G(x)=x^sR(x)/Q(x)$. For $n<s$ the count is zero. Otherwise set $B=2^{n-s+b}$ and use

$$a(n)=\left\lfloor\frac{B^{n-s}R(1/B)}{Q(1/B)}\right\rfloor\bmod B.$$

This is an exact integer floor-and-remainder formula. Write $r=\deg Q$, $M=\sum_i|[x^i]R|$. The constant $b=r+2+\operatorname{bitlength}(M)$. Since all denominator roots are roots of unity, coefficients of $1/Q$ have absolute value bounded by $\binom{j+r-1}{r-1}\le 2^{j+r-1}$. Hence the nonnegative coefficients of $R/Q$ are at most $M2^{j+r-1}$. The base $B$ exceeds all digits through index $n-s$, and the remaining tail after the desired digit is less than one. Thus the formula holds at every index. Classical coefficient packing, not a speed claim.

$\Phi_1(x)=1-x$ and $\Phi_d$ ($d>1$) denotes the usual cyclotomic polynomial. The full factors are in the appendix. A numerator coefficient block marked `i-j` lists the coefficients of $x^i$ through $x^j$ in $R$, in ascending order. All internal zeros are retained. Degree labels `3 (2)` mean two core vertices of degree three; for branching profiles they refer to children counts. All orders and periods are eventual. The graph classes count connected unlabeled simple graphs and tree classes count unlabeled nonplane trees. The full universal structural laws and their boundaries are included in the source proofs and PDF.


## Connected graphs


### G01 — g=0, k=2

Order 1; period 1; source v32/GRAPH_MODELS.json, record 0.

$$B=2^{n+2},\quad a(n)=0\ (n<2).$$

$$a(n)=\left\lfloor\frac{B^{n-2}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 2).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)$$


### G02 — g=0, k=3

Order 6; period 6; source v32/GRAPH_MODELS.json, record 1.

$$B=2^{n+5},\quad a(n)=0\ (n<4).$$

$$a(n)=\left\lfloor\frac{B^{n-4}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 4).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{3}\Phi_{2}(x)\Phi_{3}(x)$$


### G03 — g=0, k=4

Order 11; period 12; source v32/GRAPH_MODELS.json, record 2.

$$B=2^{n+10},\quad a(n)=0\ (n<5).$$

$$a(n)=\left\lfloor\frac{B^{n-5}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 5).$$

$$R(x)=1+x^{3}+x^{5}$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)^{2}\Phi_{3}(x)\Phi_{4}(x)$$


### G04 — g=0, k=5

Order 18; period 60; source v32/GRAPH_MODELS.json, record 3.

$$B=2^{n+19},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$\begin{aligned}R(x)&=1+x^{2}+3x^{3}+4x^{4}+4x^{5}+5x^{6}\\&+4x^{7}+4x^{8}+2x^{9}+2x^{10}\end{aligned}$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{7}\Phi_{2}(x)^{3}\Phi_{3}(x)\Phi_{4}(x)\\&\times \Phi_{5}(x)\end{aligned}$$


### G05 — g=1, k=0

Order 1; period 1; source v32/GRAPH_MODELS.json, record 4.

$$B=2^{n+1},\quad a(n)=0\ (n<3).$$

$$a(n)=\left\lfloor\frac{B^{n-3}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 3).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)$$


### G06 — g=1, k=1

Order 2; period 1; source v32/GRAPH_MODELS.json, record 5.

$$B=2^{n+1},\quad a(n)=0\ (n<4).$$

$$a(n)=\left\lfloor\frac{B^{n-4}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 4).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{2}$$


### G07 — g=1, k=2

Order 6; period 2; source v32/GRAPH_MODELS.json, record 6.

$$B=2^{n+6},\quad a(n)=0\ (n<5).$$

$$a(n)=\left\lfloor\frac{B^{n-5}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 5).$$

$$R(x)=2+2x-x^{2}$$

$$Q(x)=\Phi_{1}(x)^{4}\Phi_{2}(x)^{2}$$


### G08 — g=1, k=3

Order 12; period 6; source v32/GRAPH_MODELS.json, record 7.

$$B=2^{n+14},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=3+5x+8x^{2}+9x^{3}+5x^{4}+2x^{5}+x^{6}$$

$$Q(x)=\Phi_{1}(x)^{6}\Phi_{2}(x)^{2}\Phi_{3}(x)^{2}$$


### G09 — g=1, k=4

Order 18; period 12; source v32/GRAPH_MODELS.json, record 8.

$$B=2^{n+21},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$\begin{aligned}R(x)&=4+9x+16x^{2}+33x^{3}+40x^{4}+48x^{5}\\&+40x^{6}+34x^{7}+17x^{8}+10x^{9}+x^{10}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{8}\Phi_{2}(x)^{4}\Phi_{3}(x)\Phi_{4}(x)^{2}$$


### G10 — g=2, k=0

Order 5; period 3; source v32/GRAPH_MODELS.json, record 9.

$$B=2^{n+5},\quad a(n)=0\ (n<4).$$

$$a(n)=\left\lfloor\frac{B^{n-4}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 4).$$

$$R(x)=1+x$$

$$Q(x)=\Phi_{1}(x)^{3}\Phi_{3}(x)$$


### G11 — g=2, k=1

Order 9; period 6; source v32/GRAPH_MODELS.json, record 10.

$$B=2^{n+11},\quad a(n)=0\ (n<5).$$

$$a(n)=\left\lfloor\frac{B^{n-5}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 5).$$

$$R(x)=2+5x+4x^{2}+3x^{3}+x^{4}+x^{5}-x^{6}$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)^{2}\Phi_{3}(x)$$


### G12 — g=2, k=2

Order 14; period 12; source v32/GRAPH_MODELS.json, record 11.

$$B=2^{n+18},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$\begin{aligned}R(x)&=5+12x+21x^{2}+28x^{3}+30x^{4}+20x^{5}\\&+14x^{6}+3x^{7}-2x^{9}+x^{10}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{7}\Phi_{2}(x)^{3}\Phi_{3}(x)\Phi_{4}(x)$$


### G13 — g=2, k=3

Order 23; period 12; source v32/GRAPH_MODELS.json, record 12.

$$B=2^{n+31},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=\sum_{j=0}^{16} c_jx^j.$$

```text
  0-16   8, 35, 97, 218, 371, 552, 676, 773, 724, 658, 470, 323, 155, 71, 14, 4, -1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{9}\Phi_{2}(x)^{4}\Phi_{3}(x)^{3}\Phi_{4}(x)\\&\times \Phi_{6}(x)\end{aligned}$$


### G14 — g=3, k=0

Order 15; period 12; source v32/GRAPH_MODELS.json, record 13.

$$B=2^{n+20},\quad a(n)=0\ (n<4).$$

$$a(n)=\left\lfloor\frac{B^{n-4}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 4).$$

$$R(x)=\sum_{j=0}^{13} c_jx^j.$$

```text
  0-13   1, 2, 6, 14, 20, 21, 21, 12, 8, 4, 2, 0, 1, -1
```

$$Q(x)=\Phi_{1}(x)^{6}\Phi_{2}(x)^{3}\Phi_{3}(x)^{2}\Phi_{4}(x)$$


### G15 — g=3, k=1

Order 17; period 12; source v32/GRAPH_MODELS.json, record 14.

$$B=2^{n+24},\quad a(n)=0\ (n<5).$$

$$a(n)=\left\lfloor\frac{B^{n-5}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 5).$$

$$R(x)=\sum_{j=0}^{14} c_jx^j.$$

```text
  0-14   1, 6, 22, 56, 87, 114, 113, 89, 53, 28, 6, 2, 0, -2, 1
```

$$Q(x)=\Phi_{1}(x)^{8}\Phi_{2}(x)^{3}\Phi_{3}(x)^{2}\Phi_{4}(x)$$


### G16 — g=3, k=2

Order 23; period 12; source v32/GRAPH_MODELS.json, record 15.

$$B=2^{n+34},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=\sum_{j=0}^{18} c_jx^j.$$

```text
  0-18   2, 19, 96, 312, 747, 1381, 2119, 2652, 2860, 2545, 1962, 1201, 638, 229, 76, 7, 1, 2, -1
```

$$Q(x)=\Phi_{1}(x)^{10}\Phi_{2}(x)^{5}\Phi_{3}(x)^{2}\Phi_{4}(x)^{2}$$


### G17 — g=4, k=0

Order 29; period 60; source v32/GRAPH_MODELS.json, record 16.

$$B=2^{n+41},\quad a(n)=0\ (n<5).$$

$$a(n)=\left\lfloor\frac{B^{n-5}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 5).$$

$$R(x)=\sum_{j=0}^{23} c_jx^j.$$

```text
  0-16   2, 11, 33, 105, 247, 485, 835, 1288, 1733, 2178, 2431, 2525, 2364, 2064, 1589, 1163, 727
 17-23   429, 203, 98, 26, 14, -2, 2
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{9}\Phi_{2}(x)^{4}\Phi_{3}(x)^{3}\Phi_{4}(x)^{2}\\&\times \Phi_{5}(x)\Phi_{6}(x)\end{aligned}$$


## Bipartite connected graphs


### B01 — g=0, k=2

Order 1; period 1; source v32/BIPARTITE_MODELS.json, record 0.

$$B=2^{n+2},\quad a(n)=0\ (n<2).$$

$$a(n)=\left\lfloor\frac{B^{n-2}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 2).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)$$

Same rational function as G01.


### B02 — g=0, k=3

Order 6; period 6; source v32/BIPARTITE_MODELS.json, record 1.

$$B=2^{n+5},\quad a(n)=0\ (n<4).$$

$$a(n)=\left\lfloor\frac{B^{n-4}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 4).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{3}\Phi_{2}(x)\Phi_{3}(x)$$

Same rational function as G02.


### B03 — g=0, k=4

Order 11; period 12; source v32/BIPARTITE_MODELS.json, record 2.

$$B=2^{n+10},\quad a(n)=0\ (n<5).$$

$$a(n)=\left\lfloor\frac{B^{n-5}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 5).$$

$$R(x)=1+x^{3}+x^{5}$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)^{2}\Phi_{3}(x)\Phi_{4}(x)$$

Same rational function as G03.


### B04 — g=0, k=5

Order 18; period 60; source v32/BIPARTITE_MODELS.json, record 3.

$$B=2^{n+19},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$\begin{aligned}R(x)&=1+x^{2}+3x^{3}+4x^{4}+4x^{5}+5x^{6}\\&+4x^{7}+4x^{8}+2x^{9}+2x^{10}\end{aligned}$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{7}\Phi_{2}(x)^{3}\Phi_{3}(x)\Phi_{4}(x)\\&\times \Phi_{5}(x)\end{aligned}$$

Same rational function as G04.


### B05 — g=1, k=0

Order 2; period 2; source v32/BIPARTITE_MODELS.json, record 4.

$$B=2^{n+1},\quad a(n)=0\ (n<4).$$

$$a(n)=\left\lfloor\frac{B^{n-4}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 4).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)\Phi_{2}(x)$$


### B06 — g=1, k=1

Order 3; period 2; source v32/BIPARTITE_MODELS.json, record 5.

$$B=2^{n+1},\quad a(n)=0\ (n<5).$$

$$a(n)=\left\lfloor\frac{B^{n-5}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 5).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{2}\Phi_{2}(x)$$


### B07 — g=1, k=2

Order 7; period 2; source v32/BIPARTITE_MODELS.json, record 6.

$$B=2^{n+6},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=3+x-x^{2}$$

$$Q(x)=\Phi_{1}(x)^{4}\Phi_{2}(x)^{3}$$


### B08 — g=1, k=3

Order 15; period 6; source v32/BIPARTITE_MODELS.json, record 7.

$$B=2^{n+16},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$\begin{aligned}R(x)&=4+3x+7x^{2}+3x^{3}+7x^{4}+5x^{5}+3x^{6}\\&+x^{8}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{6}\Phi_{2}(x)^{3}\Phi_{3}(x)^{2}\Phi_{6}(x)$$


### B09 — g=1, k=4

Order 19; period 12; source v32/BIPARTITE_MODELS.json, record 8.

$$B=2^{n+21},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$\begin{aligned}R(x)&=8+8x+26x^{2}+33x^{3}+48x^{4}+41x^{5}\\&+41x^{6}+26x^{7}+15x^{8}+6x^{9}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{8}\Phi_{2}(x)^{5}\Phi_{3}(x)\Phi_{4}(x)^{2}$$


### B10 — g=2, k=0

Order 6; period 6; source v32/BIPARTITE_MODELS.json, record 9.

$$B=2^{n+4},\quad a(n)=0\ (n<5).$$

$$a(n)=\left\lfloor\frac{B^{n-5}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 5).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{3}\Phi_{2}(x)\Phi_{3}(x)$$


### B11 — g=2, k=1

Order 12; period 12; source v32/BIPARTITE_MODELS.json, record 10.

$$B=2^{n+13},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$\begin{aligned}R(x)&=2+2x+3x^{2}+3x^{3}+3x^{4}+2x^{5}+x^{6}\\&-x^{8}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)^{3}\Phi_{3}(x)\Phi_{4}(x)$$


### B12 — g=2, k=2

Order 17; period 12; source v32/BIPARTITE_MODELS.json, record 11.

$$B=2^{n+20},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=\sum_{j=0}^{12} c_jx^j.$$

```text
  0-12   5, 6, 14, 22, 23, 28, 18, 13, 4, 0, -1, -1, 1
```

$$Q(x)=\Phi_{1}(x)^{7}\Phi_{2}(x)^{4}\Phi_{3}(x)\Phi_{4}(x)^{2}$$


### B13 — g=2, k=3

Order 26; period 12; source v32/BIPARTITE_MODELS.json, record 12.

$$B=2^{n+33},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=\sum_{j=0}^{18} c_jx^j.$$

```text
  0-18   9, 21, 73, 145, 282, 414, 580, 663, 728, 679, 581, 435, 281, 160, 68, 26, 3, 1, -1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{9}\Phi_{2}(x)^{5}\Phi_{3}(x)^{3}\Phi_{4}(x)^{2}\\&\times \Phi_{6}(x)\end{aligned}$$


### B14 — g=3, k=0

Order 21; period 12; source v32/BIPARTITE_MODELS.json, record 13.

$$B=2^{n+24},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=\sum_{j=0}^{17} c_jx^j.$$

```text
  0-17   2, 2, 6, 5, 12, 12, 14, 16, 13, 12, 8, 5, 2, 3, 0, 0, 0, -1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{6}\Phi_{2}(x)^{5}\Phi_{3}(x)^{2}\Phi_{4}(x)^{2}\\&\times \Phi_{6}(x)\end{aligned}$$


### B15 — g=3, k=1

Order 23; period 12; source v32/BIPARTITE_MODELS.json, record 14.

$$B=2^{n+28},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=\sum_{j=0}^{18} c_jx^j.$$

```text
  0-18   4, 5, 21, 26, 56, 63, 82, 82, 77, 64, 47, 28, 14, 9, -2, 1, -1, -1, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{8}\Phi_{2}(x)^{5}\Phi_{3}(x)^{2}\Phi_{4}(x)^{2}\\&\times \Phi_{6}(x)\end{aligned}$$


### B16 — g=3, k=2

Order 29; period 12; source v32/BIPARTITE_MODELS.json, record 15.

$$B=2^{n+38},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=\sum_{j=0}^{22} c_jx^j.$$

```text
  0-16   12, 26, 122, 229, 546, 838, 1348, 1699, 2085, 2204, 2139, 1900, 1454, 1072, 619, 353, 144
 17-22   45, 15, -3, 1, 1, -1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{10}\Phi_{2}(x)^{7}\Phi_{3}(x)^{2}\Phi_{4}(x)^{3}\\&\times \Phi_{6}(x)\end{aligned}$$


### B17 — g=4, k=0

Order 43; period 120; source v32/BIPARTITE_MODELS.json, record 16.

$$B=2^{n+54},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=\sum_{j=0}^{36} c_jx^j.$$

```text
  0-18   1, 2, 4, 19, 36, 73, 132, 218, 325, 467, 631, 799, 987, 1140, 1299, 1417, 1507, 1518, 1534
 19-36   1473, 1370, 1239, 1088, 909, 729, 568, 404, 282, 176, 107, 54, 27, 10, 4, 1, -2, 2
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{9}\Phi_{2}(x)^{6}\Phi_{3}(x)^{3}\Phi_{4}(x)^{3}\\&\times \Phi_{5}(x)\Phi_{6}(x)^{2}\Phi_{8}(x)\Phi_{12}(x)\end{aligned}$$


## Connected graphs: degree profiles


### D01 — g=0, k=2; core degrees: 1 (2)

Order 1; period 1; source v32/PROFILE_MODELS.json, record 0.

$$B=2^{n+2},\quad a(n)=0\ (n<2).$$

$$a(n)=\left\lfloor\frac{B^{n-2}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 2).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)$$

Same rational function as G01.


### D02 — g=0, k=3; core degrees: 1 (3), 3 (1)

Order 6; period 6; source v32/PROFILE_MODELS.json, record 1.

$$B=2^{n+5},\quad a(n)=0\ (n<4).$$

$$a(n)=\left\lfloor\frac{B^{n-4}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 4).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{3}\Phi_{2}(x)\Phi_{3}(x)$$

Same rational function as G02.


### D03 — g=0, k=4; core degrees: 1 (4), 3 (2)

Order 9; period 4; source v32/PROFILE_MODELS.json, record 2.

$$B=2^{n+7},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=1-x+x^{2}$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)^{2}\Phi_{4}(x)$$


### D04 — g=0, k=4; core degrees: 1 (4), 4 (1)

Order 10; period 12; source v32/PROFILE_MODELS.json, record 3.

$$B=2^{n+8},\quad a(n)=0\ (n<5).$$

$$a(n)=\left\lfloor\frac{B^{n-5}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 5).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{4}\Phi_{2}(x)^{2}\Phi_{3}(x)\Phi_{4}(x)$$


### D05 — g=0, k=5; core degrees: 1 (5), 3 (3)

Order 12; period 4; source v32/PROFILE_MODELS.json, record 4.

$$B=2^{n+9},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=1-x+2x^{2}$$

$$Q(x)=\Phi_{1}(x)^{7}\Phi_{2}(x)^{3}\Phi_{4}(x)$$


### D06 — g=0, k=5; core degrees: 1 (5), 3 (1), 4 (1)

Order 10; period 6; source v32/PROFILE_MODELS.json, record 5.

$$B=2^{n+6},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{6}\Phi_{2}(x)^{2}\Phi_{3}(x)$$


### D07 — g=0, k=5; core degrees: 1 (5), 5 (1)

Order 15; period 60; source v32/PROFILE_MODELS.json, record 6.

$$B=2^{n+12},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=1$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{5}\Phi_{2}(x)^{2}\Phi_{3}(x)\Phi_{4}(x)\\&\times \Phi_{5}(x)\end{aligned}$$


### D08 — g=1, k=1; core degrees: 1 (1), 3 (1)

Order 2; period 1; source v32/PROFILE_MODELS.json, record 7.

$$B=2^{n+1},\quad a(n)=0\ (n<4).$$

$$a(n)=\left\lfloor\frac{B^{n-4}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 4).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{2}$$

Same rational function as G06.


### D09 — g=1, k=2; core degrees: 1 (2), 3 (2)

Order 6; period 2; source v32/PROFILE_MODELS.json, record 8.

$$B=2^{n+5},\quad a(n)=0\ (n<5).$$

$$a(n)=\left\lfloor\frac{B^{n-5}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 5).$$

$$R(x)=1+2x$$

$$Q(x)=\Phi_{1}(x)^{4}\Phi_{2}(x)^{2}$$


### D10 — g=1, k=2; core degrees: 1 (2), 4 (1)

Order 4; period 2; source v32/PROFILE_MODELS.json, record 9.

$$B=2^{n+2},\quad a(n)=0\ (n<5).$$

$$a(n)=\left\lfloor\frac{B^{n-5}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 5).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{3}\Phi_{2}(x)$$


### D11 — g=1, k=3; core degrees: 1 (3), 3 (3)

Order 12; period 6; source v32/PROFILE_MODELS.json, record 10.

$$B=2^{n+14},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=1+x+5x^{2}+9x^{3}+9x^{4}+5x^{5}+3x^{6}$$

$$Q(x)=\Phi_{1}(x)^{6}\Phi_{2}(x)^{2}\Phi_{3}(x)^{2}$$


### D12 — g=1, k=3; core degrees: 1 (3), 3 (1), 4 (1)

Order 9; period 6; source v32/PROFILE_MODELS.json, record 11.

$$B=2^{n+9},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=1+4x+4x^{2}+2x^{3}$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)^{2}\Phi_{3}(x)$$


### D13 — g=1, k=3; core degrees: 1 (3), 5 (1)

Order 7; period 6; source v32/PROFILE_MODELS.json, record 12.

$$B=2^{n+4},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{4}\Phi_{2}(x)\Phi_{3}(x)$$


### D14 — g=1, k=4; core degrees: 1 (4), 3 (4)

Order 16; period 4; source v32/PROFILE_MODELS.json, record 13.

$$B=2^{n+17},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$\begin{aligned}R(x)&=2+x+12x^{2}+11x^{3}+19x^{4}+16x^{5}\\&+15x^{6}+6x^{7}+2x^{8}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{8}\Phi_{2}(x)^{4}\Phi_{4}(x)^{2}$$


### D15 — g=1, k=4; core degrees: 1 (4), 3 (2), 4 (1)

Order 14; period 12; source v32/PROFILE_MODELS.json, record 14.

$$B=2^{n+16},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$\begin{aligned}R(x)&=1+4x+14x^{2}+16x^{3}+22x^{4}+15x^{5}\\&+10x^{6}+2x^{7}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{7}\Phi_{2}(x)^{3}\Phi_{3}(x)\Phi_{4}(x)$$


### D16 — g=1, k=4; core degrees: 1 (4), 3 (1), 5 (1)

Order 12; period 12; source v32/PROFILE_MODELS.json, record 15.

$$B=2^{n+11},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=1+3x+x^{2}+3x^{3}+x^{5}$$

$$Q(x)=\Phi_{1}(x)^{6}\Phi_{2}(x)^{2}\Phi_{3}(x)\Phi_{4}(x)$$


### D17 — g=1, k=4; core degrees: 1 (4), 4 (2)

Order 13; period 12; source v32/PROFILE_MODELS.json, record 16.

$$B=2^{n+12},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=1+2x+2x^{2}+3x^{3}+2x^{4}+2x^{5}-x^{6}$$

$$Q(x)=\Phi_{1}(x)^{6}\Phi_{2}(x)^{3}\Phi_{3}(x)\Phi_{4}(x)$$


### D18 — g=1, k=4; core degrees: 1 (4), 6 (1)

Order 11; period 12; source v32/PROFILE_MODELS.json, record 17.

$$B=2^{n+7},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)^{2}\Phi_{3}(x)\Phi_{4}(x)$$


### D19 — g=2, k=0; core degrees: 3 (2)

Order 6; period 6; source v32/PROFILE_MODELS.json, record 18.

$$B=2^{n+7},\quad a(n)=0\ (n<4).$$

$$a(n)=\left\lfloor\frac{B^{n-4}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 4).$$

$$R(x)=1+x+x^{2}+x^{4}$$

$$Q(x)=\Phi_{1}(x)^{3}\Phi_{2}(x)\Phi_{3}(x)$$


### D20 — g=2, k=0; core degrees: 4 (1)

Order 3; period 2; source v32/PROFILE_MODELS.json, record 19.

$$B=2^{n+1},\quad a(n)=0\ (n<5).$$

$$a(n)=\left\lfloor\frac{B^{n-5}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 5).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{2}\Phi_{2}(x)$$

Same rational function as B06.


### D21 — g=2, k=1; core degrees: 1 (1), 3 (3)

Order 7; period 2; source v32/PROFILE_MODELS.json, record 20.

$$B=2^{n+7},\quad a(n)=0\ (n<5).$$

$$a(n)=\left\lfloor\frac{B^{n-5}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 5).$$

$$R(x)=1+x+3x^{3}$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)^{2}$$


### D22 — g=2, k=1; core degrees: 1 (1), 3 (1), 4 (1)

Order 7; period 6; source v32/PROFILE_MODELS.json, record 21.

$$B=2^{n+8},\quad a(n)=0\ (n<5).$$

$$a(n)=\left\lfloor\frac{B^{n-5}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 5).$$

$$R(x)=1+2x+3x^{2}+2x^{3}+2x^{4}$$

$$Q(x)=\Phi_{1}(x)^{4}\Phi_{2}(x)\Phi_{3}(x)$$


### D23 — g=2, k=1; core degrees: 1 (1), 5 (1)

Order 4; period 2; source v32/PROFILE_MODELS.json, record 22.

$$B=2^{n+1},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{3}\Phi_{2}(x)$$


### D24 — g=2, k=2; core degrees: 1 (2), 3 (4)

Order 12; period 4; source v32/PROFILE_MODELS.json, record 23.

$$B=2^{n+14},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$\begin{aligned}R(x)&=1+x+7x^{2}+3x^{3}+17x^{4}+2x^{5}+12x^{6}\\&+x^{7}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{7}\Phi_{2}(x)^{3}\Phi_{4}(x)$$


### D25 — g=2, k=2; core degrees: 1 (2), 3 (2), 4 (1)

Order 13; period 12; source v32/PROFILE_MODELS.json, record 24.

$$B=2^{n+17},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$\begin{aligned}R(x)&=2+9x+18x^{2}+37x^{3}+43x^{4}+49x^{5}\\&+35x^{6}+21x^{7}+7x^{8}-x^{9}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{6}\Phi_{2}(x)^{3}\Phi_{3}(x)\Phi_{4}(x)$$


### D26 — g=2, k=2; core degrees: 1 (2), 3 (1), 5 (1)

Order 9; period 6; source v32/PROFILE_MODELS.json, record 25.

$$B=2^{n+10},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=1+2x+5x^{2}+5x^{3}+4x^{4}-x^{6}$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)^{2}\Phi_{3}(x)$$


### D27 — g=2, k=2; core degrees: 1 (2), 4 (2)

Order 9; period 6; source v32/PROFILE_MODELS.json, record 26.

$$B=2^{n+9},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=1+2x+3x^{2}+x^{3}+2x^{4}+x^{6}$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)^{2}\Phi_{3}(x)$$


### D28 — g=2, k=2; core degrees: 1 (2), 6 (1)

Order 6; period 2; source v32/PROFILE_MODELS.json, record 27.

$$B=2^{n+2},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{4}\Phi_{2}(x)^{2}$$


### D29 — g=2, k=3; core degrees: 1 (3), 3 (5)

Order 23; period 12; source v32/PROFILE_MODELS.json, record 28.

$$B=2^{n+30},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=\sum_{j=0}^{16} c_jx^j.$$

```text
  0-16   3, 9, 42, 101, 221, 363, 552, 663, 767, 722, 651, 476, 324, 163, 71, 17, 3
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{9}\Phi_{2}(x)^{4}\Phi_{3}(x)^{3}\Phi_{4}(x)\\&\times \Phi_{6}(x)\end{aligned}$$


### D30 — g=2, k=3; core degrees: 1 (3), 3 (3), 4 (1)

Order 13; period 6; source v32/PROFILE_MODELS.json, record 29.

$$B=2^{n+17},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$\begin{aligned}R(x)&=2+9x+33x^{2}+55x^{3}+82x^{4}+62x^{5}\\&+37x^{6}+7x^{7}-x^{8}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{8}\Phi_{2}(x)^{3}\Phi_{3}(x)$$


### D31 — g=2, k=3; core degrees: 1 (3), 3 (2), 5 (1)

Order 14; period 12; source v32/PROFILE_MODELS.json, record 30.

$$B=2^{n+17},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$\begin{aligned}R(x)&=2+7x+14x^{2}+33x^{3}+33x^{4}+39x^{5}\\&+24x^{6}+11x^{7}+3x^{8}-3x^{9}+x^{10}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{7}\Phi_{2}(x)^{3}\Phi_{3}(x)\Phi_{4}(x)$$


### D32 — g=2, k=3; core degrees: 1 (3), 3 (1), 4 (2)

Order 14; period 6; source v32/PROFILE_MODELS.json, record 31.

$$B=2^{n+18},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$\begin{aligned}R(x)&=2+11x+30x^{2}+56x^{3}+70x^{4}+68x^{5}\\&+44x^{6}+21x^{7}+4x^{8}-x^{10}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{7}\Phi_{2}(x)^{3}\Phi_{3}(x)^{2}$$


### D33 — g=2, k=3; core degrees: 1 (3), 3 (1), 6 (1)

Order 12; period 6; source v32/PROFILE_MODELS.json, record 32.

$$B=2^{n+12},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=1+2x+5x^{2}+7x^{3}+8x^{4}+3x^{5}-x^{7}$$

$$Q(x)=\Phi_{1}(x)^{6}\Phi_{2}(x)^{2}\Phi_{3}(x)^{2}$$


### D34 — g=2, k=3; core degrees: 1 (3), 4 (1), 5 (1)

Order 10; period 6; source v32/PROFILE_MODELS.json, record 33.

$$B=2^{n+9},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=1+3x+5x^{2}+x^{3}+2x^{4}$$

$$Q(x)=\Phi_{1}(x)^{6}\Phi_{2}(x)^{2}\Phi_{3}(x)$$


### D35 — g=2, k=3; core degrees: 1 (3), 7 (1)

Order 9; period 6; source v32/PROFILE_MODELS.json, record 34.

$$B=2^{n+4},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)^{2}\Phi_{3}(x)$$


### D36 — g=3, k=0; core degrees: 3 (4)

Order 15; period 12; source v32/PROFILE_MODELS.json, record 35.

$$B=2^{n+20},\quad a(n)=0\ (n<4).$$

$$a(n)=\left\lfloor\frac{B^{n-4}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 4).$$

$$R(x)=\sum_{j=0}^{12} c_jx^j.$$

```text
  0-12   1, 0, 1, 4, 9, 13, 18, 16, 16, 14, 10, 5, 4
```

$$Q(x)=\Phi_{1}(x)^{6}\Phi_{2}(x)^{3}\Phi_{3}(x)^{2}\Phi_{4}(x)$$


### D37 — g=3, k=0; core degrees: 3 (2), 4 (1)

Order 11; period 12; source v32/PROFILE_MODELS.json, record 36.

$$B=2^{n+14},\quad a(n)=0\ (n<5).$$

$$a(n)=\left\lfloor\frac{B^{n-5}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 5).$$

$$\begin{aligned}R(x)&=1+2x+5x^{2}+5x^{3}+8x^{4}+5x^{5}+7x^{6}\\&+2x^{7}+2x^{8}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)^{2}\Phi_{3}(x)\Phi_{4}(x)$$


### D38 — g=3, k=0; core degrees: 3 (1), 5 (1)

Order 7; period 6; source v32/PROFILE_MODELS.json, record 37.

$$B=2^{n+6},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=1+x+x^{2}+x^{4}$$

$$Q(x)=\Phi_{1}(x)^{4}\Phi_{2}(x)\Phi_{3}(x)$$


### D39 — g=3, k=0; core degrees: 4 (2)

Order 10; period 12; source v32/PROFILE_MODELS.json, record 38.

$$B=2^{n+11},\quad a(n)=0\ (n<5).$$

$$a(n)=\left\lfloor\frac{B^{n-5}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 5).$$

$$R(x)=1+x+x^{2}+2x^{3}+x^{4}+2x^{5}-x^{8}$$

$$Q(x)=\Phi_{1}(x)^{4}\Phi_{2}(x)^{2}\Phi_{3}(x)\Phi_{4}(x)$$


### D40 — g=3, k=0; core degrees: 6 (1)

Order 6; period 6; source v32/PROFILE_MODELS.json, record 39.

$$B=2^{n+2},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{3}\Phi_{2}(x)\Phi_{3}(x)$$


### D41 — g=3, k=1; core degrees: 1 (1), 3 (5)

Order 13; period 4; source v32/PROFILE_MODELS.json, record 40.

$$B=2^{n+16},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$\begin{aligned}R(x)&=1+7x^{2}+5x^{3}+16x^{4}+8x^{5}+17x^{6}\\&+4x^{7}+6x^{8}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{8}\Phi_{2}(x)^{3}\Phi_{4}(x)$$


### D42 — g=3, k=1; core degrees: 1 (1), 3 (3), 4 (1)

Order 16; period 12; source v32/PROFILE_MODELS.json, record 41.

$$B=2^{n+24},\quad a(n)=0\ (n<5).$$

$$a(n)=\left\lfloor\frac{B^{n-5}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 5).$$

$$R(x)=\sum_{j=0}^{14} c_jx^j.$$

```text
  0-14   1, 2, 11, 36, 85, 148, 214, 242, 234, 182, 115, 55, 19, 2, -2
```

$$Q(x)=\Phi_{1}(x)^{7}\Phi_{2}(x)^{3}\Phi_{3}(x)^{2}\Phi_{4}(x)$$


### D43 — g=3, k=1; core degrees: 1 (1), 3 (2), 5 (1)

Order 12; period 12; source v32/PROFILE_MODELS.json, record 42.

$$B=2^{n+15},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$\begin{aligned}R(x)&=1+4x+10x^{2}+12x^{3}+18x^{4}+14x^{5}\\&+15x^{6}+5x^{7}+4x^{8}-x^{9}-x^{10}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{6}\Phi_{2}(x)^{2}\Phi_{3}(x)\Phi_{4}(x)$$


### D44 — g=3, k=1; core degrees: 1 (1), 3 (1), 4 (2)

Order 10; period 6; source v32/PROFILE_MODELS.json, record 43.

$$B=2^{n+12},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$\begin{aligned}R(x)&=2+5x+9x^{2}+11x^{3}+12x^{4}+5x^{5}\\&+3x^{6}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{6}\Phi_{2}(x)^{2}\Phi_{3}(x)$$


### D45 — g=3, k=1; core degrees: 1 (1), 3 (1), 6 (1)

Order 9; period 6; source v32/PROFILE_MODELS.json, record 44.

$$B=2^{n+8},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=1+3x+4x^{2}+2x^{3}+x^{4}$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)^{2}\Phi_{3}(x)$$


### D46 — g=3, k=1; core degrees: 1 (1), 4 (1), 5 (1)

Order 11; period 12; source v32/PROFILE_MODELS.json, record 45.

$$B=2^{n+12},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$\begin{aligned}R(x)&=1+2x+3x^{2}+6x^{3}+6x^{4}+7x^{5}+4x^{6}\\&+x^{7}-x^{9}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)^{2}\Phi_{3}(x)\Phi_{4}(x)$$


### D47 — g=3, k=1; core degrees: 1 (1), 7 (1)

Order 7; period 6; source v32/PROFILE_MODELS.json, record 46.

$$B=2^{n+2},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{4}\Phi_{2}(x)\Phi_{3}(x)$$


### D48 — g=3, k=2; core degrees: 1 (2), 3 (6)

Order 19; period 4; source v32/PROFILE_MODELS.json, record 47.

$$B=2^{n+24},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=\sum_{j=0}^{12} c_jx^j.$$

```text
  0-12   5, 4, 53, 77, 194, 244, 346, 313, 293, 184, 109, 38, 12
```

$$Q(x)=\Phi_{1}(x)^{10}\Phi_{2}(x)^{5}\Phi_{4}(x)^{2}$$


### D49 — g=3, k=2; core degrees: 1 (2), 3 (4), 4 (1)

Order 19; period 12; source v32/PROFILE_MODELS.json, record 48.

$$B=2^{n+28},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=\sum_{j=0}^{15} c_jx^j.$$

```text
  0-15   5, 20, 100, 288, 680, 1176, 1723, 1989, 1968, 1547, 1018, 501, 187, 35, -3, -2
```

$$Q(x)=\Phi_{1}(x)^{9}\Phi_{2}(x)^{4}\Phi_{3}(x)^{2}\Phi_{4}(x)$$


### D50 — g=3, k=2; core degrees: 1 (2), 3 (3), 5 (1)

Order 17; period 12; source v32/PROFILE_MODELS.json, record 49.

$$B=2^{n+24},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=\sum_{j=0}^{15} c_jx^j.$$

```text
  0-15   1, 1, 15, 48, 122, 210, 315, 349, 352, 255, 163, 61, 15, -6, -3, 1
```

$$Q(x)=\Phi_{1}(x)^{8}\Phi_{2}(x)^{3}\Phi_{3}(x)^{2}\Phi_{4}(x)$$


### D51 — g=3, k=2; core degrees: 1 (2), 3 (2), 4 (2)

Order 16; period 12; source v32/PROFILE_MODELS.json, record 50.

$$B=2^{n+24},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=\sum_{j=0}^{14} c_jx^j.$$

```text
  0-14   1, 5, 30, 87, 205, 327, 441, 440, 381, 234, 118, 34, 5, -5, -1
```

$$Q(x)=\Phi_{1}(x)^{8}\Phi_{2}(x)^{4}\Phi_{3}(x)\Phi_{4}(x)$$


### D52 — g=3, k=2; core degrees: 1 (2), 3 (2), 6 (1)

Order 14; period 12; source v32/PROFILE_MODELS.json, record 51.

$$B=2^{n+17},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$\begin{aligned}R(x)&=1+4x+15x^{2}+22x^{3}+37x^{4}+32x^{5}\\&+34x^{6}+15x^{7}+8x^{8}-3x^{10}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{7}\Phi_{2}(x)^{3}\Phi_{3}(x)\Phi_{4}(x)$$


### D53 — g=3, k=2; core degrees: 1 (2), 3 (1), 4 (1), 5 (1)

Order 14; period 12; source v32/PROFILE_MODELS.json, record 52.

$$B=2^{n+18},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$\begin{aligned}R(x)&=3+17x+41x^{2}+69x^{3}+96x^{4}+95x^{5}\\&+82x^{6}+45x^{7}+18x^{8}+2x^{9}-5x^{10}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{7}\Phi_{2}(x)^{3}\Phi_{3}(x)\Phi_{4}(x)$$


### D54 — g=3, k=2; core degrees: 1 (2), 3 (1), 7 (1)

Order 10; period 6; source v32/PROFILE_MODELS.json, record 53.

$$B=2^{n+8},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=1+2x+4x^{2}+x^{3}+x^{4}-x^{5}$$

$$Q(x)=\Phi_{1}(x)^{6}\Phi_{2}(x)^{2}\Phi_{3}(x)$$


### D55 — g=3, k=2; core degrees: 1 (2), 4 (3)

Order 14; period 12; source v32/PROFILE_MODELS.json, record 54.

$$B=2^{n+16},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=\sum_{j=0}^{11} c_jx^j.$$

```text
  0-11   2, 3, 10, 12, 21, 15, 18, 6, 6, 0, 2, -1
```

$$Q(x)=\Phi_{1}(x)^{7}\Phi_{2}(x)^{3}\Phi_{3}(x)\Phi_{4}(x)$$


### D56 — g=3, k=2; core degrees: 1 (2), 4 (1), 6 (1)

Order 13; period 12; source v32/PROFILE_MODELS.json, record 55.

$$B=2^{n+14},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$\begin{aligned}R(x)&=1+2x+5x^{2}+10x^{3}+11x^{4}+12x^{5}\\&+7x^{6}+3x^{7}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{6}\Phi_{2}(x)^{3}\Phi_{3}(x)\Phi_{4}(x)$$


### D57 — g=3, k=2; core degrees: 1 (2), 5 (2)

Order 13; period 12; source v32/PROFILE_MODELS.json, record 56.

$$B=2^{n+13},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$\begin{aligned}R(x)&=1+2x+3x^{2}+5x^{3}+5x^{4}+7x^{5}+4x^{6}\\&+3x^{7}-x^{10}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{6}\Phi_{2}(x)^{3}\Phi_{3}(x)\Phi_{4}(x)$$


### D58 — g=3, k=2; core degrees: 1 (2), 8 (1)

Order 9; period 6; source v32/PROFILE_MODELS.json, record 57.

$$B=2^{n+3},\quad a(n)=0\ (n<9).$$

$$a(n)=\left\lfloor\frac{B^{n-9}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 9).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)^{2}\Phi_{3}(x)$$


### D59 — g=4, k=0; core degrees: 3 (6)

Order 25; period 12; source v32/PROFILE_MODELS.json, record 58.

$$B=2^{n+34},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=\sum_{j=0}^{20} c_jx^j.$$

```text
  0-20   2, -2, 11, 14, 49, 78, 176, 212, 393, 390, 549, 476, 544, 373, 376, 189, 169, 58, 41, 6, 6
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{9}\Phi_{2}(x)^{4}\Phi_{3}(x)^{3}\Phi_{4}(x)^{2}\\&\times \Phi_{6}(x)\end{aligned}$$


### D60 — g=4, k=0; core degrees: 3 (4), 4 (1)

Order 20; period 12; source v32/PROFILE_MODELS.json, record 59.

$$B=2^{n+30},\quad a(n)=0\ (n<5).$$

$$a(n)=\left\lfloor\frac{B^{n-5}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 5).$$

$$R(x)=\sum_{j=0}^{18} c_jx^j.$$

```text
  0-18   1, 1, 11, 29, 84, 166, 304, 441, 582, 624, 613, 499, 369, 218, 112, 44, 11, 4, -3
```

$$Q(x)=\Phi_{1}(x)^{8}\Phi_{2}(x)^{4}\Phi_{3}(x)^{2}\Phi_{4}(x)^{2}$$


### D61 — g=4, k=0; core degrees: 3 (3), 5 (1)

Order 16; period 12; source v32/PROFILE_MODELS.json, record 60.

$$B=2^{n+21},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=\sum_{j=0}^{14} c_jx^j.$$

```text
  0-14   2, 4, 13, 26, 48, 64, 78, 67, 55, 35, 21, 8, 3, -2, -2
```

$$Q(x)=\Phi_{1}(x)^{7}\Phi_{2}(x)^{3}\Phi_{3}(x)^{2}\Phi_{4}(x)$$


### D62 — g=4, k=0; core degrees: 3 (2), 4 (2)

Order 18; period 12; source v32/PROFILE_MODELS.json, record 61.

$$B=2^{n+25},\quad a(n)=0\ (n<5).$$

$$a(n)=\left\lfloor\frac{B^{n-5}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 5).$$

$$R(x)=\sum_{j=0}^{16} c_jx^j.$$

```text
  0-16   1, 2, 6, 22, 30, 68, 65, 114, 83, 118, 63, 77, 24, 29, 2, 5, -2
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{7}\Phi_{2}(x)^{3}\Phi_{3}(x)^{2}\Phi_{4}(x)\\&\times \Phi_{6}(x)\end{aligned}$$


### D63 — g=4, k=0; core degrees: 3 (2), 6 (1)

Order 17; period 12; source v32/PROFILE_MODELS.json, record 62.

$$B=2^{n+20},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=\sum_{j=0}^{13} c_jx^j.$$

```text
  0-13   2, 3, 9, 10, 19, 17, 23, 17, 17, 8, 7, 2, 1, -1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{6}\Phi_{2}(x)^{3}\Phi_{3}(x)^{2}\Phi_{4}(x)\\&\times \Phi_{6}(x)\end{aligned}$$


### D64 — g=4, k=0; core degrees: 3 (1), 4 (1), 5 (1)

Order 12; period 12; source v32/PROFILE_MODELS.json, record 63.

$$B=2^{n+14},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=\sum_{j=0}^{11} c_jx^j.$$

```text
  0-11   1, 3, 7, 11, 11, 12, 6, 8, 0, 2, -1, -1
```

$$Q(x)=\Phi_{1}(x)^{6}\Phi_{2}(x)^{2}\Phi_{3}(x)\Phi_{4}(x)$$


### D65 — g=4, k=0; core degrees: 3 (1), 7 (1)

Order 7; period 2; source v32/PROFILE_MODELS.json, record 64.

$$B=2^{n+2},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)^{2}$$


### D66 — g=4, k=0; core degrees: 4 (3)

Order 17; period 12; source v32/PROFILE_MODELS.json, record 65.

$$B=2^{n+19},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=\sum_{j=0}^{16} c_jx^j.$$

```text
  0-16   1, 1, 3, 7, 2, 12, 6, 11, 4, 8, 0, 2, 1, -2, 1, -1, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{6}\Phi_{2}(x)^{3}\Phi_{3}(x)^{2}\Phi_{4}(x)\\&\times \Phi_{6}(x)\end{aligned}$$


### D67 — g=4, k=0; core degrees: 4 (1), 6 (1)

Order 11; period 12; source v32/PROFILE_MODELS.json, record 66.

$$B=2^{n+10},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=1+x+x^{2}+2x^{3}+x^{4}+2x^{5}-x^{8}$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)^{2}\Phi_{3}(x)\Phi_{4}(x)$$


### D68 — g=4, k=0; core degrees: 5 (2)

Order 15; period 60; source v32/PROFILE_MODELS.json, record 67.

$$B=2^{n+16},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=\sum_{j=0}^{12} c_jx^j.$$

```text
  0-12   1, 1, 1, 2, 4, 3, 5, 3, 3, 1, 1, 0, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{5}\Phi_{2}(x)^{2}\Phi_{3}(x)\Phi_{4}(x)\\&\times \Phi_{5}(x)\end{aligned}$$


### D69 — g=4, k=0; core degrees: 8 (1)

Order 10; period 12; source v32/PROFILE_MODELS.json, record 68.

$$B=2^{n+4},\quad a(n)=0\ (n<9).$$

$$a(n)=\left\lfloor\frac{B^{n-9}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 9).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{4}\Phi_{2}(x)^{2}\Phi_{3}(x)\Phi_{4}(x)$$


## Bipartite graphs: degree profiles


### BD01 — g=0, k=2; core degrees: 1 (2)

Order 1; period 1; source v32/BIPARTITE_PROFILE_MODELS.json, record 0.

$$B=2^{n+2},\quad a(n)=0\ (n<2).$$

$$a(n)=\left\lfloor\frac{B^{n-2}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 2).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)$$

Same rational function as G01.


### BD02 — g=0, k=3; core degrees: 1 (3), 3 (1)

Order 6; period 6; source v32/BIPARTITE_PROFILE_MODELS.json, record 1.

$$B=2^{n+5},\quad a(n)=0\ (n<4).$$

$$a(n)=\left\lfloor\frac{B^{n-4}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 4).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{3}\Phi_{2}(x)\Phi_{3}(x)$$

Same rational function as G02.


### BD03 — g=0, k=4; core degrees: 1 (4), 3 (2)

Order 9; period 4; source v32/BIPARTITE_PROFILE_MODELS.json, record 2.

$$B=2^{n+7},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=1-x+x^{2}$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)^{2}\Phi_{4}(x)$$

Same rational function as D03.


### BD04 — g=0, k=4; core degrees: 1 (4), 4 (1)

Order 10; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 3.

$$B=2^{n+8},\quad a(n)=0\ (n<5).$$

$$a(n)=\left\lfloor\frac{B^{n-5}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 5).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{4}\Phi_{2}(x)^{2}\Phi_{3}(x)\Phi_{4}(x)$$

Same rational function as D04.


### BD05 — g=0, k=5; core degrees: 1 (5), 3 (3)

Order 12; period 4; source v32/BIPARTITE_PROFILE_MODELS.json, record 4.

$$B=2^{n+9},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=1-x+2x^{2}$$

$$Q(x)=\Phi_{1}(x)^{7}\Phi_{2}(x)^{3}\Phi_{4}(x)$$

Same rational function as D05.


### BD06 — g=0, k=5; core degrees: 1 (5), 3 (1), 4 (1)

Order 10; period 6; source v32/BIPARTITE_PROFILE_MODELS.json, record 5.

$$B=2^{n+6},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{6}\Phi_{2}(x)^{2}\Phi_{3}(x)$$

Same rational function as D06.


### BD07 — g=0, k=5; core degrees: 1 (5), 5 (1)

Order 15; period 60; source v32/BIPARTITE_PROFILE_MODELS.json, record 6.

$$B=2^{n+12},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=1$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{5}\Phi_{2}(x)^{2}\Phi_{3}(x)\Phi_{4}(x)\\&\times \Phi_{5}(x)\end{aligned}$$

Same rational function as D07.


### BD08 — g=1, k=1; core degrees: 1 (1), 3 (1)

Order 3; period 2; source v32/BIPARTITE_PROFILE_MODELS.json, record 7.

$$B=2^{n+1},\quad a(n)=0\ (n<5).$$

$$a(n)=\left\lfloor\frac{B^{n-5}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 5).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{2}\Phi_{2}(x)$$

Same rational function as B06.


### BD09 — g=1, k=2; core degrees: 1 (2), 3 (2)

Order 7; period 2; source v32/BIPARTITE_PROFILE_MODELS.json, record 8.

$$B=2^{n+5},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=2+x$$

$$Q(x)=\Phi_{1}(x)^{4}\Phi_{2}(x)^{3}$$


### BD10 — g=1, k=2; core degrees: 1 (2), 4 (1)

Order 5; period 2; source v32/BIPARTITE_PROFILE_MODELS.json, record 9.

$$B=2^{n+2},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{3}\Phi_{2}(x)^{2}$$


### BD11 — g=1, k=3; core degrees: 1 (3), 3 (3)

Order 15; period 6; source v32/BIPARTITE_PROFILE_MODELS.json, record 10.

$$B=2^{n+16},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$\begin{aligned}R(x)&=1+2x+5x^{2}+4x^{3}+6x^{4}+6x^{5}+5x^{6}\\&+2x^{7}+2x^{8}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{6}\Phi_{2}(x)^{3}\Phi_{3}(x)^{2}\Phi_{6}(x)$$


### BD12 — g=1, k=3; core degrees: 1 (3), 3 (1), 4 (1)

Order 10; period 6; source v32/BIPARTITE_PROFILE_MODELS.json, record 11.

$$B=2^{n+9},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=2+4x+4x^{2}+x^{3}$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)^{3}\Phi_{3}(x)$$


### BD13 — g=1, k=3; core degrees: 1 (3), 5 (1)

Order 8; period 6; source v32/BIPARTITE_PROFILE_MODELS.json, record 12.

$$B=2^{n+4},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{4}\Phi_{2}(x)^{2}\Phi_{3}(x)$$


### BD14 — g=1, k=4; core degrees: 1 (4), 3 (4)

Order 17; period 4; source v32/BIPARTITE_PROFILE_MODELS.json, record 13.

$$B=2^{n+18},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$\begin{aligned}R(x)&=1+8x^{2}+8x^{3}+19x^{4}+12x^{5}+21x^{6}\\&+9x^{7}+5x^{8}+x^{9}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{8}\Phi_{2}(x)^{5}\Phi_{4}(x)^{2}$$


### BD15 — g=1, k=4; core degrees: 1 (4), 3 (2), 4 (1)

Order 15; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 14.

$$B=2^{n+16},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$\begin{aligned}R(x)&=2+7x+16x^{2}+17x^{3}+21x^{4}+12x^{5}\\&+8x^{6}+x^{7}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{7}\Phi_{2}(x)^{4}\Phi_{3}(x)\Phi_{4}(x)$$


### BD16 — g=1, k=4; core degrees: 1 (4), 3 (1), 5 (1)

Order 13; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 15.

$$B=2^{n+11},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=2+2x+2x^{2}+2x^{3}+x^{5}$$

$$Q(x)=\Phi_{1}(x)^{6}\Phi_{2}(x)^{3}\Phi_{3}(x)\Phi_{4}(x)$$


### BD17 — g=1, k=4; core degrees: 1 (4), 4 (2)

Order 14; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 16.

$$B=2^{n+12},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=2+x+3x^{2}+2x^{3}+3x^{4}+x^{5}-x^{6}$$

$$Q(x)=\Phi_{1}(x)^{6}\Phi_{2}(x)^{4}\Phi_{3}(x)\Phi_{4}(x)$$


### BD18 — g=1, k=4; core degrees: 1 (4), 6 (1)

Order 12; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 17.

$$B=2^{n+7},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)^{3}\Phi_{3}(x)\Phi_{4}(x)$$


### BD19 — g=2, k=0; core degrees: 3 (2)

Order 9; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 18.

$$B=2^{n+9},\quad a(n)=0\ (n<5).$$

$$a(n)=\left\lfloor\frac{B^{n-5}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 5).$$

$$R(x)=1+x+x^{3}+x^{5}$$

$$Q(x)=\Phi_{1}(x)^{3}\Phi_{2}(x)^{2}\Phi_{3}(x)\Phi_{4}(x)$$


### BD20 — g=2, k=0; core degrees: 4 (1)

Order 6; period 4; source v32/BIPARTITE_PROFILE_MODELS.json, record 19.

$$B=2^{n+2},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{2}\Phi_{2}(x)^{2}\Phi_{4}(x)$$


### BD21 — g=2, k=1; core degrees: 1 (1), 3 (3)

Order 10; period 4; source v32/BIPARTITE_PROFILE_MODELS.json, record 20.

$$B=2^{n+9},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=1+3x^{3}+x^{5}$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)^{3}\Phi_{4}(x)$$


### BD22 — g=2, k=1; core degrees: 1 (1), 3 (1), 4 (1)

Order 11; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 21.

$$B=2^{n+12},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$\begin{aligned}R(x)&=1+2x+3x^{2}+3x^{3}+4x^{4}+3x^{5}+3x^{6}\\&+x^{7}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{4}\Phi_{2}(x)^{3}\Phi_{3}(x)\Phi_{4}(x)$$


### BD23 — g=2, k=1; core degrees: 1 (1), 5 (1)

Order 7; period 4; source v32/BIPARTITE_PROFILE_MODELS.json, record 22.

$$B=2^{n+2},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{3}\Phi_{2}(x)^{2}\Phi_{4}(x)$$


### BD24 — g=2, k=2; core degrees: 1 (2), 3 (4)

Order 15; period 4; source v32/BIPARTITE_PROFILE_MODELS.json, record 23.

$$B=2^{n+16},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$\begin{aligned}R(x)&=1+2x-x^{2}+13x^{3}-x^{4}+15x^{5}+4x^{6}\\&+9x^{7}+x^{8}+x^{9}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{7}\Phi_{2}(x)^{4}\Phi_{4}(x)^{2}$$


### BD25 — g=2, k=2; core degrees: 1 (2), 3 (2), 4 (1)

Order 16; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 24.

$$B=2^{n+19},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=\sum_{j=0}^{11} c_jx^j.$$

```text
  0-11   2, 5, 14, 22, 34, 40, 41, 32, 20, 8, 3, -1
```

$$Q(x)=\Phi_{1}(x)^{6}\Phi_{2}(x)^{4}\Phi_{3}(x)\Phi_{4}(x)^{2}$$


### BD26 — g=2, k=2; core degrees: 1 (2), 3 (1), 5 (1)

Order 12; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 25.

$$B=2^{n+12},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$\begin{aligned}R(x)&=1+x+2x^{2}+4x^{3}+4x^{4}+4x^{5}+x^{6}\\&-x^{8}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)^{3}\Phi_{3}(x)\Phi_{4}(x)$$


### BD27 — g=2, k=2; core degrees: 1 (2), 4 (2)

Order 13; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 26.

$$B=2^{n+13},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$\begin{aligned}R(x)&=1+2x+3x^{2}+3x^{3}+4x^{4}+2x^{5}+2x^{6}\\&+x^{7}+x^{8}+x^{9}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)^{4}\Phi_{3}(x)\Phi_{4}(x)$$


### BD28 — g=2, k=2; core degrees: 1 (2), 6 (1)

Order 9; period 4; source v32/BIPARTITE_PROFILE_MODELS.json, record 27.

$$B=2^{n+3},\quad a(n)=0\ (n<9).$$

$$a(n)=\left\lfloor\frac{B^{n-9}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 9).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{4}\Phi_{2}(x)^{3}\Phi_{4}(x)$$


### BD29 — g=2, k=3; core degrees: 1 (3), 3 (5)

Order 26; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 28.

$$B=2^{n+33},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=\sum_{j=0}^{19} c_jx^j.$$

```text
  0-19   1, 1, 10, 32, 78, 156, 276, 412, 562, 663, 706, 675, 578, 438, 289, 163, 74, 27, 6, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{9}\Phi_{2}(x)^{5}\Phi_{3}(x)^{3}\Phi_{4}(x)^{2}\\&\times \Phi_{6}(x)\end{aligned}$$


### BD30 — g=2, k=3; core degrees: 1 (3), 3 (3), 4 (1)

Order 19; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 29.

$$B=2^{n+24},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=\sum_{j=0}^{13} c_jx^j.$$

```text
  0-13   2, 11, 28, 68, 122, 181, 204, 207, 154, 105, 44, 17, 2, -1
```

$$Q(x)=\Phi_{1}(x)^{8}\Phi_{2}(x)^{5}\Phi_{3}(x)\Phi_{4}(x)^{2}$$


### BD31 — g=2, k=3; core degrees: 1 (3), 3 (2), 5 (1)

Order 17; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 30.

$$B=2^{n+19},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=\sum_{j=0}^{12} c_jx^j.$$

```text
  0-12   2, 3, 11, 20, 24, 37, 28, 26, 10, 4, 0, -2, 1
```

$$Q(x)=\Phi_{1}(x)^{7}\Phi_{2}(x)^{4}\Phi_{3}(x)\Phi_{4}(x)^{2}$$


### BD32 — g=2, k=3; core degrees: 1 (3), 3 (1), 4 (2)

Order 18; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 31.

$$B=2^{n+22},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=\sum_{j=0}^{13} c_jx^j.$$

```text
  0-13   2, 9, 28, 55, 90, 111, 115, 92, 64, 33, 13, 1, -2, -1
```

$$Q(x)=\Phi_{1}(x)^{7}\Phi_{2}(x)^{5}\Phi_{3}(x)^{2}\Phi_{4}(x)$$


### BD33 — g=2, k=3; core degrees: 1 (3), 3 (1), 6 (1)

Order 16; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 32.

$$B=2^{n+16},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$\begin{aligned}R(x)&=1+2x+3x^{2}+6x^{3}+11x^{4}+13x^{5}\\&+12x^{6}+5x^{7}-2x^{9}-x^{10}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{6}\Phi_{2}(x)^{4}\Phi_{3}(x)^{2}\Phi_{4}(x)$$


### BD34 — g=2, k=3; core degrees: 1 (3), 4 (1), 5 (1)

Order 12; period 6; source v32/BIPARTITE_PROFILE_MODELS.json, record 33.

$$B=2^{n+10},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=1+2x+4x^{2}+2x^{3}+2x^{4}+x^{5}$$

$$Q(x)=\Phi_{1}(x)^{6}\Phi_{2}(x)^{4}\Phi_{3}(x)$$


### BD35 — g=2, k=3; core degrees: 1 (3), 7 (1)

Order 12; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 34.

$$B=2^{n+5},\quad a(n)=0\ (n<10).$$

$$a(n)=\left\lfloor\frac{B^{n-10}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 10).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)^{3}\Phi_{3}(x)\Phi_{4}(x)$$


### BD36 — g=3, k=0; core degrees: 3 (4)

Order 21; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 35.

$$B=2^{n+24},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=\sum_{j=0}^{15} c_jx^j.$$

```text
  0-15   1, 1, 2, 1, 6, 6, 11, 12, 15, 13, 13, 10, 7, 9, 2, 2
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{6}\Phi_{2}(x)^{5}\Phi_{3}(x)^{2}\Phi_{4}(x)^{2}\\&\times \Phi_{6}(x)\end{aligned}$$


### BD37 — g=3, k=0; core degrees: 3 (2), 4 (1)

Order 15; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 36.

$$B=2^{n+16},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$\begin{aligned}R(x)&=1+3x+4x^{2}+4x^{3}+5x^{4}+5x^{5}+7x^{6}\\&+3x^{7}+4x^{8}+x^{10}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)^{4}\Phi_{3}(x)\Phi_{4}(x)^{2}$$


### BD38 — g=3, k=0; core degrees: 3 (1), 5 (1)

Order 11; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 37.

$$B=2^{n+8},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=1+x+x^{3}+x^{5}$$

$$Q(x)=\Phi_{1}(x)^{4}\Phi_{2}(x)^{3}\Phi_{3}(x)\Phi_{4}(x)$$


### BD39 — g=3, k=0; core degrees: 4 (2)

Order 16; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 38.

$$B=2^{n+16},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=\sum_{j=0}^{12} c_jx^j.$$

```text
  0-12   1, 0, 1, 0, 2, 0, 2, 0, 2, 0, 0, 0, -1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{4}\Phi_{2}(x)^{4}\Phi_{3}(x)\Phi_{4}(x)^{2}\\&\times \Phi_{6}(x)\end{aligned}$$


### BD40 — g=3, k=0; core degrees: 6 (1)

Order 12; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 39.

$$B=2^{n+5},\quad a(n)=0\ (n<10).$$

$$a(n)=\left\lfloor\frac{B^{n-10}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 10).$$

$$R(x)=1$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{3}\Phi_{2}(x)^{3}\Phi_{3}(x)\Phi_{4}(x)\\&\times \Phi_{6}(x)\end{aligned}$$


### BD41 — g=3, k=1; core degrees: 1 (1), 3 (5)

Order 17; period 4; source v32/BIPARTITE_PROFILE_MODELS.json, record 40.

$$B=2^{n+19},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=\sum_{j=0}^{12} c_jx^j.$$

```text
  0-12   1, -1, 3, 4, 11, 0, 21, 1, 20, -4, 10, -3, 1
```

$$Q(x)=\Phi_{1}(x)^{8}\Phi_{2}(x)^{5}\Phi_{4}(x)^{2}$$


### BD42 — g=3, k=1; core degrees: 1 (1), 3 (3), 4 (1)

Order 22; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 41.

$$B=2^{n+28},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=\sum_{j=0}^{18} c_jx^j.$$

```text
  0-18   1, 5, 12, 29, 50, 93, 117, 172, 163, 202, 147, 156, 78, 80, 20, 20, -2, 2, -1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{7}\Phi_{2}(x)^{5}\Phi_{3}(x)^{2}\Phi_{4}(x)^{2}\\&\times \Phi_{6}(x)\end{aligned}$$


### BD43 — g=3, k=1; core degrees: 1 (1), 3 (2), 5 (1)

Order 16; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 42.

$$B=2^{n+17},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=\sum_{j=0}^{12} c_jx^j.$$

```text
  0-12   1, 6, 8, 8, 15, 9, 19, 7, 10, 0, 0, -1, -1
```

$$Q(x)=\Phi_{1}(x)^{6}\Phi_{2}(x)^{4}\Phi_{3}(x)\Phi_{4}(x)^{2}$$


### BD44 — g=3, k=1; core degrees: 1 (1), 3 (1), 4 (2)

Order 19; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 43.

$$B=2^{n+22},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=\sum_{j=0}^{14} c_jx^j.$$

```text
  0-14   1, 2, 5, 8, 19, 16, 32, 22, 29, 18, 18, 8, 7, 0, 3
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{6}\Phi_{2}(x)^{5}\Phi_{3}(x)\Phi_{4}(x)^{2}\\&\times \Phi_{6}(x)\end{aligned}$$


### BD45 — g=3, k=1; core degrees: 1 (1), 3 (1), 6 (1)

Order 13; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 44.

$$B=2^{n+10},\quad a(n)=0\ (n<9).$$

$$a(n)=\left\lfloor\frac{B^{n-9}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 9).$$

$$R(x)=1+2x+3x^{2}+3x^{3}+2x^{4}$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)^{4}\Phi_{3}(x)\Phi_{4}(x)$$


### BD46 — g=3, k=1; core degrees: 1 (1), 4 (1), 5 (1)

Order 17; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 45.

$$B=2^{n+17},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=\sum_{j=0}^{14} c_jx^j.$$

```text
  0-14   1, 0, 2, 1, 3, 3, 5, 3, 7, 1, 4, 0, 0, 0, -1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{5}\Phi_{2}(x)^{4}\Phi_{3}(x)\Phi_{4}(x)^{2}\\&\times \Phi_{6}(x)\end{aligned}$$


### BD47 — g=3, k=1; core degrees: 1 (1), 7 (1)

Order 13; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 46.

$$B=2^{n+5},\quad a(n)=0\ (n<11).$$

$$a(n)=\left\lfloor\frac{B^{n-11}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 11).$$

$$R(x)=1$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{4}\Phi_{2}(x)^{3}\Phi_{3}(x)\Phi_{4}(x)\\&\times \Phi_{6}(x)\end{aligned}$$


### BD48 — g=3, k=2; core degrees: 1 (2), 3 (6)

Order 23; period 4; source v32/BIPARTITE_PROFILE_MODELS.json, record 47.

$$B=2^{n+28},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=\sum_{j=0}^{17} c_jx^j.$$

```text
  0-17   1, 0, 9, 11, 64, 68, 185, 190, 305, 280, 263, 247, 113, 101, 17, 18, -1, 1
```

$$Q(x)=\Phi_{1}(x)^{10}\Phi_{2}(x)^{7}\Phi_{4}(x)^{3}$$


### BD49 — g=3, k=2; core degrees: 1 (2), 3 (4), 4 (1)

Order 27; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 48.

$$B=2^{n+36},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=\sum_{j=0}^{22} c_jx^j.$$

```text
  0-16   3, 8, 40, 107, 273, 542, 957, 1481, 2012, 2564, 2772, 2967, 2556, 2336, 1566, 1204, 570
 17-22   367, 92, 51, -4, 1, -1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{9}\Phi_{2}(x)^{6}\Phi_{3}(x)^{2}\Phi_{4}(x)^{3}\\&\times \Phi_{6}(x)\end{aligned}$$


### BD50 — g=3, k=2; core degrees: 1 (2), 3 (3), 5 (1)

Order 23; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 49.

$$B=2^{n+28},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=\sum_{j=0}^{19} c_jx^j.$$

```text
  0-19   1, 4, 17, 40, 70, 135, 163, 257, 233, 301, 216, 217, 121, 92, 29, 11, -5, -2, -2, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{8}\Phi_{2}(x)^{5}\Phi_{3}(x)^{2}\Phi_{4}(x)^{2}\\&\times \Phi_{6}(x)\end{aligned}$$


### BD51 — g=3, k=2; core degrees: 1 (2), 3 (2), 4 (2)

Order 23; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 50.

$$B=2^{n+29},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=\sum_{j=0}^{19} c_jx^j.$$

```text
  0-19   3, 6, 29, 38, 130, 106, 296, 193, 393, 238, 327, 202, 161, 109, 38, 35, -3, 4, -2, -1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{8}\Phi_{2}(x)^{5}\Phi_{3}(x)\Phi_{4}(x)^{3}\\&\times \Phi_{6}(x)\end{aligned}$$


### BD52 — g=3, k=2; core degrees: 1 (2), 3 (2), 6 (1)

Order 18; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 51.

$$B=2^{n+19},\quad a(n)=0\ (n<9).$$

$$a(n)=\left\lfloor\frac{B^{n-9}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 9).$$

$$R(x)=\sum_{j=0}^{12} c_jx^j.$$

```text
  0-12   1, 6, 12, 19, 25, 31, 31, 26, 16, 4, -1, -3, -2
```

$$Q(x)=\Phi_{1}(x)^{7}\Phi_{2}(x)^{5}\Phi_{3}(x)\Phi_{4}(x)^{2}$$


### BD53 — g=3, k=2; core degrees: 1 (2), 3 (1), 4 (1), 5 (1)

Order 20; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 52.

$$B=2^{n+23},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=\sum_{j=0}^{15} c_jx^j.$$

```text
  0-15   1, 5, 14, 22, 39, 54, 61, 77, 56, 65, 32, 30, 9, 0, 2, -4
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{7}\Phi_{2}(x)^{5}\Phi_{3}(x)\Phi_{4}(x)^{2}\\&\times \Phi_{6}(x)\end{aligned}$$


### BD54 — g=3, k=2; core degrees: 1 (2), 3 (1), 7 (1)

Order 16; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 53.

$$B=2^{n+12},\quad a(n)=0\ (n<10).$$

$$a(n)=\left\lfloor\frac{B^{n-10}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 10).$$

$$R(x)=1+2x^{2}+3x^{3}+2x^{5}+x^{7}-x^{8}$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{6}\Phi_{2}(x)^{4}\Phi_{3}(x)\Phi_{4}(x)\\&\times \Phi_{6}(x)\end{aligned}$$


### BD55 — g=3, k=2; core degrees: 1 (2), 4 (3)

Order 21; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 54.

$$B=2^{n+23},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=\sum_{j=0}^{17} c_jx^j.$$

```text
  0-17   1, 1, 6, 4, 17, 14, 31, 20, 30, 19, 20, 11, 7, 4, 1, 2, 1, -1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{7}\Phi_{2}(x)^{6}\Phi_{3}(x)\Phi_{4}(x)^{2}\\&\times \Phi_{6}(x)\end{aligned}$$


### BD56 — g=3, k=2; core degrees: 1 (2), 4 (1), 6 (1)

Order 19; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 55.

$$B=2^{n+19},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=\sum_{j=0}^{14} c_jx^j.$$

```text
  0-14   1, 0, 2, 2, 6, 4, 11, 4, 12, 3, 5, 2, -1, 1, -1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{6}\Phi_{2}(x)^{5}\Phi_{3}(x)\Phi_{4}(x)^{2}\\&\times \Phi_{6}(x)\end{aligned}$$


### BD57 — g=3, k=2; core degrees: 1 (2), 5 (2)

Order 19; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 56.

$$B=2^{n+18},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=\sum_{j=0}^{15} c_jx^j.$$

```text
  0-15   1, 0, 2, 1, 3, 3, 3, 5, 4, 4, 2, 2, 0, 0, 0, -1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{6}\Phi_{2}(x)^{5}\Phi_{3}(x)\Phi_{4}(x)^{2}\\&\times \Phi_{6}(x)\end{aligned}$$


### BD58 — g=3, k=2; core degrees: 1 (2), 8 (1)

Order 15; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 57.

$$B=2^{n+6},\quad a(n)=0\ (n<12).$$

$$a(n)=\left\lfloor\frac{B^{n-12}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 12).$$

$$R(x)=1$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{5}\Phi_{2}(x)^{4}\Phi_{3}(x)\Phi_{4}(x)\\&\times \Phi_{6}(x)\end{aligned}$$


### BD59 — g=4, k=0; core degrees: 3 (6)

Order 39; period 24; source v32/BIPARTITE_PROFILE_MODELS.json, record 58.

$$B=2^{n+48},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=\sum_{j=0}^{36} c_jx^j.$$

```text
  0-21   1, -2, 1, 2, 7, -2, 26, 5, 71, 20, 151, 49, 260, 60, 377, 117, 456, 91, 527, 114, 488, 71
 22-36   448, 59, 325, 5, 228, 4, 115, -24, 58, -12, 18, -8, 6, -3, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{9}\Phi_{2}(x)^{6}\Phi_{3}(x)^{3}\Phi_{4}(x)^{3}\\&\times \Phi_{6}(x)^{2}\Phi_{8}(x)\Phi_{12}(x)\end{aligned}$$


### BD60 — g=4, k=0; core degrees: 3 (4), 4 (1)

Order 30; period 24; source v32/BIPARTITE_PROFILE_MODELS.json, record 59.

$$B=2^{n+38},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=\sum_{j=0}^{26} c_jx^j.$$

```text
  0-19   1, 1, 7, 10, 35, 47, 115, 126, 249, 227, 404, 313, 508, 323, 502, 257, 405, 139, 248, 42
 20-26   122, -8, 44, -13, 10, -6, 2
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{8}\Phi_{2}(x)^{6}\Phi_{3}(x)^{2}\Phi_{4}(x)^{3}\\&\times \Phi_{6}(x)\Phi_{8}(x)\end{aligned}$$


### BD61 — g=4, k=0; core degrees: 3 (3), 5 (1)

Order 26; period 24; source v32/BIPARTITE_PROFILE_MODELS.json, record 60.

$$B=2^{n+29},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=\sum_{j=0}^{22} c_jx^j.$$

```text
  0-22   1, 3, 3, 8, 13, 27, 22, 41, 31, 63, 27, 64, 13, 60, 3, 36, -10, 20, -5, 5, -4, 0, -1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{7}\Phi_{2}(x)^{5}\Phi_{3}(x)^{2}\Phi_{4}(x)^{2}\\&\times \Phi_{6}(x)\Phi_{8}(x)\end{aligned}$$


### BD62 — g=4, k=0; core degrees: 3 (2), 4 (2)

Order 29; period 24; source v32/BIPARTITE_PROFILE_MODELS.json, record 61.

$$B=2^{n+36},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=\sum_{j=0}^{25} c_jx^j.$$

```text
  0-20   1, 3, 5, 17, 30, 64, 77, 142, 156, 252, 224, 321, 254, 335, 214, 261, 139, 166, 57, 71, 12
 21-25   26, -3, 4, -2, 2
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{7}\Phi_{2}(x)^{6}\Phi_{3}(x)^{2}\Phi_{4}(x)^{3}\\&\times \Phi_{6}(x)\Phi_{8}(x)\end{aligned}$$


### BD63 — g=4, k=0; core degrees: 3 (2), 6 (1)

Order 25; period 24; source v32/BIPARTITE_PROFILE_MODELS.json, record 62.

$$B=2^{n+26},\quad a(n)=0\ (n<9).$$

$$a(n)=\left\lfloor\frac{B^{n-9}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 9).$$

$$R(x)=\sum_{j=0}^{18} c_jx^j.$$

```text
  0-18   1, 2, 3, 5, 6, 11, 14, 17, 12, 16, 14, 16, 5, 7, 2, 5, -1, 0, -1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{6}\Phi_{2}(x)^{5}\Phi_{3}(x)^{2}\Phi_{4}(x)^{2}\\&\times \Phi_{6}(x)\Phi_{8}(x)\end{aligned}$$


### BD64 — g=4, k=0; core degrees: 3 (1), 4 (1), 5 (1)

Order 19; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 63.

$$B=2^{n+20},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=\sum_{j=0}^{16} c_jx^j.$$

```text
  0-16   1, 1, 4, 3, 9, 4, 14, 0, 16, -3, 11, -3, 5, -2, 0, 0, -1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{6}\Phi_{2}(x)^{5}\Phi_{3}(x)\Phi_{4}(x)^{2}\\&\times \Phi_{6}(x)\end{aligned}$$


### BD65 — g=4, k=0; core degrees: 3 (1), 7 (1)

Order 17; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 64.

$$B=2^{n+11},\quad a(n)=0\ (n<11).$$

$$a(n)=\left\lfloor\frac{B^{n-11}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 11).$$

$$R(x)=1+2x^{3}-x^{4}+2x^{5}-x^{6}$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{5}\Phi_{2}(x)^{4}\Phi_{3}(x)\Phi_{4}(x)^{2}\\&\times \Phi_{6}(x)\end{aligned}$$


### BD66 — g=4, k=0; core degrees: 4 (3)

Order 30; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 65.

$$B=2^{n+30},\quad a(n)=0\ (n<9).$$

$$a(n)=\left\lfloor\frac{B^{n-9}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 9).$$

$$R(x)=\sum_{j=0}^{26} c_jx^j.$$

```text
  0-26   3, 0, 3, 0, 11, 0, 14, 0, 21, 0, 15, 0, 22, 0, 10, 0, 10, 0, 5, 0, 0, 0, -1, 0, 0, 0, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{6}\Phi_{2}(x)^{6}\Phi_{3}(x)^{2}\Phi_{4}(x)^{3}\\&\times \Phi_{6}(x)^{2}\Phi_{12}(x)\end{aligned}$$


### BD67 — g=4, k=0; core degrees: 4 (1), 6 (1)

Order 18; period 12; source v32/BIPARTITE_PROFILE_MODELS.json, record 66.

$$B=2^{n+15},\quad a(n)=0\ (n<9).$$

$$a(n)=\left\lfloor\frac{B^{n-9}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 9).$$

$$R(x)=\sum_{j=0}^{12} c_jx^j.$$

```text
  0-12   1, 0, 1, 0, 2, 0, 2, 0, 2, 0, 0, 0, -1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{5}\Phi_{2}(x)^{5}\Phi_{3}(x)\Phi_{4}(x)^{2}\\&\times \Phi_{6}(x)\end{aligned}$$


### BD68 — g=4, k=0; core degrees: 5 (2)

Order 25; period 120; source v32/BIPARTITE_PROFILE_MODELS.json, record 67.

$$B=2^{n+25},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=\sum_{j=0}^{19} c_jx^j.$$

```text
  0-19   1, 0, 0, 1, 1, 1, 1, 3, 2, 3, 2, 4, 1, 2, 0, 2, 0, 1, 0, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{5}\Phi_{2}(x)^{4}\Phi_{3}(x)\Phi_{4}(x)^{2}\\&\times \Phi_{5}(x)\Phi_{6}(x)\Phi_{8}(x)\end{aligned}$$


### BD69 — g=4, k=0; core degrees: 8 (1)

Order 20; period 24; source v32/BIPARTITE_PROFILE_MODELS.json, record 68.

$$B=2^{n+10},\quad a(n)=0\ (n<13).$$

$$a(n)=\left\lfloor\frac{B^{n-13}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 13).$$

$$R(x)=1$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{4}\Phi_{2}(x)^{4}\Phi_{3}(x)\Phi_{4}(x)^{2}\\&\times \Phi_{6}(x)\Phi_{8}(x)\end{aligned}$$


## Unicyclic graphs: independent construction


### C01 — g=1, k=1

Order 2; period 1; source v32/UNICYCLIC_MODELS.json, record 0.

$$B=2^{n+1},\quad a(n)=0\ (n<4).$$

$$a(n)=\left\lfloor\frac{B^{n-4}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 4).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{2}$$

Same rational function as G06.


### C02 — g=1, k=2

Order 6; period 2; source v32/UNICYCLIC_MODELS.json, record 1.

$$B=2^{n+6},\quad a(n)=0\ (n<5).$$

$$a(n)=\left\lfloor\frac{B^{n-5}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 5).$$

$$R(x)=2+2x-x^{2}$$

$$Q(x)=\Phi_{1}(x)^{4}\Phi_{2}(x)^{2}$$

Same rational function as G07.


### C03 — g=1, k=3

Order 12; period 6; source v32/UNICYCLIC_MODELS.json, record 2.

$$B=2^{n+14},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=3+5x+8x^{2}+9x^{3}+5x^{4}+2x^{5}+x^{6}$$

$$Q(x)=\Phi_{1}(x)^{6}\Phi_{2}(x)^{2}\Phi_{3}(x)^{2}$$

Same rational function as G08.


### C04 — g=1, k=4

Order 18; period 12; source v32/UNICYCLIC_MODELS.json, record 3.

$$B=2^{n+21},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$\begin{aligned}R(x)&=4+9x+16x^{2}+33x^{3}+40x^{4}+48x^{5}\\&+40x^{6}+34x^{7}+17x^{8}+10x^{9}+x^{10}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{8}\Phi_{2}(x)^{4}\Phi_{3}(x)\Phi_{4}(x)^{2}$$

Same rational function as G09.


### C05 — g=1, k=5

Order 26; period 60; source v32/UNICYCLIC_MODELS.json, record 4.

$$B=2^{n+33},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=\sum_{j=0}^{18} c_jx^j.$$

```text
  0-18   5, 17, 47, 106, 208, 337, 476, 602, 678, 672, 603, 472, 326, 191, 96, 41, 11, 1, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{10}\Phi_{2}(x)^{4}\Phi_{3}(x)\Phi_{4}(x)\\&\times \Phi_{5}(x)^{2}\end{aligned}$$


### C06 — g=1, k=6

Order 36; period 60; source v32/UNICYCLIC_MODELS.json, record 5.

$$B=2^{n+47},\quad a(n)=0\ (n<9).$$

$$a(n)=\left\lfloor\frac{B^{n-9}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 9).$$

$$R(x)=\sum_{j=0}^{26} c_jx^j.$$

```text
  0-14   7, 29, 104, 311, 743, 1594, 2972, 4999, 7613, 10738, 13799, 16576, 18377, 19037, 18227
 15-26   16360, 13474, 10353, 7257, 4676, 2682, 1399, 611, 234, 71, 16, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{12}\Phi_{2}(x)^{6}\Phi_{3}(x)^{4}\Phi_{4}(x)\\&\times \Phi_{5}(x)\Phi_{6}(x)^{2}\end{aligned}$$


### C07 — g=1, k=7

Order 46; period 420; source v32/UNICYCLIC_MODELS.json, record 6.

$$B=2^{n+61},\quad a(n)=0\ (n<10).$$

$$a(n)=\left\lfloor\frac{B^{n-10}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 10).$$

$$R(x)=\sum_{j=0}^{36} c_jx^j.$$

```text
  0-13   8, 46, 196, 669, 1937, 4829, 10702, 21330, 38810, 65103, 101589, 148234, 203364, 263196
 14-24   322405, 374469, 413108, 433125, 431896, 409442, 368868, 315358, 255444, 195470, 140909
 25-36   95213, 59967, 34903, 18607, 8939, 3811, 1396, 429, 107, 19, 1, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{14}\Phi_{2}(x)^{6}\Phi_{3}(x)^{3}\Phi_{4}(x)\\&\times \Phi_{5}(x)\Phi_{6}(x)\Phi_{7}(x)^{2}\end{aligned}$$


### C08 — g=1, k=8

Order 58; period 840; source v32/UNICYCLIC_MODELS.json, record 7.

$$B=2^{n+77},\quad a(n)=0\ (n<11).$$

$$a(n)=\left\lfloor\frac{B^{n-11}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 11).$$

$$R(x)=\sum_{j=0}^{46} c_jx^j.$$

```text
  0-12   10, 59, 281, 1107, 3598, 10282, 25985, 59684, 124976, 242666, 438355, 744697, 1192503
 13-22   1813288, 2622236, 3625004, 4794431, 6088898, 7427730, 8726263, 9871827, 10774204, 11338582
 23-31   11521233, 11292367, 10685467, 9747554, 8576109, 7262454, 5919447, 4630574, 3474942
 32-43   2491454, 1704803, 1106781, 680397, 392599, 211957, 105598, 48337, 19874, 7291, 2291, 611
 44-46   131, 22, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{16}\Phi_{2}(x)^{8}\Phi_{3}(x)^{3}\Phi_{4}(x)^{4}\\&\times \Phi_{5}(x)\Phi_{6}(x)\Phi_{7}(x)\Phi_{8}(x)^{2}\end{aligned}$$


### C09 — g=1, k=9

Order 72; period 2520; source v32/UNICYCLIC_MODELS.json, record 8.

$$B=2^{n+96},\quad a(n)=0\ (n<12).$$

$$a(n)=\left\lfloor\frac{B^{n-12}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 12).$$

$$R(x)=\sum_{j=0}^{60} c_jx^j.$$

```text
  0-12   12, 94, 557, 2571, 9957, 33430, 99665, 267617, 656539, 1485395, 3125972, 6162344, 11449368
 13-20   20150706, 33747923, 53987483, 82768507, 121951211, 173106177, 237210248, 314356460
 21-28   403483438, 502223217, 606873806, 712557157, 813531726, 903692195, 977128843, 1028753582
 29-36   1054844136, 1053475880, 1024726907, 970694450, 895232066, 803534979, 701565546, 595451638
 37-44   490891738, 392703216, 304486706, 228501749, 165691876, 115864896, 77949712, 50314879
 45-54   31056942, 18260497, 10179560, 5351197, 2634851, 1205955, 508126, 194900, 67044, 20360
 55-60   5310, 1168, 207, 27, 1, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{18}\Phi_{2}(x)^{8}\Phi_{3}(x)^{6}\Phi_{4}(x)^{3}\\&\times \Phi_{5}(x)\Phi_{6}(x)\Phi_{7}(x)\Phi_{8}(x)\\&\times \Phi_{9}(x)^{2}\end{aligned}$$


### C10 — g=1, k=10

Order 88; period 2520; source v32/UNICYCLIC_MODELS.json, record 9.

$$B=2^{n+118},\quad a(n)=0\ (n<13).$$

$$a(n)=\left\lfloor\frac{B^{n-13}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 13).$$

$$R(x)=\sum_{j=0}^{74} c_jx^j.$$

```text
  0-11   14, 130, 851, 4444, 19376, 73352, 246128, 745679, 2063392, 5270851, 12526260, 27893688
 12-19   58533320, 116350441, 220026716, 397404949, 687851909, 1144403209, 1834935746, 2842142162
 20-26   4261289822, 6195906773, 8750418080, 12020786216, 16082516875, 20978384615, 26705534800
 27-33   33205529091, 40356695212, 47972901408, 55806858954, 63561711406, 70906923073, 77501297093
 34-40   83016926131, 87166206950, 89724384109, 90550034394, 89596126669, 86915520253, 82655060641
 41-47   77044145435, 70373945808, 62974644771, 55188338348, 47345087986, 39740043055, 32617755371
 48-54   26160890381, 20487225340, 15651217144, 11651928611, 8443246205, 5946935846, 4065031576
 55-62   2691835418, 1723245506, 1064008293, 631911297, 359867922, 195809274, 101379944, 49703488
 63-74   22948357, 9911579, 3974438, 1465585, 491671, 147905, 39262, 8983, 1721, 267, 30, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{20}\Phi_{2}(x)^{10}\Phi_{3}(x)^{5}\Phi_{4}(x)^{3}\\&\times \Phi_{5}(x)^{4}\Phi_{6}(x)\Phi_{7}(x)\Phi_{8}(x)\\&\times \Phi_{9}(x)\Phi_{10}(x)^{2}\end{aligned}$$


### C11 — g=1, k=11

Order 102; period 27720; source v32/UNICYCLIC_MODELS.json, record 10.

$$B=2^{n+136},\quad a(n)=0\ (n<14).$$

$$a(n)=\left\lfloor\frac{B^{n-14}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 14).$$

$$R(x)=\sum_{j=0}^{88} c_jx^j.$$

```text
  0-11   16, 169, 1236, 7067, 33830, 139932, 513055, 1694713, 5109802, 14203809, 36703828, 88776203
 12-18   202174608, 435718716, 892636906, 1745165318, 3267437616, 5876712262, 10181773762
 19-24   17035376991, 27585789148, 43320101969, 66090594439, 98113909175, 141933407243
 25-30   200335877170, 276217653448, 372398964642, 491392379060, 635136728659, 804715990960
 31-36   1000086782681, 1219843716850, 1461051018851, 1719168715197, 1988093598012, 2260328701342
 37-42   2527280700405, 2779674642586, 3008059399142, 3203369286900, 3357495701269, 3463822390339
 43-48   3517675394709, 3516648760673, 3460773952105, 3352519045004, 3196615718230, 2999732098906
 49-54   2770019632839, 2516576921908, 2248875756994, 1976199576128, 1707136964572, 1449168276668
 55-60   1208368680368, 989241294419, 794677937445, 626036341150, 483310850577, 365370426598
 61-66   270233182579, 195349968814, 137871456358, 94880746904, 63578735642, 41417652857
 67-73   26183026768, 16030095009, 9482881905, 5406412518, 2961884429, 1554074110, 777983798
 74-83   369984202, 166318447, 70266268, 27712637, 10123604, 3393325, 1032220, 280988, 67348, 13874
 84-88   2405, 335, 35, 1, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{22}\Phi_{2}(x)^{10}\Phi_{3}(x)^{5}\Phi_{4}(x)^{3}\\&\times \Phi_{5}(x)^{3}\Phi_{6}(x)\Phi_{7}(x)\Phi_{8}(x)\\&\times \Phi_{9}(x)\Phi_{10}(x)\Phi_{11}(x)^{2}\end{aligned}$$


### C12 — g=1, k=12

Order 122; period 27720; source v32/UNICYCLIC_MODELS.json, record 11.

$$B=2^{n+163},\quad a(n)=0\ (n<15).$$

$$a(n)=\left\lfloor\frac{B^{n-15}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 15).$$

$$R(x)=\sum_{j=0}^{106} c_jx^j.$$

```text
  0-10   19, 199, 1568, 9711, 50159, 225381, 898402, 3236135, 10658070, 32428812, 91860073
 11-17   243924621, 610530855, 1447550585, 3264737626, 7030521324, 14503557617, 28747496644
 18-23   54891707571, 101212782944, 180600282924, 312469352090, 525135109459, 858642881820
 24-29   1367948110047, 2126307637476, 3228589187017, 4794196214331, 6969115071056, 9926666921163
 30-34   13866353009959, 19010422971518, 25597623850534, 33874058828380, 44080925897154
 35-39   56439627706112, 71134522668542, 88294518379244, 107974286244530, 130136918050200
 40-44   154639061751741, 181220618498537, 209499802695117, 238975367673312, 269035985390254
 45-49   298977768022473, 328028678011745, 355379718739443, 380220337724616, 401776980959913
 50-54   419351306624763, 432356599075191, 440348730438749, 443050613997361, 440367193579343
 55-59   432391055558593, 419397047482381, 401827492201839, 380267900011053, 355416107074577
 60-64   328045898760584, 298968755445537, 268995204236266, 238899255969056, 209387035249664
 65-69   181072162267891, 154458042754891, 129928310402811, 107744478612182, 88050789738582
 70-74   70884497313298, 56190744649408, 43839980448240, 33646835790183, 25388655798464
 75-80   18822866169332, 13701987453322, 9785992800133, 6851531400808, 4698225723608, 3152129761776
 81-86   2066877728161, 1322912449340, 825398778429, 501255797267, 295798827203, 169305766465
 87-93   93798511141, 50184915084, 25864021852, 12803072421, 6067765293, 2743106684, 1178026512
 94-103  478274693, 182572474, 65105014, 21526796, 6540309, 1806574, 447648, 97898, 18496, 2922
104-106  379, 35, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{24}\Phi_{2}(x)^{12}\Phi_{3}(x)^{8}\Phi_{4}(x)^{6}\\&\times \Phi_{5}(x)^{3}\Phi_{6}(x)^{4}\Phi_{7}(x)\Phi_{8}(x)\\&\times \Phi_{9}(x)\Phi_{10}(x)\Phi_{11}(x)\Phi_{12}(x)^{2}\end{aligned}$$


### C13 — g=1, k=13

Order 138; period 360360; source v32/UNICYCLIC_MODELS.json, record 12.

$$B=2^{n+183},\quad a(n)=0\ (n<16).$$

$$a(n)=\left\lfloor\frac{B^{n-16}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 16).$$

$$R(x)=\sum_{j=0}^{122} c_jx^j.$$

```text
  0-10   21, 252, 2163, 14440, 80769, 390621, 1676163, 6484900, 22920792, 74741297, 226701881
 11-17   643886401, 1722287342, 4359747731, 10488945489, 24073787012, 52886928453, 111541703534
 18-23   226452159832, 443627039570, 840460344155, 1542919496147, 2749728360732, 4765215779209
 24-28   8042422002501, 13237714376362, 21277560127431, 33437120258775, 51429047180846
 29-33   77499195758561, 114524115321789, 166103124445371, 236635879692510, 331374593406850
 34-38   456438999898350, 618781702936393, 826092329122008, 1086630642325104, 1408982119813142
 39-43   1801733770904651, 2273073798129397, 2830324913870146, 3479428261887500, 4224401342155028
 44-48   5066799670661958, 6005216169724450, 7034855318543932, 8147218821409697, 9329937348334277
 49-52   10566776798137966, 11837839652761781, 13119970593710353, 14387363563308562
 53-56   15612353318655579, 16766361805191125, 17820956762470066, 18748970719013068
 57-60   19525620926644874, 20129568563067089, 20543855964238741, 20756667025842110
 61-64   20761864640730069, 20559272848790246, 20154685917681101, 19559604164206106
 65-68   18790712222837957, 17869131898653060, 16819494062274944, 15668884770765138
 69-72   14445725833680308, 13178652451888077, 11895447047846017, 10622082610901602
 73-77   9381918314332759, 8195078793085957, 7078034382492715, 6043386733630846, 5099850838200556
 78-82   4252414086265390, 3502643756387398, 2849109037880442, 2287880284011062, 1813068630043339
 83-87   1417371161919944, 1092591753208790, 830113282380747, 621304036725084, 457847728235467
 88-92   331993363291581, 236726675851852, 165869638483229, 114117661992530, 77026237835632
 93-97   50959369937330, 33011965688953, 20917122274921, 12947666663650, 7819255526459
 98-103  4600371585228, 2632573601883, 1462731543334, 787593465500, 410072231254, 205969904994
104-110  99535925136, 46142266568, 20451011577, 8633611741, 3456863202, 1306361708, 463354910
111-122  153249881, 46909214, 13168432, 3354930, 765118, 153874, 26627, 3886, 451, 44, 0, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{26}\Phi_{2}(x)^{12}\Phi_{3}(x)^{7}\Phi_{4}(x)^{5}\\&\times \Phi_{5}(x)^{3}\Phi_{6}(x)^{3}\Phi_{7}(x)\Phi_{8}(x)\\&\times \Phi_{9}(x)\Phi_{10}(x)\Phi_{11}(x)\Phi_{12}(x)\\&\times \Phi_{13}(x)^{2}\end{aligned}$$


### C14 — g=1, k=14

Order 160; period 360360; source v32/UNICYCLIC_MODELS.json, record 13.

$$B=2^{n+212},\quad a(n)=0\ (n<17).$$

$$a(n)=\left\lfloor\frac{B^{n-17}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 17).$$

$$R(x)=\sum_{j=0}^{142} c_jx^j.$$

```text
  0-10   24, 316, 2924, 21253, 128566, 673460, 3125011, 13075988, 49958913, 176088842, 577191844
 11-17   1771458268, 5119399513, 13999490597, 36378638759, 90166037032, 213862129881, 486857173323
 18-23   1066586916406, 2254023987128, 4605020960238, 9113292739980, 17501484503468, 32670087332408
 24-28   59369409079048, 105177086412511, 181880901200479, 307382824930706, 508251596814191
 29-33   823056052342490, 1306604270528699, 2035193254525196, 3112933318993531, 4679152225025848
 34-37   6916799059575576, 10061664303046877, 14412103821300401, 20338817117618230
 38-41   28294078089732181, 38819677705112612, 52552704875270554, 70228204454376046
 42-45   92677695412009138, 120822558527391795, 155661382382541564, 198250547308966464
 46-49   249677575995012765, 311027149937218395, 383340096726787864, 467566162524081716
 50-53   564511873079714670, 674785333407986821, 798740259509742592, 936421973882890285
 54-57   1087518337715461872, 1251318770338009228, 1426684407395143597, 1612032257724802167
 58-61   1805335710487341452, 2004143165316859437, 2205615678501730793, 2406583649267214404
 62-65   2603621472913889848, 2793138131016525689, 2971480614651550519, 3135046293534720670
 66-69   3280399558314590011, 3404387700511978242, 3504250710079848316, 3577719884207022804
 70-73   3623100448284977110, 3639334190524841320, 3626038943959102771, 3583522989175824698
 74-77   3512773595466753387, 3415420326300764181, 3293674889873808253, 3150250574002320737
 78-81   2988265165359013912, 2811132085670748412, 2622444823159392286, 2425859986775538666
 82-85   2224984063999676791, 2023268629133236735, 1823917990913625966, 1629812499631922175
 86-89   1443449671268431747, 1266904326556310380, 1101807840585391140, 949345711308422347
 90-93   810271758260581029, 684936656699812048, 573327981510455320, 475118715276816350
 94-97   389721055776674576, 316342513169656410, 254041516166194676, 201780172035870888
 98-101  158472266538164357, 123025134263131599, 94374525708164046, 71512112410680369
102-105  53505689504976974, 39512515110170373, 28786488420298391, 20680068696331543
106-110  14641927853042420, 10211362150784300, 7010439424327648, 4734773436145359, 3143686170635537
111-115  2050379041538160, 1312580935080817, 824000479752528, 506778598839215, 305030169653184
116-120  179475771110848, 103102315797431, 57748784667870, 31491043947088, 16691593771973
121-126  8584266436356, 4275167769917, 2057355287166, 954402068006, 425660237611, 181975341185
127-133  74324496337, 28892711311, 10644703455, 3698779243, 1205444234, 366099531, 102838172
134-142  26482015, 6185412, 1293550, 238240, 37867, 5026, 546, 42, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{28}\Phi_{2}(x)^{14}\Phi_{3}(x)^{7}\Phi_{4}(x)^{5}\\&\times \Phi_{5}(x)^{3}\Phi_{6}(x)^{3}\Phi_{7}(x)^{4}\Phi_{8}(x)\\&\times \Phi_{9}(x)\Phi_{10}(x)\Phi_{11}(x)\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)^{2}\end{aligned}$$


### C15 — g=1, k=15

Order 184; period 360360; source v32/UNICYCLIC_MODELS.json, record 14.

$$B=2^{n+245},\quad a(n)=0\ (n<18).$$

$$a(n)=\left\lfloor\frac{B^{n-18}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 18).$$

$$R(x)=\sum_{j=0}^{166} c_jx^j.$$

```text
  0-10   27, 438, 4706, 38896, 266530, 1573202, 8205102, 38484377, 164503967, 647493736, 2366316390
 11-16   8084598953, 25971179176, 78832663239, 227065467473, 622939747311, 1633143303987
 17-21   4103593608213, 9908658789350, 23046982376812, 51749385419258, 112395540546559
 22-26   236556237737529, 483265958845911, 959782908845771, 1855721846487345, 3497667642193631
 27-30   6434307551304729, 11565847665854809, 20336046093980412, 35010569177918077
 31-34   59071416925624694, 97763592601094957, 158836566475871191, 253528782692829741
 35-38   397847671765994939, 614199383898347719, 933420641306904371, 1397258551322039409
 39-42   2061331777630562548, 2998587133952641743, 4303238711054328000, 6095141772735219661
 43-46   8524511112788261663, 11776844312038894343, 16077856107684180645, 21698173477688642314
 47-50   28957485448529546688, 38227791211801834638, 49935349581382995350, 64560907176711700956
 51-54   82637776967074709575, 104747357573719093832, 131511730737675721814, 163583052130478579015
 55-58   201629559984054126074, 246318165647474964516, 298293756612337297476, 358155529962583116947
 59-62   426430874398096055301, 503547521794897066981, 589804882837557880351, 685345652842719893613
 63-65   790128910398163089417, 903906020545279459116, 1026200685039999245904
 66-68   1156294446447670204537, 1293218845302211144186, 1435755249227883570422
 69-71   1582443122931704129114, 1731597196199110096678, 1881333625555863454679
 72-74   2029604850334145673484, 2174242434718511287525, 2313006785534080524052
 75-77   2443642263340817466170, 2563935883842623789183, 2671777557600317404645
 78-80   2765219655446159116724, 2842533627020495540663, 2902261447545299983750
 81-83   2943259824089186095190, 2964735351973471615699, 2966269163077254910194
 84-86   2947830033882382399878, 2909775400599939496057, 2852840237113790980953
 87-89   2778114262176831792449, 2687008428862697049127, 2581212086450101737741
 90-92   2462642570737695779778, 2333389255319213506410, 2195654271287328348222
 93-95   2051692169581484717400, 1903750758686345163443, 1754015206366978287174
 96-98   1604557259153510600135, 1457291123300910554418, 1313937185639283069224
 99-101  1175994353681788179742, 1044721384137691708543, 921127169248969147783
102-105  805969581079687353850, 699762151741390929894, 602787605606813120422, 515117066357141345324
106-109  436633641370910228998, 367059038013033744123, 305981886462497949777, 252886523880936835514
110-113  207181124551099338019, 168224227805910895948, 135348907155220476970, 107884026980438261528
114-117  85172235475048822721, 66584533538443425910, 51531430549550985081, 39470843010791090610
118-121  29913007080885668547, 22422759357490716566, 16619592437870606418, 12175914987290367767
122-125  8813943903999744360, 6301633179800540233, 4448005238881182038, 3098200958685767321
126-129  2128509071472872335, 1441578486231984491, 961961837575679566, 632087993613833983
130-133  408717242435028980, 259896502346305250, 162403536271848534, 99648560426459913
134-137  59988147328006571, 35398946989991030, 20456345191530747, 11564551352442556
138-142  6388626706769141, 3444610947929373, 1810337640978467, 926084320633990, 460409503728856
143-147  222081340570295, 103742722257653, 46839088267267, 20394135977137, 8542605351084
148-153  3433146776391, 1319804399273, 483713967033, 168383243986, 55437170285, 17179352149
154-163  4983440316, 1344663298, 335007666, 76394027, 15779958, 2914735, 473929, 66385, 7823, 741
164-166  54, 2, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{30}\Phi_{2}(x)^{14}\Phi_{3}(x)^{10}\Phi_{4}(x)^{5}\\&\times \Phi_{5}(x)^{6}\Phi_{6}(x)^{3}\Phi_{7}(x)^{3}\Phi_{8}(x)\\&\times \Phi_{9}(x)\Phi_{10}(x)\Phi_{11}(x)\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)^{2}\end{aligned}$$


### C16 — g=1, k=16

Order 208; period 720720; source v32/UNICYCLIC_MODELS.json, record 15.

$$B=2^{n+275},\quad a(n)=0\ (n<19).$$

$$a(n)=\left\lfloor\frac{B^{n-19}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 19).$$

$$R(x)=\sum_{j=0}^{188} c_jx^j.$$

```text
  0-9    30, 499, 5538, 47807, 342242, 2113878, 11543161, 56730437, 254226687, 1049601715
 10-15   4025326507, 14438195935, 48712486232, 155348085730, 470266902630, 1356323949921
 16-20   3739238249264, 9882568873952, 25104982639745, 61444047994657, 145198221700173
 21-25   331935906736432, 735422269286052, 1581699492853294, 3307309772938063, 6732844815261939
 26-29   13361632452440663, 25881036666725408, 48983816107105647, 90683199306693558
 30-33   164372297919087275, 291981101082300723, 508717484723154591, 870046905221839282
 34-37   1461771969250594337, 2414319170886726706, 3922623893488924940, 6273320426914065915
 38-41   9881279939656974820, 15337878776362780452, 23473697472606235104, 35438615897230671769
 42-45   52802442563135517149, 77679251363240804092, 112878446148030339456, 162085181012373140899
 46-49   230072080128631967858, 322943181013930170669, 448409633227003941177, 616094903217880027410
 50-52   837865066273360704543, 1128177239555045547717, 1504436383900825436451
 53-55   1987347673605483102164, 2601248528815506961447, 3374401392071510583447
 56-58   4339225597819826802080, 5532444454061209402983, 6995122153128153893755
 59-61   8772564593432142197059, 10914058836145245298504, 13472427938797986240690
 62-64   16503381432830260728622, 20064646835273210157847, 24214874292107281086095
 65-67   29012314667568241658909, 34513280913127979656470, 40770413101042595849005
 68-70   47830778680356004101437, 55733850855685563983691, 64509418927860342127557
 71-73   74175494404532172757520, 84736285043942154266466, 96180315171623265283181
 74-76   108478774023629211782196, 121584174099984485995071, 135429398177234077869998
 77-79   149927206588508786244087, 164970265574779938398821, 180431743175747779206791
 80-82   196166501587344095969327, 212012894793855344766217, 227795158269343387297180
 83-85   243326354589024487344428, 258411815824273575137662, 272853001738539464117888
 86-88   286451673040415346538689, 299014262366305815049505, 310356313077975988126207
 89-91   320306848187981496196853, 328712529216783771458713, 335441467914540358118856
 92-94   340386562487159502772191, 343468244092280062109178, 344636538313831816661373
 95-97   343872369417817131938130, 341188061379254189086572, 336627017916530477044164
 98-100  330262592751343264937873, 322196189851573028271863, 312554660172273685183696
101-103  301487085321759810128985, 289161058545925396330095, 275758588724743113348629
104-106  261471763049089528820073, 246498308470807530698538, 231037190771416571981382
107-109  215284383488759384490699, 199428927373258440639901, 183649385288986538882191
110-112  168110778319277976871369, 152962067342795787452807, 138334221495677112427927
113-115  124338891857389652353330, 111067686342459139699081, 98592021128373348215054
116-118  86963505725833286595575, 76214803670656782660179, 66360899160314062377382
119-121  57400692049400841920071, 49318839444823285754261, 42087761598076722800401
122-124  35669732531889569415839, 30018981461918522665206, 25083739014443672267502
125-127  20808171937651107134585, 17134160813328328965662, 14002886620232008220911
128-130  11356203293755558627853, 9137784194590345434047, 7294040211088473056503
131-133  5774815779113335997239, 4533876180509946389524, 3529204978267609295421
134-136  2723134331004386150279, 2082333275216224016541, 1577679991058415976890
137-139  1184043765795469924867, 880001045788443695959, 647507861353818344497
140-143  471548247158506336841, 339775291313699317466, 242158325718377459229, 170646693694584534854
144-147  118857633642664296096, 81793204465354740137, 55588915694006753454, 37294850184423572926
148-151  24688586422072645473, 16118127142266199704, 10372287921986599467, 6575550362639545471
152-155  4104188113464923120, 2520477906248838616, 1521960222387653686, 902968434968607242
156-159  525960107679351382, 300526062728902086, 168295488930490055, 92279862215852600
160-163  49492229864970252, 25934586601530528, 13262086879492766, 6609518542117907
164-168  3205831698854136, 1510980436744657, 690873948557267, 305892029340418, 130887619147127
169-174  54005222403713, 21435194128428, 8162233375373, 2972942825401, 1032324340890, 340469760162
175-182  106205734235, 31185485888, 8572824901, 2192457646, 517834179, 111981747, 21942382, 3846840
183-188  593703, 79058, 8801, 795, 50, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{32}\Phi_{2}(x)^{16}\Phi_{3}(x)^{9}\Phi_{4}(x)^{8}\\&\times \Phi_{5}(x)^{5}\Phi_{6}(x)^{3}\Phi_{7}(x)^{3}\Phi_{8}(x)^{4}\\&\times \Phi_{9}(x)\Phi_{10}(x)\Phi_{11}(x)\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\Phi_{16}(x)^{2}\end{aligned}$$


### C17 — g=1, k=17

Order 228; period 12252240; source v32/UNICYCLIC_MODELS.json, record 16.

$$B=2^{n+300},\quad a(n)=0\ (n<20).$$

$$a(n)=\left\lfloor\frac{B^{n-20}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 20).$$

$$R(x)=\sum_{j=0}^{208} c_jx^j.$$

```text
  0-9    33, 591, 7011, 64086, 485849, 3171321, 18284959, 94775431, 447542128, 1945314929
 10-15   7848387573, 29592305916, 104878221828, 351101584034, 1114980141559, 3371346163409
 16-20   9737978248235, 26948549586236, 71638240030856, 183370155803069, 452921894226611
 21-25   1081642211311289, 2502031686910235, 5615276250423952, 12245686094657801, 25986251296571415
 26-29   53730758991983678, 108380553257099270, 213512227928008667, 411242669600139310
 30-33   775190864934589400, 1431389384272195221, 2591338102994329076, 4603232186594136046
 34-37   8029865456489511239, 13764950402371113634, 23203752728183765030, 38489149273263080578
 38-41   62860598298519517449, 101141132492686791587, 160406353501813930321, 250889435333122563419
 42-44   387187125019403451500, 589843306129108194981, 887398334582759864561
 45-47   1319003344476416862206, 1937708129705819282794, 2814537910039063444681
 48-50   4043476981409629151571, 5747474477299335400777, 8085577691885928500030
 51-53   11261280087169838933345, 15532142768816643779112, 21220708620668717900946
 54-56   28726676531756297497911, 38540238810403546588271, 51256408163173478901095
 57-59   67590072481868971929262, 88391417959620719829025, 114661256519785218988943
 60-62   147565685944530140225804, 188449405144184388231439, 238846908303576632840174
 63-65   300490696484243115120226, 375315580460882566380614, 465458111133591999517321
 66-68   573250170646829477382662, 701205794661310985375775, 852000379383600636246516
 69-71   1028441559832333270377795, 1233431230428602823863853, 1469918415100695276619876
 72-74   1740842978904662119654559, 2049070501117632679904859, 2397318992464182048979711
 75-77   2788078525395444988797226, 3223525242428958457331340, 3705431597569483038568256
 78-80   4235075052278483797623408, 4813147771929565908016474, 5439670132710429530085605
 81-83   6113911034847276074833114, 6834318109986559651178090, 7598460895430734810911500
 84-86   8402989916204482676372099, 9243614362513121253028022, 10115100674981884729040790
 87-89   11011293858451674655858071, 11925162747977885520128088, 12848869764367346864083077
 90-92   13773864942508434406611821, 14691003219625468532644039, 15590683161591652993016188
 93-95   16463004514919949599579760, 17297941232301797431804412, 18085525962237987841013600
 96-98   18816041448039770724642298, 19480213874325246919701077, 20069402951332386696344467
 99-101  20575783454079096871921963, 20992513042932642780257866, 21313881485273014519909397
102-104  21535436867759396819220388, 21654085020720610826517786, 21668159148879027334726537
105-107  21577457548224865828270882, 21383248254674315449986478, 21088240479819277295549892
108-110  20696523704350438870538911, 20213476282035495393272659, 19645646319421360385525374
111-113  19000608404727779337870225, 18286800434412919051184905, 17513345304138003599897525
114-116  16689862575755484182835018, 15826275394312069115991836, 14932617907486148633076578
117-119  14018848240498552419625959, 13094671715650953680747271, 12169378496820556282633729
120-122  11251699210325245170979753, 10349681373310582845194072, 9470588680500802554745625
123-125  8620824392065169247019126, 7805879261327853080645720, 7030303671040350843565677
126-128  6297702937846257690385726, 5610754119151054933469871, 4971242132782068656844218
129-131  4380112590092349439760491, 3837538454498491568495343, 3342997471279568889616929
132-134  2895357267104078690171294, 2492965080849517654589631, 2133739248647786237918083
135-137  1815259810500498561292635, 1534855915992498386464763, 1289688064184145949799692
138-140  1076823599126617200373453, 893304279716600193863742, 736205134328223759078237
141-143  602684182372704546217884, 490022944667119482144544, 395657962993103290982285
144-146  317203800115660443040311, 252468191231300586636108, 199460165397180586811692
147-149  156392052374358585498351, 121676339914463968601441, 93918353802264855325663
150-152  71905704041749579035570, 54595382215838301689273, 41099314306016521295890
153-155  30669077056787941161473, 22680380822790756568524, 16617813579879625933033
156-158  12060234412946964711545, 8667104357411050271313, 6165951031057469483455
159-161  4341083141077728677353, 3023602884834887806952, 2082708880732973475652
162-164  1418239300953001127578, 954373534734259642068, 634389811347195204275
165-168  416364329518404073330, 269693027235042263691, 172318617463091527775, 108551416600295084599
169-172  67381441002134091692, 41190056801047821338, 24781152061768909291, 14663576670745043782
173-176  8527880807895119574, 4870775477913994694, 2729993405429827731, 1500230507151880871
177-180  807582917224998510, 425421741528347540, 219075760387241424, 110157592173203836
181-184  54018730415373018, 25799143982330869, 11983131300080643, 5404543107222989
185-189  2362821475617480, 999489895128534, 408242230582303, 160649748081428, 60757186731106
190-195  22023786871369, 7628793209545, 2516711184288, 787762200424, 232974114938, 64787876190
196-204  16849388275, 4072377181, 908055913, 185191597, 34190451, 5641620, 819204, 102420, 10775
205-208  908, 61, 1, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{34}\Phi_{2}(x)^{16}\Phi_{3}(x)^{9}\Phi_{4}(x)^{7}\\&\times \Phi_{5}(x)^{5}\Phi_{6}(x)^{3}\Phi_{7}(x)^{3}\Phi_{8}(x)^{3}\\&\times \Phi_{9}(x)\Phi_{10}(x)\Phi_{11}(x)\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\Phi_{16}(x)\\&\times \Phi_{17}(x)^{2}\end{aligned}$$


### C18 — g=1, k=18

Order 258; period 12252240; source v32/UNICYCLIC_MODELS.json, record 17.

$$B=2^{n+337},\quad a(n)=0\ (n<21).$$

$$a(n)=\left\lfloor\frac{B^{n-21}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 21).$$

$$R(x)=\sum_{j=0}^{236} c_jx^j.$$

```text
  0-9    37, 662, 8123, 77257, 609183, 4144023, 24915971, 134795869, 664823819, 3020369761
 10-15   12744541331, 50288367043, 186627439358, 654593798870, 2179166558247, 6910905691133
 16-20   20946927617244, 60856339675274, 169910376100461, 456962302140494, 1186342594126458
 21-24   2978859796513264, 7247188950905298, 17110996843315160, 39266152011394580
 25-28   87700166500449162, 190888215621125463, 405389381080352424, 840934752384332844
 29-32   1705684215769611773, 3386114251601270660, 6585133947676779146, 12556148943281591902
 33-36   23492185822464030027, 43160960065213129615, 77923054470998950460, 138336547716128693576
 37-39   241644321648656450350, 415568340071368300840, 704008651519574633766
 40-42   1175475733784068726094, 1935386770120074193625, 3143744622097547392885
 43-45   5040208620262048709513, 7979174873387019669376, 12478225600162277776458
 46-48   19284194475047923104969, 29462136281595085648819, 44513685878749944165041
 49-51   66532636285017381784546, 98407039632300240138598, 144078704671463380430175
 52-54   208872580358154743391770, 299910107717041892314867, 426622101724850996373174
 55-57   601377979919842769013331, 840249051954799543999094, 1163923972022470014361943
 58-60   1598794165195299464135260, 2178225889557920613148597, 2944033404645720491526422
 61-63   3948164304632619172636958, 5254603279083602421132374, 6941494251046489265871452
 64-66   9103472919670944532848862, 11854192167459730734247296, 15329011615794134269268601
 67-69   19687809946536413106762834, 25117864666777711895249078, 31836729097680801434148145
 70-72   40095020943606192741214638, 50179021380725341846626031, 62412968832131559999658979
 73-75   77160918197911793842586668, 94828025081434660387443482, 115861106342563408866430887
 76-78   140748323970309673924718213, 170017839635541196491498444, 204235293122145445361046500
 79-81   243999969797190448871234917, 289939540858728083163503952, 342703285586183359030564485
 82-84   402953737254455986594151018, 471356733525649962567239698, 548569897455422791572979616
 85-87   635229625882782008637162862, 731936716720148560484143769, 839240824029456171217907311
 88-90   957623987974463128334718936, 1087483543766744269169957826, 1229114767374511449673387173
 91-93   1382693663751069302109987977, 1548260343349176876659348348, 1725703462498962554314647068
 94-96   1914746220789462564193519238, 2114934412154771204786560745, 2325627014538844710361237491
 97-99   2545989774897956390142466513, 2774992201523959822010437247, 3011408314481302256801860202
100-102  3253821428208739889097495798, 3500633149569594579312460246, 3750076671973387159830077154
103-105  4000234334368790214454090080, 4249059296136635851845399813, 4494401058833828992619923419
106-108  4734034447252741536436618568, 4965691549430344875312230218, 5187096012091579765537788487
109-111  5395998998421163951326432382, 5590216042545673597945128676, 5767663982737209668189012119
112-114  5926397125535620343067804648, 6064641787438084936626521009, 6180828380379607159612670884
115-117  6273620251935997818198781561, 6341938560102191769817881454, 6384982553863715073034171715
118-120  6402244741956597635788391088, 6393520559862576069171717964, 6358912285219683097341718957
121-123  6298827100010870263355869047, 6213969349352648015546906553, 6105327196577478936317031218
124-126  5974154017750228434468135279, 5821945011220513902332003468, 5650409615113010675975016843
127-129  5461440424225468206108977666, 5257079374737229191550219002, 5039482018361785390736108572
130-132  4810880735873507875260316258, 4573547742998231900964407490, 4329758720035712078402140450
133-135  4081757851711519307098758973, 3831724997808844439659981148, 3581745630971442328922711694
136-138  3333784079067788427748823655, 3089660499447890192744675778, 2851031895295529311959820045
139-141  2619377364161990568620315337, 2395987649631898222338277895, 2181958952676602583315645989
142-144  1978190852967546843248133735, 1785388095172100365671578764, 1604065913380581919688278805
145-147  1434558500065260378774104319, 1277030175438721375914893881, 1131488779224422877097071411
148-150  997800789506857965741302539, 875707671771251610291564542, 764842974237824278481935078
151-153  664749711507952986309269540, 574897615400884635560753035, 494699877495992028013952542
154-156  423529060004533803752769175, 360731907866616121722954105, 305642853155687230369339740
157-159  257596060887697075309028671, 215935921297418463564107719, 180025945959367219854637017
160-162  149256072490294589105271788, 123048423998074595895836123, 100861604280777636986070165
163-165  82193637692746936101547134, 66583683531218476732518723, 53612668971003893162752891
166-168  42902992414992469928315099, 34117451242759067859800231, 26957545061953583252513772
169-171  21161298516727236905978160, 16500737339845521364898102, 12779138507592302319389402
172-174  9828160889076819881929867, 7504947432699967498993832, 5689274374566952254035763
175-177  4280807760911376204218157, 3196513214784277455374713, 2368251703532979276434180
178-180  1740582327629282419982787, 1268783004476474608804092, 917091424842010610123182
181-183  657161801213050376135616, 466727631079459533206640, 328456841497336491998989
184-186  228983108281091903938144, 158095677985546558337768, 108069478812410387611475
187-189  73117504489830505865182, 48948218688125044661665, 32411897375894423940825
190-192  21221262166744194168646, 13733339843772583427396, 8781114317413084768231
193-195  5545141119102639319895, 3456814845868248194986, 2126378261433311535107
196-198  1290014765639002748537, 771462987760952520101, 454532502657373176074
199-202  263689610408183074572, 150533284185432511600, 84508391726489354968, 46622216855302147202
203-206  25257469065524728052, 13426006069586668991, 6996751118571775720, 3571453482037960210
207-210  1783899308016533031, 871001124751546475, 415242346763067028, 193059924775833898
211-214  87421963562251119, 38500801655892585, 16465299651853673, 6826383087992241
215-219  2738650566859877, 1061050547374972, 396125036917844, 142158067370168, 48909017307178
220-225  16083922637914, 5038949149384, 1498370983952, 421126647056, 111342247245, 27542780615
226-236  6334971362, 1344958146, 261321387, 45988506, 7239232, 1002919, 119898, 11969, 978, 55, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{36}\Phi_{2}(x)^{18}\Phi_{3}(x)^{12}\Phi_{4}(x)^{7}\\&\times \Phi_{5}(x)^{5}\Phi_{6}(x)^{6}\Phi_{7}(x)^{3}\Phi_{8}(x)^{3}\\&\times \Phi_{9}(x)^{4}\Phi_{10}(x)\Phi_{11}(x)\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\Phi_{16}(x)\\&\times \Phi_{17}(x)\Phi_{18}(x)^{2}\end{aligned}$$


### C19 — g=1, k=19

Order 280; period 232792560; source v32/UNICYCLIC_MODELS.json, record 18.

$$B=2^{n+364},\quad a(n)=0\ (n<22).$$

$$a(n)=\left\lfloor\frac{B^{n-22}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 22).$$

$$R(x)=\sum_{j=0}^{258} c_jx^j.$$

```text
  0-9    40, 775, 10073, 100918, 838542, 5998179, 37892905, 215165249, 1112902749, 5297893713
 10-15   23406376667, 96633910073, 374967169930, 1374230400937, 4777199880339, 15810545113888
 16-20   49980704208904, 151358079754211, 440241404490299, 1232767755539628, 3330463340328503
 21-24   8697746890771413, 21996912601956143, 53961111962761740, 128593826280396179
 25-28   298116475404121939, 673195130761818511, 1482545398076753378, 3187676875862793778
 29-32   6698764346494537166, 13771925947049984776, 27725083097473902496, 54702014614232731117
 33-36   105861403683936183063, 201097517445412072549, 375251374258302618539, 688301241641295771705
 37-39   1241804801891598483911, 2205003820758432904770, 3855629014513826302774
 40-42   6642729796115084066809, 11282017501257668373885, 18898519626268879537901
 43-45   31237120991310712722006, 50969199478725349383065, 82133492487480256009377
 46-48   130762054156005489900342, 205758226835010674884074, 320113526024078027034703
 49-51   492574802509474727797173, 749902544687232891806790, 1129896189016910275903861
 52-54   1685403158566072647989128, 2489575195541154857514594, 3642688272288738181886821
 55-57   5280900486457259580330826, 7587384966698088763097004, 10806340515099367488417836
 58-60   15260449475494637716259790, 21372417464419070507088215, 29691289745078308687492973
 61-63   40924290043591026851551459, 55974964661206316295895149, 75988432321569188424016673
 64-66   102404532242194141548495999, 137019622963114371779168267, 182057705842418668580120873
 67-69   240251423260431510186641418, 314933306297285602687563671, 410137414591586477182534232
 70-72   530711218095292398935770402, 682437214020308899441959379, 872163352057360331154818172
 73-75   1107940859138376468597476743, 1399167516790848509459969510, 1756733858002503390783501430
 76-78   2193169128563569404868710701, 2722783215880709385857865593, 3361800105760364440172555426
 79-81   4128477807653284692752736313, 5043209117493133456820776694, 6128597093275124133643295623
 82-84   7409498732423929907973788185, 8913030093129097245953211373, 10668526025181945708516363877
 85-86   12707447798788317738372154438, 15063232268655132794982454123
 87-88   17771076807109642063557337206, 20867655099835487990662899201
 89-90   24390760029271335762191914559, 28378871273347224375246163697
 91-92   32870646910733844576258961930, 37904340227225858668538408133
 93-94   43517145029256311084040610751, 49744475046689234972935871461
 95-96   56619185394054841311936524680, 64170746493497743939566000683
 97-98   72424383271609352253016024181, 81400194747048354442334959228
 99-100  91112271243065159511912669231, 101567828303675297558454518767
101-102  112766377880477212566562665508, 124698958409654725397850611035
103-104  137347445943965068317021266952, 150683968481922472207329908282
105-106  164670444999458767078311699244, 179258269408449136438996446359
107-108  194388157731170452613558635265, 209990174200466444575271777076
109-110  225983948804544415460320920609, 242279095047596741287933174692
111-112  258775832469200511881736077147, 275365813853385004614173499906
113-114  291933152177101234804165218567, 308355637327324279684375714156
115-116  324506127597137170476884147682, 340254096101723339362246087147
117-118  355467307685094422168029536281, 370013597764390461691285479657
119-120  383762721019204327427033535859, 396588235003724316621362060221
121-122  408369381746512891472412000763, 418992929290984800328851969284
123-124  428354934977651633904615427095, 436362393106804308838327328282
125-126  442934731446909333077518709117, 448005123837921400823492883381
127-128  451521589817656978952352197702, 453447856682007173304488479434
129-130  453763964558403592389937286081, 452466600786216573113236231639
131-132  449569155999109898466275420010, 445101500621307253359650845219
133-134  439109486843500477972447842153, 431654187354768474775165067419
135-136  422810887999180052492101608490, 412667856935184513349878567780
137-138  401324917653996391473189542722, 388891857232441539278679754215
139-140  375486704353593830825525629969, 361233913850512377814772138187
141-142  346262495770106141320764567473, 330704127202280614673943463170
143-144  314691284391576941683241419613, 298355430991583981955720428096
145-146  281825295810804135596554812484, 265225270130714199400448572387
147-148  248673950770806763647349918138, 232282850665167849129270379517
149-150  216155293944791476561934666136, 200385507538736247084433869167
151-152  185057916264815242617968166223, 170246643421282256810698217443
153-154  156015214149916151721697494724, 142416454439446898256147679509
155-156  129492574680921959396259143191, 117275423258389362636305390969
157-158  105786892822910286674995833601, 95039459696987962042666795222
159-160  85036835309366029310248667406, 75774707664701004302210391717
161-162  67241550586741757796846492644, 59419478797354946751500112864
163-164  52285127751720645878186523203, 45810538474674465276275581761
165-166  39964029357759567451715766018, 34711038898531148684289598881
167-168  30014925607917966046190317462, 25837713693414414955663719905
169-170  22140775564319123725601382946, 18885444624728187626004145145
171-172  16033554152944137635536458791, 13547900254193808063497921873
173-175  11392628869354243204938836805, 9533548589133154498646993999, 7938372535398174185811323053
176-178  6576893814552808148967803896, 5421100017690713498415003369, 4445232943640453060830651748
179-181  3625800166876280450946061692, 2941545282193545886962901046, 2373383656769155605325590543
182-184  1904310336156691043223432381, 1519286414520269257792034911, 1205109722459056475867811789
185-187  950275139206273692589948366, 744829229464763477466059138, 580223266035547444250876620
188-190  449168052127469189242786175, 345493322820726826763312293, 264013900947373623876223442
191-193  200404222255283982384294486, 151082338080482758419428399, 113104057350875185160829731
194-196  84067506925375659472695571, 62028070626409484647515215, 45423411126502947430447872
197-199  33008081520867073063566447, 23797089979721770935575065, 17017685387666520824846288
200-202  12068577843856050790078125, 8485788609832668348055439, 5914332936344881273538176
203-205  4084969891134200905695716, 2795300072378083682570418, 1894549788483880642456685
206-208  1271444484355418093313054, 844641204196269200327697, 555256736422883625472287
209-211  361092511265104380031970, 232217668242255100733948, 147626883702038662990654
212-214  92738922210333368391553, 57545207738690615637350, 35255059825384678697460
215-217  21315887813104073405728, 12713018632633453027136, 7475480987472414133986
218-220  4331557866417486009035, 2471834389994957834797, 1388372433635962967149
221-224  767059749660348256038, 416578703674973216529, 222228111603059157456, 116360104851188421796
225-228  59752955237986984526, 30066834167909872503, 14811036830744813295, 7135429132297585806
229-232  3358359367917993206, 1542435846591278259, 690433039732620313, 300807872071958456
233-236  127374040793091671, 52337681965037913, 20832823825022277, 8018137071344199
237-241  2977878393505567, 1064829639292527, 365702577245257, 120302716345236, 37793788641979
242-247  11300937631164, 3204333823397, 857963931734, 215896804665, 50782982938, 11096228656
248-258  2235988445, 411974692, 68697764, 10236385, 1342252, 151503, 14393, 1091, 69, 0, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{38}\Phi_{2}(x)^{18}\Phi_{3}(x)^{11}\Phi_{4}(x)^{7}\\&\times \Phi_{5}(x)^{5}\Phi_{6}(x)^{5}\Phi_{7}(x)^{3}\Phi_{8}(x)^{3}\\&\times \Phi_{9}(x)^{3}\Phi_{10}(x)\Phi_{11}(x)\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\Phi_{16}(x)\\&\times \Phi_{17}(x)\Phi_{18}(x)\Phi_{19}(x)^{2}\end{aligned}$$


### C20 — g=1, k=20

Order 312; period 232792560; source v32/UNICYCLIC_MODELS.json, record 19.

$$B=2^{n+404},\quad a(n)=0\ (n<23).$$

$$a(n)=\left\lfloor\frac{B^{n-23}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 23).$$

$$R(x)=\sum_{j=0}^{288} c_jx^j.$$

```text
  0-9    44, 861, 11564, 120460, 1040590, 7753041, 51049086, 302389369, 1632608565, 8117514318
 10-15   37477435190, 161765173682, 656519167279, 2517523150042, 9159861811026, 31738689716067
 16-20   105070183197195, 333280927788232, 1015549574204259, 2979615878724389, 8435331789199147
 21-24   23086581349938186, 61191998525240681, 157328414399704916, 392954681918858687
 25-28   954766710868111850, 2259565741825796895, 5214830334032648357, 11749582935908768840
 29-32   25871386268347431879, 55725129023656500355, 117519392246498561868, 242864495768196947851
 33-35   492222599266276968840, 979104102905897632535, 1912820162294880605710
 36-38   3672724059680125152345, 6934998286564164410701, 12885715887329908640817
 39-41   23573354651386950160215, 42483335621014036384956, 75460909208217768439000
 42-44   132172886844570315220012, 228391508580723622376298, 389516049004338160858912
 45-47   655933871974492440453995, 1091080954418917822746347, 1793415769106746553821624
 48-50   2913999020737904237333338, 4682010923971239926312375, 7441380831067309257452043
 51-53   11702802538911693662142452, 18216822574556274855239969, 28075486861575342637001112
 54-56   42852290319506218120692743, 64792978248585836409969366, 97073187263354044358047625
 57-59   144143079128951047702196237, 212184103946675144176825176, 309708914287265992040651104
 60-62   448342311036766283139645469, 643828986646606755085800570, 917322764772444439830005609
 63-65   1297022000382771353787010475, 1820226734550021073540176734, 2535904964768144505701998362
 66-68   3507867792633367385814478950, 4818665959029706179798200112, 6574332990230106387707440712
 69-71   8910112370574859144362312515, 11997317233176550232290643629, 16051480312620177404724561181
 72-73   21341958517104916772032629768, 28203159535460634730528165773
 74-75   37047556394052488236496588516, 48380648752164280012283291537
 76-77   62818015868464798654562381221, 81104584483269130149731607300
 78-79   104136204284383470204241099930, 132983583198546814953523226274
 80-81   168918583670519341577259416432, 213442818770108311537355565593
 82-83   268318413098692815913330768526, 335600708095321603190871838737
 84-85   417672594924674087612288452075, 517280051593524039393590160929
 86-87   637568345737768916070981235347, 782118242657107401034052206988
 88-89   954981432237254854536958210734, 1160714261562450186621643946388
 90-91   1404408736018384989145793588720, 1691719634771946124768681374942
 92-93   2028886481389625524110989181725, 2422749022071349120941548080277
 94-95   2880754797801205616342032354625, 3410957357992541504252296150192
 96-97   4022003657164201944107235551812, 4723109207758263296091789804732
 98-99   5524019635811618268215927826029, 6434957405508113210294957078272
100-101  7466552646392862973133348262228, 8629757234793225868518835245227
102-103  9935741548966488706241087567797, 11395773634363871813391348906352
104-105  13021080878180820976775635114833, 14822694696327525325977779787231
106-107  16811279174584616995313718337620, 18996945070734719191167670945817
108-109  21389051065929192082792839716902, 23995994639996468351563779991125
110-111  26824995424055756906819143044581, 29881874340897702294385587060351
112-113  33170832264694110973252385782593, 36694232302014100597346570098780
114-115  40452390101344249034571023384397, 44443376824496962943405285518185
116-117  48662839547749377873633188088064, 53103843892242858082287034056417
118-119  57756743603152547907192751875239, 62609081599029409761658554922657
120-121  67645526693062268529968488884876, 72847849746591174754465872572796
122-123  78194942455255233480227683619917, 83662881296495639539450026047994
124-125  89225038394144858164150269883178, 94852240195391384497967472081042
126-127  100512973924621812418615984322561, 106173640797527144791311221022268
128-129  111798853969859409265654064764623, 117351778182673224650139894871802
130-131  122794507075333027759223648220130, 128088473195090979132554319707442
132-133  133194884863458416408423542555697, 138075183289709512203186150337295
134-135  142691512673645533764517316804468, 147007195533651592798927546344479
136-137  150987205149268252103527328488965, 154598626833319250729716716209502
138-139  157811099756050527064225870902061, 160597231237004475164523380667270
140-141  162932975798752608155703882418073, 164797971834394087045763244369890
142-143  166175829467162115461228220033676, 167054364060121187109687252411066
144-145  167425770846974290966843746006417, 167286737277826940974420637346664
146-147  166638490879586408382365266444131, 165486781690343196715796973689727
148-149  163841799609834009704168381120546, 161718028282518452888127733487789
150-151  159134038364729780890342140259225, 156112224192766786321347568642142
152-153  152678488936652720370793314196334, 148861884269407721037983373542942
154-155  144694211382370672501950146244746, 140209590815806100434000981003773
156-157  135444009037728484617163641053113, 130434849984456098589954248646829
158-159  125220419870761977119851286861064, 119839473487557798459490790280232
160-161  114330749937603085220189308420428, 108732525326124304692499476766749
162-163  103082189338889846615222869252123, 97415851924218811392518533780486
164-165  91767985469479683326360556318197, 86171106950923989751752766361081
166-167  80655503563648189046815023356006, 75249004332167583738623083438484
168-169  69976799187426166915847950679957, 64861305998080490459623013133995
170-171  59922085086009477470990712693357, 55175799859469718122848737717726
172-173  50636221380679112629219019327604, 46314273963328292004196256087102
174-175  42218118281647478453699918657492, 38353267974717023272585719797039
176-177  34722735352612570142013486064993, 31327201556112531234990174860585
178-179  28165206387090222635748925774237, 25233353007312539489081652180618
180-181  22526522791367720938936560436663, 20038095804724070961314127388090
182-183  17760172648475586122394992174508, 15683793754776755600264238901176
184-185  13799152617022261278113002503886, 12095799881802371443402349248123
186-187  10562835700922089719536504683363, 9189088227157434431397225393126
188-189  7963276623628870268921934750229, 6874157431571318665775865246328
190-191  5910653594164273305721151788251, 5061965855864793651870240288807
192-193  4317666639998464318197907718903, 3667776846636821674916033542363
194-195  3102826304224884883307113556842, 2613898849935846036526031525904
196-197  2192663204833453978918365510463, 1831390951576740830862478894289
198-199  1522963016825493510449938454433, 1260866110975975718230288928793
200-201  1039180588488475530758782446892, 852561167594734953539852169515
202-203  696211893727019256363660339122, 565856651923217528546995093338
204-205  457706435074142667327725766925, 368424462377276028601812538546
206-207  295090120637311653409232953582, 235162574594597333581244713885
208-209  186444765262617064941057337724, 147048390762724261651776440044
210-211  115360345226130851246350795080, 90010980271524257343730839944
212-213  69844452069424804743802187153, 53891326237377045941909895963
214-215  41343533440897498905903811253, 31531700829338441726075743691
216-217  23904828158227299369308512446, 18012232170647945231844834366
218-220  13487647811703502139852577992, 10035349230383633072014545087, 7418136257068952792157040981
221-223  5447022039012821720330241475, 3972453656462763400121621632, 2876898734958638003947406895
224-226  2068636273930123263395184078, 1476598165264309696473029888, 1046118310869852924304322148
227-229  735458104980229288605698184, 512989676128965393393863107, 354931148109788466579415714
230-232  243540848827530953844747663, 165689540792556039708412983, 111741127468067703636018598
233-235  74682745402143752942543408, 49454590210370354612386657, 32438207853825326808837993
236-238  21069318361809046932217579, 13547567934776000639797003, 8620992123581809505144689
239-241  5427498289766235892178368, 3379429492634273466024498, 2080347285992499993215037
242-244  1265659485326155567154623, 760708273023131945993759, 451504938226722352529177
245-247  264523027915743715377163, 152906009344597412790614, 87164252914284036061445
248-250  48976324369474668146084, 27110439511530661161512, 14775588103836128700424
251-253  7924130317314078581198, 4179094240984113783245, 2165930857388871159666
254-256  1102373148360633341597, 550559201431620191268, 269599298891876203857
257-260  129329333323137355130, 60720746605237339946, 27874605043061763529, 12498284521379453311
261-264  5467216168643865753, 2330356327969632897, 966590905241827093, 389587221592748814
265-268  152346916412452456, 57702790228102653, 21129837442815425, 7465523420877038
269-273  2539420340452544, 829602574751672, 259602924978234, 77583870881641, 22071391144805
274-279  5955108351463, 1517599347748, 363580150642, 81451257005, 16958092528, 3257738064
280-288  572586482, 91137506, 12975753, 1625787, 175937, 15877, 1177, 61, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{40}\Phi_{2}(x)^{20}\Phi_{3}(x)^{11}\Phi_{4}(x)^{10}\\&\times \Phi_{5}(x)^{8}\Phi_{6}(x)^{5}\Phi_{7}(x)^{3}\Phi_{8}(x)^{3}\\&\times \Phi_{9}(x)^{3}\Phi_{10}(x)^{4}\Phi_{11}(x)\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\Phi_{16}(x)\\&\times \Phi_{17}(x)\Phi_{18}(x)\Phi_{19}(x)\Phi_{20}(x)^{2}\end{aligned}$$


### C21 — g=1, k=21

Order 344; period 232792560; source v32/UNICYCLIC_MODELS.json, record 20.

$$B=2^{n+446},\quad a(n)=0\ (n<24).$$

$$a(n)=\left\lfloor\frac{B^{n-24}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 24).$$

$$R(x)=\sum_{j=0}^{320} c_jx^j.$$

```text
  0-9    48, 1088, 16221, 185220, 1747863, 14175680, 101395959, 651228959, 3806621808, 20463526238
 10-15   102025128088, 475028294076, 2077459205447, 8576046481894, 33560656266524, 124960782703376
 16-20   444156780466862, 1511397743077700, 4936614120771495, 15513273266667937, 47002589126604853
 21-24   137569459075290537, 389646248535200343, 1069722088064667942, 2850835382508158724
 25-28   7385399310136846613, 18622286191228139250, 45757974866707017960, 109687714626963521178
 29-31   256777849339779859543, 587608123577242416301, 1315663570959720319118
 32-34   2884702427905487580106, 6198786974224556008927, 13064483030085592648519
 35-37   27025227050926014379377, 54907636368795856702255, 109638038281976812471893
 38-40   215287602383924464566389, 415964764620782640931212, 791246174018961791563768
 41-43   1482552946825661525189341, 2737582449722058810283136, 4984104790074557594516038
 44-46   8950863916380520650392013, 15863038211775481045234636, 27754198084139200615875607
 47-49   47958010152684161530947351, 81873906135552663086476336, 138145383520266642814980964
 50-52   230452639057634681059055788, 380209579499972436778947664, 620577649964045816857384747
 53-55   1002376589207412546326590216, 1602699375346079209983241260, 2537343032176479795005396486
 56-58   3978570542813756505963460908, 6180248538242741060524166580, 9513092710765812665736019678
 59-60   14513635930156860395639737718, 21951656974651913843723904770
 61-62   32922221301855114111562795147, 48970246543677571167700733880
 63-64   72257677729201882134786240208, 105786009311027201753472911062
 65-66   153690095674107761821014336921, 221623023910435936370356691265
 67-68   317256356805111586589489285501, 450925360962746180391822992855
 69-70   636454977555813815481461646976, 892209320936044454612962605956
 71-72   1242415433876662484423486829277, 1718820892198316732036427990076
 73-74   2362754607277424991361323392261, 3227670752268170991358770965514
 75-76   4382267016704951029396285535822, 5914280196014732237565888543214
 77-78   7935074202322231074355510843066, 10585147621759694633592611907413
 79-80   14040699542130533173309570646273, 18521403049527127966348397812329
 81-82   24299544973149788591443760295526, 31710697488365475047732732757841
 83-84   41166091332269412711961693027661, 53166860834707270524436597644124
 85-86   68320326853006132384733747916664, 87358474112117848452504723016217
 87-88   111158763468121793512816577038855, 140767396318680528410285931491651
 89-90   177425116911815035988557136009251, 222595597872010293020052964474546
 91-92   277996404215994927427978894190348, 345632470989714402216358560523083
 93-94   427831959165772853905440009379781, 527284273611006636707112514498809
 95-96   647079936099687699936090104089740, 790751906204886559701326693231735
 97-98   962317834546156525158783970250703, 1166322617835971298798751666188691
 99-100  1407880505433839256684949755307175, 1692715885131419219168065558461051
101-102  2027201754556158712141340083754258, 2418394767230790275321101219081111
103-104  2874065632691111011525072943696722, 3402723552209342133385852121623807
105-106  4013633289916056653087487282120428, 4716823417940303723755956395985753
107-108  5523084238118750295065299438503113, 6443953876295430079283081324995004
109-110  7491691072444546019855223070013006, 8679233254609253487492832731654574
111-112  10020138590215175642984063629134648, 11528510857226067864183904908930476
113-114  13218906171519289813079521901272115, 15106220846399722261851889610822198
115-116  17205559944807111053739754335763431, 19532086412690740014596667075279407
117-118  22100851050051814643045860305758913, 24926603979699690863841735800183663
119-120  28023588706819217865709821019040969, 31405320317594005882975972869862406
121-122  35084349833646650439824200140342352, 39072017211019185024831404979101851
123-124  43378195936879162219476236688816138, 48011032622346818607242084079930688
125-126  52976685403499616222496296932653805, 58279065332178511344438342811712602
127-128  63919585251235903508895091850655981, 69896920893306290823147762525311500
129-130  76206789106830320907316093498822879, 82841748187880301394192845248892826
131-132  89791025272817937009229296546198936, 97040375618341399993951393345040694
133-134  104571978357617579107637596708674046, 112364372971971277617303251314042798
135-136  120392440257707372668298510984930428, 128627431000577217502769523365604379
137-138  137037044902553019503125587211733463, 145585561546205387732154578371916968
139-140  154234024343135749980078310808592431, 162940477509250545964931341485177457
141-142  171660255158178756793066135288451558, 180346320623835871346589819393589147
143-144  188949653134626444925830646630983020, 197419677986770677560071488091677033
145-146  205704735425041864309259013790346811, 213752582558135826124960304757144898
147-148  221510921834717542476667998764615669, 228927948905500329302103468826212239
149-150  235952912115363997420820980651419046, 242536675424074783316511839681870043
151-152  248632276258403885863198589974211030, 254195469662897201869572334326997600
153-154  259185250148184876302536570648382095, 263564342837643578475440531746157411
155-156  267299655884531345607542781115993725, 270362686667430914041362790982682197
157-158  272729874962979599407391284276033145, 274382897128610152754684688394471787
159-160  275308896287996967393764931295746642, 275500644578538250951923733643830777
161-162  274956634671247454104588448548890149, 273681098984466783113879468094109559
163-164  271683956257908463791422195314601182, 268980686405858889474483590456599881
165-166  265592135800943612723296622996578874, 261544256326149583406230395949655735
167-168  256867782647520077169387590064819871, 251597853179587601460724850844259661
169-170  245773581119115103472509898319573785, 239437582691933128768899189361313335
171-172  232635470377813307324268427450504711, 225415319338332100664054937526845384
173-174  217827115565411299255719511961231236, 209922194390583504962613632301974720
175-176  201752677947990220901128736109361460, 193370919972598877664944754057666120
177-178  184828965947786837919498055973649299, 176178036105381841614176478278934040
179-180  167468038141603578872418975546478915, 158747115761823067774213189490103246
181-182  150061238325391181352422565252881431, 141453835950207597918816643510902593
183-184  132965483477316960780857645079790158, 124633635711034555238104063477239360
185-186  116492415362037037459452176664924627, 108572454150784175059329058153470232
187-188  100900786596499388411269173792422568, 93500795140869497063832006341533656
189-190  86392204451590843048116420563158300, 79591122032372698337854733336322885
191-192  73110121643789460550175875727480163, 66958365521390141678876169841324955
193-194  61141760968773702280065665123497129, 55663146606105318550329860752568980
195-196  50522503368208731273700436240408504, 45717185267770738913121356333989808
197-198  41242164962840759075808866253023187, 37090289286151914301398826246330220
199-200  33252540097553381734668430144652020, 29718296099375870042157167681301472
201-202  26475591596196538574738588045623868, 23511368572935662188148037756196677
203-204  20811718895942837536452931058420411, 18362113898226830061254032274356989
205-206  16147619080152094113525437293721476, 14153092129341228933371851266170469
207-208  12363362927675335455212949509857333, 10763394659773988283743180221475576
209-210  9338425558025031337260449707959357, 8074091207346330638213235930080165
211-212  6956527683039512629633722676270990, 5972456103410153190356245956971072
213-214  5109249442747482124819310801693400, 4354982668576522712551781208996246
215-216  3698467439844410298982011714471325, 3129272731014525658015756102358854
217-218  2637732833014037053129041151301172, 2214944228515868154231021389035868
219-220  1852752849681311556388086878672737, 1543733205268958397687356566913488
221-222  1281160815271065881077096872035429, 1058979319476533280042973638655666
223-224  871763536111523523360367220024646, 714679642405298790994199159429530
225-226  583443534792910001698113535327897, 474278306424072406344845114635935
227-228  383871657258705843593440809869420, 309333930437616790302615988954118
229-230  248157350516950041841243694085775, 198176926780139224709679450269780
231-232  157533379962593296307350290229549, 124638354667097684780972409497202
233-234  98142093416128009185017354428415, 76903672199692731893530795719486
235-236  59963831708877036438648565664933, 46520383073278407660955957689526
237-238  35906121473206236453977100013051, 27569144902854760819990096678751
239-240  21055447894113228721791516679524, 15993640340253961020369964230743
241-242  12081628786353121485188205558572, 9075090751639009533653182020936
243-244  6777570893319765273815991261288, 5032030216236658286559295992984
245-246  3713685232651001287603884761584, 2723982202635713785059164295595
247-248  1985561636363937982163624655413, 1438079497638297398039348493614
249-250  1034763482759968757942906983452, 739594916146099179945125495298
251-252  525018842951316384473126812694, 370096526103072338506214260891
253-254  259025558289597228819193177744, 179963029219428440204780920216
255-256  124096550160125005543854049336, 84916382642358448003728716993
257-258  57649435235679331673039129666, 38822500196864273939538054333
259-260  25927841844902696011053465714, 17169178121332737879870101568
261-263  11270283871038185496400998885, 7331962677255296667674307887, 4726059357101513715438892907
264-266  3017592214749565804575828875, 1908044336588945945839197872, 1194433213699403887298040216
267-269  740038523892865535675087724, 453663295251056901473470013, 275081597071131891102122880
270-272  164927571739183846856643293, 97741095969176009867801664, 57234041634137153510307918
273-275  33102298900900561651586585, 18902243951741566149472792, 10652120882154350545114135
276-278  5921515385648434576547100, 3245637762930100008971787, 1753166167639988072771090
279-281  932772375598235251483066, 488561161288980876648336, 251767927480695674596602
282-284  127571296103125118218911, 63517546536832130742835, 31054363252714820377178
285-287  14897766558135329672236, 7007299224876646776289, 3228870249679431664714
288-290  1456252213509269438976, 642241418183177830368, 276692192423648767797
291-294  116322134325593522039, 47663987791987162644, 19012483686364145023, 7372656028804104754
295-298  2775336468321263596, 1012587011631954215, 357466390112606867, 121876810197539820
299-303  40051105590465113, 12657803947580566, 3837979557265095, 1113502640544838, 308209343050166
304-309  81123409363696, 20230485331414, 4760403651667, 1052061598930, 217218379655, 41644338183
310-320  7360848671, 1189460355, 173955808, 22738216, 2616016, 259313, 21638, 1446, 79, 1, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{42}\Phi_{2}(x)^{20}\Phi_{3}(x)^{14}\Phi_{4}(x)^{9}\\&\times \Phi_{5}(x)^{7}\Phi_{6}(x)^{5}\Phi_{7}(x)^{6}\Phi_{8}(x)^{3}\\&\times \Phi_{9}(x)^{3}\Phi_{10}(x)^{3}\Phi_{11}(x)\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\Phi_{16}(x)\\&\times \Phi_{17}(x)\Phi_{18}(x)\Phi_{19}(x)\Phi_{20}(x)\\&\times \Phi_{21}(x)^{2}\end{aligned}$$


### C22 — g=1, k=22

Order 378; period 232792560; source v32/UNICYCLIC_MODELS.json, record 21.

$$B=2^{n+488},\quad a(n)=0\ (n<25).$$

$$a(n)=\left\lfloor\frac{B^{n-25}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 25).$$

$$R(x)=\sum_{j=0}^{352} c_jx^j.$$

```text
  0-9    52, 1250, 19484, 233440, 2307854, 19604217, 146788313, 986554195, 6032360352, 33912182092
 10-15   176760047684, 860165574048, 3930705601937, 16951026776200, 69280282965801, 269355623699595
 16-19   999463435136300, 3549724980007243, 12098699868951875, 39665745472203120
 20-23   125356291043980760, 382620518934874981, 1129921528165571443, 3233626392502081771
 24-27   8981345940471633977, 24243914037221965854, 63683957083898315860, 162982415120603899854
 28-30   406834083782954401247, 991541068140074406796, 2361800426167171693982
 31-33   5503146634965874549533, 12554137572003944886579, 28062174697482389773154
 34-36   61509915085598481138451, 132303270439530552454410, 279442810547594525325048
 37-39   579951545441691053665671, 1183400556058102947736643, 2375551289128634779303754
 40-42   4693839989428158041557041, 9133773147599585503733866, 17512415604304392465050565
 43-45   33099489536640012194148317, 61698100972269752235861849, 113470861438799756231414902
 46-48   205985783111710970337656650, 369233220585444208688451192, 653789096288550749518844128
 49-51   1143940995718397860683022581, 1978552564272589647615153976, 3383858804794107800117952968
 52-54   5724456135805264216635569154, 9581745443817787883018706075, 15873369328005113860885807748
 55-56   26033247269573223396532231150, 42280306857966329516169384493
 57-58   68015792640385791114909410882, 108405220843825029597715973946
 59-60   171223070942502549881050091569, 268067986568950276591051654960
 61-62   416095892696020796694023558749, 640470879768707112445981849540
 63-64   977802476807058900127195249268, 1480927320755941247173684216032
 65-66   2225508392876593544067599774954, 3319072086807835453978680340254
 67-68   4913289640731907515557165529453, 7220543334377987932490033958131
 69-70   10536108999836163684005757896456, 15267645794526566299760098471215
 71-72   21974124093968739553455086069197, 31416856267458338199044260959767
 73-74   44625937584584901474561066912897, 62986171029059406839505408686669
 75-76   88347456397523760725525741965674, 123165686896288807088976519177950
 77-78   170681431250563135558684330672827, 235145100709238154332026621738547
 79-80   322098920880508242074067189470614, 438727857697199004931259424659307
 81-82   594293690466921429825820879823023, 800668682945308009851592769891789
 83-84   1072987768840357265283545230205699, 1430440825868862604096485475649140
 85-86   1897229437201219338095979540735078, 2503715493997160553560977249666422
 87-88   3287792027715189468199799469291080, 4296509711281752144892617486941319
 89-90   5587995453404413276710307554843979, 7233702332730379678528338756471509
 91-92   9321032663020176025956174266221372, 11956378114090475972664566298894377
 93-94   15268622385667289068846232560300198, 19413152775848738765421647358584354
 95-96   24576426921470745213857280853149828, 30981139821318518158025669435686328
 97-98   38892033783567306767417813801732706, 48622389961027862715967781071791589
 99-100  60541234448373273707340552991680663, 75081284319307188007029913395767235
101-102  92747649298797295988237580478284223, 114127292839772846292058596601351867
103-104  139899242081098750895533318605844470, 170845519421754652129556763931712678
105-106  207862749223545122173584513788317910, 251974371480393631745299109730765330
107-108  304343370264945688861714995393511142, 366285398559422597621265197410564734
109-110  439282152959339360654270628677449844, 524994822058926780642878753467558107
111-112  625277401534167430854838279642900283, 742189637578493612229151735231017820
113-114  878009329058686889008627630314030184, 1035243688277871081769196176450874602
115-116  1216639431377370240116116679181343895, 1425191243072936941772333029136984695
117-118  1664148237557384842265444262192254956, 1937018019007928096720794980226426389
119-120  2247567932231419945109899136042764186, 2599823087580703892073187414690200356
121-122  2998060745367397911061690065268876373, 3446800654508444183986932674297824666
123-124  3950790958913005815789152649561103079, 4514989313857237029523777667911064419
125-126  5144538893866119172860647805681181507, 5844739023795738401880543915091921384
127-128  6621010226040650444709206312330187864, 7478853548989528423259056769256986644
129-130  8423804124660738959564409595468187581, 9461378996224676452155099228381675176
131-132  10597019357920468594100604432556660272, 11836027459456666878179692799113257899
133-134  13183498542803567077163770839264474321, 14644248299503633758011684443779029472
135-136  16222736459140351828952942803172448424, 17922987242066795751847171262459930388
137-138  19748507529350546024804998517798650413, 21702203717429484492008036827069578946
139-140  23786298331376268497227073585581611398, 26002247566075982237435680585148846965
141-142  28350661006191360234166879895582981275, 30831224840775343320100524711309853814
143-144  33442629934209821150920156305795408819, 36182506139460792698533001935052763811
145-146  39047364240415817569642468593947037524, 42032546885664781106062766820842080794
147-148  45132189825302588453183377402861276610, 48339194684479954627789515223635576591
149-150  51645214402365436386402616686583704586, 55040652333355658284703301652147586121
151-152  58514675849839648452133926387956323686, 62055245104265247787341689956257309513
153-154  65649157404961596969937681324323899318, 69282107438023116596683186546623927461
155-156  72938763329990479627343396317528026785, 76602858297003764162848075334366191976
157-158  80257297369911551991864882875721876495, 83884278426201789523103691649788133938
159-160  87465426503530488648120391513566178074, 90981940121162511114027293845893259800
161-162  94414748099936617409921534690774887284, 97744675153471045401037129283709956101
163-164  100952614328077440951572656980441625522, 104019704200767916557414214091962530712
165-166  106927508607902927374721739688855566576, 109658196574973294242348792377549289971
167-168  112194720053635162520734209663504577382, 114520987047596842443159074576597963552
169-170  116622027725677303772857420074042595068, 118484151178865906341063445786402427677
171-172  120095090578193231373842963468260602133, 121444134630479869360984721085034432569
173-174  122522243407507554537264766533900990634, 123322146837970697542476598342430647669
175-176  123838424397058328212178568873227878635, 124067564801329819687960034693814815139
177-178  124008004811718670559323403303205208348, 123660146559563909481632824325520579699
179-180  123026353133686368303072508950267171510, 122110922494606591020864775048841070333
181-182  120920040108840086468578812697578501236, 119461711015629300744265631804891814879
183-184  117745672344472006269611977043066384991, 115783287588675892460961773431749904445
185-186  113587424202630101865205439877956473327, 111172316323801147058607315173889661645
187-188  108553414620543514583434142985776167454, 105747225430305692511267798282792733735
189-190  102771141477149492266735371659551488666, 99643266540968061492180743904424086744
191-192  96382236492539920043744215127394805260, 93007039108621449721056607579143721283
193-194  89536835040545288579603037368299554373, 85990782229964697009186216650905601147
195-196  82387865948936674102201162056941863231, 78746736491633461172611069980456006356
197-198  75085556365380507357783474002306489916, 71421858623709342093263318001029488973
199-200  67772417758349531114539434421836240595, 64153134325505342444185695938908523758
201-202  60578934229467915451704708887789710714, 57063683328738991505119481532966247557
203-204  53620117771446236349198367091352420104, 50259790212783514717082211635434458442
205-206  46993031822093298435006481677099683492, 43828929755223647669789154861456668347
207-208  40775319552681829320382343949151775485, 37838791729092013059471810033739163368
209-210  35024711647197296324655228808475581659, 32337251622176299888263515496837934096
211-212  29779434080803373876600190882905309333, 27353184505782105909822959017555346293
213-214  25059392828633300913567122335366469525, 22897981894454160381280881473298513460
215-216  20867981607783323132601487257328982224, 18967607379321518897387505788379773168
217-218  17194341526561303843157579432122538154, 15545016335306778031943933356710685238
219-220  14015897561165524753008071877774761755, 12602767237709513970607655892904719719
221-222  11301004758332009878196064997747238565, 10105665309012363955484153266405114583
223-224  9011554846384182991333169640711910834, 8013300936898828637744437741956122852
225-226  7105418895827583709781316990761694520, 6282372786872828242604279563155960108
227-228  5538630962003113315268983533075134381, 4868715934786029655992830267460996468
229-230  4267248487243087744854311461527295550, 3728986008665226717287495215196139013
231-232  3248855153782133562502359472275424599, 2821978986351948186385055358855076236
233-234  2443698842103247783073260469266062141, 2109591201771223184595400829853794563
235-236  1815479910736769887567928949829006274, 1557444116747252919351192080916993290
237-238  1331822321823268793680695200837054098, 1135212959364070820077097542933168261
239-240  964471913425353304977690004659769701, 816707395036691914285469465980508044
241-242  689272581209833402110077522086096358, 579756406967977536912678092077349278
243-244  485972880323239577769588127515057394, 405949265659803069234659190897446025
245-246  337913453428090467054407820972108485, 280280804354106850165496420632447576
247-248  231640725384535609888771201856319674, 190743203109201056453706782540686888
249-250  156485489126491246989497175659710048, 127899101348152049155202350374128767
251-252  104137276084375890914817927232453575, 84462978318357963770357741682704129
253-254  68237552187425457658413082483426177, 54910070562138251249637634380182530
255-256  44007421899354732540787049828084963, 35125154309208028098916209202324036
257-258  27919081022177664616117187755875267, 22097638117097505405232964960170704
259-260  17414974372869793709489713240339812, 13664744296890900895247876512981971
261-262  10674568594051102744854239625009278, 8301121383790981946564429217359362
263-264  6425800148876956136439746536693482, 4950932502728244087494866442777252
265-266  3796473187409975888709778954209072, 2897145062714042858989790183760416
267-268  2199979028914310017438876969403967, 1662209665756636372207240611432035
269-270  1249485707405162195410691408469774, 934357163719030959290451018543294
271-272  695003816381543591853360111007603, 514172855892334540522135659425899
273-274  378296491564953492380851373010623, 276763387393643722622392281513166
275-276  201320693412655738224721549530649, 145586210541372250027473970947349
277-278  104652815054348045736193813193830, 74769655888071595597322898244846
279-280  53086812511451753942313576340247, 37452059344168623939047973721437
281-282  26250127290807603206816662701880, 18276391354373409610262665620730
283-284  12638256637184699764564246844469, 8678677018532373259296373086491
285-286  5917236710679666736645860519426, 4005070844751664757032666067817
287-288  2690613500793983963653117858367, 1793756107074217792342145906685
289-290  1186491105105640020410759338787, 778519425805290635530077219049
291-292  506628691899414038680367237718, 326913923120608975375332163384
293-294  209124338512888424133047654509, 132587799067396621709166422753
295-296  83296453463202409493063043094, 51840025530811378702398553844
297-298  31952644784055600921385993314, 19499954840391661360073788318
299-301  11779387411081253382041616735, 7041185034124299041998371638, 4163596244114224823426924838
302-304  2434730813571281666667120883, 1407492040659505941518578991, 804081006567100903814628818
305-307  453786250990810053701272035, 252889891096879982147221890, 139111405815357451361730296
308-310  75502041696846334501153032, 40413205166014773345852753, 21323094242693057417417719
311-313  11084654721920641983103380, 5674270012865245657779021, 2858721811464697468202066
314-316  1416616817918544607364347, 690051199507549920765656, 330196610340833141367312
317-319  155104027739277989204814, 71467885996090281212462, 32277083076703223011643
320-322  14276091442621712620935, 6178292464305709961690, 2613714474547645738397
323-326  1079782838018396408791, 435141264016992564701, 170856902227923999995, 65282752838499671751
327-330  24240514804062212653, 8734348199441560939, 3049167202880200076, 1029565380039711195
331-334  335617600179531052, 105409104794812996, 31827141194584431, 9216259991436750
335-339  2552675498542004, 674287832825095, 169312162397778, 40266471400859, 9033080705359
340-346  1902636296841, 374291549785, 68352748480, 11505637108, 1770236284, 246447810, 30663755
347-352  3356214, 316794, 24994, 1599, 70, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{44}\Phi_{2}(x)^{22}\Phi_{3}(x)^{13}\Phi_{4}(x)^{9}\\&\times \Phi_{5}(x)^{7}\Phi_{6}(x)^{5}\Phi_{7}(x)^{5}\Phi_{8}(x)^{3}\\&\times \Phi_{9}(x)^{3}\Phi_{10}(x)^{3}\Phi_{11}(x)^{4}\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\Phi_{16}(x)\\&\times \Phi_{17}(x)\Phi_{18}(x)\Phi_{19}(x)\Phi_{20}(x)\\&\times \Phi_{21}(x)\Phi_{22}(x)^{2}\end{aligned}$$


### C23 — g=1, k=23

Order 404; period 5354228880; source v32/UNICYCLIC_MODELS.json, record 22.

$$B=2^{n+519},\quad a(n)=0\ (n<26).$$

$$a(n)=\left\lfloor\frac{B^{n-26}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 26).$$

$$R(x)=\sum_{j=0}^{378} c_jx^j.$$

```text
  0-9    56, 1418, 23172, 289644, 2986334, 26424860, 205963135, 1439911674, 9152597873, 53455337666
 10-14   289302218477, 1460990519940, 6924848213724, 30959640815796, 131118413030175
 15-19   528001509969362, 2028328395196958, 7454883764315921, 26283127826749064, 89097960229978583
 20-23   291029839898921060, 917757205042863673, 2799033437406924610, 8269608641307241987
 24-27   23703348380104702413, 66006192263733006324, 178800506671619667048, 471717322034826276889
 28-30   1213413655598125724537, 3046514886564649807467, 7472912504431709726292
 31-33   17925341040536299621844, 42083408396232922824099, 96777319482827777077709
 34-36   218166837603376200701183, 482470980564643071159406, 1047415050255722445123306
 37-39   2233642539243260938769538, 4681912276677151662791399, 9651649029406721723522434
 40-42   19578962842597243729767037, 39103643160205629061188183, 76931212472228939108911574
 43-45   149160513997090554955884567, 285147490319500177848090891, 537698715938624039877132749
 46-48   1000559816130789959205096454, 1838038288629275558744457031, 3334561751500484561134524933
 49-51   5976595195327392186293846499, 10586471167376093626390837227, 18538559489957043184010667046
 52-53   32104597289211179404346668377, 54999451006671908704010515299
 54-55   93234662404926224343240777181, 156439820770806749970939759417
 56-57   259887972745179280779717670734, 427570305134610431654815932401
 58-59   696819880515196498427640842065, 1125201208681934314173040454644
 60-61   1800684325971663592078187599992, 2856538232244079384435519928943
 62-63   4492947177166638378001100462232, 7008123481929840452895910650637
 64-65   10842724848888151986884774057465, 16642761318673931827442034359100
 66-67   25347995733721266921519717545919, 38315223738846309325234504649575
 68-69   57488914536095363244382512104051, 85635683390500603780363334402988
 70-71   126664169597968891288813000134498, 186058369245743937222805458469685
 72-73   271460627046466439770977213728160, 393450683272510035599436243461797
 74-75   566579812914962313539469859808798, 810734655492849397086750435714262
 76-77   1152924346543483670421979261041350, 1629607617340717419322963413087459
 78-79   2289704277981214890197585478358905, 3198468644675564035551922888255902
 80-81   4442441764722413592426673866940179, 6135745515893738556840724368932353
 82-83   8428035611759166445381405184546094, 11514493027373365293041990432135551
 84-85   15648305135579085469834952242195454, 21156169612688237298030363074532245
 86-87   28457446528429831283518518653641868, 38087687422736621044178764142498669
 88-89   50727384831599464864245926783098744, 67236911634251171821691388025039539
 90-91   88698756406959234046969221211454710, 116468307943499940045235674422511335
 92-93   152234598033059499310545382997849309, 198092574730384220314798456355635976
 94-95   256628646360727050907690031431759505, 331021406349622561693687477526462771
 96-97   425159616896758758710634139083384577, 543779690982357270809287116944428520
 98-99   692625061842081626254155004395478990, 878629960673637364588977336854818702
100-101  1110130229912503155717884199669799990, 1397103873099700446625573926974849292
102-103  1751444074581446886793940071037319732, 2187267403798560021589910788908610240
104-105  2721259839991106790280745909929402641, 3373063103656884487574083602230004386
106-107  4165703550812840238092746271318647636, 5126065564874188934218993539412364136
108-109  6285410959039847548820651760273834686, 7679945370430773201741000025806006585
110-111  9351431977930114351321373876925970798, 11347852102255435669648223210250375498
112-113  13724111344674295051565103634096200097, 16542788887685761830120147516046067614
114-115  19874926417398591297327699257406475187, 23800851836859707150284095775272039644
116-117  28411031529385477933479318649883167620, 33806943412080066136450310822783196086
118-119  40101961407441433154453763330161365540, 47422240274930543499465467373116282842
120-121  55907588008851279677462505304692269698, 65712311252699727016867491340316789855
122-123  77006017436660961093187261993234592684, 89974355651849300536406987731393506411
124-125  104819676673869243491457422068038325324, 121761591084465824398178526878094621721
126-127  141037403161418595607573047670650951739, 162902397163436532419287547467414168452
128-129  187629951879750856815559759259216221039, 215511458894509680617338686509045266874
130-131  246856019983885907757545688463195086054, 281989899466439224232178713208011225364
132-133  321255708208235974866520666696362590612, 365011297381678793951813948581702722198
134-135  413628342022251372620732201069441357689, 467490596943477847869748302314136688396
136-137  526991810670684034900280215565371384492, 592533286741002860307498590670358623621
138-139  664521085980729570476144395962061805178, 743362868188744513281477102682411103037
140-141  829464376989586610947955449971268583673, 923225577420878674510138020104030988523
142-143  1025036462021709271053353374736469626436, 1135272547711504428935130323417194150813
144-145  1254290092499355297415181892005531654272, 1382421067935332595725525953684145250498
146-147  1519967930090082437907024569611416337778, 1667198238599138318528122453948752295149
148-149  1824339179798225402317940114600250449808, 1991572056064226877802363617767483020191
150-151  2169026809019491520360554023409430072647, 2356776649111009809591245579176464368010
152-153  2554832868100207851856234248944221695520, 2763139914059843083512920456913146517748
154-155  2981570810447835980833070128496738770626, 3209923001603251000376928186084046320416
156-157  3447914706493021905012200019831136752550, 3695181860655004127611773543501244530026
158-159  3951275722981558754636262604254609476476, 4215661219241027727041245160682962755485
160-161  4487716088041925774904121539799015015261, 4766730887334610778806375208730582111287
162-163  5051909910575073525025671123098858195368, 5342373051432406292737553606271254277950
164-165  5637158644521836209896658807475480819106, 5935227297233551732361860015726479842261
166-167  6235466714475032859659230839674291752191, 6536697504246456615091502178024045716519
168-169  6837679937641292532807680243570364581195, 7137121622341144907352528631068424567493
170-171  7433686034202179097242161692885484858961, 7726001837365604333587993203430161780848
172-173  8012672909725758646914386896116043830161, 8292288977813739482201498956028733019854
174-175  8563436753452535387203203725526388893634, 8824711454149017406406747276200058442930
176-177  9074728580328911902121155977890862988863, 9312135815390106514942279839247071794443
178-179  9535624909316903564847514497719299987873, 9743943403400967364657539548571447359083
180-181  9935906052556238211247320528876804704631, 10110405802859336473899143112404854297157
182-183  10266424185317993813819927570202743351714, 10403040992450323878432827875140137651154
184-185  10519443111987886018436675633357548470215, 10614932401794774044224717660640042176389
186-187  10688932501782794636800958864617039850819, 10740994492021121421210678249338578156759
188-189  10770801321175294423979989610451647356754, 10778170945622496027497114743739120925119
190-191  10763058136809528741496218487141171652945, 10725554932358430092373035250677617096392
192-193  10665889724779254388426159818049966729813, 10584425000108879858239462202782572968492
194-195  10481653757045285103460037934409444454078, 10358194654879317261053127431734868847132
196-197  10214785955441739217314891466685141601208, 10052278340099945488157591168371516763907
198-199  9871626697295902400951499999267397689356, 9673880988981507475193226451530437404182
200-201  9460176315378249131992871396784485812553, 9231722306598774569597572530896146918092
202-203  8989791976691103404979616679697425447857, 8735710180514572267207413848494849598664
204-205  8470841816484606865577804385236079087280, 8196579918627429881500773158589078039665
206-207  7914333779603400887673900850509188999885, 7625517242466129072399174934383341357376
208-209  7331537293038422617511806081642091369318, 7033783077054379272437652048093391563525
210-211  6733615456818742140072231915493762337986, 6432357211275361985849740532434078546317
212-213  6131283971282780958548754947590581257769, 5831615968809230491757564102504561291598
214-215  5534510664935102715040031011685852587544, 5241056307246903739436360798014773122712
216-217  4952266452681459069333565970853261801524, 4669075477386087077821724012786469506103
218-219  4392335080942792899434802299027448714493, 4122811778590795736993837938812443106371
220-221  3861185362081723732623620083004985009197, 3608048297703268533061196878010644433635
222-223  3363906018972659865457337724402003391597, 3129178061666487352936402999651134370627
224-225  2904199980324968555774167521284433631531, 2689225978224054844015561469547070325316
226-227  2484432177095476491033760032213194337423, 2289920448611552323631467480446809657895
228-229  2105722726828952699020937187311252064357, 1931805719367940136439768243648713239810
230-231  1768075935031123064944043179971934471586, 1614384946757091656523001767410369351214
232-233  1470534811159450468057375515883577767290, 1336283569305194867237792378455387827288
234-235  1211350757710351452288333658630555782173, 1095422863638715989291275845495587133396
236-237  988158664539269536104328216134658004363, 889194397705080866561009693096080070881
238-239  798148712837705601930425971897646810475, 714627367016482583707858831619005193125
240-241  638227628468229980693477098206987822690, 568542362384764797536210577930292126580
242-243  505163778729021175277557812278410336862, 447686828402988536614052030758295710320
244-245  395712240233111454074513219863244432673, 348849196886072063062277233019234224639
246-247  306717652999309637799242707946233119126, 268950303449989989853052005854883206519
248-249  235194213761393604661166765177525289074, 205112128138461868284416105011609578612
250-251  178383473528963651419663866027631228544, 154705080429644722773446092485447724939
252-253  133791642914602443018740994351015308289, 115375941582030174776418845044340333311
254-255  99208853829258339037133039766143482802, 85059176114889782043778393646489185996
256-257  72713282695871810659337567779051967389, 61974644785090206700183440232224047771
258-259  52663233212098901432511188602790364975, 44614826537278081470847158826240824464
260-261  37680245219015386042710494064973554776, 31724530913967671598559112724625061988
262-263  26626088349290840577794786607513561552, 22275805487049072974648357990217270711
264-265  18576165945284305699977917627176493237, 15440365883774976433722012702519446300
266-267  12791445837255567288958583003441912928, 10561446312142127517883989119335260368
268-269  8690594377335535154076486534274906649, 7126526993636630984139210959742963793
270-271  5823555453522594117308998100744289666, 4741974053207824090982303225701317388
272-273  3847414997959375009542950947746939891, 3110250552048177155724814103345258042
274-275  2505042585964319711114639482999526545, 2010038942480792519558547415343900485
276-277  1606715434518268693848455043407188100, 1279361794498717026214279094863274902
278-279  1014709508591296875763476220717633394, 801599180604350455026683737835502042
280-281  630684869309007674563330189891219033, 494172719447944351947511844347810004
282-283  385591150327588390064775512406929307, 299589866675829745412054305687887394
284-285  231765004749716777699287377617143629, 178507813451136839263345802289704146
286-287  136874387095389009007106307214545386, 104474105891562688103671271710167367
288-289  79374595369014839274642494055057215, 60021180996405107038974254122614725
290-291  45168984001155315833402626520588266, 33825974632647963194667722399436525
292-293  25205466317848475043176731133751718, 18686695546317440929391749521258444
294-295  13782285759802803986377700706090054, 10111537461971549403649980342025950
296-297  7378620171976021037395531468936653, 5354864128357509723488261575774861
298-299  3864460585048672135814766183473636, 2772979210586279244250188375911358
300-301  1978199828254159542835471085891945, 1402834026698592561566825107737954
302-303  988780669768127930038730921949437, 692618773197741358930805620163614
304-305  482092379011984063812895076014158, 333385752013099298935508846637999
306-307  229024248045926299999654592508685, 156267338367542667054984840957693
308-309  105886256837940531739590405443366, 71240255651411061898319758721199
310-311  47583143439973601753856731911210, 31546209282143193841171007657643
312-313  20755318839681338395816951901731, 13549355787464420097873291314376
314-315  8774666522272008747026781052110, 5636088414139683585678777726877
316-317  3589791457646458005868133719924, 2266784972788363406599295794299
318-319  1418739810917196007993665512791, 879921960265348532656269102208
320-321  540664627657899751278089793904, 329035789117298520389678632800
322-323  198277750358275104949981460860, 118276865295510899251934835682
324-325  69822383391922687546185900993, 40778107961518883793925475756
326-328  23553725689284939606613571895, 13450816249111978546693311699, 7591784225825958112361224059
329-331  4233386355189168534296850304, 2331395330109189690724890575, 1267520640782914087974425996
332-334  680023414615535482938934051, 359858616985860333090867629, 187749565491132070332261356
335-337  96528230884444185620641803, 48880581291421955855248023, 24366394773646252543179651
338-340  11950127866184327417016617, 5762618400629360159930002, 2730599633160294455625499
341-343  1270562003274150283534070, 580129425448564644122654, 259727506817886492232768
344-346  113927242968123137053995, 48919768953940411759288, 20544474962792928371482
347-349  8430244272151447416075, 3376540116159529240074, 1318594832288112385220
350-353  501470559232017574841, 185491278877185613779, 66642837991239004891, 23221888508154987065
354-357  7835503696290293051, 2555737409099350916, 804334421080366384, 243751962014721716
358-362  70972491815018293, 19806622455445153, 5283876134562754, 1343506045899767, 324529763764686
363-368  74202162812316, 15993771156820, 3234818553579, 610694224873, 106962953198, 17258501322
369-378  2543849224, 339102439, 40375538, 4228420, 381389, 28928, 1758, 87, 1, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{46}\Phi_{2}(x)^{22}\Phi_{3}(x)^{13}\Phi_{4}(x)^{9}\\&\times \Phi_{5}(x)^{7}\Phi_{6}(x)^{5}\Phi_{7}(x)^{5}\Phi_{8}(x)^{3}\\&\times \Phi_{9}(x)^{3}\Phi_{10}(x)^{3}\Phi_{11}(x)^{3}\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\Phi_{16}(x)\\&\times \Phi_{17}(x)\Phi_{18}(x)\Phi_{19}(x)\Phi_{20}(x)\\&\times \Phi_{21}(x)\Phi_{22}(x)\Phi_{23}(x)^{2}\end{aligned}$$


### C24 — g=1, k=24

Order 444; period 5354228880; source v32/UNICYCLIC_MODELS.json, record 23.

$$B=2^{n+567},\quad a(n)=0\ (n<27).$$

$$a(n)=\left\lfloor\frac{B^{n-27}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 27).$$

$$R(x)=\sum_{j=0}^{416} c_jx^j.$$

```text
  0-8    61, 1547, 25861, 332165, 3520175, 32047560, 257088813, 1850559130, 12114320063
  9-14   72884863275, 406423741009, 2115137264643, 10333366301953, 47625596788510, 207964987355234
 15-18   863594907339406, 3421570050879940, 12971851681440416, 47181486678268127
 19-22   165026340861617391, 556249105334504188, 1810335810064459394, 5698886777893178853
 23-26   17380663546915997983, 51432440671794218957, 147877612485415422726, 413636395210455949458
 27-29   1126947374092008832770, 2993916441503283443045, 7763862983413410447612
 30-32   19671641069202767800424, 48744345310661557160290, 118222856374637878637468
 33-35   280881481457753018437236, 654214478585146641798628, 1494875865250044730767045
 36-38   3353309362040819167182164, 7389337409954388474318723, 16005382861406273518884875
 39-41   34096288314610751768208235, 71477241677823525891820177, 147528365588171811660784480
 42-44   299948567306381138334993514, 601018370701882746354047633, 1187394290071138843692248968
 45-47   2313960582842723967499640393, 4449895480304345513842272522, 8447877548253220136648477917
 48-49   15838459843727218444249647128, 29336097922966988773532731929
 50-51   53698933754164464624141158559, 97173189249675309435338565123
 52-53   173893097036047249562522918641, 307826005773011283159960114387
 54-55   539190229331775946822956565736, 934790049206686497729882211109
 56-57   1604494913292846041145860301412, 2727263532448539960955398161635
 58-59   4591857012045843095988259161342, 7659951101785292697922479843370
 60-61   12663100116263923130530341385927, 20750415435498639004034524372301
 62-63   33711575648832203086078331755139, 54310804959746288017965468637580
 64-65   86782987176455853889465466886994, 137564794080530283793244963476269
 66-67   216363818131596332270144678429655, 337710134994441861267956426581348
 68-69   523191304689963815158444126972689, 804648509383906306730101999088579
 70-71   1228714699216660291266806013997412, 1863213415546619431377306012035239
 72-73   2806119691408143364594603552631298, 4198025042600335624539691299717189
 74-75   6239363204498724048585126709151508, 9214061910360488563392833327645030
 76-77   13521813159003046336065190357218830, 19721829936454697707034697077147806
 78-79   28591817311565780796272617221720257, 41206973468362582603571625943912395
 80-81   59045203006579932557039644661582249, 84126431422206641131175452449345721
 82-83   119196027079854661598110008820496806, 167964947595356866855001454780588034
 84-85   235422426123202677056660758209823607, 328240907611239718900686648403278657
 86-87   455297657631174471714755487068672622, 628343133322868125848283024556627795
 88-89   862852978243271884108592092624757864, 1179108545645954769968118045013649499
 90-91   1603560346458877257010967964079552084, 2170539949363331643150138328892014773
 92-93   2924398830885936764272305942772655045, 3922167689716047490075684463760890728
 94-95   5236847010249430994184994647995025107, 6961459391337317106356601055945824530
 96-97   9214016543607841484421380964034124041, 12143579081480786587692196932111162484
 98-99   15937615446676613074722607592196293087, 20830897614283914771840675743310207613
100-101  27116205717182881838154732739514528159, 35157151384782034264578525240380841565
102-103  45403470356297194768879855358266791885, 58409178634266086323242224000610482681
104-105  74854032820042627169444189308361032633, 95568783924852316189455789484830119186
106-107  121564764342090959855708902174594750047, 154068399106590913707574059570263726077
108-109  194561284190374557710556442489971676612, 244826525342486150112737251336345469690
110-111  307002079626984093770325919927007693531, 383641886897852960565333671011517384261
112-113  477785618313737103230746022160139783311, 593037901772391716719582879912589407077
114-115  733657907766214523345235942952856746606, 904660191368481725370929042544780795764
116-117  1111927684427534715326952194476394518904, 1362337714003280125091498092954032761987
118-119  1663901885950299482598719931578889962007, 2025920613595495048257091098536267245348
120-121  2459152987927275033974663939621205232910, 2976002574912702757132976101315333734662
122-123  3590719584917842691901670273735778673248, 4319619686357105246895024013074112951849
124-125  5181319528561972722001152196849118417587, 6196988795742959998869057378623870256082
126-127  7390618333605988636103357595963970150228, 8789303572040911175264406914575587136117
128-129  10423542111372543216692952801968016211547, 12327543946780779999936407836989635521334
130-131  14539552377359138854774255540342953565074, 17102173185555876722593069142796974856396
132-133  20062709183133099157780606940141018737862, 23473496706092604982929958082822886721177
134-135  27392240109204174360282818214122963624342, 31882339767954135756817277747096009933956
136-137  37013208550200795627466707520964417896210, 42860571181013092358705449472584798173574
138-139  49506740402600482469358786205342135966501, 57040863338434657596202846613453290806892
140-141  65559131019013115388993854599112905114770, 75164943629338051641257797341949099068121
142-143  85969023708730273474614364515343019468490, 98089469286024069278053046806745478930313
144-145  111651738781506008903759763091164669183584, 126788559464948961610967849617196383955935
146-147  143639751339993094080143499649178302241480, 162351958541309617754392416958733705231654
148-149  183078280693607548607718862808671864504926, 205977797200197988053709473882495589512476
150-151  231214978111181806820142364447052991142272, 258958976072773645607105084745726942368922
152-153  289382794882616551553607575447266373300809, 322662331371070393861752959732838214910208
154-155  358975288692089420254100115493154968552368, 398499960632751179175580746064014081045871
156-157  441413888227492186068005511752180433332005, 487892391777683583871513360123880476652787
158-159  538106983311643212885027309558733306657872, 592223666553122686681319199907758320618312
160-161  650401133572728141304749835545832923343055, 712788869448232138741776768071219543496484
162-163  779525178424798349550191636239786271063106, 850735147210513273654444488165588280775866
164-165  926528563129756148740744809680054950767398, 1006997806848544893947729099159678997736018
166-167  1092215741242639849703906088760160054697857, 1182233619660975988113534930022435713881838
168-169  1277079038304310751474441285140854288649370, 1376753958653253815410255405453678201786924
170-171  1481232826804381159832690244052111945230060, 1590460817173902088648197574680145431064277
172-173  1704352228274811991908228423612019693623973, 1822789058139381245912713160326967134270781
174-175  1945619786422997556005254775140505520719146, 2072658389272324361317559939618592040493160
176-177  2203683611661339040838891723531630976689991, 2338438520090816994963047829948391070901578
178-179  2476630356315252795375468517821378339908992, 2617930710118637401122663549797144520530521
180-181  2761976026127223112209198599567091417526256, 2908368456251386016677622510955559970945230
182-183  3056677065625459581300360029773411849052860, 3206439395906706432914765815601545360457405
184-185  3357163385551910605002206715616551790109322, 3508329642268021352400068869412254084756454
186-187  3659394058292816744127706526549603812254476, 3809790754568065162764336232478311740017819
188-189  3958935335289924668017808351286961839962766, 4106228429830367638582785853933704637899997
190-191  4251059494691315420058228766944836675055045, 4392810844051724459067588555122024161644197
192-193  4530861873667315477988497796577889644634133, 4664593439450308643814303142005845638435944
194-195  4793392349055530922899553847645512520300818, 4916655922287224955023274972911061393253713
196-197  5033796574168766864927619445901475795776235, 5144246373128486075353234540507835010196274
198-199  5247461525983340510348549381988293280028197, 5342926741273263349136118109028448022732472
200-201  5430159423027306552466420983511151807763486, 5508713648232363061035816141951696836793997
202-203  5578183883119452916890427097350083280193942, 5638208395863553168576324875679536281917705
204-205  5688472326382186964301823031227239473166176, 5728710377576489444812550715100234541187215
206-207  5758709096537416007549650693724377799371794, 5778308718881258674111008801910937026308049
208-209  5787404554416679063533533370283201745908957, 5785947897707047215731126513917491204317748
210-211  5773946452698257923044298775998848624087864, 5751464266350292908670671534124409087861569
212-213  5718621172054639397797118161088335050493106, 5675591749451942278835644445708475507472824
214-215  5622603812997841562253766282261037345738126, 5559936447174469797665425151289612074109582
216-217  5487917611528469838795672374585008072408900, 5406921343656279339518830009813806193749429
218-219  5317364592782527957242422345198373219989510, 5219703720623724295202821938203130781627931
220-221  5114430709741374730170829941370849973130949, 5002069122519973471742427960692412538782638
222-223  4883169856219649910809093119819692685994459, 4758306741224916672823800934923469987167529
224-225  4628072030625050785347006722048346701929224, 4493071829614246000207942683181525639057987
226-227  4353921512897738569890394051867327013383551, 4211241177351117870184968477171815233719567
228-229  4065651175631508864715307274344217812566286, 3917767774318121889503679693989307072257446
230-231  3768198977511162433018344273309916343680260, 3617540553695126010406422336225595164375038
232-233  3466372300134289241752680672983490578019210, 3315254575179124857745861819412023463587046
234-235  3164725124690670763444004970714381524118740, 3015296224406385028077760615692336719699062
236-237  2867452155547760466638489858680116165721657, 2721647026378907345067631626181144116009054
238-239  2578302947837033673823028254868756585858626, 2437808566838287602280946381762307811840567
240-241  2300517956480123553931847991776548857599753, 2166749858173875319948176658413282603801715
242-243  2036787266802662981864570395785742909585258, 1910877346357919784115469746302952108293880
244-245  1789231660203599654025064550247930784042323, 1672026697184088163161227031977389286489926
246-247  1559404672255958798862845819157674481890274, 1451474578203241610635668691271311711799550
248-249  1348313463301367112537201536355616554743412, 1249967908529476044932504782107379051140660
250-251  1156455677090220106118611044810463492440362, 1067767508569647862669292705724577637109894
252-253  983869030040201375939333618358072634881667, 904702756754608005983276022498770318698477
254-255  830190155770052566344896565914775576910879, 760233746848886357348511833389173379932438
256-257  694719216269416938424778752746744845750770, 633517520710706917214137437538219032109206
258-259  576486960109827238855864912099486347434157, 523475200288852226307377381483538775984128
260-261  474321228172166335206672080479370254588761, 428857224523138920785281610910095736452832
262-263  386910341284984987013442199881877275273908, 348304372777641443180680282003698421666372
264-265  312861312147144132511297480462601448115157, 280402786555539282097974244721319476074229
266-267  250751366610255053699299384279978663799831, 223731747438009109714756331808357043021428
268-269  199171800589289006948033371169138582067578, 176903497598494386412235431208376770183721
270-271  156763707508992454164911506862486757197505, 138594871992305053733177092996416403023569
272-273  122245562840654548158722230125553820953273, 107570927589738461642023426764765771687954
274-275  94433029834584378459362850604367839455404, 82701091439193313029878490838364170457926
276-277  72251644316465374214198556622087903854364, 62968599776850451822520255875922704337438
278-279  54743243622343593292696710839398620151711, 47474165208389423962158376413843755169756
280-281  41067128622634691314636003455265057695221, 35434893949715509745834257014720679115820
282-283  30496996319283765870888256817621491787932, 26179490084314432801027336582830093772297
284-285  22414665062315652176724461647222023006270, 19140741306937111196061984475089610994602
286-287  16301548374602784304836168615645764111317, 13846194522376473899477421020798142722409
288-289  11728730730582728759556563889723320129974, 9907813897004000917746280278067862741474
290-291  8346373007902419827465181042718619973679, 7011281562660725320490456343296123198165
292-293  5873039020315955309601079751935877386863, 4905463553317301179039310584887264513937
294-295  4085397940983624658043806554507857256011, 3392430015785588753124979066462748970426
296-297  2808628692129512579842859284519973460713, 2318296261230267808143907743032923694513
298-299  1907737327531919759059727260471350878772, 1565044491814772526963934851915916764061
300-301  1279900652807942747436887495193642874113, 1043397601445401336835884531239121349898
302-303  847870418044359753792728315443836487275, 686747050474258031944139403893241334305
304-305  554412348382756801675722596806836702716, 446085752131246804645491472464592864322
306-307  357711782541789707647352764465949736561, 285862446110384896631452715649981297641
308-309  227650657263287356570881030111932710925, 180653781865023351805421500643679096995
310-311  142846421988029390665728844730663606086, 112541588535154575844742460312776945035
312-313  88339443454888585090830237435965071530, 69082834986539309517767385163156106309
314-315  53818895804933190425108187101119541295, 41766023497126186937244330883079503971
316-317  32285614101194616338677693515130608478, 24857971276740551834179735050102915081
318-319  19061865059849968894346920233184733437, 14557264265805467234170880442855628948
320-321  11070814793156197390859085048497894300, 8383681857941415550814058999886764016
322-323  6321417188658876301158065816942950796, 4745552202585309724239165030027946733
324-325  3546655027331484981434531445107894101, 2638622880535295491110792984918290219
326-327  1954011800157263262035790574666657355, 1440233110964759973785841921043401253
328-329  1056470447862866730840829395879067933, 771192795974582510578617993551223475
330-331  560158036690805691557997352894566476, 404818109097628761453417583526326464
332-333  291051315503250709308807519969423087, 208159727794680959681004598984586631
334-335  148080293966525278840922232149433167, 104767299765161855630240348663972441
336-337  73711496942814874755234882670880224, 51567642614560270390721560764559985
338-339  35867565385723990036169132198081947, 24800330542541980817204172499706303
340-341  17044751320709189526099455958307835, 11642504329868615710752558444774762
342-343  7902559004833473796497639562696748, 5329614778789197972127131843575590
344-345  3570834677625000859208894284466689, 2376438238801337153662731248493298
346-347  1570728031357198630241603238248059, 1030921592562804192898897451358063
348-349  671785380990210846989845473378215, 434553543181485023261176984984661
350-351  278990096489159497840187150667285, 177741627872148828403510389225202
352-353  112347549243468756997712031381004, 70441448334568625833220305988283
354-355  43802216698394146383327130755932, 27007013537253580215914618825025
356-357  16507284778149417432988126691418, 9999896812823526975444569844899
358-359  6002530881618755152778087741580, 3569326906055964202727547516103
360-361  2102039601758009280346808447523, 1225696769187000031748273165731
362-363  707445129281766053100487470129, 404059026592507548557616178027
364-365  228301317413154158716466166579, 127569518555492568915475062040
366-367  70472132948000355143670777373, 38474270912689639786783660962
368-370  20751490799634347992421928847, 11053251938059629205670487299, 5811933765992290025426218145
371-373  3015508139837867324226311877, 1543192008547539259840385050, 778573598937570196037065371
374-376  387070316473372205327260838, 189526375101407053878215882, 91349506506708235039748121
377-379  43316550043123709028455088, 20195433423082099347978612, 9251877561470738773140335
380-382  4161919425483714677692993, 1837117710027850232999807, 795121627074154722863370
383-385  337160672450697740544893, 139951817860583440281596, 56815404461639636246954
386-388  22536226877783119790266, 8725233730169939787320, 3293637767467509306997
389-392  1210780900483953496665, 432909228151826702213, 150341525928256937763, 50637874284130179515
393-396  16515785556567695495, 5207228262849652239, 1584129789113088585, 464059641444290474
397-401  130616377924366840, 35238144080511664, 9087962037635703, 2234007115644731, 521740108239399
402-407  115345101516489, 24040823732361, 4702218322591, 858569072531, 145457112159, 22704465921
408-416  3238000693, 417689282, 48139638, 4879133, 426459, 31135, 1854, 75, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{48}\Phi_{2}(x)^{24}\Phi_{3}(x)^{16}\Phi_{4}(x)^{12}\\&\times \Phi_{5}(x)^{7}\Phi_{6}(x)^{8}\Phi_{7}(x)^{5}\Phi_{8}(x)^{6}\\&\times \Phi_{9}(x)^{3}\Phi_{10}(x)^{3}\Phi_{11}(x)^{3}\Phi_{12}(x)^{4}\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\Phi_{16}(x)\\&\times \Phi_{17}(x)\Phi_{18}(x)\Phi_{19}(x)\Phi_{20}(x)\\&\times \Phi_{21}(x)\Phi_{22}(x)\Phi_{23}(x)\Phi_{24}(x)^{2}\end{aligned}$$


## Rooted trees: fixed leaf counts


### R01 — k=1 leaves

Order 1; period 1; source v31/ROOTED_MODELS.json, record 0.

$$B=2^{n+3},\quad a(n)=0\ (n<1).$$

$$a(n)=\left\lfloor\frac{B^{n-1}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 1).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)$$


### R02 — k=2 leaves

Order 4; period 2; source v31/ROOTED_MODELS.json, record 1.

$$B=2^{n+4},\quad a(n)=0\ (n<3).$$

$$a(n)=\left\lfloor\frac{B^{n-3}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 3).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{3}\Phi_{2}(x)$$


### R03 — k=3 leaves; A055278 (offset 4)

Order 8; period 6; source v31/ROOTED_MODELS.json, record 2.

$$B=2^{n+8},\quad a(n)=0\ (n<4).$$

$$a(n)=\left\lfloor\frac{B^{n-4}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 4).$$

$$R(x)=1+x^{2}+x^{3}$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)\Phi_{3}(x)$$


### R04 — k=4 leaves; A055279 (offset 5)

Order 14; period 12; source v31/ROOTED_MODELS.json, record 3.

$$B=2^{n+16},\quad a(n)=0\ (n<5).$$

$$a(n)=\left\lfloor\frac{B^{n-5}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 5).$$

$$\begin{aligned}R(x)&=1+x+3x^{2}+5x^{3}+7x^{4}+5x^{5}+5x^{6}\\&+2x^{7}+x^{8}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{7}\Phi_{2}(x)^{3}\Phi_{3}(x)\Phi_{4}(x)$$


### R05 — k=5 leaves; A055280 (offset 6)

Order 18; period 20; source v31/ROOTED_MODELS.json, record 4.

$$B=2^{n+21},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=\sum_{j=0}^{11} c_jx^j.$$

```text
  0-11   1, 0, 4, 7, 7, 12, 13, 9, 10, 4, 2, 1
```

$$Q(x)=\Phi_{1}(x)^{9}\Phi_{2}(x)^{3}\Phi_{4}(x)\Phi_{5}(x)$$


### R06 — k=6 leaves; A055281 (offset 7)

Order 30; period 60; source v31/ROOTED_MODELS.json, record 5.

$$B=2^{n+39},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=\sum_{j=0}^{22} c_jx^j.$$

```text
  0-17   1, 3, 12, 36, 91, 190, 356, 568, 832, 1089, 1303, 1401, 1397, 1250, 1028, 756, 503, 287
 18-22   149, 61, 21, 5, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{11}\Phi_{2}(x)^{5}\Phi_{3}(x)^{3}\Phi_{4}(x)\\&\times \Phi_{5}(x)\Phi_{6}(x)\end{aligned}$$


### R07 — k=7 leaves; A055282 (offset 8)

Order 38; period 420; source v31/ROOTED_MODELS.json, record 6.

$$B=2^{n+49},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=\sum_{j=0}^{29} c_jx^j.$$

```text
  0-15   1, 3, 15, 52, 147, 359, 777, 1484, 2564, 4040, 5872, 7889, 9884, 11551, 12657, 12994
 16-29   12515, 11281, 9523, 7482, 5463, 3674, 2258, 1248, 618, 262, 94, 26, 6, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{13}\Phi_{2}(x)^{5}\Phi_{3}(x)^{3}\Phi_{4}(x)\\&\times \Phi_{5}(x)\Phi_{6}(x)\Phi_{7}(x)\end{aligned}$$


### R08 — k=8 leaves; A055283 (offset 9)

Order 48; period 840; source v31/ROOTED_MODELS.json, record 7.

$$B=2^{n+63},\quad a(n)=0\ (n<9).$$

$$a(n)=\left\lfloor\frac{B^{n-9}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 9).$$

$$R(x)=\sum_{j=0}^{38} c_jx^j.$$

```text
  0-15   1, 3, 19, 70, 230, 629, 1576, 3440, 6932, 12669, 21630, 34197, 51020, 71433, 95046, 119655
 16-26   143821, 164349, 179792, 187419, 187211, 178250, 162544, 141020, 116915, 91820, 68629
 27-38   48217, 32008, 19710, 11346, 5918, 2839, 1183, 445, 132, 35, 6, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{15}\Phi_{2}(x)^{7}\Phi_{3}(x)^{2}\Phi_{4}(x)^{3}\\&\times \Phi_{5}(x)\Phi_{6}(x)\Phi_{7}(x)\Phi_{8}(x)\end{aligned}$$


### R09 — k=9 leaves; A055284 (offset 10)

Order 62; period 2520; source v31/ROOTED_MODELS.json, record 8.

$$B=2^{n+83},\quad a(n)=0\ (n<10).$$

$$a(n)=\left\lfloor\frac{B^{n-10}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 10).$$

$$R(x)=\sum_{j=0}^{51} c_jx^j.$$

```text
  0-13   1, 5, 32, 150, 591, 2009, 6040, 16231, 39638, 88653, 183357, 353177, 637831, 1085641
 14-22   1750407, 2683761, 3927059, 5500043, 7391926, 9552618, 11891918, 14280464, 16562039
 23-31   18567214, 20134937, 21130433, 21466135, 21110409, 20095165, 18508892, 16486926, 14190994
 32-41   11791766, 9446026, 7283513, 5394770, 3829375, 2597091, 1677190, 1026817, 592998, 320996
 42-51   161714, 75081, 31815, 12118, 4084, 1189, 294, 57, 9, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{17}\Phi_{2}(x)^{7}\Phi_{3}(x)^{5}\Phi_{4}(x)^{3}\\&\times \Phi_{5}(x)\Phi_{6}(x)\Phi_{7}(x)\Phi_{8}(x)\\&\times \Phi_{9}(x)\end{aligned}$$


### R10 — k=10 leaves; A055285 (offset 11)

Order 78; period 2520; source v31/ROOTED_MODELS.json, record 9.

$$B=2^{n+105},\quad a(n)=0\ (n<11).$$

$$a(n)=\left\lfloor\frac{B^{n-11}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 11).$$

$$R(x)=\sum_{j=0}^{66} c_jx^j.$$

```text
  0-13   1, 7, 49, 269, 1245, 4939, 17343, 54498, 155594, 407196, 985891, 2223228, 4700120, 9363975
 14-21   17666816, 31693673, 54266477, 88965432, 140056732, 212257121, 310365528, 438709666
 22-28   600516525, 797186752, 1027670339, 1287926986, 1570718773, 1865656065, 2159722750
 29-35   2438071372, 2685244987, 2886466238, 3029095739, 3103813605, 3105644095, 3034402979
 36-42   2894794940, 2695854225, 2450097732, 2172215141, 1877748726, 1581657118, 1297190764
 43-50   1034948746, 802424625, 603837156, 440401878, 310786833, 211803084, 139084706, 87780260
 51-60   53085057, 30656767, 16837939, 8755381, 4286118, 1963164, 834733, 326670, 116299, 37220
 61-66   10510, 2575, 527, 89, 11, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{19}\Phi_{2}(x)^{9}\Phi_{3}(x)^{5}\Phi_{4}(x)^{3}\\&\times \Phi_{5}(x)^{3}\Phi_{6}(x)\Phi_{7}(x)\Phi_{8}(x)\\&\times \Phi_{9}(x)\Phi_{10}(x)\end{aligned}$$


### R11 — k=11 leaves; A055286 (offset 12)

Order 88; period 27720; source v31/ROOTED_MODELS.json, record 10.

$$B=2^{n+117},\quad a(n)=0\ (n<12).$$

$$a(n)=\left\lfloor\frac{B^{n-12}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 12).$$

$$R(x)=\sum_{j=0}^{75} c_jx^j.$$

```text
  0-12   1, 6, 47, 266, 1263, 5177, 18769, 60951, 179955, 487584, 1223378, 2862360, 6285398
 13-20   13022831, 25582989, 47850258, 85534428, 146605593, 241656105, 384071231, 589934789
 21-27   877536517, 1266455966, 1776144437, 2424106819, 3223717555, 4181942242, 5297107115
 28-34   6557112544, 7938246477, 9404989000, 10910820916, 12400270673, 13811940920, 15082506024
 35-41   16151138672, 16964167668, 17479271997, 17669007020, 17523039001, 17049087756, 16272223800
 42-48   15232845748, 13983311589, 12583834011, 11097831980, 9587442202, 8109393717, 6711815514
 49-55   5432000069, 4295414923, 3315739229, 2495937184, 1829975302, 1305038205, 903830941
 56-63   606823856, 394146532, 247090964, 149103026, 86339436, 47804628, 25205387, 12594818
 64-75   5931666, 2615640, 1071799, 404293, 138898, 42849, 11693, 2755, 549, 87, 11, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{21}\Phi_{2}(x)^{9}\Phi_{3}(x)^{4}\Phi_{4}(x)^{3}\\&\times \Phi_{5}(x)^{3}\Phi_{6}(x)\Phi_{7}(x)\Phi_{8}(x)\\&\times \Phi_{9}(x)\Phi_{10}(x)\Phi_{11}(x)\end{aligned}$$


### R12 — k=12 leaves; A055287 (offset 13)

Order 110; period 27720; source v31/ROOTED_MODELS.json, record 11.

$$B=2^{n+147},\quad a(n)=0\ (n<13).$$

$$a(n)=\left\lfloor\frac{B^{n-13}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 13).$$

$$R(x)=\sum_{j=0}^{96} c_jx^j.$$

```text
  0-12   1, 8, 69, 449, 2482, 11785, 49587, 186969, 641662, 2021943, 5903631, 16077927, 41096754
 13-19   99090716, 226422797, 492240454, 1021807195, 2031716645, 3880696123, 7138702627
 20-25   12676736947, 21776363811, 36256520204, 58608661581, 92129786496, 141033891922
 26-31   210523745823, 306795274941, 436955435518, 608826385471, 830628500323, 1110528687262
 32-37   1456072797685, 1873513284558, 2367085792779, 2938271782128, 3585130863341, 4301752025361
 38-43   5077917244894, 5899011456180, 6746252620116, 7597230676352, 8426783103506, 9208132272869
 44-48   9914258001046, 10519371375789, 11000425650594, 11338501075680, 11519998764447
 49-53   11537495716183, 11390237931407, 11084178909353, 10631610706827, 10050368403207
 54-59   9362725583196, 8594023685881, 7771195308109, 6921250389670, 6069883747993, 5240256380194
 60-65   4452066095487, 3720912708949, 3058009385100, 2470190922390, 1960211448773, 1527244589686
 66-71   1167543832841, 875167973916, 642725440628, 462061682448, 324862665286, 223132915137
 72-78   149548309796, 97675507892, 62079512109, 38332621005, 22954623991, 13304028116, 7446318138
 79-86   4014718385, 2079264293, 1031146514, 487909461, 219367789, 93284960, 37313705, 13953352
 87-96   4841136, 1545430, 448929, 117316, 27078, 5439, 916, 127, 13, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{23}\Phi_{2}(x)^{11}\Phi_{3}(x)^{7}\Phi_{4}(x)^{5}\\&\times \Phi_{5}(x)^{3}\Phi_{6}(x)^{3}\Phi_{7}(x)\Phi_{8}(x)\\&\times \Phi_{9}(x)\Phi_{10}(x)\Phi_{11}(x)\Phi_{12}(x)\end{aligned}$$


### R13 — k=13 leaves

Order 124; period 360360; source v31/ROOTED_MODELS.json, record 12.

$$B=2^{n+165},\quad a(n)=0\ (n<14).$$

$$a(n)=\left\lfloor\frac{B^{n-14}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 14).$$

$$R(x)=\sum_{j=0}^{109} c_jx^j.$$

```text
  0-12   1, 8, 75, 517, 3018, 15173, 67452, 268875, 974689, 3244464, 10003524, 28766775, 77623841
 13-19   197557012, 476390084, 1092784939, 2393088221, 5018983453, 10110062706, 19610905567
 20-25   36717196802, 66496320852, 116715661234, 198900948384, 329631005744, 532046673431
 26-31   837519569178, 1287380975010, 1934570172218, 2845011427617, 4098498068054, 5788829735263
 32-36   8022955220080, 10918883783053, 14602194671112, 19201042235186, 24839686459539
 37-41   31630693429442, 39666124773135, 49008156417689, 59679732512500, 71655926990586
 42-46   84856778951118, 99142320593512, 114310491575894, 130098442702177, 146187583894739
 47-51   162212419141685, 177772989192214, 192450383944247, 205824583007002, 217493580881838
 52-56   227092670629742, 234312607753427, 238915483550650, 240747177789081, 239745562730823
 57-61   235943834001268, 229468773383918, 220534021898514, 209428881752242, 196503388252785
 62-66   182150723101541, 166788110926785, 150837483442816, 134707072410354, 118775038901366
 67-71   103375961241352, 88790814595078, 75240715182599, 62884477196141, 51819701033171
 72-76   42086947788188, 33676338413296, 26535871700046, 20580683078908, 15702545644437
 77-82   11778965211061, 8681382252280, 6282109986796, 4459817952167, 3103489277488, 2114924067580
 83-88   1409937425645, 918479951585, 583926808468, 361796853130, 218134887226, 127763430543
 89-95   72559995198, 39874682789, 21154583451, 10806929979, 5300762924, 2488326741, 1113826950
 96-105  473443915, 190192046, 71817360, 25328996, 8282837, 2489322, 680615, 167090, 36297, 6824
106-109  1086, 139, 14, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{25}\Phi_{2}(x)^{11}\Phi_{3}(x)^{7}\Phi_{4}(x)^{5}\\&\times \Phi_{5}(x)^{3}\Phi_{6}(x)^{3}\Phi_{7}(x)\Phi_{8}(x)\\&\times \Phi_{9}(x)\Phi_{10}(x)\Phi_{11}(x)\Phi_{12}(x)\\&\times \Phi_{13}(x)\end{aligned}$$


### R14 — k=14 leaves

Order 144; period 360360; source v31/ROOTED_MODELS.json, record 13.

$$B=2^{n+191},\quad a(n)=0\ (n<15).$$

$$a(n)=\left\lfloor\frac{B^{n-15}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 15).$$

$$R(x)=\sum_{j=0}^{128} c_jx^j.$$

```text
  0-11   1, 9, 90, 672, 4245, 23019, 110391, 474185, 1851742, 6637118, 22031069, 68193332
 12-18   198052656, 542479457, 1407804022, 3475235793, 8189550946, 18481826865, 40057327584
 19-24   83596744908, 168377411419, 328010668615, 619219885260, 1134813456772, 2022241583476
 25-29   3509283929658, 5938506316938, 9812012279456, 15847746459358, 25047986659868
 30-34   38779833490816, 58866217926309, 87684518684033, 128267990382412, 184403435163641
 35-39   260716465915307, 362734230031365, 496913930275430, 670625194028599, 892074257012490
 40-44   1170159735598436, 1514251810080396, 1933891026304585, 2438407162302089, 3036465250268680
 45-49   3735551405447772, 4541418728718312, 5457518648682739, 6484449605680232, 7619457331981275
 50-53   8856024225401829, 10183582881930507, 11587387253308474, 13048566738023871
 54-57   14544381951265510, 16048687789451559, 17532599543844481, 18965342224033578
 58-61   20315253268526956, 21550894424009891, 22642222256056308, 23561757246820782
 62-65   24285691927178070, 24794876321328565, 25075627628886749, 25120316509194558
 66-69   24927698065774202, 24502966547965511, 23857532333003462, 23008532238092006
 70-73   21978103083935096, 20792458053239667, 19480819314104075, 18074263637599788
 74-77   16604544018233262, 15102945750902251, 13599233705096055, 12120736144180877
 78-82   10691602702083790, 9332258844968261, 8059068861141564, 6884204076526830, 5815703896936219
 83-87   4857705308328204, 4010811363571645, 3272562626701847, 2637975574114113, 2100111029007041
 88-92   1650640255111585, 1280379696539351, 979772572822913, 739300971996906, 549819715802900
 93-97   402808561116172, 290545457653675, 206207180359704, 143907325237747, 98682982343552
 98-102  66442536539427, 43886386625133, 28411637914220, 18009979582107, 11166302277696
103-108  6763474885751, 3996977883960, 2301323400121, 1288931976876, 701039073584, 369565091319
109-115  188435836716, 92714474608, 43904848643, 19952436497, 8673106618, 3592925489, 1412504264
116-126  524482290, 182923427, 59548724, 17958720, 4974823, 1252261, 283060, 56475, 9784, 1420, 170
127-128  15, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{27}\Phi_{2}(x)^{13}\Phi_{3}(x)^{6}\Phi_{4}(x)^{5}\\&\times \Phi_{5}(x)^{3}\Phi_{6}(x)^{3}\Phi_{7}(x)^{3}\Phi_{8}(x)\\&\times \Phi_{9}(x)\Phi_{10}(x)\Phi_{11}(x)\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\end{aligned}$$


### R15 — k=15 leaves

Order 168; period 360360; source v31/ROOTED_MODELS.json, record 14.

$$B=2^{n+224},\quad a(n)=0\ (n<16).$$

$$a(n)=\left\lfloor\frac{B^{n-16}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 16).$$

$$R(x)=\sum_{j=0}^{151} c_jx^j.$$

```text
  0-11   1, 12, 130, 1114, 7984, 49277, 268021, 1305674, 5772860, 23406144, 87774552, 306612926
 12-18   1003722186, 3095153421, 9031281609, 25033948851, 66151857516, 167164788142, 405096408544
 19-24   943814673442, 2119010599157, 4594235717015, 9637534756014, 19595753702856, 38682241205879
 25-29   74245663582809, 138754745974097, 252816473836755, 449642365829784, 781484928930018
 30-34   1328677178615483, 2212011091455720, 3609271115864441, 5776777539252745, 9076770029049017
 35-38   14011350735177126, 21263486684390698, 31745223487871272, 46652774335939670
 39-42   67527516741457424, 96321165124026755, 135462515273731631, 187922220431606027
 43-46   257271117613217950, 347726753789850653, 464182052150113550, 612209605739374174
 47-50   798034983602885004, 1028472771753201855, 1310819915120257156, 1652702320736302041
 51-54   2061872630003827970, 2545959534267140074, 3112171905988381500, 3766964219243545381
 55-58   4515673059048173607, 5362137761711434924, 6308321148315033155, 7353948671429183290
 59-62   8496185852126660677, 9729374440948911675, 11044847130306110508, 12430838792479460719
 63-66   13872509098427186980, 15352087071349841675, 16849142803357308833, 18340985472489050989
 67-70   19803180255593865535, 21210170127200160650, 22535982264084162684, 23754993260376967569
 71-74   24842722971698575808, 25776623886821874342, 26536831705421289411, 27106843433486743063
 75-78   27474091806859468794, 27630389132272709597, 27572219465762487067, 27300865120499610759
 79-82   26822361390476188308, 26147281641069973323, 25290363049867000709, 24269990812619608109
 83-86   23107565108093463905, 21826780187120108966, 20452848332494243936, 19011702982412751836
 87-90   17529214973599640049, 16030453738304883812, 14539021567203248115, 13076484029190111842
 91-94   11661913668430443736, 10311557591028168927, 9038632912351815533, 7853247668070784385
 95-98   6762439041978448139, 5770315929558578547, 4878289138703980682, 4085370056272036529
 99-102  3388517404476569235, 2783011727585578535, 2262838353579702540, 1821061588892081422
103-106  1450175598146499219, 1142420557344037630, 890056000566058265, 685586585214348577
107-110  521938579887783512, 392588081283445761, 291644180824709944, 213891970900490162
111-114  154801387569769488, 110508459085520665, 77775623089422878, 53937471932358484
115-118  36837677256343791, 24762030662496015, 16371609458702607, 10639119529578410
119-123  6790549166891956, 4253440637620593, 2612383762571613, 1571775736451973, 925476354012791
124-128  532709521450550, 299403404594381, 164101411325636, 87590709616505, 45461314491495
129-134  22906203557978, 11184432219994, 5281677924522, 2407073359039, 1056163961775, 444991681105
135-141  179505028362, 69100728542, 25291432646, 8764938855, 2862638165, 876383875, 249946491
142-151  65933596, 15951469, 3504011, 690328, 120141, 18106, 2304, 237, 19, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{29}\Phi_{2}(x)^{13}\Phi_{3}(x)^{9}\Phi_{4}(x)^{5}\\&\times \Phi_{5}(x)^{5}\Phi_{6}(x)^{3}\Phi_{7}(x)^{3}\Phi_{8}(x)\\&\times \Phi_{9}(x)\Phi_{10}(x)\Phi_{11}(x)\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\end{aligned}$$


### R16 — k=16 leaves

Order 192; period 720720; source v31/ROOTED_MODELS.json, record 15.

$$B=2^{n+255},\quad a(n)=0\ (n<17).$$

$$a(n)=\left\lfloor\frac{B^{n-17}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 17).$$

$$R(x)=\sum_{j=0}^{174} c_jx^j.$$

```text
  0-11   1, 13, 151, 1382, 10609, 70022, 407295, 2120973, 10022078, 43416823, 173935326, 648984334
 12-17   2268973329, 7471740531, 23279223903, 68894345363, 194350530344, 524238581799
 18-22   1355907528095, 3371227671191, 8076093793774, 18680153936704, 41798362405050
 23-27   90636668064729, 190774567005871, 390356305075362, 777553339781891, 1509690940399160
 28-32   2860592510019526, 5295652405037075, 9588071944246046, 16994735503296217, 29516473240087076
 33-36   50274980362206089, 84047349949665726, 138008767058517754, 222743946821125642
 37-40   353597666413765845, 552443276160701801, 849954130502499641, 1288464986712109144
 41-44   1925506897431094998, 2838088236728508114, 4127774510111550905, 5926589030286872690
 45-48   8403714248627828917, 11772919064661451673, 16300571056003289726, 22314015668834026705
 49-52   30210019379359827903, 40462884481796908518, 53631754303518977093, 70366545484172343468
 53-56   91411875290507249307, 117608304475073404146, 149890197355347675147, 189279518035055626929
 57-60   236874940908515600790, 293835759589723105293, 361360233053393978014, 440658210854246682385
 61-64   532918126516524445355, 639268732748808401857, 760736262697334631431, 898198024592070870976
 65-67   1052333755419075388767, 1223576354678092870407, 1412063871318698893709
 68-70   1617594806966197499934, 1839588907557874956083, 2077055629366554694759
 71-73   2328572371860046827665, 2592274364258168510295, 2865857773876317940928
 74-76   3146597180542909353862, 3431378044552448383651, 3716744207216372878547
 77-79   3998959826974721955351, 4274084501954018089065, 4538059692867121703638
 80-82   4786803974111094416760, 5016314136873706698098, 5222768778113630005854
 83-85   5402630756430926338755, 5552744800775721152936, 5670426628899803312680
 86-88   5753540173371803746004, 5800559913888879555781, 5810615861320419574274
 89-91   5783519404163404589133, 5719768982648727608509, 5620535360337785441275
 92-94   5487627080408108146970, 5323437480988637519905, 5130875364592632411779
 95-97   4913282033569387542905, 4674337890083610331470, 4417962131559829053200
 98-100  4148209240398563417817, 3869165964081922225398, 3584852316385711813013
101-103  3299129814131399229661, 3015619720518933119851, 2737633520955103005772
104-106  2468117244139766688635, 2209610591740888040937, 1964221190006093776337
107-109  1733613656202427147938, 1519012611901838853407, 1321218295439508422370
110-112  1140633046181800868520, 977296662676153736869, 830928480611098950869
113-116  700973970923102609640, 586653716282216504142, 487012771347120463444, 400968633019005329039
117-120  327356321541765889724, 264969382755159326623, 212595945757490221313, 169049291361700676071
121-124  133192688612888521193, 103958527180180807747, 80362002745915943887, 61509795293792820181
125-128  46604313594422132238, 34944164304873206062, 25921543893201033427, 19017251737479648290
129-132  13793989707292055037, 9888555083570799378, 7003457307661145174, 4898402338676915829
133-136  3381997832513823310, 2303943698755496733, 1547890161593799032, 1025072523082262609
137-140  668770280116027533, 429589004711946226, 271526325292603317, 168757679885869015
141-144  103061880746855463, 61799319308980240, 36355050078108489, 20963290115836929
145-149  11837428962127696, 6539081187849683, 3529888405136808, 1859838860927560, 955217936202165
150-154  477570948166593, 232072856203126, 109432296622282, 49982585378580, 22069191292461
155-160  9399531393705, 3852469054521, 1515429922647, 570453261076, 204818141119, 69885471492
161-168  22567311566, 6864590325, 1956458346, 519259044, 127424371, 28671371, 5856005, 1072724
169-174  173531, 24330, 2872, 277, 20, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{31}\Phi_{2}(x)^{15}\Phi_{3}(x)^{9}\Phi_{4}(x)^{7}\\&\times \Phi_{5}(x)^{5}\Phi_{6}(x)^{3}\Phi_{7}(x)^{3}\Phi_{8}(x)^{3}\\&\times \Phi_{9}(x)\Phi_{10}(x)\Phi_{11}(x)\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\Phi_{16}(x)\end{aligned}$$


### R17 — k=17 leaves

Order 208; period 12252240; source v31/ROOTED_MODELS.json, record 16.

$$B=2^{n+273},\quad a(n)=0\ (n<18).$$

$$a(n)=\left\lfloor\frac{B^{n-18}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 18).$$

$$R(x)=\sum_{j=0}^{189} c_jx^j.$$

```text
  0-11   1, 12, 146, 1360, 10622, 71354, 422318, 2237716, 10758754, 47426521, 193348269, 734207684
 12-17   2612727085, 8758308920, 27781627408, 83718852880, 240512242482, 660776541049
 18-22   1740975789118, 4410124215663, 10765323988496, 25376511839366, 57876044227046
 23-27   127936257339510, 274550369007276, 572843574085609, 1163696129562150, 2304587394336117
 28-31   4454696154164736, 8413949796504512, 15545038491900844, 28120121407139966
 32-35   49850823410458380, 86681915686037553, 147956463737692184, 248093671538999946
 36-39   408960268581856800, 663161680632014877, 1058529327638760743, 1664133277816209658
 40-43   2578202248307836185, 3938381555429101401, 5934798938022636317, 8826431944802259998
 44-47   12961271631035968082, 18800747805369653815, 26948812983913300429, 38185967798516641939
 48-51   53508343206370910373, 74171729493489761431, 101740156505401108800, 138138284839453167092
 52-55   185706469299130535349, 247256913788733658776, 326128866468303349662, 426240325926791800052
 56-58   552133269213791062865, 709009000726584074532, 902749890738455840313
 59-61   1139923558693068060399, 1427765494466358486594, 1774136232877149128535
 62-64   2187449530760483484567, 2676568561809567950308, 3250667952900811967505
 65-67   3919060534697514198012, 4690988954076763697600, 5575383765686539840750
 68-70   6580591240039497958186, 7714075835724739777801, 8982104011739046238924
 71-73   10389417719189601144331, 11938907421074226153909, 13631295751916475144508
 74-76   15464843857431349128495, 17435092965841093705142, 19534653769837037085294
 77-79   21753055690501399470640, 24076667025676329829169, 26488695352943006553931
 80-82   28969275390068093563757, 31495648868427401884640, 34042437933482581251708
 83-85   36582010259525364435603, 39084930586809796359221, 41520489903625708114308
 86-88   43857300161822902747817, 46063939387425191873115, 48109629480442719095428
 89-91   49964927022980986289136, 51602406146309790550115, 52997312026165671405779
 92-94   54128163930770556819884, 54977287944826385320449, 55531261506282624494121
 95-97   55781254648582756534294, 55723256234822998121412, 55358177361246285627480
 98-100  54691828334636223542822, 53734770009022407341302, 52502044615832627421986
101-103  51012795349588550473595, 49289787705326922258900, 47358848746410889173412
104-106  45248242986444411972484, 42988005299950491140599, 40609252178728631856052
107-109  38143492705319828883401, 35621959846666809865983, 33074981138121429088458
110-112  30531405626053626765782, 28018101185639993597288, 25559533172385506764840
113-115  23177431953726528045375, 20890553360677132525207, 18714532651503439683133
116-118  16661829334375908839066, 14741757277198580124599, 12960592043652129391017
119-121  11321745408449149350522, 9825995569474759796204, 8471760705680840210380
122-124  7255403217878386593426, 6171552197960912306066, 5213432344634246490024
125-127  4373188605747409770745, 3642197194770850089571, 3011355209927258334113
128-130  2471342787979218555468, 2012853462105880548434, 1626790085615317029025
131-133  1304425261308147870756, 1037526625841842363860, 818448538825182041988
134-137  640192693195831439183, 496440885899838067740, 381563669338066000246, 290608858367098733458
138-141  219273918514745891922, 163866138072500713164, 121254224026060834755, 88814594630698186900
142-145  64375204975379583616, 46159268484693755113, 32730755953267554339, 22943088346385068600
146-149  15892009224113323570, 10873240656617045919, 7345201361404801260, 4896801152026706686
150-153  3220121465708991486, 2087644263060027340, 1333595273204547666, 838915103867669435
154-157  519355178493482345, 316206658259017313, 189201766082663932, 111171299381101447
158-161  64093698680016836, 36225040187342709, 20052124786802197, 10859891454563583
162-166  5748108479344588, 2969895541524274, 1495938807341620, 733559086653894, 349658533837783
167-171  161741185474566, 72473201755736, 31394389928253, 13118869247798, 5275518964505
172-177  2036113064489, 752007294730, 264907047849, 88677157299, 28091230126, 8381552919
178-188  2342835360, 609734040, 146694416, 32351908, 6475313, 1161878, 184127, 25256, 2926, 274, 20
189-189  1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{33}\Phi_{2}(x)^{15}\Phi_{3}(x)^{8}\Phi_{4}(x)^{7}\\&\times \Phi_{5}(x)^{5}\Phi_{6}(x)^{3}\Phi_{7}(x)^{3}\Phi_{8}(x)^{3}\\&\times \Phi_{9}(x)\Phi_{10}(x)\Phi_{11}(x)\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\Phi_{16}(x)\\&\times \Phi_{17}(x)\end{aligned}$$


### R18 — k=18 leaves

Order 240; period 12252240; source v31/ROOTED_MODELS.json, record 17.

$$B=2^{n+315},\quad a(n)=0\ (n<19).$$

$$a(n)=\left\lfloor\frac{B^{n-19}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 19).$$

$$R(x)=\sum_{j=0}^{220} c_jx^j.$$

```text
  0-10   1, 14, 182, 1845, 15677, 114482, 736299, 4237709, 22123575, 105862231, 468344523
 11-16   1929477523, 7447500014, 27073091415, 93107476598, 304135455871, 946896586106
 17-21   2818649986614, 8044394929797, 22067379598437, 58318055435572, 148782448907844
 22-26   367131319266625, 877746901904030, 2036538582915714, 4592356405295100, 10078472333961024
 27-30   21553798364068778, 44971576893101086, 91646911635249968, 182604464717240591
 31-34   356072306885936924, 680128743974184759, 1273616654299205465, 2340060982042618574
 35-38   4221648209122316376, 7483588163627771804, 13043665536821959411, 22367838966980454758
 39-42   37760743043681754921, 62790310616696034382, 102898890240001568963, 166269600984337763468
 43-46   265036600526717411841, 416951688601338034619, 647647297919436099710, 993667263371837263907
 47-49   1506471304938953368865, 2257656001052280080893, 3345672772013223307333
 50-52   4904360095000389720628, 7113640294636608690016, 10212757652331111533285
 53-55   14516450523055058832788, 20434451403566234279964, 28494690838396023426444
 56-58   39370538870619081210399, 53912346686753529215910, 73183446791835337639527
 59-61   98500628826646533480808, 131478927496445162822774, 174080338052475709688664
 62-64   228665814378832019162253, 298049608352014365607118, 385554682828888180668030
 65-67   495067583330519208977419, 631090797208494702435552, 798790278691775909421865
 68-70   1004035491329500388897812, 1253429035769785520278511, 1554322711975200119606242
 71-73   1914816732950083751778365, 2343738783650852131680402, 2850599724162810717114040
 74-76   3445522987900096170889955, 4139145136692603691346364, 4942485612959948725641339
 77-79   5866784475735426352979029, 6923307815537672473993959, 8123121597892852867989243
 80-82   9476835862964082746844779, 10994322476626733281231663, 12684410945782364753808364
 83-85   14554568129648816846973340, 16610568945593240294613813, 18856166325140966765444466
 86-88   21292769664230606819494798, 23919141773627581751558960, 26731124816991422928682359
 89-91   29721405878354513667273731, 32879332590713230210951816, 36190788658007283023398505
 92-94   39638138103776705194525478, 43200245686761452803205788, 46852579159671022729075381
 95-97   50567396952167590960755775, 54314022489769851005131815, 58059203788596546365828905
 98-100  61767554276742751176604662, 65402068081064856630830449, 68924700384426786350956029
101-103  72297001005667697146064453, 75480787183491903562956228, 78438839749375669589816777
104-106  81135605535918834998744338, 83537888052281023352983269, 85615508215688253096939276
107-109  87341917283521268014991442, 88694745087659218239088010, 89656268210300241106822903
110-112  90213784814262925353717977, 90359885383768194547394295, 90092611558013314378724226
113-115  89415498446685221229359055, 88337499189967203027414159, 86872793943772414379518739
116-118  85040488810919413685866801, 82864213380350267406084800, 80371628368063310991270818
119-121  77593857276332823283670441, 74564857921073945883009691, 71320751059594781773661623
122-124  67899124144558329163806228, 64338328419976002202249842, 60676787171338694637807889
125-127  56952331976657896418722890, 53201582331939215158377460, 49459382114484575800199091
128-130  45758304086496361130574469, 42128231125404113046145328, 38596020198202631917663416
131-133  35185252377547297277235253, 31916069527462199308109498, 28805095758542529916794653
134-136  25865439448509117653509532, 23106769611793419313196885, 20535458734181735164471200
137-139  18154782900691598991008689, 15965169155158397702822726, 13964479539482446411862040
140-142  12148321154766098360000288, 10510371836936518652239237, 9042711605873004378191936
143-145  7736150880156544337538141, 6580547494125298428656664, 5565105751205514285885332
146-148  4678652038595838425621820, 3909882856304212493877419, 3247582425893887550393160
149-151  2680808294703485088400068, 2199044501161120104002021, 1792322885759223035899381
152-154  1451313998936985906949218, 1167389758762487151961104, 932660543568482253066166
155-157  739989770557014950585607, 582989220348134320666354, 455998434052747468300547
158-160  354051452167430746484940, 272834004281156056628227, 208634017388314597088948
161-163  158288010616055164279995, 119125606580594840330073, 88914033724187066246212
164-166  65804136840953400536910, 48279068726178087519045, 35106515675105208398568
167-169  25295021564558466247320, 18054724778024480173820, 12762611943369291152550
170-172  8932222752985934410235, 6187609550431781783623, 4241260987307694480875
173-175  2875636933472940382146, 1927927399866480471291, 1277636657331344081215
176-179  836600186995336977098, 541062007971124354483, 345469162091459211289, 217675097259058718242
180-183  135281390812619558604, 82885313518588481690, 50037367331969125876, 29746885684514177844
184-187  17404282905188806054, 10015185183249794681, 5664381697232142773, 3146439472057613115
188-191  1715223362781075334, 916840776659598458, 480121071899768582, 246078993634596373
192-195  123315412722823070, 60352729258346476, 28813288063738155, 13401162434670571
196-200  6063680258580952, 2665092682781107, 1135925754824689, 468665225980716, 186805655186131
201-206  71777307172174, 26522477224882, 9399865675420, 3185925280199, 1029287686937, 315818737951
207-214  91654393866, 25041683538, 6407159928, 1525866279, 335846162, 67754335, 12404350, 2036388
215-220  295187, 37089, 3925, 339, 22, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{35}\Phi_{2}(x)^{17}\Phi_{3}(x)^{11}\Phi_{4}(x)^{7}\\&\times \Phi_{5}(x)^{5}\Phi_{6}(x)^{5}\Phi_{7}(x)^{3}\Phi_{8}(x)^{3}\\&\times \Phi_{9}(x)^{3}\Phi_{10}(x)\Phi_{11}(x)\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\Phi_{16}(x)\\&\times \Phi_{17}(x)\Phi_{18}(x)\end{aligned}$$


### R19 — k=19 leaves

Order 260; period 232792560; source v31/ROOTED_MODELS.json, record 18.

$$B=2^{n+339},\quad a(n)=0\ (n<20).$$

$$a(n)=\left\lfloor\frac{B^{n-20}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 20).$$

$$R(x)=\sum_{j=0}^{239} c_jx^j.$$

```text
  0-10   1, 14, 191, 2010, 17705, 134064, 893464, 5327104, 28799378, 142662511, 653193399
 11-16   2784213557, 11115788274, 41784973510, 148561588735, 501554369528, 1613513192092
 17-21   4961589087089, 14624245709489, 41421149271872, 112994285534348, 297493885426991
 22-26   757376203466803, 1867732876728599, 4468742122454280, 10388868489442213, 23499646350905011
 27-30   51786877498493262, 111316693644533480, 233649660525457972, 479385417921516734
 31-34   962367635108720836, 1892034645211789336, 3646029972656400966, 6892288092283479980
 35-38   12790488474971437925, 23318517178102820095, 41792359745645672925, 73680213408162906386
 39-42   127856752540396373760, 218505345721955315502, 367959321478244124082, 610883606981016626592
 43-45   1000341424791513933428, 1616473990173207642710, 2578751364499275886703
 46-48   4063036755314859762091, 6325050951655877788179, 9732233276577380281789
 49-51   14806473313730781215861, 22280733488266495581721, 33173191913467817354334
 52-54   48883197953595310070045, 71314033379338886896326, 103028185882055340383388
 55-57   147441536622691608931540, 209063497827990948107939, 293790659224717978271293
 58-60   409261853234150993646925, 565282660045958062648234, 774327170119605231539657
 61-63   1052124224374893299326005, 1418334281569304490680060, 1897321441635627915010038
 64-66   2519022914764206548405045, 3319915314121209728607567, 4344073530314630790579719
 67-69   5644313608838710465879040, 7283406020357750318156046, 9335340047743817317072694
 70-72   11886613815136072839805293, 15037517900003227035049451, 18903373693104457120376427
 73-75   23615680943282671524313039, 29323122527191225069328620, 36192368738529440579320130
 76-78   44408618645951543436899206, 54175812689353460681650903, 65716449039589663196822900
 79-81   79270936692108180941200248, 95096421124137787393887096, 113465023890350262764139399
 82-84   134661445965174389180385973, 158979896073221866021353450, 186720319687944225441865919
 85-87   218183921706652806980561351, 253667995779764218685298818, 293460095498335354083903396
 88-90   337831606604073172676945531, 387030804426105276578661487, 441275506096866984978190222
 91-93   500745451884677616562012727, 565574573259884047262645208, 635843326101060694931193366
 94-96   711571284760526960854208522, 792710205593779762024054944, 879137776144297567396129346
 97-99   970652267714086220640072095, 1066968303954883085241417990, 1167713945998087821966941897
100-102  1272429275347531362468164172, 1380566629386543029372134794, 1491492611267039726453221416
103-105  1604491956793303670037528698, 1718773296591909813719724135, 1833476803522319223879990574
106-108  1947683664295740985068574413, 2060427262171619189967901655, 2170705906053030245983689405
109-111  2277496892029110491925408838, 2379771638139385065594189858, 2476511593518948672284768967
112-114  2566724590649062700589225696, 2649461285510990632009702280, 2723831316093149684019926598
115-117  2789018805699088092077548897, 2844296844270447555045234944, 2889040598530398131886729126
118-120  2922738729846398618626760640, 2945002836608902053057365347, 2955574684573156423033334629
121-123  2954331042641956160038444256, 2941286001333669629721852478, 2916590714823815832740894978
124-126  2880530572967446506362948906, 2833519875030185316766290974, 2776094139912503245333029713
127-129  2708900246463012639940227692, 2632684650219420041647684962, 2548279967991850543486461202
130-132  2456590257797204497442081649, 2358575347776906616654705779, 2255234583256040748911371413
133-135  2147590365777501989310633259, 2036671851897272057581555761, 1923499163247004885973711891
136-138  1809068433686032991366489147, 1694337985400710517196436105, 1580215884934704637453010622
139-141  1467549083905019064192161312, 1357114299252921775902454138, 1249610736028271784406012748
142-144  1145654703630229168241650424, 1045776125771381922296264116, 950416896708074751683078595
145-147  859930992816630950486399705, 774586210501255300782435026, 694567369551630956333873727
148-150  619980796016166450090997168, 550859880736441802686006951, 487171498948560410277637279
151-153  428823072595104061678973479, 375670059778756012075425891, 327523664503021520534447533
154-156  284158573709193381742316424, 245320546739655876023374997, 210733703772643337294732244
157-159  180107383490228263486255343, 153142465278419125885462197, 129537076681490114431484309
160-162  108991631786134227201070127, 91213169941800053932209777, 75918986100584748848062831
163-165  62839563585435094754635172, 51720836909883108347208725, 42325826153948508572053458
166-168  34435695257729044900759121, 27850294454164153215630741, 22388252057327393992832368
169-171  17886683170516231132253322, 14200582864809093750551687, 11201969336471950506163607
172-174  8778838841718598968157525, 6833989201034687889262701, 5283762727849547455288083
175-177  4056752913324295266541215, 3092512405345914794400859, 2340293031536100461641599
178-180  1757842065203373475112741, 1310272804943224211945305, 969021971444440576646065
181-183  710901512421365826376358, 517248200565835157886249, 373170925578709991295506
184-186  266892804490929557514390, 189183124693491624533302, 132872632939250182503484
187-189  92444720029999769438004, 63694546799205636354273, 43448031791788089879878
190-192  29332795783379167835417, 19593558755114627142814, 12945043965516347792643
193-195  8456102678539859093658, 5459482567483170063866, 3482382935133810318428
196-198  2193639927619479329508, 1364042551269883022211, 836880663866789805126
199-202  506360671175517571155, 301990041215300170141, 177428573706911602000, 102636172530711823525
203-206  58419167384375362884, 32696668427711615924, 17982154888842144082, 9710620397409886707
207-210  5144870094769639136, 2672117033640055994, 1359238282153931014, 676506059914393923
211-214  329101074470323513, 156307347135835674, 72392691555836716, 32651693716602872
215-219  14321738462207421, 6099521294340874, 2518129754252956, 1005887515177860, 388009456076030
220-224  144213448927003, 51522128232120, 17646236133194, 5776994824701, 1801860938475
225-231  533483013704, 149318823811, 39326446255, 9694680507, 2223418250, 471071974, 91438532
232-239  16101312, 2541141, 354142, 42727, 4353, 359, 23, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{37}\Phi_{2}(x)^{17}\Phi_{3}(x)^{11}\Phi_{4}(x)^{7}\\&\times \Phi_{5}(x)^{5}\Phi_{6}(x)^{5}\Phi_{7}(x)^{3}\Phi_{8}(x)^{3}\\&\times \Phi_{9}(x)^{3}\Phi_{10}(x)\Phi_{11}(x)\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\Phi_{16}(x)\\&\times \Phi_{17}(x)\Phi_{18}(x)\Phi_{19}(x)\end{aligned}$$


### R20 — k=20 leaves

Order 290; period 232792560; source v31/ROOTED_MODELS.json, record 19.

$$B=2^{n+376},\quad a(n)=0\ (n<21).$$

$$a(n)=\left\lfloor\frac{B^{n-21}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 21).$$

$$R(x)=\sum_{j=0}^{268} c_jx^j.$$

```text
  0-10   1, 14, 202, 2198, 20159, 158664, 1100285, 6826596, 38422463, 198209421, 945417580
 11-16   4199381273, 17476702897, 68501614867, 254020191447, 894687093229, 3003443744597
 17-21   9639501854722, 29660461578126, 87714502662956, 249870681930159, 687071119716798
 22-25   1827032258922397, 4706492812920119, 11763719578204280, 28570965812426787
 26-29   67519352550248297, 155454318834365985, 349107146314305907, 765547456799048283
 30-33   1640921658117076290, 3441299801078438231, 7067515817866762310, 14226158031841306198
 34-37   28088603737643238017, 54440158239596067974, 103648202935787065637, 193975394069803959665
 38-40   357065068871220275210, 646878271600167653496, 1154030052066344112460
 41-43   2028444459382129695700, 3514639054449556906446, 6005911999846290002169
 44-46   10126431258390325755043, 16853958977255583301285, 27700983993296124326397
 47-49   44978743117486578490948, 72177415449045256672131, 114507169000704399430287
 50-52   179659285651062765859938, 278864905258849392402001, 428351669947491131309989
 53-55   651326389313761577163988, 980645444671775585381595, 1462374602868730873342535
 56-58   2160486699580564650371882, 3162999577290526494395215, 4589917763551649722459196
 59-61   6603409342503564529446628, 9420723559186704786694212, 13330433617167098503595950
 62-64   18712670970771390371618220, 26064099541491326825088034, 36028457284756647519068068
 65-67   49433564141678062230542780, 67335754522711939069803167, 91072733147008829688179570
 68-70   122325868607224733010271718, 163192922115738072435466568, 216272151746472122052073213
 71-73   284758627156516115790139274, 372553428429199652194193111, 484386178010730719332759526
 74-76   625951060363260511817143040, 804056115011094289992432939, 1026785142165220016450415721
 77-79   1303671035606458035331506256, 1645878757538993918141800651, 2066395500715342335295153065
 80-82   2580224854207593853943297773, 3204581014866316503582350439, 3959078285263647061839590600
 83-85   4865910293616358667125535891, 5950012588904975050114174914, 7239201536004984216364346093
 86-88   8764281795201316113951418126, 10559114154349984399306487478, 12660635127859325715740037503
 89-90   15108819582198909365746830117, 17946577728960300963090488518
 91-92   21219578176580553643568689153, 24975989378916049061464131640
 93-94   29266132784526950812998991084, 34142042288222018603399327129
 95-96   39656926219657422124896313956, 45864530065013662957039807963
 97-98   52818400387085499881508980352, 60571052953719590926719351359
 99-100  69173050858284096019203741220, 78672001359673649847197685001
101-102  89111483211752728433758730450, 100529919310750451766488906071
103-104  112959412472300107018102424276, 126424564959308114944895948677
105-106  140941304915352275831112528447, 156515745013112422265836077698
107-108  173143100303516216101368872632, 190806693355872918730888309305
109-110  209477075229725611008588782996, 229111290547481221852271063927
111-112  249652313892715766809913901579, 271028682913178785484233206036
113-114  293154350853932841984745880593, 315928777804272343782895254709
115-116  339237275757618611266129204578, 362951617728697206441136645364
117-118  386930915744459077822237248675, 411022766645909174722201270210
119-120  435064658449387799413300861528, 458885623677585850312525791546
121-122  482308119754747741372447938666, 505150110447090641525759867879
123-124  527227316599943280841383255549, 548355599255221247507371600717
125-126  568353433793801715327390433323, 587044430188584782587130226714
127-128  604259851904909882333203510016, 619841084548641218592049371313
129-130  633642005110514726646280876334, 645531203626483138667626910851
131-132  655394011269501540512668587745, 663134292273600616003845624001
133-134  668675961594357947668856134414, 671964195724753849482632593967
135-136  672966310473332067312345798428, 671672286606702152636106667832
137-138  668094931871767740214345785037, 662269675839460248615987706657
139-140  654254002035464902022322760258, 644126529725997634237012556048
141-142  631985765293133619185741526858, 617948550160776131899985446624
143-144  602148238532257530992353253501, 584732643610618053110726121547
145-146  565861795357459177673811205193, 545705556103255189144183104381
147-148  524441142383125686877281606438, 502250602206424454277951396330
149-150  479318296581732824550885144703, 455828432553003563520990072540
151-152  431962692333096675467818835854, 407897999454060216535123448828
153-154  383804458321311479657205501286, 359843498314965853213885846883
155-156  336166247794682020823341242127, 312912157213201579970944536726
157-158  290207884210029497949820887529, 268166447220048735360955933978
159-160  246886647963430454972497318064, 226452757341199621810115586181
161-162  206934453885446620727744988777, 188386999123641019542736013784
163-164  170851630107711573383366194322, 154356145999965273330485938150
165-166  138915663042238892413887058492, 124533510478612442174235996975
167-168  111202239046862699857058556110, 98904713467880773507457656741
169-170  87615260892926121564442031200, 77300848445943827879444155108
171-172  67922264738150522829028512505, 59435282440591563275410617155
173-174  51791781576733731010348382136, 44940816038309212669172861985
175-176  38829608831314524191051409223, 33404464627419679360070546305
177-178  28611591238105079957786192849, 24397824563194581247950596439
179-180  20711254321749541017110145969, 17501750393745565613761552150
181-182  14721391840810512143704559646, 12324802602182870087825462052
183-185  10269399459439767767619190845, 8515559124206421903564207078, 7026712231754665632489647087
186-188  5769372634639269921319053148, 4713110706842425857932403532, 3830479419277331334500133209
189-191  3096901765507332950025194020, 2490527738719493883464542485, 1992068525185870251099468177
192-194  1584614923396511635649511148, 1253446258059510989449447807, 985835268112454052327172051
195-197  770853638335885131888994230, 599182041806617977968908290, 462927787705530769705374933
198-200  355452443941486955839837027, 271211140312684209240758580, 205604664969879602000401694
201-203  154844950361368377461172686, 115834106781330071416821887, 86056801292149397161721995
204-206  63485493899727308216597799, 46497826265637025132141926, 33805304397828143260097035
207-209  24392318219502909797607211, 17464489760545903904675560, 12405329941887786378942668
210-212  8740203755571210347322247, 6106647777574056056145484, 4230145741155602788132268
213-215  2904541474177317668441138, 1976348837255931610121754, 1332301221372668653234686
216-218  889565344052382556446120, 588122977572716551320037, 384898018866210670681210
219-221  249273759273964898789566, 159705651856481356199229, 101188053311100697991871
222-224  63379422954952927610579, 39229629158235263846882, 23985854476401206738651
225-227  14480722430880359123957, 8628362901029149507794, 5071871151491569377595
228-230  2939657662425905279773, 1679147605060100973697, 944726658697802154679
231-234  523234017497481354431, 285095361158127005824, 152722786928464366296, 80377408174801267138
235-238  41529606421196857277, 21048974840678876264, 10456480753479455053, 5086605008336219403
239-242  2420675518063155335, 1125792751696057694, 511100954899048939, 226233370379525580
243-246  97508383506593718, 40864837542248897, 16627067640407791, 6557184738582680
247-251  2501889183821198, 921738530961786, 327185531458762, 111632633225972, 36513713898109
252-257  11416236496927, 3400823220069, 961759026234, 257158582973, 64712757842, 15245897545
258-268  3342536769, 677189879, 125746704, 21189515, 3202345, 427374, 49471, 4820, 385, 23, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{39}\Phi_{2}(x)^{19}\Phi_{3}(x)^{10}\Phi_{4}(x)^{9}\\&\times \Phi_{5}(x)^{7}\Phi_{6}(x)^{5}\Phi_{7}(x)^{3}\Phi_{8}(x)^{3}\\&\times \Phi_{9}(x)^{3}\Phi_{10}(x)^{3}\Phi_{11}(x)\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\Phi_{16}(x)\\&\times \Phi_{17}(x)\Phi_{18}(x)\Phi_{19}(x)\Phi_{20}(x)\end{aligned}$$


### R21 — k=21 leaves

Order 322; period 232792560; source v31/ROOTED_MODELS.json, record 20.

$$B=2^{n+418},\quad a(n)=0\ (n<22).$$

$$a(n)=\left\lfloor\frac{B^{n-22}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 22).$$

$$R(x)=\sum_{j=0}^{299} c_jx^j.$$

```text
  0-10   1, 17, 260, 3113, 31157, 268007, 2027556, 13716572, 84089878, 472112550, 2448598942
 11-16   11816515751, 53383703054, 226955602870, 912111153925, 3478915392719, 12636920508406
 17-21   43851405404737, 145771599618649, 465363057305858, 1429948809946047, 4237897079666168
 22-25   12136590546910728, 33643980157279917, 90421430396833455, 235952945175384165
 26-29   598631534754404929, 1478503640190676760, 3558973899180519444, 8358799829423153787
 30-33   19174593937997900615, 43002134304758047086, 94368783687209442934, 202819986452450659002
 34-36   427253110275598713815, 882836055139534362844, 1790627355638813260390
 37-39   3567416085134330838370, 6985590340935446203527, 13452905674741130482719
 40-42   25494236609498310897575, 47568289081302107564765, 87431422912642327647728
 43-45   158382042732815005033015, 282902177238079384053050, 498485486752412683651668
 46-48   866841090179523223628251, 1488242005291825372693867, 2523614871041709565921936
 49-51   4228135243180133364859361, 7001718715531185930889573, 11464034228181552341846678
 52-54   18564703629117142591843155, 29743428661551488403299798, 47160193898734339789484688
 55-57   74022781820858066838227835, 115048018658719592598596544, 177104928908704563812171191
 58-60   270102862918370649249890809, 408206291205113461987403055, 611481004056383232529082952
 61-63   908104631759573841648623194, 1337308448236927029025806164, 1953258070781460461114957445
 64-66   2830128607546869064957766020, 4068685625289079859985752429, 5804747453179097638204402734
 67-69   8219977024039837640389631111, 11555532603166834383882937968, 16129195903846739128294083052
 70-71   22356692299594027202878672089, 30778019609711740478452556162
 72-73   42089707091699837149863891849, 57184031912929795905671953326
 74-75   77196322772528276447207795357, 103561574914759699084910524162
 76-77   138081682039257152445156556715, 183004652211879885016246954300
 78-79   241117209622423119672449461748, 315852183998589588174857772722
 80-81   411412046165070864598409504728, 532909852756321971385279643251
 82-83   686528706474407795894708288176, 879700611781336189341531004760
 84-85   1121305301398644630247718650062, 1421889219383866429617467472101
 86-87   1793904366332759564581712471750, 2251966137939225841100380367728
 88-89   2813128618829980016014337654254, 3497175031470303614949345577395
 90-91   4326920190782716349924914347762, 5328520888714280248124618348680
 92-93   6531789143469597759805863599352, 7970502214227124929663578763808
 94-95   9682702227298272119257579295869, 11710977211918444913039425211953
 96-97   14102714335596499562343038388131, 16910315196533196166242400286883
 98-99   20191362213641030978390743468564, 24008724495114861028481068530737
100-101  28430591107541715683810200059073, 33530419452399230443157612360397
102-103  39386786527179310370036652261809, 46083131242885996594247302155836
104-105  53707376722084322842884675957414, 62351422639256040576090368474249
106-107  72110499206904195963118976140082, 83082376365678518930147416658083
108-109  95366424102405485171526489012954, 109062522581291149976505642829470
110-111  124269823902118455507493472751857, 141085370752210778925765884249830
112-113  159602580939189590532725551830645, 179909610708036978752256516534712
114-115  202087613774455447540152548885982, 226208917050989240788099701681037
116-117  252335137996940793965878202652319, 280515272274408284620200199387142
118-119  310783783822796580899552931428787, 343158732453578074442253345559917
120-121  377639976498804496845481873820823, 414207489809837808344748579865143
122-123  452819833395858438249744688424732, 493412822127609348677622734056377
124-125  535898426140735763165971039828765, 580163944806065827581336706889303
126-127  626071488366160659702365352282455, 673457798569545995667603912967363
128-129  722134434895175182936128718436313, 771888347307531594254639372797304
130-131  822482850003729756246117563687349, 873659003422164917247144976884077
132-133  925137404017742317208698188825991, 976620373134654636676717691283424
134-135  1027794527906680788482401139241156, 1078333708684653406017956052959811
136-137  1127902229238547364796143273211367, 1176158408119234869386846890090196
138-139  1222758332302163696591835724526673, 1267359797773846983198341978172229
140-141  1309626366249711157921754898063533, 1349231472896004132768287728543574
142-143  1385862516910957954072014657641513, 1419224865212573306915232396902691
144-145  1449045699359049662527955409867029, 1475077637232203672224668306884828
146-147  1497102063943770216622930533358994, 1514932110838422032772201844946501
148-149  1528415227284845558095909462658010, 1537435297048121402313930079168427
150-151  1541914259268373643553781792475431, 1541813203246107554996854803781956
152-153  1537132916141322969501234544301514, 1527913873098230383920810275096530
154-155  1514235669962974776052322751888943, 1496215909413833335430100569122845
156-157  1474008561717630544848236972045110, 1447801831215630739256157898035110
158-159  1417815568794207152177356217309852, 1384298278798194209294998775022904
160-161  1347523775912652226000751007116781, 1307787553318033590509054918826199
162-163  1265402927796207250617166913606827, 1220697030350633498126215108446465
164-165  1174006712263371885868301827411077, 1125674436345166823271102899133192
166-167  1076044221482798741514576138403268, 1025457705528005850455809546777918
168-169  974250387216841684602328409265220, 922748102300011044535822093118610
170-171  871263782571718970382200726576079, 820094539195079813809994777824614
172-173  769519103838431589837412086312531, 719795652869129145986702857760935
174-175  671160031411370277756956934063320, 623824385669816228259572808121193
176-177  577976203748671574784668318102892, 533777757438829176145822110976208
178-179  491365930266432017589302073112543, 450852410634299973260651887977769
180-181  412324223256662344044908370227283, 375844567373225304502561500708594
182-183  341453926487729188331921515446771, 309171411637011258689415632009954
184-185  278996298459523864902597758358072, 250909717571426841606445990215210
186-187  224876457924139109112339974002145, 200846843839117481227726256808485
188-189  178758648205711427553580683070103, 158539006784573136086690090889625
190-191  140106301570784004688927750594953, 123371984620147783859725912349931
192-193  108242317509413039139764563192587, 94620005568385081395407652878812
194-195  82405710075543267930806900626298, 71499425643040086580188364082590
196-197  61801713935939029865193051905044, 53214788590219730751013204787557
198-199  45643449643625235761680112446372, 38995868916072578103997482705383
200-201  33184230529676203744421008972218, 28125233114222851966515547868420
202-203  23740462187572126493946157607124, 19956642729974213123069321969081
204-205  16705783096119260998669611244785, 13925222148185035498579678212433
206-207  11557591874805516757902839338062, 9550707818836864486102151578792
208-209  7857399409910300398833880477160, 6435291827956005385229258256577
210-211  5246550354529713135717715713737, 4257597343225558832484671453523
212-213  3438811000751311435690110316199, 2764214156001740962857258136451
214-215  2211160142027430927127217863776, 1760021857539964078446943348945
216-217  1393889038496692632255756723185, 1098277779696536597831125968978
218-219  860855419810298468916157244532, 671183054876505932196111242137
220-221  520477184663538027667576071431, 401391329064410767914123093369
222-223  307817879907354844602503034003, 234709976200250732440131372576
224-225  177922804279108453874899342921, 134073422958036604518971390761
226-227  100417990411138667728743460780, 74745115942502059726437004692
228-229  55283967203108664067054332994, 40625722762918754934335335999
230-231  29656962328198117627013260453, 21503623779044582167883437888
232-234  15484219654201748578843868023, 11071088537510647677669180790, 7858552650773300955953295862
235-237  5536956368049483952119289546, 3871666769148433460934927289, 2686223047489169974132368791
238-240  1848923698299087070708450341, 1262236800198004350851036797, 854507888555404484406683858
241-243  573520991709048551048840978, 381540923633631735414847158, 251528843287969382391060329
244-246  164278641995117725063152910, 106269364153083839876304754, 68069211001422238582938238
247-249  43160420577515477914384122, 27082200508311707166545628, 16811659407364804509985201
250-252  10321058292247386797745818, 6264361210445886813007665, 3757620923463300826883678
253-255  2226741387987490439274149, 1303095017188424291506960, 752752099484837201421812
256-258  429050295394792466543680, 241182341863195085377821, 133645357122382615435481
259-261  72964526275969274564378, 39227012548561520088488, 20755202269888077549966
262-264  10801280811741962928896, 5525261165607400340072, 2776294320619424428437
265-267  1369307405465091363310, 662410133917670991264, 314043481273072652942
268-271  145784771144959890185, 66205063872840068081, 29382989769000670313, 12731065979904629578
272-275  5379006033959536694, 2213476820466476422, 885950897602380142, 344418514506516937
276-279  129847992126583806, 47394629050210092, 16717761598427321, 5687496082094817
280-284  1862158709594686, 585372639821290, 176210552690256, 50647663396256, 13855462734679
285-291  3594691695371, 880919408551, 202989240405, 43754965702, 8770388488, 1623492002, 275289381
292-299  42346449, 5839359, 711224, 75040, 6688, 483, 27, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{41}\Phi_{2}(x)^{19}\Phi_{3}(x)^{13}\Phi_{4}(x)^{9}\\&\times \Phi_{5}(x)^{7}\Phi_{6}(x)^{5}\Phi_{7}(x)^{5}\Phi_{8}(x)^{3}\\&\times \Phi_{9}(x)^{3}\Phi_{10}(x)^{3}\Phi_{11}(x)\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\Phi_{16}(x)\\&\times \Phi_{17}(x)\Phi_{18}(x)\Phi_{19}(x)\Phi_{20}(x)\\&\times \Phi_{21}(x)\end{aligned}$$


### R22 — k=22 leaves

Order 356; period 232792560; source v31/ROOTED_MODELS.json, record 21.

$$B=2^{n+461},\quad a(n)=0\ (n<23).$$

$$a(n)=\left\lfloor\frac{B^{n-23}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 23).$$

$$R(x)=\sum_{j=0}^{332} c_jx^j.$$

```text
  0-10   1, 19, 307, 3918, 41760, 382143, 3073059, 22080303, 143657020, 855331527, 4701243440
 11-16   24027452366, 114890068195, 516673311324, 2195239746513, 8847188526755, 33939626534013
 17-21   124319323757873, 436022534735094, 1467932486180110, 4754610852542255, 14846755366574630
 22-25   44779013244981586, 130675779727254710, 369560174936150194, 1014341198576104057
 26-29   2705729898087673970, 7023234205023288836, 17760513671588483649, 43804527903383157865
 30-32   105481512595952664539, 248226638059011530220, 571387128718719554866
 33-35   1287640270084463519214, 2843094123527566513047, 6155329856047814404820
 36-38   13076376572172805954606, 27276913105645336362877, 55905535465393210637616
 39-41   112650139544495604881608, 223294486051845428077519, 435645268491576015124249
 42-44   836997876121657137994058, 1584413950639602336489717, 2956461196946196941138356
 45-47   5440408788950084283324020, 9877208573574812697913574, 17699428148600052079870343
 48-50   31316809361059341014319954, 54733399483538334701148575, 94523592942388831300726872
 51-53   161357967301461202825906994, 272361773438275835426952801, 454720546585621486687720632
 54-56   751133515252638885443772514, 1227976073211736068455459408, 1987393345900191827189749609
 57-59   3185041085192219886023622002, 5055860124255606963647255244, 7951169717283339183410583927
 60-61   12391559532664701078346832997, 19141631212157576444973651308
 62-63   29314686888227800452184870615, 44518101930970334629086701356
 64-65   67053491926803858527320949421, 100190051918161467347383516923
 66-67   148534795737133812703827460881, 218530065598339012314656130691
 68-69   319116851149627024085457670965, 462612408260549079501172016274
 70-71   665862673509418005563462402880, 951744314335486441559111682318
 72-73   1351108223631004771535374570101, 1905276139275712459528645024220
 74-75   2669225099463898150952174552699, 3715620849752095728198515106633
 76-77   5139891253727304385324987300430, 7066564298804011819691756851753
 78-79   9657132394869195741913821811159, 13119745160687452839575834625136
 80-81   17721076436331427804901559615137, 23800757303857057004014945531926
 82-83   31788814665384689053223874673989, 42226603378290509470162775906982
 84-85   55791767753715875712793308738338, 73327813749753801514151231144237
 86-87   95878914473170112346055499668857, 124730606352976445321321546119883
 88-89   161457058952444116937064239861760, 207975614927190494268451424040085
 90-91   266609294932268640598495733892659, 340157941932457724494364333613895
 92-93   431978636835447281139126705806726, 546075949052925729298150869990520
 94-95   687202487963076767948621716711606, 860970090950275190809999953674534
 96-97   1073971817718879032245856097118847, 1333914716399742973601768326931926
 98-99   1649763082743234284902388234076900, 2031891648426541680961327586262644
100-101  2492247808237548774297296946448927, 3044521629889446920055871811398602
102-103  3704321987109343287182703117487275, 4489356720600865094964152970972321
104-105  5419614268326434235894342504656309, 6517543723845187649802486218221568
106-107  7808229788506490422127388087807656, 9319558591225277440423135593554383
108-109  11082369871128916295005342274607175, 13130590567888106016716393694838429
110-111  15501344457687601580803709541443123, 18235032126276034858215319210878720
112-113  21375375301784386094532084185742497, 24969419396732526394481698102608826
114-115  29067488048367750148421180802922446, 33723083515976969395883338244988804
116-117  38992727008545425273677352103760578, 44935733389630012456040377904137486
118-119  51613915249552428955597715423467846, 59091212055805080527756749693380685
120-121  67433240994952323595496146417001940, 76706767203057041771056908687730494
122-123  86979092341762839387193235058438677, 98317361903479977922468488423193811
124-125  110787793206140002578215856909164173, 124454827744681587040317175619128152
126-127  139380213376327394436683755663558640, 155622023698067782119740525771250319
128-129  173233623890959058243793734685982388, 192262594215923069757051180241468870
130-131  212749624205159261674831155365408695, 234727392354815396165665306986325911
132-133  258219447739335825161868676079581328, 283239111386592432982611344432575110
134-135  309788416427021806046616071198638125, 337857106913272903232042748768755216
136-137  367421715756660405776183089599792599, 398444742405389702763524243694610198
138-139  430873950665819895909887039548892667, 464641806418359347107295210460637840
140-141  499665073889124297062475179107594127, 535844587602153771732908078771236886
142-143  573065215160160716970593904190260204, 611196023600874059406199680625123511
144-145  650090659278527490070273242905886978, 689587948064596457974824387639651461
146-147  729512719197764132294575136595945566, 769676852399541843768529502669578494
148-149  809880543977114524811625937889425771, 849913783634528571314206001789605374
150-151  889558029688951416564492880733164875, 928588066426194396781648726373620275
152-153  966774023516883275436067146734197664, 1003883533839394432573339105323879977
154-155  1039684002803447590021527539861623198, 1073944959419987014251268535825692506
156-157  1106440456992845077963750509556104237, 1136951489480950512424284644691900697
158-159  1165268388351027240175040934894172660, 1191193164151890760805138825262037785
160-161  1214541757120830438353578643914494480, 1235146161893559541700170685290558640
162-163  1252856392829709803664413300798973708, 1267542258567984532675720038449100457
164-165  1279094917155431207050206575390900550, 1287428186405441345917068201067678126
166-167  1292479587966653651546626894855002322, 1294211107854973585195331786474435626
168-169  1292609660827649487373078398143424727, 1287687250867207623944413110480552659
170-171  1279480825093016311496368415817878011, 1268051823524301065792687699409871481
172-173  1253485432174152875541849828583297730, 1235889551854287622295004954199133408
174-175  1215393499713698810911831776855216290, 1192146464825908295633815722420934325
176-177  1166315742992921339113616094314052320, 1138084779273612676544052035472649123
178-179  1107651049506974296383448874089552993, 1075223814237211315769369763955151093
180-181  1041021779923782325837720289940033320, 1005270703116403984131986017120654508
182-183  968200973389791557904332694674066333, 930045210278037293924018495377663932
184-185  891035908251492553203963803785055320, 851403161981168723554144562062584576
186-187  811372501790897240052588219120854479, 771162866370567691278017044969885707
188-189  730984736588459132123050763540907316, 691038450677661261143437602823962057
190-191  651512717266217103862793929264833646, 612583338760717400486757354814597729
192-193  574412153566644452858656278993052703, 537146201621828004753623818575935880
194-195  500917113813949815278141579567561667, 465840722125259566737972311368224739
196-197  432016883866194191035996245989613538, 399529510184232235302756908943130341
198-199  368446786214967372720422773742335608, 338821567818302714494168481800533354
200-201  310691937842023530040537708390149396, 284081903294782575585128041668121458
202-203  259002213696711735221441533795560626, 235451280203911830740631640236172290
204-205  213416174858625900528602945518148947, 192873689476774189701044726327962535
206-207  173791434217799890544541503266029266, 156128956751059570073606995526343715
208-209  139838864095801985549597519331344688, 124867930621923764354878104893115455
210-211  111158177307689627855040229676675439, 98647909109061250551687290472088179
212-213  87272699154179993767473503616771750, 76966310388463166751588806453212481
214-215  67661547215914978881683155859395386, 59291031569392367516644951521728529
216-217  51787899659772955644514762204746743, 45086417369185361561827642145807012
218-219  39122513839874519205422572941777990, 33834234246548642446898083673156331
220-221  29162114010366134568631794211173503, 25049477806651538207045595647683739
222-223  21442667630719677791832005783939173, 18291204916370352029822377548896878
224-225  15547892253558064914840958957295149, 13168860633103744956698333701308724
226-227  11113568367967423859281514165010357, 9344757916002422625594524321021592
228-229  7828376773688328356710060957456380, 6533468440869206984398812793078755
230-231  5432039190548398953658482829231119, 4498906033078389799872321475873140
232-233  3711530858134894726265343273240036, 3049845287489107472025353184053971
234-235  2496070292554602195701776588425040, 2034534137417362372394706932727663
236-237  1651491713446048843301575041740728, 1334947846824941741482863354137854
238-239  1074486694890147390870014987605361, 861108908636422871654201758694231
240-241  687077833109462424990814054391179, 545775648857255150576916066956619
242-243  431570028892150045427241746852131, 339691598025414484711684318242832
244-245  266122235063546689028514289113943, 207494052237481210668053450485349
246-247  160998718545395490957730185961663, 124306661919220833768281361138342
248-249  95495586260608038908283205247208, 72987670078437527353724513381269
250-251  55494770147998752001966697653710, 41970932690166436393404715773199
252-253  31571512474995817225454238017511, 23618213567159773310900334012688
254-255  17569390943316870128849678835661, 12994986984014150654409673598634
256-257  9555518238936527549563325353353, 6984573572244102071880477648578
258-259  5074332833407310449242983209694, 3663663913602012202653570523520
260-261  2628404095701419259027219564919, 1873477935283610970350524361841
262-263  1326547733165752100400880489573, 932933423459596710444343214404
264-265  651576054566249392630441275771, 451852804538601837433182830169
266-267  311081607706024782446143876232, 212580048385873746036903395996
268-269  144166356421831867800170224018, 97010335494668596645024138961
270-271  64759126141348013633680501669, 42877131496916981424735522077
272-273  28151503817733948447503543787, 18324590045865027394997623178
274-276  11822940001330816800738686898, 7559148869178858333869723593, 4788172739332692019006858317
277-279  3004034662603720354872255003, 1866217088127930509719710663, 1147678439883101406661527907
280-282  698477531989793489454214798, 420558461956396747346406447, 250439877467044094214741142
283-285  147447946793754295605733102, 85798597371203508201582600, 49325170086055250312996081
286-288  28005082282507404041435540, 15696742946501735986153079, 8681651323106487726955800
289-291  4736105647471332673433615, 2547197573488023573118728, 1349929641204060926273585
292-294  704596062299025001500618, 362001697898796831206087, 182965632076526643841271
295-297  90917934600684544569319, 44388206809060265981510, 21277642132277122617390
298-300  10006880430772970943982, 4613757061382083429388, 2083681568853674880091
301-304  920968587254063681166, 398002346651647315305, 168002679874706964514, 69193962057638776885
305-308  27774067958380694806, 10851526667280003684, 4121373886613313472, 1519383639155327963
309-312  542864249043467697, 187664211198844029, 62653231087098747, 20161010199218104
313-317  6239409733641252, 1852689593356277, 526444419520626, 142737409982258, 36810061143451
318-323  8996780316348, 2075676150149, 450007164210, 91207426103, 17179976580, 2986823972
324-332  475418893, 68613169, 8873068, 1012955, 100168, 8350, 567, 29, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{43}\Phi_{2}(x)^{21}\Phi_{3}(x)^{13}\Phi_{4}(x)^{9}\\&\times \Phi_{5}(x)^{7}\Phi_{6}(x)^{5}\Phi_{7}(x)^{5}\Phi_{8}(x)^{3}\\&\times \Phi_{9}(x)^{3}\Phi_{10}(x)^{3}\Phi_{11}(x)^{3}\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\Phi_{16}(x)\\&\times \Phi_{17}(x)\Phi_{18}(x)\Phi_{19}(x)\Phi_{20}(x)\\&\times \Phi_{21}(x)\Phi_{22}(x)\end{aligned}$$


### R23 — k=23 leaves

Order 378; period 5354228880; source v31/ROOTED_MODELS.json, record 22.

$$B=2^{n+486},\quad a(n)=0\ (n<24).$$

$$a(n)=\left\lfloor\frac{B^{n-24}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 24).$$

$$R(x)=\sum_{j=0}^{353} c_jx^j.$$

```text
  0-10   1, 18, 299, 3865, 41716, 386515, 3146485, 22883867, 150691106, 908053143, 5051170438
 11-16   26126564638, 126429822651, 575408648768, 2474225587528, 10091728378293, 39181223254334
 17-21   145254417394923, 515619802573473, 1756983229411256, 5760084655310348, 18205793384574915
 22-25   55581304392138310, 164186523873237682, 470032333607445381, 1305986287687147436
 26-29   3526651758394921190, 9267235695142465468, 23725454174660064605, 59242677660356840684
 30-32   144430546810716189161, 344118599040840763397, 802004763975583697937
 33-35   1829941150611629273068, 4091088818658060102241, 8968355403637727477999
 36-38   19291727886358945539675, 40748282548851001485971, 84568218718857457431479
 39-41   172556000555747404160718, 346361625223583276723298, 684298376124775895785017
 42-44   1331388342129898527900090, 2552254382064272590747766, 4822911665543438470650975
 45-47   8987881127444316010041507, 16525532246730061592413411, 29990427891238440211495608
 48-50   53741511126040879002249714, 95126273181835295092339236, 166383695795170692718055485
 51-53   287667166325816499975083954, 491792949681223422477187946, 831618257959769846508004117
 54-56   1391384043753826550333627295, 2303973677145135588355255913, 3776909852965681205241728864
 57-59   6131131570571165869412912578, 9858283096666738189147110254, 15704566188983679885271448510
 60-61   24792359370650032545457024445, 38795052686197950399575949935
 62-63   60186208652987285866404429468, 92591644784072127957355618340
 64-65   141282837906794406282009314295, 213862781124668391887119004314
 66-67   321211809202353688983575955070, 478781813898116683445189380086
 68-69   708353715909864190894482563756, 1040406227524521863223543179099
 70-71   1517285186080719529447037548373, 2197413597339317111676797743323
 72-73   3160844710717821054014336873041, 4516535833082709091047918051366
 74-75   6411811200119189368736922792581, 9044590206274584412497951170186
 76-77   12679084858883420499276763624258, 17665819691709577613859967796891
 78-79   24467000700107703343961772914786, 33688459127680695037029654820120
 80-81   46119622837699851989148329179304, 62783223807962758087009452889186
 82-83   84996735671865821700731298801816, 114447850098117808355760101327858
 84-85   153286644096724947858665151450301, 204237459822630239976779747951513
 86-87   270733910488430504600377220474130, 357080835346632171273063985117635
 88-89   468647446284302263625236286823378, 612096329287363429111308858214970
 90-91   795653374580473624785964825614148, 1029424096005541484120601716177208
 92-93   1325762147133241074022384429833167, 1699696130249890923981179813181222
 94-95   2169421003909806220948354043023069, 2756860502170287245250546730019779
 96-97   3488306958969156678864356657176708, 4395144757831718029906662591678730
 98-99   5514663272604460948194522484793867, 6890964601164073208432307863688154
100-101  8575970593314954940220312193177290, 10630532609838907412388897172294405
102-103  13125646097572880216029495611653793, 16143770404453180651734033690783259
104-105  19780252272173961619060061542313700, 24144849121724536269043771121204753
106-107  29363345584903038211183177906735488, 35579253737586503481221456314869154
108-109  42955584172251765129034033389023253, 51676671432844092100673212967775209
110-111  61950033461087784879530685247618704, 74008240618654586540068197557983631
112-113  88110765616121449160136030934073811, 104545781372377242723053057061603924
114-115  123631869535096833259054339981506387, 145719598214559890619283733251143087
116-117  171192923531385272368060024124126324, 200470365975631170126422574463351444
118-119  234005909450219411172635044457210685, 272289568361511626732786812304732763
120-121  315847566362651918330731598853140233, 365242069489079768901876897987807210
122-123  421070416584342417261292041278889065, 483963791223786835162037465730050300
124-125  554585281917304717691704590865499661, 633627281306724468311377988228487227
126-127  721808180444267165368961749788172350, 819868321095905132883415545987182585
128-129  928565177378275143050787155223418723, 1048667747897756473244994390595434443
130-131  1180950150867033817213961316675910585, 1326184427340952863048619415962434813
132-133  1485132571612559832590530313487986093, 1658537822773802393113427997155064306
134-135  1847115267264782847702292667463041366, 2051541818662877976880098418884950023
136-137  2272445657714120243725865937390915779, 2510395232366880514862215598003315970
138-139  2765887933987250692824164046014124197, 3039338581650096681496128399905039698
140-141  3331067861028559066510718653882307080, 3641290877560462061082808215065901999
142-143  3970105994867788941590533895444693362, 4317484138472193388662296852715924613
144-145  4683258751334330822130445826245586240, 5067116591328243798345793916436033888
146-147  5468589561166300935147701425453063875, 5887047758288382060949898609271371354
148-149  6321693925653847222937888714261253114, 6771559474126354308151403933771392437
150-151  7235502233193580917879697571623631021, 7712206069168841583431945663773645939
152-153  8200182488913887155800346074775380694, 8697774322719524822782121508085070975
154-155  9203161552583400914242734173733961250, 9714369322112455548418687719611228129
156-157  10229278132106195809475359779828414444, 10745636192068928265716758168709357776
158-159  11261073863036181979400818464422645336, 11773120091812457649392020064871316148
160-161  12279220701669338756149147166974777617, 12776758370431655498238368710267697750
162-163  13263074094378195784025118975853025715, 13735489906186795752639658036532745114
164-165  14191332587920938932346122007558957725, 14627958096404851071765117785209182534
166-167  15042776398828935907253337043122561811, 15433276401559119181929960270005994565
168-169  15797050645300463894347274379439078220, 16131819435300475051743664599586952234
170-171  16435454076379664531246796865132616416, 16705998889343692614967694537858944801
172-173  16941691697744468217210804458293280089, 17140982491881225040493439839543832716
174-175  17302550000114682047446327818361336324, 17425315925643408381215288070447785673
176-177  17508456639391199888898358533872703450, 17551412156011022509677316437633568636
178-179  17553892259573662174498020081687419047, 17515879687555700518312240659895095610
180-181  17437630325494842830696881690977373775, 17319670409326056339171593157036111951
182-183  17162790777114656531585786262165760176, 16968038255826327047034126885436523331
184-185  16736704311100296536360635746601223771, 16470311127937209733030622796993226414
186-187  16170595327047026867136225118441108535, 15839489554662607691745557452203162418
188-189  15479102212332333013763855891497797788, 15091695617075924336558056248020312633
190-191  14679662900941863830396560866512139002, 14245503972174495596323405573794138964
192-193  13791800867732028667280701784003530331, 13321192828758818071523760332197897547
194-195  12836351426888248078547179572751794469, 12339956060130220633533554981744039163
196-197  11834670122879118040646672316102009897, 11323118135660117952283807940496464306
198-199  10807864097095238715191726233835345708, 10291391293769357148771395981131836547
200-201  9776083773822810372731795724944905524, 9264209657846231282584322880734444959
202-203  8757906426687335997813465732797709728, 8259168290792064839574898916028238980
204-205  7769835710382859028565620995995683538, 7291587100794440233905801541373167065
206-207  6825932723278114104085724790863068441, 6374210729138829296841075913870111466
208-209  5937585294716970630114351569554162725, 5517046756934319196986132612750456614
210-211  5113413634281820990884550000439634945, 4727336396547472372664431912498378985
212-213  4359302828495028820860612085123745947, 4009644818254245124842570655781853100
214-215  3678546390434502711125834660706795818, 3366052796910170859148299111033325499
216-217  3072080474757464264405697335598311015, 2796427680790122771938600554610234230
218-219  2538785615325362145573291522255528341, 2298749853940399257653012725552978333
220-221  2075831914738689107676489886786840911, 1869470799685927816429512991422626556
222-223  1679044361527795756323880950343860072, 1503880362279953558897360121419810489
224-225  1343267104897814256321979648632364143, 1196463536106173315332820431637086240
226-227  1062708735127414543815146461459828069, 941230719843023104290715125176323663
228-229  831254518434871510879086692403690765, 732009470490736810401367136459547761
230-231  642735736669453068662351109062026857, 562690010090632305509040623608359274
232-233  491150435468162253288887618806179856, 427420753512884217732203723575261823
234-235  370833698195584349931713168514468035, 320753683033241675939773159018654344
236-237  276578819622503089705751302533296118, 237742317211297871531425013035340734
238-239  203713316219040779220834628275052533, 173997211360672261252416552245602736
240-241  148135521494251494387176059401283677, 125705363607711397475143054818840427
242-243  106318587612436937442932731919147110, 89620626952983025342864610671830147
244-245  75289117611620261214101479913856014, 63032335022534898837459514440043933
246-247  52587494850038337152117376073263611, 43718959659328666312448410483948494
248-249  36216389340630496916413392758865476, 29892868851534049758871914880794596
250-251  24583042520336088237829859320695591, 20141279895042335464197207273548255
252-253  16439894005318511404301717822429228, 13367428991777244455439032105766303
254-255  10827030399235655735551858416698466, 8734908066102284232112207975836294
256-257  7018898497180798418715829960673446, 5617130897395941768658510619915621
258-259  4476798675007672154526830934870798, 3553036192023755880033141920338111
260-261  2807898836755171198606627609370712, 2209443102844075611051331548030672
262-263  1730902260014224074685289944575676, 1349952370163352678372620665922468
264-265  1048062811808168912387389962139882, 809925098556491073597275236664258
266-267  622953585052068523112531981421284, 476851618909803038126896494230747
268-269  363236792732564841082427882851957, 275319151098168726955862011365381
270-271  207626490063270483908783793794978, 155771230076212890450531254966858
272-273  116253728407468181724075984357152, 86297307911133057259467495605499
274-275  63710701166977790911553273312011, 46774031215489142615179254691214
276-277  34144862809250522182015517136462, 24781254041653332760262295914442
278-279  17879111918806101232647789288932, 12821503101500839653666865122026
280-281  9137890277701152762257206233990, 6471554256178751485788380827699
282-283  4553721717337307733825089158926, 3183149231375143871715608723214
284-285  2210116881559552644760108416571, 1523961283468124100909520152834
286-287  1043429945111647590321963251783, 709268924481537213409043502442
288-289  478565846188799847907499501723, 320462770738734872246227004213
290-291  212930335454392875097314722584, 140358058223468612179565566442
292-293  91767620552474741699859490317, 59498064072718268414781881573
294-295  38245706217560886492068909372, 24368588024368030753058736205
296-298  15386616018891222668957564259, 9625290275459096784533444177, 5963906751576331727209696509
299-301  3659128128128456818921429464, 2222452568064059284933899437, 1335882966958999753809315370
302-304  794424279431161508959360243, 467246260988217919037273780, 271708322978492486350128260
305-307  156160602612362376668355900, 88673067456228061179740154, 49727447825492947577086013
308-310  27530170025429211855545545, 15039904492199099240065856, 8104203855152035653897756
311-313  4305267527706946137246442, 2253714512687328152404457, 1161928327781496197257732
314-316  589659824720099369732066, 294382498949321264485202, 144491576578711302122374
317-319  69680170608154110806220, 32992176948657851562524, 15325981607087034496268
320-322  6979456488267294994955, 3113361304366888063230, 1359148766709232157781
323-326  580127050832372141115, 241857049606809853618, 98379326965159501309, 38999086084031429578
327-330  15047667862129818815, 5643722762782331087, 2054545797837499636, 724838211998435984
331-334  247403908376211048, 81548212630116086, 25905757849665088, 7914144898192144
335-339  2319525079990171, 650489111198557, 174047204344810, 44287727895491, 10679046824311
340-346  2430352672624, 519665586891, 103861621888, 19288026626, 3305459537, 518519486, 73735796
347-353  9393311, 1056280, 102832, 8451, 563, 29, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{45}\Phi_{2}(x)^{21}\Phi_{3}(x)^{12}\Phi_{4}(x)^{9}\\&\times \Phi_{5}(x)^{7}\Phi_{6}(x)^{5}\Phi_{7}(x)^{5}\Phi_{8}(x)^{3}\\&\times \Phi_{9}(x)^{3}\Phi_{10}(x)^{3}\Phi_{11}(x)^{3}\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\Phi_{16}(x)\\&\times \Phi_{17}(x)\Phi_{18}(x)\Phi_{19}(x)\Phi_{20}(x)\\&\times \Phi_{21}(x)\Phi_{22}(x)\Phi_{23}(x)\end{aligned}$$


### R24 — k=24 leaves

Order 420; period 5354228880; source v31/ROOTED_MODELS.json, record 23.

$$B=2^{n+539},\quad a(n)=0\ (n<25).$$

$$a(n)=\left\lfloor\frac{B^{n-25}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 25).$$

$$R(x)=\sum_{j=0}^{394} c_jx^j.$$

```text
  0-10   1, 20, 350, 4808, 55137, 542470, 4687296, 36166328, 252548933, 1613090441, 9507013864
 11-16   52078789680, 266798727258, 1284996851446, 5845188044446, 25211918944209, 103478975086817
 17-21   405409767693319, 1520357990535250, 5471408469455861, 18938348834175779, 63179069884455423
 22-25   203522839058523247, 634182990835564231, 1914566713824344752, 5608168254345402061
 26-29   15960973005672636461, 44191293639077795635, 119169921725173659331, 313349340625126188106
 30-32   804214631245897813762, 2016587779512883764410, 4944925005300012642507
 33-35   11867844071395189622884, 27900001436599914975245, 64296587869435271226253
 36-38   145356947958539732924030, 322584791456379887073931, 703222370777056047086147
 39-41   1506774165330377894789072, 3175140023835845205002394, 6583802661657655419860306
 42-44   13440585393188046209936174, 27027402336024683464407112, 53560199978596078420596237
 45-47   104647588084926650656979320, 201675784764277177879499907, 383526730791245778295876194
 48-50   719990436273709543769901348, 1334785090668613705126291730, 2444593873948459303138197174
 51-53   4424491496465832972879033433, 7916358883680451654369772541, 14006552526943287743527627224
 54-55   24513947300117110429053821170, 42452047218164187815679134378
 56-57   72762820984664060705561193624, 123470498506587502821650065623
 58-59   207478152610254597228413038302, 345338829606872542355584804414
 60-61   569490613375243268709243320803, 930670975091229026297651471840
 62-63   1507546805362457787786944447292, 2421048645326647183682843260487
 64-65   3855528862552485315735993936090, 6089737372239957033570557254237
 66-67   9541808221453378215165662923134, 14834084051666374401729244758801
 68-69   22885812337695519532228284303347, 35044705040627763381353160560077
 70-71   53272286713586745894407316706021, 80403147150537797575439659668031
 72-73   120505014038554990828945557594141, 179375401075074139174195953558349
 74-75   265221995985731663988760385703517, 389588570887456790737292367122765
 76-77   568606793040997935266454102296355, 824677801794939551416480513447668
 78-79   1188716875806517090221834266259027, 1703131203015721521628889488700288
 80-81   2425746141376611938127875155240801, 3434951089521991453024018215516116
 82-83   4836404063969035085869635273431928, 6771716421680038957283547424200161
 84-85   9429638219533661220514049101455150, 13060383029616621817859668194358184
 86-87   17993871394447554230780649823655657, 24662837440182651354063424757530964
 88-89   33631936521075965455374615948152863, 45634216256539056979049352942470938
 90-91   61616572032287172306237909106315641, 82796103934226926541753650347182342
 92-93   110729627884583809906929654881026919, 147398971775397525086879625667569336
 94-95   195315109399579609053696874908639417, 257644651958076599070998289062906390
 96-97   338362728889753787754874964894445565, 442436845530811638434870858970781169
 98-99   576046901997984412999538186378577187, 746847191307145964095030037515633027
100-101  964276858685672050072150905016180632, 1239925989640112035150945460060795273
102-103  1587965190397228966056633118715074531, 2025647216876272989770668709784618291
104-105  2573889880433495441403254506704706403, 3257950090179767433919899381011874734
106-107  4108199459419176708455709415123758404, 5161012381156870778388611436707098057
108-109  6459777834968762677132917638451929051, 8056046392101837989816121203402794842
110-111  10010823902057796399692814528457190653, 12396023134390495495762235294541084006
112-113  15296084174577034163281618851099359686, 18809773592143832099094312800986780217
114-115  23052171272128943225407641996379675599, 28156852287687606466835449671991547992
116-117  34278269254471980001968524086559327302, 41594338211936492274049752143050274405
118-119  50309228193285085339966422880161154595, 60656351251006587502391893677036787965
120-121  72901545783328668931289779494675357063, 87346441552449577526716298477557056294
122-123  104331989803200963772693231728550231173, 124242136398685741971519998757789097609
124-125  147507609919442299265065519896001113162, 174609790272341975193377808466442773892
126-127  206084616588881023689057016773837509386, 242526486141383746293668677001129638150
128-129  284592088769444016787776634385200130710, 333004114005311180740169237443969075442
130-131  388554760851209085294071271783844265479, 452108973145993588917048054278877329381
132-133  524607316830868926315540299907873380648, 607068409365477849012315175460368065053
134-135  700590806249058857302457434661912235630, 806354245267083992317578469711570599839
136-137  925620145916832506165244171487664591858, 1059731259670959628718503380314078964845
138-139  1210110366517144755990413791185268798138, 1378257914755774692427301686129220212150
140-141  1565748504522948869934996965523180108499, 1774226121089091222371343251259648106384
142-143  2005398031794223371360970116686672052408, 2261027270617846549523551728487523212376
144-145  2542923646905523659607522586867080323334, 2852933229704432255667286789580456317023
146-147  3192926276468199844754057313123876674699, 3564783594498159775883002781873173420924
148-149  3970381345260693555179735142356198534440, 4411574325469332822896734406450055188133
150-151  4890177784299424994323606145142092097936, 5407947863009174135106903489635528298024
152-153  5966560771215205845348846850102628489227, 6567590842702628282140023783972408200719
154-155  7212487642480189431061834258054235973177, 7902552325319960094914468157914680431392
156-157  8638913473712818604938569393377654704962, 9422502669464803804346029775188755995217
158-159  10254030077478104996293502010645961886718, 11133960342022093592373658271812708762252
160-161  12062489114429354463047142055562505198276, 13039520546093660703064291046883028019973
162-163  14064646091378276832525582028650900017225, 15137124971086498161890884113130950826758
164-165  16255866648083073113175992364607205147505, 17419415662137152322523152168136863490374
166-167  18625939160819173748450178436546433519522, 19873217447153008751158756325918048891788
168-169  21158637842629944874696828955656101742018, 22479192136170821532564910487992301120731
170-171  23831477855829130305563490412843413236387, 25211703560730406767528664163275985164761
172-173  26615698306328496552361175304133736486437, 28038925387029349342164305588491756337163
174-175  29476500407200577405786488551464684431794, 30923213675266061633190839280303897301736
176-177  32373556856788657917329250524085355475090, 33821753762060719730353450890625354700150
178-179  35261795082708124401968222524164609782531, 36687476831174758882778174350211366444193
180-181  38092442177728174089676882133845978577296, 39470226322862038944337499514352266574993
182-183  40814303989706666494516171953568380522553, 42118139072304556932327678655251464670924
184-185  43375235932321567845976167421276860164715, 44579191799831961020938661276567083369130
186-187  45723749704031521630252492474723224992185, 46802851337781666187450397748151461317650
188-189  47810689246327224459579617207154705210067, 48741757725779469588599156618217744201465
190-191  49590901821280524804196920443834469371066, 50353363828272185947903707042050036247105
192-193  51024826722923224286470622580617735476873, 51601453979299534832293998749164678969367
194-195  52079925270901484171532713229463085240632, 52457467602193521034990929404137460703779
196-197  52731881471013008239400012042204056548998, 52901561724430314368356294132567855235803
198-199  52965512837779143527440564762660224592792, 52923358418118110895903991056324111684352
200-201  52775344808169695998932948064889484168525, 52522338743595833896112258803064849950337
202-203  52165819094055892509701691843944326034755, 51707862795582865657988006539144738401681
204-205  51151125157147169686308609017384873007998, 50498814796628556611592126532044725416400
206-207  49754663529617432512027027162250890304063, 48922891597429863464781167793778323532135
208-209  48008168677459501999309086084720527624778, 47015571168637922768542316389579865493809
210-211  45950536286601159193683576030482629174718, 44818813536581523054756065689227655681963
212-213  43626414156634767526844944213376921813717, 42379559139311929592218615576103233998924
214-215  41084626446197910542463301346245336357354, 39748098026935828653302941400704294033238
216-217  38376507242669532017256840917908879035515, 36976387273652212505130296266572554536208
218-219  35554221062615641794899814276710984517865, 34116393310030543260847989099689177314594
220-221  32669144995386110858167967544148648400465, 31218530850943638222558918973234615218341
222-223  29770380162020041925071633609864198969062, 28330261211732159208715077621228655727283
224-225  26903449629317413139882971887383057895679, 25494900840689879337993228831093113909456
226-227  24109226758835054899333216544325407252480, 22750676791006841785627560640444359088975
228-229  21423123180435842675000489028069835785636, 20130050643295672652919430657089081358011
230-231  18874550207832332606577552210105642759530, 17659317112578628616006273960194359514731
232-233  16486652575087644941325421235798968200896, 15358469202153552527854809838176101646252
234-235  14276299777457082222888999547857463965575, 13241309133272007020642014280512818264801
236-237  12254308789475728409390307735923026162940, 11315774025684256323034709235006146879501
238-239  10425863040831824624935995512606292417288, 9584437848786763686507937275072127914506
240-241  8791086558391658344993474887994865028158, 8045146691305900095839472633680068963219
242-243  7345729200807538159278237482838537221939, 6691742868812537656462900937632666231771
244-245  6081918776278346945300048056007923010604, 5514834563324829736133434590911748992694
246-247  4988938219256532608286145567478866212369, 4502571168623669479988062079077264653973
248-249  4053990446935268837813180720688252997996, 3641389788070471246987619989049830007190
250-251  3262919474280671968249486868426523870213, 2916704828426616602588770985342388898447
252-253  2600863256281725190298405525610929931470, 2313519773933641410244469928888049915894
254-255  2052820981159614331390132885629421072547, 1816947465822018355052743376728923644791
256-257  1604124646569058875415723424668608107569, 1412632081230743652117444652468871986889
258-259  1240811286126320595340913978899542458474, 1087072126956045273760891541677887819564
260-261  949897854998541938854071385093094588869, 827848872984316212163153233979041683944
262-263  719565323318790645928074755003045157156, 623768597375623754720851570307112173044
264-265  539261868497112116947445636477671070960, 464929753274613938691243472593957633160
266-267  399737205811288759019607544476713596393, 342727748181166572533276516466667630043
268-269  293021137392366432284449024243185130542, 249810565043343911176454463123993415624
270-271  212359480735213737405748474822582750194, 179998124372734473529640594997533430383
272-273  152119845946375414287204382575836050813, 128177284422384379254713890838335263562
274-275  107678470148140890916407504090108146085, 90182907862298577930139783055190304327
276-277  75297690122583435087838808394827665229, 62673683850273227022505748006860220510
278-279  52001825842914004913001232588856592672, 43009556611250252210901505198542898738
280-281  35457415820537398616586607625700200248, 29135817011384892949819619721613667472
282-283  23862014176251850268146287734583950456, 19477268195370160411067497474665586990
284-285  15844217097819192027770807146585663000, 12844450605839823785508589618384138799
286-287  10376286429500492085820668999356884591, 8352743282531423099786677970034109656
288-289  6699703559924299916929408822888744463, 5354257020080707405006497390420385692
290-291  4263215611590850364692866485386778673, 3381788737553868316122932923903173595
292-293  2672407718042120562099614391035013234, 2103687953154165123299561730836786721
294-295  1649517265243440089637586313019960556, 1288259071103626930238022274424750354
296-297  1002059367086642192016977856845004356, 776246968923299919485366632108757566
298-299  598817002974782994598889361304478170, 459988269493357850991097945237201810
300-301  351825767193633729950887717887678878, 267920361259227538047762633220554821
302-303  203118276227014240894946968756963116, 153293786413768345589446093396872869
304-305  115159147912057855034527746150900673, 86106458508416918120892894503025030
306-307  64076738326395401295389941737245469, 47452089795006867796485302264249564
308-309  34967317707394792933340870466331582, 25637867208111634671898131327549923
310-311  18701369340671472931540593853117970, 13570471136436576900072953899373186
312-313  9794971771987840777825370796043832, 7031590309704298324392136427035613
314-315  5019956637911426622611219788412310, 3563648390387126903425063212311745
316-317  2515295944011234142229525627788223, 1764948201099930334582386280887746
318-319  1231036846500733134826503022014396, 853399103309472847827127340817029
320-321  587921507823187391870005425318604, 402452500818490419681087467076586
322-323  273702087866136439943498312409439, 184904627571269138223021206132227
324-325  124067904772921964285003428082653, 82669752077914960956048810747724
326-327  54694098677399061326757874555232, 35922749689648199427466023671350
328-329  23418546307854375335394973868322, 15150772781460353704255291066402
330-331  9725556589053449243611845831465, 6193216586421665936448878136719
332-333  3911598682206023227149631609052, 2449848716880899535775334420135
334-335  1521172220049205007038925066698, 936213949470076695294702539247
336-337  570990599807603570656965531038, 345012883169956252884531104082
338-339  206483408484064250865535611518, 122367154747628324784824205602
340-341  71788664833049565988533165934, 41680649339733369408667671410
342-344  23942607213610949262691830110, 13602906802038158676864556080, 7641420345785446122189726086
345-347  4242782263562033836536627050, 2327592245134651627668907183, 1261189492745660480997202831
348-350  674684814129441652047336332, 356196865505504782074817876, 185506965246336034713177663
351-353  95260769101062656115196654, 48210777855551988015814895, 24034317831629908244642623
354-356  11796322533795818979241381, 5696990668597951200939300, 2705649840049884106170545
357-359  1262854588565052952749976, 578899758204174426705246, 260445652102795340359586
360-362  114913619720836792673501, 49684784124325501413233, 21033323664138824291857
363-365  8710366317148057792207, 3525288013397584437212, 1392964320859214748381
366-369  536783763994144862304, 201495720242171188339, 73586036671164696553, 26109790435201426372
370-373  8987934864650414432, 2996989272607965879, 966370740620326693, 300772490430035526
374-378  90178072273987735, 25988811488386487, 7182234009346138, 1898382341382887, 478525777960822
379-384  114666274052269, 26027224059379, 5573758114471, 1121088579186, 210705863177, 36787513331
385-394  5925676133, 873553511, 116723198, 13971175, 1475874, 135029, 10414, 654, 31, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{47}\Phi_{2}(x)^{23}\Phi_{3}(x)^{15}\Phi_{4}(x)^{11}\\&\times \Phi_{5}(x)^{7}\Phi_{6}(x)^{7}\Phi_{7}(x)^{5}\Phi_{8}(x)^{5}\\&\times \Phi_{9}(x)^{3}\Phi_{10}(x)^{3}\Phi_{11}(x)^{3}\Phi_{12}(x)^{3}\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\Phi_{16}(x)\\&\times \Phi_{17}(x)\Phi_{18}(x)\Phi_{19}(x)\Phi_{20}(x)\\&\times \Phi_{21}(x)\Phi_{22}(x)\Phi_{23}(x)\Phi_{24}(x)\end{aligned}$$


## Unrooted trees: fixed leaf counts


### U01 — k=2 leaves

Order 1; period 1; source v31/UNROOTED_MODELS.json, record 0.

$$B=2^{n+2},\quad a(n)=0\ (n<2).$$

$$a(n)=\left\lfloor\frac{B^{n-2}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 2).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)$$

Same rational function as G01.


### U02 — k=3 leaves

Order 6; period 6; source v31/UNROOTED_MODELS.json, record 1.

$$B=2^{n+5},\quad a(n)=0\ (n<4).$$

$$a(n)=\left\lfloor\frac{B^{n-4}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 4).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{3}\Phi_{2}(x)\Phi_{3}(x)$$

Same rational function as G02.


### U03 — k=4 leaves

Order 11; period 12; source v31/UNROOTED_MODELS.json, record 2.

$$B=2^{n+10},\quad a(n)=0\ (n<5).$$

$$a(n)=\left\lfloor\frac{B^{n-5}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 5).$$

$$R(x)=1+x^{3}+x^{5}$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)^{2}\Phi_{3}(x)\Phi_{4}(x)$$

Same rational function as G03.


### U04 — k=5 leaves

Order 18; period 60; source v31/UNROOTED_MODELS.json, record 3.

$$B=2^{n+19},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$\begin{aligned}R(x)&=1+x^{2}+3x^{3}+4x^{4}+4x^{5}+5x^{6}\\&+4x^{7}+4x^{8}+2x^{9}+2x^{10}\end{aligned}$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{7}\Phi_{2}(x)^{3}\Phi_{3}(x)\Phi_{4}(x)\\&\times \Phi_{5}(x)\end{aligned}$$

Same rational function as G04.


### U05 — k=6 leaves

Order 27; period 60; source v31/UNROOTED_MODELS.json, record 4.

$$B=2^{n+32},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=\sum_{j=0}^{19} c_jx^j.$$

```text
  0-19   1, 1, 2, 7, 13, 25, 37, 51, 64, 78, 78, 76, 67, 53, 35, 24, 10, 5, 2, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{9}\Phi_{2}(x)^{4}\Phi_{3}(x)^{3}\Phi_{4}(x)\\&\times \Phi_{5}(x)\Phi_{6}(x)\end{aligned}$$


### U06 — k=7 leaves

Order 36; period 420; source v31/UNROOTED_MODELS.json, record 5.

$$B=2^{n+44},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=\sum_{j=0}^{26} c_jx^j.$$

```text
  0-18   1, 1, 4, 13, 32, 65, 128, 218, 349, 508, 695, 870, 1035, 1136, 1183, 1147, 1048, 885, 711
 19-26   518, 354, 218, 123, 58, 28, 9, 3
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{11}\Phi_{2}(x)^{5}\Phi_{3}(x)^{3}\Phi_{4}(x)\\&\times \Phi_{5}(x)\Phi_{6}(x)\Phi_{7}(x)\end{aligned}$$


### U07 — k=8 leaves

Order 47; period 840; source v31/UNROOTED_MODELS.json, record 6.

$$B=2^{n+58},\quad a(n)=0\ (n<9).$$

$$a(n)=\left\lfloor\frac{B^{n-9}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 9).$$

$$R(x)=\sum_{j=0}^{37} c_jx^j.$$

```text
  0-16   1, 1, 5, 19, 49, 126, 277, 575, 1074, 1889, 3060, 4706, 6760, 9258, 11957, 14797, 17353
 17-30   19548, 20931, 21553, 21113, 19890, 17792, 15297, 12440, 9692, 7089, 4954, 3205, 1971, 1095
 31-37   576, 261, 114, 36, 13, 2, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{13}\Phi_{2}(x)^{6}\Phi_{3}(x)^{3}\Phi_{4}(x)^{3}\\&\times \Phi_{5}(x)\Phi_{6}(x)\Phi_{7}(x)\Phi_{8}(x)\end{aligned}$$


### U08 — k=9 leaves

Order 60; period 2520; source v31/UNROOTED_MODELS.json, record 7.

$$B=2^{n+77},\quad a(n)=0\ (n<10).$$

$$a(n)=\left\lfloor\frac{B^{n-10}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 10).$$

$$R(x)=\sum_{j=0}^{48} c_jx^j.$$

```text
  0-14   1, 2, 10, 38, 128, 372, 1002, 2419, 5433, 11244, 21762, 39436, 67540, 109393, 168735
 15-24   248202, 349640, 472370, 613935, 768196, 927549, 1081228, 1218567, 1328061, 1401093
 25-34   1430394, 1414082, 1352831, 1252653, 1121470, 970625, 810707, 653162, 506378, 377338
 35-48   269345, 183903, 119432, 73648, 42778, 23339, 11805, 5539, 2340, 902, 300, 89, 19, 5
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{15}\Phi_{2}(x)^{7}\Phi_{3}(x)^{5}\Phi_{4}(x)^{3}\\&\times \Phi_{5}(x)\Phi_{6}(x)\Phi_{7}(x)\Phi_{8}(x)\\&\times \Phi_{9}(x)\end{aligned}$$


### U09 — k=10 leaves

Order 75; period 2520; source v31/UNROOTED_MODELS.json, record 8.

$$B=2^{n+97},\quad a(n)=0\ (n<11).$$

$$a(n)=\left\lfloor\frac{B^{n-11}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 11).$$

$$R(x)=\sum_{j=0}^{63} c_jx^j.$$

```text
  0-14   1, 3, 13, 59, 219, 735, 2219, 6147, 15665, 37118, 82052, 170502, 334350, 621903, 1100929
 15-23   1862237, 3018061, 4700633, 7051449, 10211633, 14300801, 19401947, 25534396, 32642771
 24-32   40575480, 49089714, 57847045, 66443431, 74424030, 81335265, 86750185, 90325741, 91820619
 33-41   91137825, 88316531, 83547100, 77132623, 69476435, 61024920, 52243271, 43558547, 35343559
 42-50   27878823, 21355278, 15862176, 11408334, 7928794, 5314701, 3426486, 2119303, 1252756
 51-63   705360, 376238, 189295, 89123, 39052, 15716, 5785, 1893, 552, 136, 30, 4, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{17}\Phi_{2}(x)^{8}\Phi_{3}(x)^{5}\Phi_{4}(x)^{3}\\&\times \Phi_{5}(x)^{3}\Phi_{6}(x)\Phi_{7}(x)\Phi_{8}(x)\\&\times \Phi_{9}(x)\Phi_{10}(x)\end{aligned}$$


### U10 — k=11 leaves

Order 88; period 27720; source v31/UNROOTED_MODELS.json, record 9.

$$B=2^{n+114},\quad a(n)=0\ (n<12).$$

$$a(n)=\left\lfloor\frac{B^{n-12}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 12).$$

$$R(x)=\sum_{j=0}^{74} c_jx^j.$$

```text
  0-13   1, 3, 17, 81, 337, 1226, 4087, 12380, 34635, 89752, 217318, 493726, 1058753, 2151251
 14-22   4159842, 7680623, 13587071, 23092196, 37808160, 59767765, 91419988, 135550692, 195159226
 23-30   273236368, 372508430, 495091570, 642166216, 813611696, 1007751321, 1221129427, 1448495008
 31-37   1682868248, 1915867758, 2138110907, 2339850625, 2511597216, 2644879136, 2732845917
 38-44   2770881603, 2756925864, 2691709296, 2578632260, 2423547178, 2234220293, 2019776812
 45-52   1789946466, 1554420362, 1322154021, 1100896110, 896768137, 714116194, 555443875, 421580580
 53-60   311891134, 224630843, 157269663, 106864031, 70339820, 44755834, 27459376, 16201387
 61-72   9162139, 4948827, 2541744, 1235695, 565098, 241673, 95756, 34899, 11514, 3421, 881, 200
 73-74   35, 6
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{19}\Phi_{2}(x)^{9}\Phi_{3}(x)^{5}\Phi_{4}(x)^{3}\\&\times \Phi_{5}(x)^{3}\Phi_{6}(x)\Phi_{7}(x)\Phi_{8}(x)\\&\times \Phi_{9}(x)\Phi_{10}(x)\Phi_{11}(x)\end{aligned}$$


### U11 — k=12 leaves

Order 107; period 27720; source v31/UNROOTED_MODELS.json, record 10.

$$B=2^{n+139},\quad a(n)=0\ (n<13).$$

$$a(n)=\left\lfloor\frac{B^{n-13}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 13).$$

$$R(x)=\sum_{j=0}^{93} c_jx^j.$$

```text
  0-13   1, 3, 19, 99, 436, 1761, 6386, 21281, 65356, 186833, 499134, 1255000, 2980658, 6719643
 14-21   14427713, 29611184, 58256302, 110184986, 200824311, 353541970, 602357067, 995140974
 22-28   1596792298, 2492463490, 3789851023, 5620727333, 8140229029, 11524455724, 15964524137
 29-35   21658482506, 28798983439, 37559517086, 48076942248, 60434790095, 74644792288, 90632768322
 36-41   108225423091, 127145519357, 147010284571, 167341106692, 187577024847, 207100102489
 42-47   225262359526, 241422335227, 254978434104, 265407351145, 272293295607, 275357284828
 48-53   274471973558, 269673147394, 261154290510, 249257347515, 234447834472, 217288972751
 54-59   198404533437, 178445668881, 158052347268, 137823737662, 118288493823, 99887165919
 60-66   82957446719, 67731899077, 54338709714, 42812514726, 33106347614, 25109762069, 18665312561
 67-73   13587318044, 9676785722, 6735808803, 4577266290, 3032786681, 1956462716, 1226961554
 74-82   746687611, 440122507, 250695628, 137669950, 72673885, 36769761, 17762270, 8162219, 3548849
 83-93   1453492, 556273, 197932, 64616, 19288, 5109, 1223, 239, 43, 5, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{21}\Phi_{2}(x)^{10}\Phi_{3}(x)^{7}\Phi_{4}(x)^{5}\\&\times \Phi_{5}(x)^{3}\Phi_{6}(x)^{3}\Phi_{7}(x)\Phi_{8}(x)\\&\times \Phi_{9}(x)\Phi_{10}(x)\Phi_{11}(x)\Phi_{12}(x)\end{aligned}$$


### U12 — k=13 leaves

Order 122; period 360360; source v31/UNROOTED_MODELS.json, record 11.

$$B=2^{n+158},\quad a(n)=0\ (n<14).$$

$$a(n)=\left\lfloor\frac{B^{n-14}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 14).$$

$$R(x)=\sum_{j=0}^{106} c_jx^j.$$

```text
  0-12   1, 3, 24, 128, 628, 2698, 10640, 38079, 126142, 387368, 1112893, 3002787, 7652914
 13-20   18490019, 42526959, 93406524, 196549668, 397292293, 773421388, 1453335888, 2641715632
 21-27   4653697849, 7959275634, 13237491046, 21440809822, 33866149053, 52230433866, 78742561060
 28-33   116166748145, 167864311251, 237807321992, 330548116043, 451140339518, 604996251312
 34-39   797683704124, 1034653193612, 1320911546227, 1660641953566, 2056803081349, 2510716065722
 40-45   3021686425147, 3586673545130, 4200061579631, 4853538266511, 5536131380350, 6234391257602
 46-51   6932754175010, 7614048210154, 8260155170885, 8852761754145, 9374194577724, 9808250937870
 52-56   10141011654585, 10361541646765, 10462471794258, 10440379307246, 10295982585613
 57-62   10034093218854, 9663372120746, 9195863406036, 8646381997483, 8031754510797, 7370006927670
 63-68   6679510900130, 5978182611281, 5282742252750, 4608111513467, 3966940671290, 3369315759987
 69-74   2822615606545, 2331540975043, 1898267520653, 1522723106267, 1202933118369, 935423982615
 75-80   715631954811, 538308225100, 397879980849, 288766294388, 205625037824, 143539327502
 81-87   98134666955, 65642329488, 42910167232, 27378527287, 17026719117, 10305404797, 6060026579
 88-95   3455851274, 1907194519, 1016256914, 521480335, 256960726, 121179116, 54497130, 23268929
 96-106  9390397, 3559667, 1260547, 413084, 124504, 33936, 8352, 1771, 339, 48, 7
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{23}\Phi_{2}(x)^{11}\Phi_{3}(x)^{7}\Phi_{4}(x)^{5}\\&\times \Phi_{5}(x)^{3}\Phi_{6}(x)^{3}\Phi_{7}(x)\Phi_{8}(x)\\&\times \Phi_{9}(x)\Phi_{10}(x)\Phi_{11}(x)\Phi_{12}(x)\\&\times \Phi_{13}(x)\end{aligned}$$


### U13 — k=14 leaves

Order 143; period 360360; source v31/UNROOTED_MODELS.json, record 12.

$$B=2^{n+186},\quad a(n)=0\ (n<15).$$

$$a(n)=\left\lfloor\frac{B^{n-15}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 15).$$

$$R(x)=\sum_{j=0}^{127} c_jx^j.$$

```text
  0-12   1, 4, 28, 172, 895, 4216, 17920, 69758, 250193, 833901, 2597093, 7602745, 21014279
 13-20   55083040, 137424832, 327446926, 747376155, 1638549292, 3459172076, 7047994426, 13887820009
 21-26   26515715522, 49139058841, 88532106536, 155297423809, 265588036256, 443382330944
 27-32   723400300220, 1154717620458, 1805104298051, 2766040960802, 4158305423405, 6137903595252
 33-37   8902039152839, 12694667330623, 17811112804764, 24601086457586, 33469438083578
 38-42   44873887962487, 59319110200505, 77346539448274, 99519574843490, 126403958395500
 43-47   158543584054582, 196432163097846, 240481775955627, 290989480960710, 348103777748419
 48-52   411792699345526, 481815830523850, 557702226895387, 638736523793146, 723954816005585
 53-57   812151959573921, 901900860534622, 991584205951230, 1079437743048326, 1163604083886295
 58-62   1242194601682048, 1313357053567691, 1375345320670730, 1426588123721651, 1465752679000621
 63-67   1491800238557448, 1504029987775939, 1502109240905910, 1486087757483744, 1456395794221524
 68-72   1413825552199939, 1359497533373529, 1294813280827856, 1221397615152847, 1141033133124981
 73-77   1055590946031326, 966960862394780, 876984921813428, 787397008109279, 699771524947611
 78-82   615482681323443, 535675915827325, 461251519526434, 392860442393432, 330910990190686
 83-87   275585174528841, 226862548156283, 184549646555545, 148312624973366, 117711200698189
 88-92   92231825108594, 71318676436576, 54401103875460, 40916839371513, 30330417484085
 93-97   22146830267222, 15920538626568, 11260375252659, 7830877933938, 5350816947863
 98-103  3589587380462, 2362205985296, 1523496126095, 962015585508, 594110306527, 358410656223
104-110  210939910951, 120943719824, 67448853718, 36524710037, 19168701089, 9729304154, 4764687089
111-119  2245559563, 1015486463, 439208245, 180998789, 70776652, 26130595, 9060112, 2929770, 877572
120-127  240918, 60137, 13378, 2645, 437, 65, 6, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{25}\Phi_{2}(x)^{12}\Phi_{3}(x)^{7}\Phi_{4}(x)^{5}\\&\times \Phi_{5}(x)^{3}\Phi_{6}(x)^{3}\Phi_{7}(x)^{3}\Phi_{8}(x)\\&\times \Phi_{9}(x)\Phi_{10}(x)\Phi_{11}(x)\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\end{aligned}$$


### U14 — k=15 leaves

Order 166; period 360360; source v31/UNROOTED_MODELS.json, record 13.

$$B=2^{n+217},\quad a(n)=0\ (n<16).$$

$$a(n)=\left\lfloor\frac{B^{n-16}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 16).$$

$$R(x)=\sum_{j=0}^{148} c_jx^j.$$

```text
  0-12   1, 6, 45, 298, 1762, 9269, 44245, 192730, 773836, 2882620, 10027507, 32745899, 100872081
 13-19   294326533, 816492903, 2160598920, 5470068783, 13285511728, 31031091737, 69858767676
 20-25   151894300578, 319578546599, 651755374192, 1290506258362, 2484564818266, 4657519831068
 26-30   8511977600543, 15184349315640, 26468859455677, 45133457311580, 75354224181861
 31-35   123298010537314, 197884823932287, 311761025696131, 482510968252331, 734127300991444
 36-40   1098748267311908, 1618653127587463, 2348484518553808, 3357638986654403, 4732735427813885
 41-44   6580036627657833, 9027664310666191, 12227414993382961, 16355956635925601
 45-48   21615167015692464, 28231368737347329, 36453224691621281, 46548085952875788
 49-52   58796631414214332, 73485707521273366, 90899363773015410, 111308185143723282
 53-56   134957138646021824, 162052275058096902, 192746747039005481, 227126716967087172
 57-60   265197818333784432, 306872899540785787, 351961805307921702, 400163938197786498
 61-64   451064280944573576, 504133455009303062, 558732237148539276, 614120766912341284
 65-68   669472454563361031, 723892360959501213, 776439573223464681, 826152866893663829
 69-72   872078732181333827, 913300673624384607, 948968570818887063, 978326833636566394
 73-76   1000740093143097237, 1015715252590339171, 1022918866748693565, 1022189027290919578
 77-80   1013541183430548177, 997167618351539657, 973430603764106239, 942849561658958201
 81-84   906082843447279582, 863904988089487530, 817180515871694770, 766835454828154283
 85-88   713827863584628471, 659118617514857783, 603643655095853187, 548288756373428346
 89-92   493867744410924788, 441104787375385971, 390621237625808708, 342927200358707662
 93-96   298417783122201084, 257373761707814258, 219966209801710032, 186264496151600224
 97-100  156246950900535783, 129813451483447759, 106799169477104032, 86988755480279368
101-104  70130306743944659, 55948559580230556, 44156861292579865, 34467600353730129
105-108  26600895761297550, 20291463570346883, 15293680771966343, 11384953015606452
109-113  8367557574644667, 6069178325581021, 4342373612307523, 3063224801602465, 2129404050731393
114-118  1457879377824154, 982445710802356, 651236972192732, 424338518990262, 271584991070601
119-123  170597064602361, 105083809459320, 63415498329132, 37455478530387, 21628454657577
124-129  12195987096677, 6707147675329, 3592432447258, 1871182236839, 946253319319, 463747993354
130-136  219828115330, 100569643117, 44298612402, 18736763592, 7587367436, 2931796956, 1076961793
137-148  374494691, 122682600, 37652000, 10757269, 2839142, 686265, 150142, 29387, 5031, 743, 87, 9
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{27}\Phi_{2}(x)^{13}\Phi_{3}(x)^{9}\Phi_{4}(x)^{5}\\&\times \Phi_{5}(x)^{5}\Phi_{6}(x)^{3}\Phi_{7}(x)^{3}\Phi_{8}(x)\\&\times \Phi_{9}(x)\Phi_{10}(x)\Phi_{11}(x)\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\end{aligned}$$


### U15 — k=16 leaves

Order 189; period 720720; source v31/UNROOTED_MODELS.json, record 14.

$$B=2^{n+246},\quad a(n)=0\ (n<17).$$

$$a(n)=\left\lfloor\frac{B^{n-17}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 17).$$

$$R(x)=\sum_{j=0}^{171} c_jx^j.$$

```text
  0-12   1, 6, 46, 325, 2006, 11120, 55732, 255385, 1078162, 4225623, 15467993, 53177219, 172503271
 13-19   530243600, 1550091197, 4323951031, 11543298343, 29571208513, 72870608091, 173118252061
 20-25   397302021052, 882460716850, 1900253797403, 3973358761331, 8079246271276, 15997120887896
 26-30   30883028439817, 58199108506911, 107178548089730, 193081037810256, 340586729826654
 31-35   588791713690461, 998404441708997, 1661898590434923, 2717547395111829, 4368439352357859
 36-39   6907740482290307, 10751607576111190, 16481245000357061, 24895610740066575
 40-43   37076182206111736, 54464962885963258, 78956512355585740, 113004197014434579
 44-47   159740061811947329, 223106719966873582, 307998445492926125, 420407276525098849
 48-51   567568426292732459, 758097746336179864, 1002112458380048949, 1311325008936808398
 52-55   1699098792055684216, 2180453805710245115, 2772010138123081559, 3491857700104401105
 56-59   4359341862450510691, 5394756765888752651, 6618940984830945556, 8052774014646564140
 60-63   9716576522806905481, 11629422432834486403, 13808376356658985812, 16267675546343401469
 64-67   19017880931420678167, 22065026792855455281, 25409802655183251243, 29046803939341143771
 68-71   32963889271926515837, 37141682104897970032, 41553252018029698560, 46164006982105586042
 72-75   50931821670947179315, 55807419120342192380, 60735013547131968162, 65653211725261139418
 76-79   70496159029671480612, 75194905072266348865, 79678952897096764288, 83877946034087276086
 80-83   87723439402636245366, 91150694117076267945, 94100432550912055479, 96520489390861805431
 84-87   98367296430128112934, 99607144065898708054, 100217170109581922177, 100186036852805877051
 88-91   99514269278737943277, 98214240899721434027, 96309807658286934965, 93835604574341820673
 92-95   90836033032819716179, 87363978752832061141, 83479310361661633096, 79247216270001410907
 96-99   74736442269332267501, 70017494381114843807, 65160870373541701768, 60235379754018560494
100-103  55306605662696068398, 50435553901488586039, 45677524298887376762, 41081228821831047487
104-107  36688169388051554466, 32532277271318414150, 28639805400185908193, 25029455638285335350
108-111  21712715249815273453, 18694370861768827380, 15973164101375789019, 13542551100780134370
112-115  11391527806814940539, 9505484652197532058, 7867057092688356978, 6456942759478398214
116-119  5254660929077077422, 4239235560462344780, 3389788745445010925, 2686036955303888438
120-123  2108687510439657705, 1639737208653981604, 1262678734757188299, 962623389396389082
124-127  726350678601608499, 542296530276068161, 400492328094116041, 292466761317873601
128-131  211121732441069450, 150592439277946429, 106100332675271680, 73806117607558135
132-135  50668383431346461, 34311944493924091, 22908585089172224, 15071705954824340
136-140  9765369123961717, 6227460556334878, 3906114611639887, 2408165492448410, 1458172777010913
141-145  866489356842239, 504862839701431, 288161138428893, 160958463825746, 87889839693595
146-150  46859937312383, 24364202459324, 12336500387061, 6073932738872, 2903189952079
151-156  1344716809848, 602396192042, 260429367737, 108396382500, 43321707675, 16575925559
157-165  6051992551, 2100627457, 690257917, 213694647, 61991883, 16742674, 4179442, 955328, 198031
166-171  36638, 5982, 829, 100, 8, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{29}\Phi_{2}(x)^{14}\Phi_{3}(x)^{9}\Phi_{4}(x)^{7}\\&\times \Phi_{5}(x)^{5}\Phi_{6}(x)^{3}\Phi_{7}(x)^{3}\Phi_{8}(x)^{3}\\&\times \Phi_{9}(x)\Phi_{10}(x)\Phi_{11}(x)\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\Phi_{16}(x)\end{aligned}$$


### U16 — k=17 leaves

Order 208; period 12252240; source v31/UNROOTED_MODELS.json, record 15.

$$B=2^{n+270},\quad a(n)=0\ (n<18).$$

$$a(n)=\left\lfloor\frac{B^{n-18}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 18).$$

$$R(x)=\sum_{j=0}^{188} c_jx^j.$$

```text
  0-12   1, 6, 53, 391, 2579, 15090, 80095, 387580, 1727639, 7140356, 27546148, 99720095, 340406702
 13-19   1100305823, 3380297587, 9902819415, 27747388202, 74560931095, 192614057109, 479422642281
 20-24   1152096585614, 2678012276261, 6031702712472, 13184524204095, 28011026556038
 25-29   57920277890474, 116714550526340, 229472258207608, 440686798323924, 827517233629721
 30-34   1520880159547562, 2738301420952134, 4834024705223311, 8373912251540352, 14245236079608343
 35-38   23814589178668528, 39150860824124810, 63334481915070891, 100878863395848213
 39-42   158294943467226447, 244834767515635793, 373454669606013489, 562042439868422594
 43-46   834955253235243382, 1224915448095367703, 1775308722486698292, 2542923225286618938
 47-50   3601157594083432390, 5043710620048443308, 6988744371726873940, 9583486088202232217
 51-54   13009201962344176273, 17486438606586031562, 23280386346361907422, 30706174014909864957
 55-58   40133859409830489604, 51992835531167302680, 66775332806378702261, 85038665027210975337
 59-62   107405844798592853174, 134564186484540715221, 167261523807085737781, 206299698395620413982
 63-66   252525026407046699522, 306815524322777409338, 370064771796374399286, 443162408141972332456
 67-70   526971396576622985251, 622302343093490292739, 729885318793455857742, 850339799547494074596
 71-73   984143496582488379641, 1131600998295759148394, 1292813267792090196655
 74-76   1467649134618983073972, 1655719974147380047244, 1856358778294605706189
 77-79   2068604780712124494014, 2291194706335450643689, 2522561567604762196205
 80-82   2760841731125238541504, 3003890732623190721679, 3249308033784997579537
 83-85   3494470600571084916896, 3736574852632487059474, 3972686199730477818293
 86-88   4199795060017557826670, 4414877959956966422924, 4614962062806566838403
 89-91   4797191273269726353525, 4958891933122570115025, 5097636062778636268568
 92-94   5211300123990144886572, 5298117378678136385475, 5356722098058056840592
 95-97   5386184126625333625779, 5386032619784107504656, 5356268137094444067251
 98-100  5297362672318086713235, 5210247617524626351762, 5096290075878129980208
101-103  4957258336291518601491, 4795277688189904243470, 4612778068731080949406
104-106  4412435287468590964024, 4197107752785634732478, 3969770726529768225254
107-109  3733450153656510482663, 3491158055892271984442, 3245831345458819070735
110-112  3000275717108882458801, 2757116023193918129882, 2518754242282251748618
113-115  2287335829582774998023, 2064724903953173443458, 1852488394652815380313
116-118  1651888956795214246334, 1463886178324733531459, 1289145355012921593913
119-121  1128052909639861717552, 980737383587694551511, 847094834383834246930
122-125  726817432094210762705, 619424056748759586316, 524291754292132360055, 440687002114736433442
126-129  367795860143184070418, 304752230240629281492, 250663607406979131970, 204633871692001047111
130-133  165782832810358027952, 133262392709561352402, 106269329906776042259, 84054828558256115060
134-137  65930972798759563773, 51274501107291788559, 39528166764744081635, 30200079590896253322
138-141  22861413481190735878, 17142856196887470486, 12730155836928057139, 9359085531274353696
142-145  6810107720290791437, 4902974879723986304, 3491457726358722733, 2458347042066696636
146-149  1710833336040322392, 1176330915872215985, 798780573609050447, 535438384268960911
150-153  354137202967627378, 230992014846032528, 148509899150595275, 94059312814108267
154-157  58650972252733584, 35983012028878876, 21705607212360701, 12864161996817171
158-162  7484920221261668, 4271947386732500, 2389506865963863, 1308627642542002, 700969827813923
163-167  366836849871297, 187332536872950, 93229488677318, 45152165191961, 21248137936325
168-173  9699562718224, 4287230214248, 1831147022229, 754107070539, 298710002190, 113501933722
174-181  41247195548, 14287973561, 4700093408, 1462042427, 428009421, 117267675, 29881872, 7027934
182-188  1512728, 294523, 51296, 7803, 1030, 107, 10
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{31}\Phi_{2}(x)^{15}\Phi_{3}(x)^{9}\Phi_{4}(x)^{7}\\&\times \Phi_{5}(x)^{5}\Phi_{6}(x)^{3}\Phi_{7}(x)^{3}\Phi_{8}(x)^{3}\\&\times \Phi_{9}(x)\Phi_{10}(x)\Phi_{11}(x)\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\Phi_{16}(x)\\&\times \Phi_{17}(x)\end{aligned}$$


### U17 — k=18 leaves

Order 237; period 12252240; source v31/UNROOTED_MODELS.json, record 16.

$$B=2^{n+306},\quad a(n)=0\ (n<19).$$

$$a(n)=\left\lfloor\frac{B^{n-19}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 19).$$

$$R(x)=\sum_{j=0}^{217} c_jx^j.$$

```text
  0-11   1, 6, 54, 425, 2902, 17826, 98878, 501103, 2338652, 10128759, 40960944, 155540237
 12-18   557221849, 1891310515, 6104543591, 18799152280, 55398968928, 156640202336, 425982185632
 19-23   1116661557149, 2827260772257, 6926675012793, 16448820794906, 37920633437992
 24-28   84991657143812, 185447303365305, 394412591289680, 818601284275838, 1659804950819168
 29-32   3291133398318473, 6387786174838042, 12146707756076837, 22648179350006890
 33-36   41439629912578872, 74460770971940907, 131483392587185385, 228313388256804944
 37-40   390102175888324626, 656245653654245653, 1087517661029148060, 1776298142175065104
 41-44   2861020022916233712, 4546278233176600720, 7130422523438454833, 11042892826089909435
 45-48   16894048067882783894, 25540777150477918979, 38171748615862161529, 56416729571290635797
 49-52   82484952880674079200, 119337992805950205374, 170902973033787740647, 242332117655075544522
 53-56   340314599213369666217, 473446266077765225024, 652662071400125351775, 891734805400057006869
 57-59   1207841988652697473769, 1622200463695909650544, 2160765295104453131212
 60-62   2854986045662423716570, 3742609365989672996018, 4868512177130415261637
 63-65   6285544648205407886349, 8055356820625733030675, 10249177306350752415811
 66-68   12948507225242180137162, 16245687730037240855266, 20244295401184521232322
 69-71   25059316815504967787122, 30817052031846599804577, 37654696929245093140756
 72-74   45719556566557907486526, 55167846266532520719746, 66163044128435205511973
 75-77   78873768244753834118960, 93471164006945574674698, 110125801411087715090700
 78-80   129004098929958763717641, 150264308920546389495734, 174052119129221309927154
 81-83   200495945008553355632061, 229702007484299336541057, 261749309696865333735142
 84-86   296684643171233020284994, 334517767977286198142621, 375216921826624072582853
 87-89   418704818956745385833457, 464855300364994990962671, 513490792001826337351499
 90-92   564380716555593784691477, 617240987421199809780306, 671734690457376987438075
 93-95   727474030683521604431997, 784023587780671650928818, 840904887139763957193602
 96-98   897602253342710538568342, 953569871776803053145987, 1008239942981739703877229
 99-101  1061031774934784761718859, 1111361622285030793540339, 1158653050133119479756457
102-104  1202347574619364380965201, 1241915314596182632673920, 1276865378871854786822267
105-107  1306755712637942026242090, 1331202134940667796852521, 1349886316448848281562513
108-110  1362562472786834998453184, 1369062582644440350145909, 1369299980541738800499535
111-113  1363271220210192039167597, 1351056154334622097314679, 1332816228193311125791071
114-116  1308791036573590198126823, 1279293243450366434797756, 1244702010403908806201033
117-119  1205455121070583770594936, 1162040023547785607579738, 1114984039559829081026331
120-122  1064844007420347789954727, 1012195635020968834019001, 957622839041891695063166
123-125  901707337664494810585200, 845018746781618164692790, 788105405038939837605243
126-128  731486122081189879251688, 675643008564919354623277, 621015507254124162324800
129-131  567995703477068786004495, 516924951878339814395641, 468091816313065710890966
132-134  421731282194003829351169, 378025166867188562864318, 337103624558480421826697
135-137  299047618880363814818237, 263892218212943463229763, 231630557722846937769824
138-140  202218306244025088407657, 175578476470982469463456, 151606422363542094850214
141-143  130174877715323994281353, 111138903668083993017069, 94340629735370017691381
144-146  79613691694684816544945, 66787289658501105582165, 55689809860304349607714
147-149  46151973450042617651644, 38009494186952716243972, 31105243823168346782876
150-152  25290938748112495674530, 20428373850360057170582, 16390239380160480507258
153-155  13060563851901830847856, 10334830776078701343416, 8119819441838300621302
156-158  6333220315024488180561, 4903074180646112202600, 3767081259209026101480
159-161  2871822512130926310512, 2171930548135302738300, 1629242272478424779256
162-164  1211959961355264344238, 893842045784788646412, 653439748443248507773
165-168  473390992755474661846, 339778801458905603212, 241557791901270301827, 170049382831303838455
169-172  118503950599049789986, 81726378530406159026, 55760183064431657285, 37624608312053701818
173-176  25098686584137019407, 16546190651312787128, 10775582325280289678, 6929422862233678724
177-180  4398193897775280356, 2754030832186127684, 1700451844875036036, 1034741579056572224
181-184  620195005256562389, 365927380979930812, 212401079263882851, 121205006195959543
185-188  67947525971974688, 37392265568480742, 20183073357648440, 10675957564524704
189-193  5528773250006336, 2800337297334727, 1385716424694181, 669122326731495, 314880783529621
194-198  144208665428345, 64177598820218, 27708019926666, 11584408799874, 4680900622341
199-204  1824011726778, 683794732086, 245963066804, 84639943624, 27772174148, 8656864554
205-214  2552790597, 708755219, 184270837, 44577016, 9961803, 2037626, 377821, 62495, 9137, 1128
215-217  121, 9, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{33}\Phi_{2}(x)^{16}\Phi_{3}(x)^{11}\Phi_{4}(x)^{7}\\&\times \Phi_{5}(x)^{5}\Phi_{6}(x)^{5}\Phi_{7}(x)^{3}\Phi_{8}(x)^{3}\\&\times \Phi_{9}(x)^{3}\Phi_{10}(x)\Phi_{11}(x)\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\Phi_{16}(x)\\&\times \Phi_{17}(x)\Phi_{18}(x)\end{aligned}$$


### U18 — k=19 leaves

Order 258; period 232792560; source v31/UNROOTED_MODELS.json, record 17.

$$B=2^{n+332},\quad a(n)=0\ (n<20).$$

$$a(n)=\left\lfloor\frac{B^{n-20}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 20).$$

$$R(x)=\sum_{j=0}^{236} c_jx^j.$$

```text
  0-11   1, 6, 62, 503, 3655, 23560, 137684, 732971, 3593135, 16326653, 69229270, 275414472
 12-17   1033036142, 3668564226, 12381139240, 39842720389, 122618797839, 361866733230
 18-22   1026548875350, 2805496108557, 7401444555444, 18884478578982, 46678453176106
 23-27   111952886152338, 260912827251649, 591677882175982, 1307231780464193, 2817135628991740
 28-31   5928266554144731, 12194352144332278, 24542510664124339, 48372772769887943
 32-35   93448767881669159, 177085856417202378, 329426759031426692, 602014545894117212
 36-39   1081482256994987904, 1911046765553429947, 3323709571131516158, 5692737370533033245
 40-43   9607251043513547140, 15983745857438169876, 26228271976363863715, 42469013218106400047
 44-47   67885314272250056864, 107167022454549926218, 167147515459282586378, 257665133414967194309
 48-50   392721018000103418847, 592016595042635440430, 882971018473865634187
 51-53   1303337573068416743786, 1904557883000365267482, 2756013151101008000021
 54-56   3950351681620986619329, 5610090477330295585539, 7895704345696403473247
 57-59   11015427027241817248935, 15236993465284831326811, 20901548359741200999566
 60-62   28439931353130224093568, 38391521297717789425978, 51425778842225667861402
 63-65   68366566042332949007824, 90219242202249118272627, 118200435569009414218590
 66-68   153770270422229307364900, 198666688982057362134928, 254941348910563356983604
 69-71   324996402669778107240936, 411621278593514081476322, 518028390497980522491821
 72-74   647886509630376745038786, 805350347576174734433738, 995084730404550968207867
 75-77   1222281602632414140326409, 1492667994951391496864625, 1812503032608738038189738
 78-80   2188562062162798159870369, 2628106042459469129793802, 3138834489246178816199761
 81-83   3728820487988246311207257, 4406426599958590021113983, 5180200883231853541390824
 84-86   6058752730258818184755713, 7050608780799874199964355, 8164049792973831422204730
 87-89   9406930031742278010718803, 10786481445391932210688411, 12309105624936330391415398
 90-92   13980157254539326991070758, 15803723436328652295304426, 17782403882474871060230839
 93-95   19917097482755951951763725, 22206801149701951335080934, 24648427090261993737740271
 96-98   27236644730756151103195830, 29963753412787286653943520, 32819591669765460998045390
 99-101  35791488380807690509196546, 38864260382621006868083321, 42020260209396893933885292
102-104  45239476542778916110197634, 48499688712864524864525349, 51776675228810285833149626
105-107  55044474871640354568907283, 58275697395700727937160461, 61441879405539478876925153
108-110  64513879551171338909618773, 67462305865864450312900308, 70257966904919073585296826
111-113  72872337375514297095488902, 75278028215964557524462445, 77449250619445275387961563
114-116  79362263326350396477877394, 80995792644635992667633208, 82331415102702806419500555
117-119  83353893387060201622801595, 84051457249571116302807410, 84416022357949175986441397
120-122  84443341571108137817292158, 84133084801952732092650679, 83488845432493828831371679
123-125  82518073112813654087021153, 81231934647706466943013417, 79645106493190438500883792
126-128  77775504092630830263776992, 75643954825490510919617406, 73273822674061060439604351
129-131  70690593795366692293533365, 67921432987042117378009486, 64994721537105517306405924
132-134  61939587139283506741736627, 58785436439180665706808732, 55561500364572017018139485
135-137  52296401707055496734587329, 49017753493189368307984303, 45751795548710749720682909
138-140  42523075363387081511219260, 39354177953640813856717867, 36265507944942983339775435
141-143  33275125605184233769535714, 30398637101603923875439600, 27649137871169261323046208
144-146  25037206726866358919320961, 22570947202875829563051020, 20256071696171619550734390
147-149  18096023208780807250852223, 16092128944477507647967681, 14243779668648068985647645
150-152  12548628596155871764985871, 11002803617959445218492649, 9601126896343176740538323
153-155  8337336229250894193116358, 7204303081548266966970124, 6194242777685554784069822
156-158  5298913018030271833290854, 4509797591767818989507610, 3818272885825206194017980
159-161  3215755506697827738379026, 2693830018345923841093195, 2244356435654089537867975
162-164  1859557684452232886593399, 1532087734680323187742918, 1255081525953967449452826
165-167  1022188131188344199927032, 827588844319607342217301, 666002035711455595547852
168-170  532676699426669801075921, 423376627969608388698516, 334357101720201871740430
171-173  262335882250882016455993, 204460161679949278675229, 158270954637041096382841
174-176  121666235341212093648685, 92863928875490390982795, 70365671122672224057565
177-179  52922062855715940576606, 39499965720214558689884, 29252225490043086678506
180-182  21490063940164361598785, 15658256646665854495116, 11313110633387105922890
183-185  8103172740442074551031, 5752535878246427106836, 4046564356626158573977
186-188  2819829273184849490646, 1946028293596076785096, 1329658764502733914351
189-192  899216689048863164592, 601704517060975175343, 398245991016559225806, 260624723639741915931
193-196  168583299751314190262, 107740306061602704538, 68002870276618527144, 42371356052328336955
197-200  26050349939244664534, 15795716871260128111, 9441170217145925728, 5559500923316282774
201-204  3223425577461072704, 1839094824785905598, 1031836981344252814, 568900130270033359
205-208  308004058021579532, 163616829185132310, 85208407724274895, 43463586455860658
209-213  21693733176418619, 10584103164974996, 5041913878616562, 2342234481485219, 1059712632604712
214-218  466283737408202, 199225674679432, 82516772855841, 33070680521882, 12798962002181
219-224  4772854341743, 1710793214620, 587847849760, 193056873866, 60396646804, 17932093784
225-234  5031661685, 1327979741, 327857593, 75247043, 15933837, 3087015, 540872, 84784, 11596, 1383
235-236  129, 11
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{35}\Phi_{2}(x)^{17}\Phi_{3}(x)^{11}\Phi_{4}(x)^{7}\\&\times \Phi_{5}(x)^{5}\Phi_{6}(x)^{5}\Phi_{7}(x)^{3}\Phi_{8}(x)^{3}\\&\times \Phi_{9}(x)^{3}\Phi_{10}(x)\Phi_{11}(x)\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\Phi_{16}(x)\\&\times \Phi_{17}(x)\Phi_{18}(x)\Phi_{19}(x)\end{aligned}$$


### U19 — k=20 leaves

Order 289; period 232792560; source v31/UNROOTED_MODELS.json, record 18.

$$B=2^{n+370},\quad a(n)=0\ (n<21).$$

$$a(n)=\left\lfloor\frac{B^{n-21}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 21).$$

$$R(x)=\sum_{j=0}^{267} c_jx^j.$$

```text
  0-11   1, 6, 64, 548, 4124, 27869, 169935, 946432, 4851635, 23072192, 102415237, 426734765
 12-17   1676969840, 6241715611, 22084993606, 74531524498, 240607824009, 745004965187
 18-22   2217833905531, 6361601549498, 17617150538021, 47187748260848, 122454929343424
 23-27   308354196627018, 754524153154426, 1796489276639745, 4167183191010069, 9428205750791558
 28-31   20828264425383114, 44973202328695624, 95004241440784630, 196520255991188773
 32-35   398391859414167912, 792127083754746461, 1545907256857754043, 2963336514081813671
 36-39   5583101153914896405, 10345213630597665350, 18863872402881012060, 33868358676758260106
 40-43   59904752927854237016, 104436525304168410459, 179546413649509757360, 304532146367531744982
 44-46   509812989559353910269, 842733386844035268484, 1376077054876564861035
 47-49   2220405311657876515985, 3541725347456341469715, 5586498492259047619054
 50-52   8716638656332164768283, 13457952457570590796806, 20566461830771959157316
 53-55   31118254124955705654577, 46629949519261230568336, 69218583557738085589409
 56-58   101811690607083224712688, 148420650612102847498525, 214492923429069115676604
 59-61   307361623869511770442429, 436813948800145253745877, 615803194877098725485843
 62-64   861332414596157751741515, 1195541032524104992872934, 1647028833317087557669612
 65-67   2252454455291017174399384, 3058447660230507582058455, 4123875952126540584607359
 68-70   5522506305467633584482148, 7346101536180990060609373, 9707987888674916375326945
 71-73   12747125401647579981056845, 16632705243701252253308447, 21569288195602714111843806
 74-76   27802485561095903887165331, 35625167841202369880426151, 45384167420830144119908511
 77-79   57487419313821778477124315, 72411458840980517755459030, 90709167271842508483026639
 80-82   113017626399494586051111647, 140065911368657255157009824, 172682618642860231168029442
 83-85   211802893758496211894186144, 258474692612372640422557540, 313863981757381196804203170
 86-88   379258558941020187609728383, 456070156404657438119097035, 545834477783954077483477777
 89-91   650208816318168899751329073, 770966908901233165893078564, 909990698567031379057978933
 92-94   1069258708341547130450799840, 1250830772788834807480774638, 1456828930430663802484773052
 95-97   1689414350538179866314499853, 1950760251101220697678653660, 2243020860115640417221378390
 98-100  2568296578180607933666308264, 2928595614746540441527485331, 3325792490637954264737046215
101-103  3761583922679118872464220830, 4237442728909625546473451338, 4754570511220411367050401040
104-106  5313849982227764756899139404, 5915797900714153504701153275, 6560519660864965570720998181
107-109  7247666640894306439026489612, 7976397452835551612966839120, 8745344244150720181634057561
110-112  9552585180840462377827355621, 10395624189178696040826970858, 11271378948141646934571894587
113-114  12176178007166638431920774207, 13105767755152369006112375421
115-116  14055329788816426564965539806, 15019509024864708306336744817
117-118  15992452675185553780981109037, 16967859962594788040248281707
119-120  17939042202534654991871446832, 18898992620139945147362330355
121-122  19840465019326128547967066055, 20756060178275119678851510982
123-124  21638318621226711520659782292, 22479818216829100039556531642
125-126  23273274885064509109264274024, 24011644563735455034979375927
127-128  24688224496618601777688137961, 25296751862384143156843105875
129-130  25831497768769170364117122095, 26287354691310667066824221450
131-132  26659915539847177321648796013, 26945542687054184857133610548
133-134  27141425488204086171449184864, 27245625055377167002677852217
135-136  27257105316607796349902413551, 27175749683876287661799110652
137-138  27002362965668870941611016738, 26738658481541300800029816848
139-140  26387230659041985941462238425, 25951513708633814442881846291
141-142  25435727271412492643819348258, 24844810209373056971303253218
143-144  24184343951531299972075842383, 23460467015059620399603740546
145-146  22679782483745957451321005919, 21849260342757949540748872445
147-148  20976136636666556546664678150, 20067811436106585235962034729
149-150  19131747568065728401723465420, 18175371987660522686734604939
151-152  17205981548864857167476848314, 16230654772568667217959357474
153-154  15256171018219716638435277734, 14288938246485482945912633763
155-156  13334930321857982405228397885, 12399634553122585036382067237
157-159  11488009913488972115922340418, 10604456128046354520162307739, 9752793570856127918913066889
160-162  8936253683560608361329784914, 8157479417313414133674953658, 7418535014601657306665567890
163-165  6720924290691196261178650782, 6065616448422786465860194284, 5453078366358982535354768511
166-168  4883312239156247120864884297, 4355897419910528997197723802, 3870035315527394162345919409
169-171  3424596215590355314740119975, 3018166989716046408262258127, 2649098664497630523065515567
172-174  2315552984939802611785960975, 2015547172706387871995690191, 1746996210357299653149576359
175-177  1507752102988145121327963747, 1295639692413102492369529770, 1108488720709607524285249632
178-180  944161956399930464330814157, 800579305106963310667479641, 675737924998495039475453092
181-183  567728454094408670926106035, 474747530430578465936855050, 395106846565059273849804265
184-186  327239026847166944406054847, 269700649569221494938316433, 221172757258503985088957642
187-189  180459207940555843466237965, 146483219432951002558419004, 118282449010534106090964529
190-192  95002933604699011294700277, 75892192593990353777875143, 60291767713404482719127883
193-195  47629444097535972862134575, 37411364302565223735956868, 29214214516137369649307424
196-198  22677630086434048355060485, 17496936838741233920868792, 13416316072905684213632428
199-201  10222455151901124304826703, 7738722534303352303322262, 5819886158484808809982966
202-204  4347377303658762254518456, 3225088372016890201853174, 2375682301853714191313474
205-207  1737383309961188662086265, 1261213096647055831948893, 908633222868081219620111
208-210  649552764745125204258386, 460660246179264659367835, 324039936425062338706961
211-213  226034589532056795895542, 156319336873346446224922, 107154495679799059899371
214-216  72788332351321809928382, 48984161023558368294781, 32649439945907281732959
217-219  21547656393659559793265, 14076698226235617716825, 9100054226332069759810
220-222  5819543394411079236221, 3680339263890599045078, 2300835349340191079250
223-225  1421407676406032029161, 867391763142273933646, 522630013522583590579
226-229  310788436144143016145, 182316200687023048254, 105453903622184183968, 60110713956550323182
230-233  33748507844588591855, 18651686626686436666, 10140852063822165860, 5420493549016546482
234-237  2846481484657399067, 1467440175960061673, 742080142757797693, 367800185989044650
238-241  178505031026866810, 84750997476706480, 39322621510218127, 17809702864940829
242-246  7864351957894081, 3381387264463135, 1413642714782250, 573762810136749, 225709666754710
247-252  85902310846153, 31567088211249, 11176199124641, 3803146174677, 1240602177154, 386800359020
253-260  114891276351, 32392011116, 8632790621, 2164597238, 507933573, 110838118, 22334288, 4117520
261-267  688182, 102556, 13524, 1500, 148, 9, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{37}\Phi_{2}(x)^{18}\Phi_{3}(x)^{11}\Phi_{4}(x)^{9}\\&\times \Phi_{5}(x)^{7}\Phi_{6}(x)^{5}\Phi_{7}(x)^{3}\Phi_{8}(x)^{3}\\&\times \Phi_{9}(x)^{3}\Phi_{10}(x)^{3}\Phi_{11}(x)\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\Phi_{16}(x)\\&\times \Phi_{17}(x)\Phi_{18}(x)\Phi_{19}(x)\Phi_{20}(x)\end{aligned}$$


### U20 — k=21 leaves

Order 320; period 232792560; source v31/UNROOTED_MODELS.json, record 19.

$$B=2^{n+411},\quad a(n)=0\ (n<22).$$

$$a(n)=\left\lfloor\frac{B^{n-22}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 22).$$

$$R(x)=\sum_{j=0}^{296} c_jx^j.$$

```text
  0-11   1, 8, 88, 806, 6617, 48331, 319545, 1925820, 10681304, 54900356, 263206952, 1183460878
 12-17   5014679107, 20108908651, 76596497303, 278060570993, 964862661371, 3208798745268
 18-22   10252165497392, 31538021420662, 93597853030226, 268475330070112, 745556968504903
 23-26   2007566159083566, 5249236575312160, 13345647877524263, 33032413560708686
 27-30   79689629431874064, 187583718161380764, 431282176493756887, 969426680976836411
 31-34   2132282336338113655, 4593218638691594897, 9697897464629532563, 20084089245529378227
 35-38   40827134348416011041, 81519100041696989139, 159977790959299002352, 308753326945792155330
 39-41   586359104442763937996, 1096356435799066998378, 2019297462673456493405
 42-44   3665411502316776071324, 6560279900056321687097, 11582249417318520532628
 45-47   20179904711943455209876, 34711810442025642412574, 58970625544472583929933
 48-50   98981810981283903661507, 164206395888971084820658, 269331355692378831362820
 51-53   436904793692735417962989, 701172164774480364345559, 1113601423731916589832583
 54-56   1750757898739715233754977, 2725414187609031812214618, 4202068478205178074110331
 57-59   6418410185267907509337844, 9714730148426271405757036, 14573840842060509598807341
 60-62   21674768291604672777135237, 31964320548663265755048653, 46751646507739129303233363
 63-65   67832091451695859786607728, 97648047744639511984392274, 139496102702502314656552147
 66-68   197791607705639272572495763, 278403832652754590037835428, 389077118048681866576971566
 69-71   539955871795150328591610092, 744233843427329032729954558, 1018950792958033184142231151
 72-74   1385962383844832482448925126, 1873111778514272228480073626, 2515633887011749889687255891
 75-77   3357825378578919715250147750, 4455015253468640104111643524, 5875871807626953099864381760
 78-80   7705082006175689811765948648, 10046438397340223868018267417, 13026366520352632839584807163
 81-82   16797922058656304752761684092, 21545281537344726949873958567
 83-84   27488742948926630872999524375, 34890243126869603471376305340
 85-86   44059386821661613863588540784, 55359968169178717930336274953
 87-88   69216948539298807250427934927, 86123835654158892686152722751
 89-90   106650387499920771378035090832, 131450541153972675241697049513
 91-92   161270441551939618792190570636, 196956418883366719555160797299
 93-94   239462736309206069082253884263, 289858902735269424694465994746
 95-96   349336319264309173568916057512, 419214003599203802428222898089
 97-98   500943115081714863843258990220, 596109985291759598492889967733
 99-100  706437346305663289169895448731, 833783441929001525984259149127
101-102  980138707560046760196859541630, 1147619712811614700706746567818
103-104  1338460078515443384024533660056, 1554998106987810841965902253473
105-106  1799660901977491356609279627479, 2074944802830404316300368690709
107-108  2383392016086910921589037830704, 2727563396656459526751969240044
109-110  3110007409224251058011722881546, 3533225387608626366411211961892
111-112  3999633304011390349498083905784, 4511520359730524690037039073707
113-114  5071004811837549812073406295295, 5679987554152358629107664668774
115-116  6340104072905013750599016853107, 7052675494880765854703369371456
117-118  7818659535592132793177083362804, 8638602234050002866194181924904
119-120  9512591425993404298936540618628, 10440212956100073368150435619134
121-122  11420510659088178666676649834550, 12451951147420053992953134858465
123-124  13532394427649267180816265800277, 14659071326950738994434275010906
125-126  15828568645275485436266423931053, 17036822856774054896167085064964
127-128  18279123067240399830434197383692, 19550123793679319808975534075763
129-130  20843867969771980110546745067209, 22153820399800455312659333200265
131-132  23472911686963862463305588053348, 24793592454053860753287138913970
133-134  26107897459752417816088540357910, 27407518997373911689047409375547
135-136  28683888749979647812375900508314, 29928267071864842546677839419413
137-138  31131838476857788850105960729835, 32285811943904759136146203308346
139-140  33381524504934001283729018957057, 34410546463401908320081162947157
141-142  35364786507996024322100079631604, 36236594937715439529114110787273
143-144  37018863204113470879682577039616, 37705118005062919949003268695684
145-146  38289608232174496349561044386194, 38767383180113524850892277243025
147-148  39134360568637786623779574277265, 39387383104346370034626338752678
149-150  39524262515085981522769910454679, 39543810221079619148021748169944
151-152  39445854057790018359560567769552, 39231240730415902933642238990104
153-154  38901823952457250507190506407892, 38460438494474213923967352641670
155-156  37910860637467344015506137330794, 37257755781841314608974026278243
157-158  36506614201629588808518568273592, 35663676149004993614302200802408
159-160  34735847701187544733666942318583, 33730608896580568076154597182746
161-162  32655915826107786180838053060961, 31520098427049625531533883659811
163-164  30331755768969261016277017763608, 29099650624398263715416796093385
165-166  27832605081660095213940541238827, 26539398885365264746295853093702
167-168  25228672084433839849178471114645, 23908833431509941867113448648506
169-170  22587975815528950625787700630192, 21273799825722773627435361357799
171-172  19973546345632819869915758550442, 18693938865107999424182323356789
173-174  17441135982232481525953404631243, 16220694351008902913931280663938
175-176  15037542119540647022994373195182, 13895962702171057955838673674682
177-178  12799588541825144828470096306560, 11751404349358298642063501697592
179-180  10753759158089202198246651094938, 9808386406216035252130618271941
181-182  8916431159086586537878828409198, 8078483508175487926272191330525
183-184  7294617134256287809137173711120, 6564431998102505494047040231785
185-186  5887100121946791257832584252179, 5261413447157814242872399433832
187-188  4685832795982766941658841904997, 4158537025201326359329557586621
189-190  3677471534324666131541950646041, 3240395377559663558345045729942
191-192  2844926324079637326908726165982, 2488583312155067268337891906395
193-194  2168825846462687194559833413618, 1883089991652423217003934562385
195-196  1628820716497129926792005716893, 1403500439464331985157566741940
197-198  1204673716449860389330580375480, 1029968093175316554689729052077
199-200  877111217217236343075116715368, 743944367014094965264346008045
201-202  628432607048889149653941433725, 528671819620774545898554339094
203-204  442892894388601469752716598451, 369463377643216750256147809274
205-206  306886894714895132557140915445, 253800661893777630204176841855
207-208  208971399711933452126361686854, 171289948469484939427412950280
209-210  139764870592662302392606862478, 113515303903505879907054490623
211-212  91763306246125093678401756139, 73825906182960832540778042471
213-214  59107047595740329080781434212, 47089588850474807572615213740
215-216  37327490453406218257693977279, 29438299456300406552718254223
217-218  23096014765065195132829210430, 18024395346568567745005887832
219-221  13990753382574322449845707064, 10800256849920678820433517103, 8290750881424628330899551724
222-224  6328094569837988912970537225, 4801999536421013687563068028, 3622348460374219538229844334
225-227  2715965677901256988262140989, 2023807703474555594098844139, 1498538876857266495100010146
228-230  1102456066269116041187691126, 805726230938452840631903035, 584901444039064643883901651
231-233  421677492888866038629177331, 301864218983681216394834837, 214538168837100273419790610
234-236  151350753237748836691192483, 105967835982575632807781271, 73619394459645643218374481
237-239  50740535942524977596642198, 34687656898829842845067896, 23515857120153596666622234
240-242  15805840160843257772365647, 10530433130869520582508975, 6952539252961216650447696
243-245  4547800686155992294436230, 2946507805193377401505723, 1890359414739480914742129
246-248  1200573865474774163741433, 754592624376795950422147, 469224708445950604029720
249-251  288571182873342053256928, 175461235170862898929478, 105441291078564664176450
252-254  62600682079753666866819, 36704182712954019245960, 21244219317904089376345
255-257  12132937142278152759751, 6834272297860142116335, 3794986394119097255750
258-260  2076341030361207747123, 1118727063697095957806, 593252649340127508431
261-264  309445343261464849305, 158664571658238338783, 79916018809283591682, 39512396068664708652
265-268  19162245923316605335, 9107919006968735482, 4239104954614053810, 1930225984583290514
269-272  858992868341196042, 373212134662850930, 158128436277048317, 65255596557392672
273-277  26194069998911055, 10212763156329132, 3861577427214588, 1413631187478326, 500105430243766
278-282  170636812210909, 56029793997598, 17662675589141, 5331310857383, 1536304507210
283-289  421277415247, 109526957598, 26887376750, 6203358397, 1337920909, 268094605, 49546952
290-296  8374195, 1280146, 174903, 20907, 2159, 176, 13
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{39}\Phi_{2}(x)^{19}\Phi_{3}(x)^{13}\Phi_{4}(x)^{9}\\&\times \Phi_{5}(x)^{7}\Phi_{6}(x)^{5}\Phi_{7}(x)^{5}\Phi_{8}(x)^{3}\\&\times \Phi_{9}(x)^{3}\Phi_{10}(x)^{3}\Phi_{11}(x)\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\Phi_{16}(x)\\&\times \Phi_{17}(x)\Phi_{18}(x)\Phi_{19}(x)\Phi_{20}(x)\\&\times \Phi_{21}(x)\end{aligned}$$


### U21 — k=22 leaves

Order 353; period 232792560; source v31/UNROOTED_MODELS.json, record 20.

$$B=2^{n+452},\quad a(n)=0\ (n<23).$$

$$a(n)=\left\lfloor\frac{B^{n-23}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 23).$$

$$R(x)=\sum_{j=0}^{329} c_jx^j.$$

```text
  0-11   1, 9, 97, 943, 8075, 61910, 428578, 2706133, 15714944, 84558551, 424256790, 1995875871
 12-17   8846235422, 37097101169, 147739688039, 560622337371, 2033044276858, 7064546485355
 18-22   23579205982949, 75758634365462, 234779689130457, 703086945715733, 2038020320245791
 23-26   5727081950880555, 15624569134325291, 41439271347626114, 106975695311479031
 27-30   269110401966320767, 660418055283376335, 1582674191019503061, 3707338306629368220
 31-34   8496112945029187624, 19064799539875304171, 41922172916250785993, 90402681850860023286
 35-37   191316946156646989577, 397605401532200599080, 811997366789015796909
 38-40   1630508359371044222001, 3221119102741413275007, 6263870575142993813158
 41-43   11996548722113879554133, 22639243030182998586819, 42117621429007529186975
 44-46   77278186167302224153157, 139902988526335167147275, 250006599166730473939981
 47-49   441163787261434073694939, 769013861821110319675128, 1324675143608382884205108
 50-52   2255661051884257233442103, 3798127770882501798613930, 6326050783729955308334348
 53-55   10425421485202561561328101, 17005035985841122098061938, 27460254787570312518057258
 56-58   43912679506313224717226427, 69557573888010648013501578, 109162744236855462422457832
 59-61   169778348030906550299806295, 261737770183614608864772216, 400056564473779793807894206
 62-64   606371018413780145032347627, 911601946568169936257033409, 1359584919451215982598952937
 65-67   2011977658454429113013966068, 2954841433645209279307944838, 4307398933869284065320885241
 68-70   6233599428821338595678253490, 8957276495119494932278252519, 12781867628826302565919988043
 71-72   18115882210559255561180121584, 25505557874961106221143204657
 73-74   35676438383109318925031643979, 49585941072953378504902537901
 75-76   68489360526538424584123056954, 94022177792047162862577239597
 77-78   128302010440967409983720719033, 174054045232147006360631993726
 79-80   234764337320590672460808808415, 314865930347142941894446652290
 81-82   419963339985384357421557760191, 557101535910978975333419290846
 83-84   735086136391164807510140692465, 964862074610648701398825627616
 85-86   1259958481299331634304491897548, 1637007925028176780325308990303
 87-88   2116348426612255438921004127747, 2722716780719151363047324538785
 89-90   3486041636228182313666546011780, 4442344464919587267142942254333
 91-92   5634755942029314884584364172762, 7114654328140014741932403271967
 93-94   8942931136988454811451346118013, 11191387658041108821087043555450
 95-96   13944263740761142300368153035778, 17299897610685586229668742194693
 97-98   21372512355927559519444713681309, 26294121087782002925387833558744
 99-100  32216538645343338715012486416004, 39313483101531735613954567663028
101-102  47782745274248214293230238054812, 57848399008321825397576488120229
103-104  69763019248817197026138692601588, 83809868972913163997150290323447
105-106  100305010006449046882446234081295, 119599286764226857266918863430267
107-108  142080126182347649899489462145392, 168173091736623922944672512719970
109-110  198343124659297980623805921777707, 233095401484542730847646505593004
111-112  272975734086384669595874183619365, 318570436637462340008650305387626
113-114  370505583625812411663071722113568, 429445584420986516808957134205356
115-116  496091003063254369720666347234790, 571175557117583630795044588152576
117-118  655462236711148295797497217890338, 749738494341978313506779842038565
119-120  854810467741679231570935510908896, 971496211977205264336850443775471
121-122  1100617933005999492210092045865430, 1242993232912081909799695006749309
123-124  1399425396838035786925848432751938, 1570692772912097616083419850131266
125-126  1757537318907140386765152585403061, 1960652412552473185661238068998306
127-128  2180670045885336385096474476927531, 2418147547261536982760085352243239
129-130  2673553997087741905604135485746161, 2947256524406145670966322540901524
131-132  3239506690554317515646381749192431, 3550427182636883077480093099095390
133-134  3879999052894447725867445195490568, 4228049749684169817793628957316253
135-136  4594242191190463800329044674581277, 4978065133724819194935665863983768
137-138  5378825082194928106415009788398346, 5795639980767467358107418080879319
139-140  6227434906769493595831072840048665, 6672939970446208259314090872443994
141-142  7130690597423952225782709849606134, 7599030339858167727912746323058492
143-144  8076116326654994919198948911789043, 8559927423354916098712953460600038
145-146  9048275128898489032297884003172452, 9538817190316999880449227604945092
147-148  10029073868268455842547188940594433, 10516446737222323628020722553510782
149-150  10998239855001790601160598992774236, 11471683088380173937012057203275559
151-152  11933957335576235026443467354244358, 12382221343870215991039273148954199
153-154  12813639782200309455276524377448641, 13225412195465630095779374146929157
155-156  13614802440233273704886798369652996, 13979168181384482365644206455228708
157-158  14315990016560556618467644421958292, 14622899790547356650652281732056755
159-160  14897707665258948313679795903494797, 15138427522852400756529085786894770
161-162  15343300299641980409916467906297321, 15510814876604433542055820661525486
163-164  15639726187911247325180537244513775, 15729070251442247724338291677287701
165-166  15778175873814981792274978561102004, 15786672836145667181353800788134129
167-168  15754496424454587771817032974204638, 15681888229157191705599590305125168
169-170  15569393200187282936402790255127192, 15417853006686935019539965269463887
171-172  15228395811568369314888389751753342, 15002422630330462416234572884385323
173-174  14741590499077919412256308753657243, 14447792727612222521160031019243515
175-176  14123136558722080973315689078956710, 13769918593517426514424542713772939
177-178  13390598374103862856151088081101642, 12987770538537324954208954275183802
179-180  12564135978470675367657832217036940, 12122472437035897032516884752861884
181-182  11665604983320810394584611459295693, 11196376790509458108098903033383780
183-184  10717620627751124804805883731660602, 10232131451660351365707924772410720
185-186  9742640452732728680449815711021886, 9251790875718412798754810016022978
187-188  8762115892059099683808383627521356, 8276018757872688081676436070626170
189-190  7795755443719984058304971364494351, 7323419873587689969466043377244478
191-192  6860931861243603001042721254241883, 6410027783403184276524052594619210
193-194  5972253981974639125882804338337962, 5548962842927132582430462556200608
195-196  5141311457861228845908696358214724, 4750262736846808073265263700209666
197-198  4376588808101773975123887300458456, 4020876512052569467940646336050599
199-200  3683534774546166305506807801215432, 3364803626637455717928991112916343
201-202  3064764626487349931271717054528285, 2783352432380575539488181522708288
203-204  2520367274496737371034517291700891, 2275488076528202509858724108798574
205-206  2048285986128346023226539351089025, 1838238085014447910653939659542165
207-208  1644741064804721497426984521240217, 1467124672762495804360187329582198
209-210  1304664751953780876099184609428448, 1156595722292613514549312436820449
211-212  1022122371956563710590138264453139, 900430852131144618900352293546896
213-214  790698791451351501919721256854275, 692104469362585263320661028983308
215-216  603835009488333786330533642221583, 525093574596080093288143213271244
217-218  455105563589284458150192276649295, 393123827882595440456094671240703
219-220  338432939367607146409208076845277, 290352554840796097428172231791402
221-222  248239932198903553695765711333375, 211491661922119509510638472672626
223-224  179544683425114976044654859402978, 151876659867597882490643747640942
225-226  128005787123827611050640291913222, 107490112987841857548659252749993
227-228  89926441533055760451778611877661, 74948895060585998243312622590148
229-230  62227202476482452395810512426454, 51464778451071578052848012762158
231-232  42396652545847576062164780214275, 34787301846830128243735560335721
233-234  28428434706021437946128509624801, 23136767135261691883313612346118
235-236  18751827370542610903521936029583, 15133818259778321465158007015382
237-238  12161561531490574552383524516354, 9730542762455963640836630456364
239-240  7751071044620272491326149472763, 6146563001127933137867725890303
241-242  4851956945430646957916895042487, 3812259626983475307411781553177
243-244  2981225158542699162177510318561, 2320163357987830461953425672110
245-246  1796872836507813493234996895411, 1384692691908608739623095741523
247-248  1061665582196393856287951407274, 809804218386802974935863441897
249-250  614452882795591762916153497646, 463735405707414305025730539064
251-252  348081076132336204787065453651, 259820180234461797919109049867
253-254  192841215708494031914412311581, 142302287091913231499485516087
255-256  104389714762542305985421879286, 76117462231570943220981639246
257-258  55161579399724503786466759331, 39724454749209145269185108023
259-260  28424251791386173614738906489, 20205462733951559118883493418
261-263  14267036643559673948350631250, 10005024474897087366916936799, 6967125683281950215741409874
264-266  4816919169253948183252744968, 3305915048649163617925552358, 2251874475477301600956474499
267-269  1522114674651632972207166237, 1020748328226769677455102658, 679003778019824818818677178
270-272  447938650069910148727422984, 292998016333060831874076286, 189982557357005468089170575
273-275  122085680501512371295273118, 77734252953932548467985077, 49028324528684057506122180
276-278  30623443519941805839778532, 18937109974606780686163472, 11590470501893645723861030
279-281  7019164243768479133495553, 4204651035681444061693514, 2490528639406241958316595
282-284  1458210217422445252711304, 843642514452434983735058, 482104802983869329259493
285-287  272016859693074472715117, 151474454037643261724983, 83210967209712679361590
288-290  45073119278393620678900, 24062344664527231947043, 12653693689872666621888
291-293  6551171478866517611604, 3337279918777065607043, 1671758413126314443546
294-297  822964505587967925502, 397848659420321584499, 188741759472973022160, 87800205003485851827
298-301  40016849959355175936, 17853725654611068451, 7790159170994479000, 3320932135128579962
302-305  1381667590620360092, 560372359580928323, 221279691155623482, 84960844709789180
306-310  31672565891847115, 11446125040292345, 4003235546725261, 1352520704564712, 440542242559525
311-316  138035697758514, 41506127518872, 11945400575481, 3280841526537, 857140752687, 212236527853
317-324  49603294653, 10891896242, 2235075156, 425985192, 74867490, 12028051, 1748558, 226801
325-329  25871, 2515, 209, 12, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{41}\Phi_{2}(x)^{20}\Phi_{3}(x)^{13}\Phi_{4}(x)^{9}\\&\times \Phi_{5}(x)^{7}\Phi_{6}(x)^{5}\Phi_{7}(x)^{5}\Phi_{8}(x)^{3}\\&\times \Phi_{9}(x)^{3}\Phi_{10}(x)^{3}\Phi_{11}(x)^{3}\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\Phi_{16}(x)\\&\times \Phi_{17}(x)\Phi_{18}(x)\Phi_{19}(x)\Phi_{20}(x)\\&\times \Phi_{21}(x)\Phi_{22}(x)\end{aligned}$$


### U22 — k=23 leaves

Order 378; period 5354228880; source v31/UNROOTED_MODELS.json, record 21.

$$B=2^{n+482},\quad a(n)=0\ (n<24).$$

$$a(n)=\left\lfloor\frac{B^{n-24}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 24).$$

$$R(x)=\sum_{j=0}^{352} c_jx^j.$$

```text
  0-11   1, 9, 107, 1077, 9667, 77196, 557118, 3662316, 22131932, 123837306, 645761465, 3155559373
 12-17   14520214458, 63183481482, 260974501083, 1026605346529, 3857574977407, 13883345063203
 18-22   47972743587016, 159503749198915, 511322212390849, 1583303748229528, 4743663352093742
 23-26   13772762756235008, 38807271829804486, 106260630081530970, 283100782758766683
 27-30   734725555997768467, 1859507247742817578, 4594125118855458255, 11090636817672570409
 31-34   26184883719810994278, 60513799526142916525, 136998576992987121402, 304063702844448915396
 35-37   662081189271707033469, 1415307643148855755242, 2972096373949452373729
 38-40   6134972663791319585953, 12455240078644518257821, 24884043089363930472475
 41-43   48949383776686623065629, 94852371384418863982303, 181146904141529607441175
 44-46   341108813081727721159105, 633611197114705379118214, 1161450672771369844923288
 47-49   2101836448569469326506500, 3756487946576217678275483, 6632964171175541697326905
 50-52   11575155552716096082321728, 19970282195485217008731828, 34073631597817927743200735
 53-55   57512536073625109045956373, 96060345355111028450968156, 158812934374614290333718438
 56-58   259959351073200903784706062, 421420858644970505426398522, 676747135641092131650510392
 59-61   1076815509885848736836675565, 1698092619316928554177087642, 2654505353845631230924798892
 62-64   4114351389654058361915154331, 6324186512411182714328358767, 9642289994621113901578574823
 65-66   14585171632596502236475095424, 21891694121624748557294285932
 67-68   32610801124617558687956116088, 48220633929592578611878312430
 69-70   70789068499594145857863391633, 103188502397993894909646555564
 71-72   149381172176971100600867475851, 214795503197400828911511232473
 73-74   306819113960887012901393662260, 435440254685691696442577411502
 75-76   614076802138574216718850732277, 860640612000786557826720712896
 77-78   1198895199810381737829787260737, 1660176531119592779029730250404
 79-80   2285560289433489149127275770074, 3128574476350202831168947880186
 81-82   4258573673290481139772875210088, 5764910810132628179328069292321
 83-84   7762063843193931591773335405151, 10395898278489128700187720881610
 85-86   13851271841751451817216044318566, 18361214555553966175564849071127
 87-88   24217945687609146287423315122361, 31786018010102490872849461384835
 89-90   41517908946648782209178088081668, 53972406719785993814715450238753
 91-92   69836166626716208043835930343741, 89948836977335061313773358218345
 93-94   115332174772056809363217277276807, 147223586459305030371953594633159
 95-96   187114537521603991566227932864482, 236794274485780571098745419378058
 97-98   298399292415484477720958842684018, 374468958122717059897182657091969
 99-100  468007662292113718265496647882169, 582553820524321845182037284533540
101-102  722255972123984054101878976618209, 891956134576861939059326170651165
103-104  1097280459590703130474556149407005, 1344737102126446604479685834963869
105-106  1641821056217110968952299243119844, 1997125530232584612616930392027385
107-108  2420459229833813862259609885651001, 2922968690052030928879404820110731
109-110  3517264550337267963004960551670503, 4217550400451317167573310620450433
111-112  5039752543991313562513443147224788, 6001648734269526601418346880106900
113-114  7122993639299323412755044441730303, 8425638494705086929996446822478868
115-116  9933642112311887929868497478200119, 11673370135610519968021500218954277
117-118  13673579179576403769642446592847187, 15965482270369859567591365089067190
119-120  18582791819604035820099248363555368, 21561736237706590037945044096827545
121-122  24941046220997393754244540936911061, 28761906746786173019078193024301997
123-124  33067870888870901773367960969390644, 37904731730290386304653237186363495
125-126  43320348907943505504871926311140494, 49364426680210982070533092658324261
127-128  56088240867771714417523904076231801, 63544312581171837380470735078514242
129-130  71786027315910546936088423666057911, 80867198763913299792898783476552316
131-132  90841577553686082432388501146560309, 101762306081832474998370390284382235
133-134  113681321624789822273001036744871481, 126648711007607415050276803214047745
135-136  140712021239624117854048181992992692, 155915531685718570671063128465728431
137-138  172299494504801352787612577552195116, 189899351230811769908869041574335202
139-140  208744934470515683167237299360875448, 228859664720629481132451526000794534
141-142  250259753237434275634968937515622115, 272953422698375668360727497043557859
143-144  296940158051165175438724305923015336, 322210000426998673426745801924519628
145-146  348742897278153954877736093995646462, 376508121966653662741113765006564526
147-148  405463775863527948729098394177320635, 435556385605156063384184109727923379
149-150  466720607486452323448515707007124030, 498879050047567754278015454483033952
151-152  531942224733977341875689886000273703, 565808633087627752334170169009633388
153-154  600364997273301998468231418375249350, 635486638879321266011455448174945566
155-156  671038008880523498667053913047652407, 706873369444760848487982636855321495
157-158  742837625937364962988838643387323500, 778767305070755096488315709315356493
159-160  814491672701687050166661960527761432, 849833982342255235857747815922619853
161-162  884612843070031303772459369393757397, 918643693245665460884221470396036276
163-164  951740364320479320240976204007650261, 983716717088102354889197364108742844
165-166  1014388331046479881327046985128064619, 1043574226129342698844262498623980824
167-168  1071098594974501573121559964325873390, 1096792523149505415025989053993118967
169-170  1120495674376229130194513443315788645, 1142057917800669022298098845033523403
171-172  1161340874750823253908613662195906572, 1178219363214254545208493808159171477
173-174  1192582719439880180544573340528463285, 1204335977609734922844897095919321753
175-176  1213400890412082628072068071783952407, 1219716775546070916399675813894501576
177-178  1223241175662083613145270015522874638, 1223950321946979341973691650313710364
179-180  1221839394450356259774819106118925433, 1216922575263674168424168390514217148
181-182  1209232893752461122545571384085208236, 1198821866145279713204245703578872368
183-184  1185758934843639044635794445622192850, 1170130715777574993042781216598477999
185-186  1152040064937363853808601166126950342, 1131604977811388841398406547486082168
187-188  1108957337806697790503649148542363792, 1084241531780979130820897034921856149
189-190  1057612952537665197431946838105564811, 1029236409501893190932264425141434347
191-192  999284469784010059122414932661866962, 967935752437081255456714021116697231
193-194  935373198921468386009859031585253663, 901782342607068860674805931209746951
195-196  867349599584187587163657223080822147, 832260602136570918631866699272071397
197-198  796698594981026778503831924937630709, 760842912829506914465829146155307116
199-200  724867556018968892576827639908550094, 688939878923435382705789564609537872
201-202  653219403656289084890657387439564182, 617856769235950917733748591556472562
203-204  582992823972653930965488959532554079, 548757866385918947692850624791687989
205-206  515271037528285256440746116208952712, 482639865215438644459121551899938003
207-208  450959958387658947668508468360300394, 420314847690196789621195938091320261
209-210  390775966393997932938167822388397136, 362402764011299430410950960335726862
211-212  335242943415771077935718198181786616, 309332810971141890005147122680178695
213-214  284697728116937457631720925610004672, 261352652060638221562900617923999911
215-216  239302752682283948969021268396920237, 218544092465087092250026082613507128
217-218  199064356213938368301188164851272303, 180843617498427899629277987070811222
219-220  163855129140055128698074753155689106, 148066125633440621153465314803973403
221-222  133438626124923859046060988994950160, 119930227443523094770857784465678636
223-224  107494877662370945717147624080267837, 96083621736548443139927164697290915
225-226  85645311889078471660574440396611159, 76127276574878179142828745376078495
227-228  67475943018214069424335719244660867, 59637409469942152565531079858988115
229-230  52557964445994908994139082606693993, 46184551270092508984970023497947479
231-232  40465177236062408412243543356669619, 35349267615791030000879895932350217
233-234  30787965557882394199092909758195863, 26734379642552677564583443489449190
235-236  23143781475859941964892893550666383, 19973756219339869462931080132671718
237-238  17184309360148635923728143826580569, 14737933334692582196700126728034021
239-240  12599637830102287166936478386077516, 10736947709007957424827568416775503
241-242  9119872541384628568573434001710587, 7720851691215796699793094293242589
243-244  6514678804497245295842027624707241, 5478409388178283227893572741653270
245-246  4591254966645974758763260227804388, 3834467062812682079014256780179392
247-248  3191213983954967219146487980626026, 2646453106854088546083777627040853
249-250  2186801060535850804818999581527685, 1800403905268412844092896845710181
251-252  1476809109876145041523609131495705, 1206840841399638575426240518197108
253-254  982479806298892458297602404676648, 796748624475307444636597169504707
255-256  643603479218030699153203990309419, 517832569771506118998965968307263
257-258  414961699817312308851346655229333, 331167165316163281630737095411008
259-260  263195958807896804465697046789207, 208293183839470094405171175491188
261-262  164136471672211260215492874583913, 128777111454444230630764523548425
263-264  100587543019215942624165761741505, 78214816584114087325143446461303
265-266  60539593988219782443400842496147, 46640249753956664122095093607992
267-268  35761625275374530297858916390073, 27287993935008859043323265688387
269-270  20719807161866624100884332913940, 15653809712625626972762710967482
271-272  11766135283381247961250976540490, 8798019597465949481942249082740
273-274  6543796190569835346412197187570, 4840869220370735304771094497751
275-276  3561386921097120614048638494077, 2605368117109681377682921956659
277-278  1895061962213546777073042330090, 1370347373712659724074705299191
279-280  985003190610691384242723604680, 703702714814861305267356670162
281-282  499606890969589932857074674343, 352448915341278390917446273233
283-284  247019566089264894830853583935, 171977090805864618006753667942
285-286  118918180637157256864822761273, 81657535301178584530495814053
287-288  55672926213218299672694236012, 37680649246117279343558532438
289-290  25312979150068243175752136414, 16874845579433489845663870168
291-293  11161590211795092463049945433, 7323470201906698731008768423, 4765668575342785590830022581
294-296  3075068403312703412650031928, 1967043573378348577450578860, 1247101313874303544763300687
297-299  783455279422996610103943167, 487576983330332265847494981, 300521720215788080358980761
300-302  183397967028982937693943353, 110783805808252126731770292, 66220555268569578610472844
303-305  39157052450432714185595722, 22897470862553307211297717, 13236664436291779873038414
306-308  7561872500579710366584653, 4267550983529290440559755, 2378250578348317548637313
309-311  1308243459521148688675685, 710043849083108376074984, 380059310434059275444141
312-314  200530711411702138573638, 104245285400842972579622, 53364058226793083446512
315-317  26885392188303409380309, 13323046823735503971112, 6489933223237590039671
318-320  3105563213566667274008, 1458817003739546948573, 672202030702983591801
321-324  303595631872185381573, 134283973418280141835, 58116344771246594385, 24586933914740265892
325-328  10157822228247417261, 4093682130581063604, 1607451694266658337, 614225084255443792
329-332  228085166888041183, 82189173841904420, 28694423615666243, 9689606276993365
333-337  3158910177103478, 992238726862859, 299631262936453, 86776564210911, 24038596319333
338-343  6350861752865, 1594987176628, 379403344676, 85130429491, 17934640190, 3528694732
344-352  644445434, 108457210, 16677852, 2318110, 287670, 31232, 2923, 218, 14
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{43}\Phi_{2}(x)^{21}\Phi_{3}(x)^{13}\Phi_{4}(x)^{9}\\&\times \Phi_{5}(x)^{7}\Phi_{6}(x)^{5}\Phi_{7}(x)^{5}\Phi_{8}(x)^{3}\\&\times \Phi_{9}(x)^{3}\Phi_{10}(x)^{3}\Phi_{11}(x)^{3}\Phi_{12}(x)\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\Phi_{16}(x)\\&\times \Phi_{17}(x)\Phi_{18}(x)\Phi_{19}(x)\Phi_{20}(x)\\&\times \Phi_{21}(x)\Phi_{22}(x)\Phi_{23}(x)\end{aligned}$$


### U23 — k=24 leaves

Order 417; period 5354228880; source v31/UNROOTED_MODELS.json, record 22.

$$B=2^{n+529},\quad a(n)=0\ (n<25).$$

$$a(n)=\left\lfloor\frac{B^{n-25}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 25).$$

$$R(x)=\sum_{j=0}^{391} c_jx^j.$$

```text
  0-11   1, 9, 108, 1134, 10460, 86303, 642270, 4356330, 27156918, 156772734, 843456390, 4252895468
 12-17   20194807468, 90693817580, 386659901277, 1570159889455, 6091398914579, 22636693682583
 18-22   80776228916170, 277385537773128, 918511511281426, 2938214129036577, 9095223109535046
 23-26   27286665802144905, 79454849083230875, 224855620671703210, 619213941080379241
 27-30   1661251006829299965, 4346687751077489110, 11103288249636955684, 27715900665064510241
 31-34   67667487482940054383, 161722911199657657560, 378659980095471868731, 869241225695317612792
 35-37   1957731860435486437957, 4328930147365059545397, 9403719253467261823096
 38-40   20080451906486489299038, 42174688841556601840629, 87171067537703834867840
 41-43   177402969857888982055095, 355658045446735823599972, 702736802321503692154624
 44-46   1369104706323461749350769, 2631183996933489691558175, 4990162314191745974111682
 47-49   9343238617965584533777425, 17276768263891195448889856, 31562096671043879848633818
 50-52   56984508064522189620749391, 101713470956589591968937106, 179542817590607035667813673
 53-55   313514090632513268486402236, 541716210578489147173395028, 926474738821349075562829198
 56-58   1568768251681948256148645252, 2630627816108194618418983935, 4369614061294967478457792216
 59-61   7191398757475256154080224872, 11729242207843808387330110985, 18963076995714052947687542396
 62-63   30396416517456364037247048969, 48316980829344019141508137439
 64-65   76177534639816543707836754416, 119147959157763357432849487799
 66-67   184909322288786338739630996444, 284787329299493057407374503262
 68-69   435358141222361054756706689279, 660706808166887346638118052308
 70-71   995580817569994195258623835667, 1489762645256644954569174037236
 72-73   2214090814807579852828617901884, 3268695030462100471015111516876
 74-75   4794184959107492095057563133365, 6986753192353935561073957773073
 76-77   10118431497730365638557125753891, 14564088227168851879347125150380
 78-79   20837188322385971200900360478360, 29636872619977270356597821417274
 80-81   41909569389232542297891350868570, 58929150009141397044783699058021
 82-83   82400606731744896599856524536737, 114593390427683203259923126296320
 84-85   158511929295050381237345116963106, 218112487101110254621548515249609
 86-87   298577444728667078416791908231780, 406660335906980026181968467242786
 88-89   551117571739633026516693312092598, 743245783174037883511355043618598
 90-91   997547128316794209713173961809652, 1332548781710529328725434225016902
 92-93   1771807169656441724009184627953747, 2345132356798118286504277377423831
 94-95   3090073332742733503071222367313255, 4053710790131032555044221291529042
 96-97   5294810309606359324046656427045594, 6886395637719738871271480847139405
 98-99   8918808905920049430592825355389513, 11503332114202146142071931598868036
100-101  14776451887341253109119543465921370, 18904857271560640485724879069637674
102-103  24091268010059642342903537327138925, 30581198118502519741550211718911229
104-105  38670766442530628160301841963469714, 48715671948718031629540863843506451
106-107  61141456472196362860290967266449666, 76455181177507465887636751549041245
108-109  95258644710499025642182720866508950, 118263270525623396123672816225553530
110-111  146306787738305473981253690106661590, 180371823632429992191669416889214381
112-113  221606516196035907868068551257876790, 271347241312940600518639971519671803
114-115  331143531066372177335438446631420003, 402785236601494653372754184493818782
116-117  488331960777228338585714191479171790, 590144752102006482269087196960187731
118-119  710920011956081107157929975238197975, 853725521710659520512880050653111855
120-121  1022038445028673559851939421745170612, 1219785103469762921626538825479007809
122-123  1451382260766093363121795665543203372, 1721779583191567869095009950680689616
124-125  2036502870897207529597317985646557589, 2401697578700631045478688700014629219
126-127  2824172065564835559653997137010804972, 3311439931048955767210700755511343125
128-129  3871760715730133386314032577247753487, 4514178162545238953534040892340291435
130-131  5248555158932589098712105172100729324, 6085604407483142250719581648404132558
132-133  7036913807598338252983061389200700247, 8114965474572749321965709946225919505
134-135  9333147277827496422744235645985183070, 10705755749004648076787289419538139532
136-137  12247989195571445159028820557154417226, 13975929858689093047870294186218903124
138-139  15906513977464461915052420436706369351, 18057488667231507956881039152642637040
140-141  20447354588863640560373400436821405919, 23095293480650084822181517076654111015
142-143  26021079744957818593076657925641368523, 29244975429293034189985449756163612034
144-145  32787608115531663342529176135470797618, 36669831431529532721067323569568533432
146-147  40912568124992885804039413477276790832, 45536635888722923342247503060043168501
148-149  50562556396847085824903242923623232979, 56010348300481087059210974891801214687
150-151  61899305234865013173440440802265134745, 68247760204212025351568112898949125986
152-153  75072838030557624037531418053947464333, 82390197873544254584651988192780890607
154-155  90213768143619130157536144639738417978, 98555476435503472577153254842270523850
156-157  107424977395693110062100198634664405041, 116829381700715419239768017263462060679
158-159  126772989555421530480000284018416856517, 137257032316379978954670416091427202781
160-161  148279425998363667679261539967305544659, 159834540526297203688151383251815694160
162-163  171912988645719134221091582223509596613, 184501438397370293381997485758039387681
164-165  197582452992332247269204712952446723769, 211134361790550850287875852877769336047
166-167  225131165885997974684057265155524511945, 239542481535718897301335586537035718360
168-169  254333524338386891553814728740841582161, 269465136672827438256598442003916135677
170-171  284893860451677377112617508612946250772, 300572056734609199374169150251860274037
172-173  316448073185349904124961498303512974456, 332466459754240593742465426508239694010
174-175  348568232331620360574457593050880051309, 364691183456179724008367635708497174582
176-177  380770238486773145822578223069630786389, 396737854966849214378277577161403359608
178-179  412524462238985218184369424961071487734, 428058937714616646491945701745926793335
180-181  443269115582607389916972545629596678140, 458082323161315878410152292633058274884
182-183  472425939573370180579740123383094569848, 486227970960922369230294185045348731542
184-185  499417636071290261800280080112164334087, 511925955737109071719877794500501429329
186-187  523686339558620584958503997194102409916, 534635162974280646354177477519555272469
188-189  544712327883620442003704656394633659065, 553861800065686412736782503854765004713
190-191  562032116818038423154651194332840929867, 569176858523989391010994917534910294397
192-193  575255078236451224323185876146490607031, 580231683840519465116864172553973826412
194-195  584077767917140630715659944770779734876, 586770881068579980617444418422620229159
196-197  588295245173166957358109577843685070174, 588641903800848568566432992684230737954
198-199  587808807830227004124238416869159584511, 585800835148920575307609450642939215918
200-201  582629744178566661787732714387554784444, 578314061829524139821848367051627268643
202-203  572878907344189548425389527171864539367, 566355754317867260058489752220446474684
204-205  558782133978844464890710501088663391848, 550201283551957499969933519242977269704
206-207  540661744210707931792660178694782084321, 530216913731299474774823329171518648644
208-209  518924559488615364380751856063160626395, 506846297871491702582609949494857237414
210-211  494047046536705255915084407147604460846, 480594456163707083789129838108976938133
212-213  466558328512958673347831435168989749350, 452010027629284190400181567050867651780
214-215  437021890969295077556936069309226388674, 421666647071800511713912422191639565024
216-217  406016846136997151810427838832280499965, 390144309540492099760614138787728145996
218-219  374119603889603271148938732812199331119, 358011544740857824687546592831902548907
220-221  341886734549130683769719293783158031115, 325809138821172159232594809895288277929
222-223  309839703810658034451039753735424325494, 294036018429964483513595431807175438544
224-225  278452022377311525822766110521611391754, 263137761798271111084822707293526668504
226-227  248139193129070570159550939674374200658, 233498035116239376839658391702023354222
228-229  219251668382792314227816213408711246155, 205433081324244310424226326308704834803
230-231  192070860576188313733453907933602426669, 179189223805654025021964205468937088628
232-233  166808092146478501161411491476428951965, 154943199228645953023282810755589993276
234-235  143606233445869039929700778968784482290, 132805009866160062946948213820718507997
236-237  122543668017081699612085742146429647891, 112822891669868487046221598687499641251
238-239  103640146702640451366786698019503377796, 94989933139431880219116344846036985806
240-241  86864047534765959844229835392822210324, 79251851998276579505511588973506429517
242-243  72140546325029837125853717853699639855, 65515439908852916556808508351396163096
244-245  59360220361911928806060702613684171573, 53657216037564053375972181319624263855
246-247  48387649948649785877040796211058983754, 43531882883463108725367201021600596796
248-249  39069643840405524732345859051736183159, 34980246223858024191977420776145878934
250-251  31242788562552008817464149834332882595, 27836338822620119188776793877892508167
252-253  24740101686034734234778826875801476211, 21933568447357494193515219734142449268
254-255  19396649444309274712629055234905372454, 17109789177944413978417335523194619381
256-257  15054064494130823367285472307999335770, 13211266388178896748045412639919512935
258-259  11563966158006794192415502028227855541, 10095566767921788857192025313333793502
260-261  8790340395200272336541689984745856087, 7633453215893110282086798854079343094
262-263  6610978545808075694581893265679261709, 5709899488914793189031724281483946927
264-265  4918102260252421974169896838591996786, 4224361345789729670951706170152070356
266-267  3618317639743596595060306147092924186, 3090450662856715940610469151491822467
268-269  2632045915362717358131551681710386654, 2235158358113231840304636395282133110
270-271  1892572946838424217381537095614780665, 1597763069898011637882364301601009651
272-273  1344847661163788692991510540381665927, 1128547678712317956762565682583391552
274-275  944142558477196918087463419607712553, 787427171403488867587136267873564830
276-277  654669734253019529195042282702750034, 542571049116829442474765385726072649
278-279  448225375788423871590980705447778587, 369083175132660022723603814132876534
280-281  302915900959732550699082536823371754, 247782963019531716672438333053604491
282-283  202000934749640112493254256794076169, 164115036381311257843057356387875706
284-285  132872886850532827756109797703870443, 107200486490265167120533752465928184
286-287  86180366423901322609750329770319092, 69031819599627227253515523842881027
288-289  55093112110280213336389486278348769, 43805561407800407990236465504531898
290-291  34699359798798697843337409035155766, 27381016743376051565281501305822857
292-293  21522291521426303065829935589104734, 16850488340048317189966146932907800
294-295  13139988513446146443134623191593837, 10204898560214739360426096962315658
296-297  7892698570474692614253600251220042, 6078781669169097993137998493598580
298-299  4661782549938552149107527934313453, 3559600620677687698485149141154402
300-301  2706031067481779497186104448806625, 2047924923373654934022061694404621
302-303  1542806870108024408017160920440838, 1156886884285545199128571821258694
304-305  863408869737804053303125663806575, 641286028477805131200788551782993
306-307  473978866279436730758496678186963, 348577378970887861854440690433936
308-309  255054110645081894755572009665811, 185659417258002441162859985840254
310-311  134434421140423469437292097121079, 96820824615211573645074023077484
312-313  69349991060779087537253459102426, 49396530426275515232537346307516
314-315  34984076971956754397487583328983, 24633054662061638475889238664143
316-317  17242025049337607020143489123418, 11995737740708210527734341537161
318-319  8294287238815149033900498472873, 5698852776973651702968710788640
320-321  3890388084317566536922208547456, 2638361733530452539006362566437
322-323  1777249173106834383695428662845, 1188965510863706868150546343942
324-325  789821896184607164785072138723, 520903892754614455632911908605
326-327  341021298903630955434221837465, 221577212665652270881215842754
328-329  142859700392826937729366844985, 91380552275340835195666106600
330-331  57979226659918808704143262018, 36481906163991139238656499109
332-334  22760272371257347826841142077, 14075923345872213909344793558, 8627334188465091389021249051
335-337  5239300613334055136001156689, 3151804876304024144779498947, 1877683518826388377484610286
338-340  1107504340811114664394616312, 646556112118752888025830366, 373488363370891925471049437
341-343  213414808999502852088431327, 120589384121431696796113162, 67357283122600600891812165
344-346  37179024255897375520243543, 20271643565847340446138082, 10914132573669867094551204
347-349  5799921699984959123754328, 3040899519313053581834875, 1572294343563073145115522
350-352  801331153435158256129451, 402364957514698701863354, 198943601997933366560239
353-355  96805622517687665417173, 46331610740777730470630, 21796720761853403165217
356-358  10072951394387470830170, 4569533473737034126133, 2033366724353890539512
359-362  886844236628740596725, 378794780755075432039, 158306618342310367703, 64672571885182167953
363-366  25800396576628341473, 10040284772446435408, 3806915731289656001, 1404639305606743047
367-370  503658430583517656, 175249510115291042, 59080724230035524, 19264837395780059
371-375  6064769326398912, 1839586421385447, 536451019419254, 150037309311455, 40140085880370
376-381  10242278829280, 2484523509998, 570874832432, 123742121468, 25186131997, 4788251323
382-391  845072880, 137472352, 20434364, 2747603, 329487, 34768, 3117, 239, 13, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{45}\Phi_{2}(x)^{22}\Phi_{3}(x)^{15}\Phi_{4}(x)^{11}\\&\times \Phi_{5}(x)^{7}\Phi_{6}(x)^{7}\Phi_{7}(x)^{5}\Phi_{8}(x)^{5}\\&\times \Phi_{9}(x)^{3}\Phi_{10}(x)^{3}\Phi_{11}(x)^{3}\Phi_{12}(x)^{3}\\&\times \Phi_{13}(x)\Phi_{14}(x)\Phi_{15}(x)\Phi_{16}(x)\\&\times \Phi_{17}(x)\Phi_{18}(x)\Phi_{19}(x)\Phi_{20}(x)\\&\times \Phi_{21}(x)\Phi_{22}(x)\Phi_{23}(x)\Phi_{24}(x)\end{aligned}$$


## Rooted trees: branching profiles


### T01 — k=1; children counts: no branching vertices

Order 1; period 1; source v31/DEGREE_PROFILE_MODELS.json, record 0.

$$B=2^{n+3},\quad a(n)=0\ (n<1).$$

$$a(n)=\left\lfloor\frac{B^{n-1}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 1).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)$$

Same rational function as R01.


### T02 — k=2; children counts: 2 (1)

Order 4; period 2; source v31/DEGREE_PROFILE_MODELS.json, record 1.

$$B=2^{n+4},\quad a(n)=0\ (n<3).$$

$$a(n)=\left\lfloor\frac{B^{n-3}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 3).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{3}\Phi_{2}(x)$$

Same rational function as R02.


### T03 — k=3; children counts: 2 (2)

Order 6; period 2; source v31/DEGREE_PROFILE_MODELS.json, record 2.

$$B=2^{n+4},\quad a(n)=0\ (n<5).$$

$$a(n)=\left\lfloor\frac{B^{n-5}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 5).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)$$


### T04 — k=3; children counts: 3 (1)

Order 7; period 6; source v31/DEGREE_PROFILE_MODELS.json, record 3.

$$B=2^{n+6},\quad a(n)=0\ (n<4).$$

$$a(n)=\left\lfloor\frac{B^{n-4}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 4).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{4}\Phi_{2}(x)\Phi_{3}(x)$$


### T05 — k=4; children counts: 2 (1), 3 (1)

Order 10; period 6; source v31/DEGREE_PROFILE_MODELS.json, record 4.

$$B=2^{n+9},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=2+2x+x^{2}$$

$$Q(x)=\Phi_{1}(x)^{6}\Phi_{2}(x)^{2}\Phi_{3}(x)$$


### T06 — k=4; children counts: 2 (3)

Order 12; period 4; source v31/DEGREE_PROFILE_MODELS.json, record 5.

$$B=2^{n+11},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=2+x+4x^{2}+2x^{3}+x^{4}$$

$$Q(x)=\Phi_{1}(x)^{7}\Phi_{2}(x)^{3}\Phi_{4}(x)$$


### T07 — k=4; children counts: 4 (1)

Order 11; period 12; source v31/DEGREE_PROFILE_MODELS.json, record 6.

$$B=2^{n+9},\quad a(n)=0\ (n<5).$$

$$a(n)=\left\lfloor\frac{B^{n-5}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 5).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{5}\Phi_{2}(x)^{2}\Phi_{3}(x)\Phi_{4}(x)$$


### T08 — k=5; children counts: 2 (1), 4 (1)

Order 13; period 12; source v31/DEGREE_PROFILE_MODELS.json, record 7.

$$B=2^{n+10},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=2+x^{2}$$

$$Q(x)=\Phi_{1}(x)^{7}\Phi_{2}(x)^{2}\Phi_{3}(x)\Phi_{4}(x)$$


### T09 — k=5; children counts: 2 (2), 3 (1)

Order 15; period 12; source v31/DEGREE_PROFILE_MODELS.json, record 8.

$$B=2^{n+15},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=5+7x+11x^{2}+10x^{3}+7x^{4}+2x^{5}$$

$$Q(x)=\Phi_{1}(x)^{8}\Phi_{2}(x)^{3}\Phi_{3}(x)\Phi_{4}(x)$$


### T10 — k=5; children counts: 2 (4)

Order 14; period 4; source v31/DEGREE_PROFILE_MODELS.json, record 9.

$$B=2^{n+11},\quad a(n)=0\ (n<9).$$

$$a(n)=\left\lfloor\frac{B^{n-9}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 9).$$

$$R(x)=3+2x+5x^{2}+3x^{3}+x^{4}$$

$$Q(x)=\Phi_{1}(x)^{9}\Phi_{2}(x)^{3}\Phi_{4}(x)$$


### T11 — k=5; children counts: 3 (2)

Order 11; period 6; source v31/DEGREE_PROFILE_MODELS.json, record 10.

$$B=2^{n+7},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{7}\Phi_{2}(x)^{2}\Phi_{3}(x)$$


### T12 — k=5; children counts: 5 (1)

Order 16; period 60; source v31/DEGREE_PROFILE_MODELS.json, record 11.

$$B=2^{n+13},\quad a(n)=0\ (n<6).$$

$$a(n)=\left\lfloor\frac{B^{n-6}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 6).$$

$$R(x)=1$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{6}\Phi_{2}(x)^{2}\Phi_{3}(x)\Phi_{4}(x)\\&\times \Phi_{5}(x)\end{aligned}$$


### T13 — k=6; children counts: 2 (1), 3 (2)

Order 21; period 12; source v31/DEGREE_PROFILE_MODELS.json, record 12.

$$B=2^{n+21},\quad a(n)=0\ (n<9).$$

$$a(n)=\left\lfloor\frac{B^{n-9}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 9).$$

$$\begin{aligned}R(x)&=5+7x+15x^{2}+17x^{3}+20x^{4}+17x^{5}\\&+15x^{6}+10x^{7}+5x^{8}+x^{9}\end{aligned}$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{9}\Phi_{2}(x)^{4}\Phi_{3}(x)^{2}\Phi_{4}(x)\\&\times \Phi_{6}(x)\end{aligned}$$


### T14 — k=6; children counts: 2 (1), 5 (1)

Order 19; period 60; source v31/DEGREE_PROFILE_MODELS.json, record 13.

$$B=2^{n+16},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=2+2x+x^{2}+x^{3}+x^{4}$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{8}\Phi_{2}(x)^{3}\Phi_{3}(x)\Phi_{4}(x)\\&\times \Phi_{5}(x)\end{aligned}$$


### T15 — k=6; children counts: 2 (2), 4 (1)

Order 17; period 12; source v31/DEGREE_PROFILE_MODELS.json, record 14.

$$B=2^{n+15},\quad a(n)=0\ (n<9).$$

$$a(n)=\left\lfloor\frac{B^{n-9}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 9).$$

$$R(x)=5+7x+7x^{2}+5x^{3}+4x^{4}$$

$$Q(x)=\Phi_{1}(x)^{9}\Phi_{2}(x)^{4}\Phi_{3}(x)\Phi_{4}(x)$$


### T16 — k=6; children counts: 2 (3), 3 (1)

Order 24; period 12; source v31/DEGREE_PROFILE_MODELS.json, record 15.

$$B=2^{n+27},\quad a(n)=0\ (n<10).$$

$$a(n)=\left\lfloor\frac{B^{n-10}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 10).$$

$$R(x)=\sum_{j=0}^{12} c_jx^j.$$

```text
  0-12   12, 34, 85, 139, 196, 229, 241, 211, 173, 111, 57, 20, 4
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{10}\Phi_{2}(x)^{4}\Phi_{3}(x)^{3}\Phi_{4}(x)\\&\times \Phi_{6}(x)\end{aligned}$$


### T17 — k=6; children counts: 2 (5)

Order 18; period 4; source v31/DEGREE_PROFILE_MODELS.json, record 16.

$$B=2^{n+16},\quad a(n)=0\ (n<11).$$

$$a(n)=\left\lfloor\frac{B^{n-11}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 11).$$

$$\begin{aligned}R(x)&=6+10x+24x^{2}+18x^{3}+19x^{4}+6x^{5}\\&+x^{6}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{11}\Phi_{2}(x)^{5}\Phi_{4}(x)$$


### T18 — k=6; children counts: 3 (1), 4 (1)

Order 17; period 12; source v31/DEGREE_PROFILE_MODELS.json, record 17.

$$B=2^{n+14},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=2+2x+2x^{2}+x^{3}$$

$$Q(x)=\Phi_{1}(x)^{8}\Phi_{2}(x)^{3}\Phi_{3}(x)^{2}\Phi_{4}(x)$$


### T19 — k=6; children counts: 6 (1)

Order 22; period 60; source v31/DEGREE_PROFILE_MODELS.json, record 18.

$$B=2^{n+18},\quad a(n)=0\ (n<7).$$

$$a(n)=\left\lfloor\frac{B^{n-7}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 7).$$

$$R(x)=1$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{7}\Phi_{2}(x)^{3}\Phi_{3}(x)^{2}\Phi_{4}(x)\\&\times \Phi_{5}(x)\Phi_{6}(x)\end{aligned}$$


### T20 — k=7; children counts: 2 (1), 3 (1), 4 (1)

Order 19; period 12; source v31/DEGREE_PROFILE_MODELS.json, record 19.

$$B=2^{n+17},\quad a(n)=0\ (n<10).$$

$$a(n)=\left\lfloor\frac{B^{n-10}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 10).$$

$$R(x)=9+8x+11x^{2}+5x^{3}+3x^{4}$$

$$Q(x)=\Phi_{1}(x)^{10}\Phi_{2}(x)^{3}\Phi_{3}(x)^{2}\Phi_{4}(x)$$


### T21 — k=7; children counts: 2 (1), 6 (1)

Order 24; period 60; source v31/DEGREE_PROFILE_MODELS.json, record 20.

$$B=2^{n+20},\quad a(n)=0\ (n<9).$$

$$a(n)=\left\lfloor\frac{B^{n-9}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 9).$$

$$R(x)=2+x^{2}+x^{4}$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{9}\Phi_{2}(x)^{3}\Phi_{3}(x)^{2}\Phi_{4}(x)\\&\times \Phi_{5}(x)\Phi_{6}(x)\end{aligned}$$


### T22 — k=7; children counts: 2 (2), 3 (2)

Order 23; period 12; source v31/DEGREE_PROFILE_MODELS.json, record 21.

$$B=2^{n+23},\quad a(n)=0\ (n<11).$$

$$a(n)=\left\lfloor\frac{B^{n-11}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 11).$$

$$\begin{aligned}R(x)&=17+22x+49x^{2}+52x^{3}+65x^{4}+54x^{5}\\&+49x^{6}+32x^{7}+16x^{8}+4x^{9}\end{aligned}$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{11}\Phi_{2}(x)^{4}\Phi_{3}(x)^{2}\Phi_{4}(x)\\&\times \Phi_{6}(x)\end{aligned}$$


### T23 — k=7; children counts: 2 (2), 5 (1)

Order 22; period 60; source v31/DEGREE_PROFILE_MODELS.json, record 22.

$$B=2^{n+20},\quad a(n)=0\ (n<10).$$

$$a(n)=\left\lfloor\frac{B^{n-10}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 10).$$

$$R(x)=5+7x+7x^{2}+6x^{3}+6x^{4}+3x^{5}+2x^{6}$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{10}\Phi_{2}(x)^{4}\Phi_{3}(x)\Phi_{4}(x)\\&\times \Phi_{5}(x)\end{aligned}$$


### T24 — k=7; children counts: 2 (3), 4 (1)

Order 25; period 12; source v31/DEGREE_PROFILE_MODELS.json, record 23.

$$B=2^{n+26},\quad a(n)=0\ (n<11).$$

$$a(n)=\left\lfloor\frac{B^{n-11}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 11).$$

$$R(x)=\sum_{j=0}^{11} c_jx^j.$$

```text
  0-11   12, 23, 52, 65, 85, 84, 85, 58, 46, 21, 8, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{11}\Phi_{2}(x)^{4}\Phi_{3}(x)^{3}\Phi_{4}(x)\\&\times \Phi_{6}(x)\end{aligned}$$


### T25 — k=7; children counts: 2 (4), 3 (1)

Order 27; period 12; source v31/DEGREE_PROFILE_MODELS.json, record 24.

$$B=2^{n+30},\quad a(n)=0\ (n<12).$$

$$a(n)=\left\lfloor\frac{B^{n-12}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 12).$$

$$R(x)=\sum_{j=0}^{13} c_jx^j.$$

```text
  0-13   28, 97, 252, 453, 683, 843, 930, 877, 745, 533, 314, 137, 42, 6
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{12}\Phi_{2}(x)^{5}\Phi_{3}(x)^{3}\Phi_{4}(x)\\&\times \Phi_{6}(x)\end{aligned}$$


### T26 — k=7; children counts: 2 (6)

Order 20; period 4; source v31/DEGREE_PROFILE_MODELS.json, record 25.

$$B=2^{n+17},\quad a(n)=0\ (n<13).$$

$$a(n)=\left\lfloor\frac{B^{n-13}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 13).$$

$$\begin{aligned}R(x)&=11+18x+36x^{2}+32x^{3}+26x^{4}+8x^{5}\\&+x^{6}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{13}\Phi_{2}(x)^{5}\Phi_{4}(x)$$


### T27 — k=7; children counts: 3 (1), 5 (1)

Order 22; period 60; source v31/DEGREE_PROFILE_MODELS.json, record 26.

$$B=2^{n+19},\quad a(n)=0\ (n<9).$$

$$a(n)=\left\lfloor\frac{B^{n-9}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 9).$$

$$R(x)=2+2x+2x^{2}+x^{3}+x^{4}$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{9}\Phi_{2}(x)^{3}\Phi_{3}(x)^{2}\Phi_{4}(x)\\&\times \Phi_{5}(x)\end{aligned}$$


### T28 — k=7; children counts: 3 (3)

Order 22; period 12; source v31/DEGREE_PROFILE_MODELS.json, record 27.

$$B=2^{n+19},\quad a(n)=0\ (n<10).$$

$$a(n)=\left\lfloor\frac{B^{n-10}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 10).$$

$$\begin{aligned}R(x)&=2+4x^{2}+2x^{3}+4x^{4}+x^{5}+2x^{6}\\&+x^{7}\end{aligned}$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{10}\Phi_{2}(x)^{4}\Phi_{3}(x)^{2}\Phi_{4}(x)\\&\times \Phi_{6}(x)\end{aligned}$$


### T29 — k=7; children counts: 4 (2)

Order 18; period 12; source v31/DEGREE_PROFILE_MODELS.json, record 28.

$$B=2^{n+12},\quad a(n)=0\ (n<9).$$

$$a(n)=\left\lfloor\frac{B^{n-9}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 9).$$

$$R(x)=1$$

$$Q(x)=\Phi_{1}(x)^{9}\Phi_{2}(x)^{3}\Phi_{3}(x)^{2}\Phi_{4}(x)$$


### T30 — k=7; children counts: 7 (1)

Order 29; period 420; source v31/DEGREE_PROFILE_MODELS.json, record 29.

$$B=2^{n+24},\quad a(n)=0\ (n<8).$$

$$a(n)=\left\lfloor\frac{B^{n-8}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 8).$$

$$R(x)=1$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{8}\Phi_{2}(x)^{3}\Phi_{3}(x)^{2}\Phi_{4}(x)\\&\times \Phi_{5}(x)\Phi_{6}(x)\Phi_{7}(x)\end{aligned}$$


### T31 — k=8; children counts: 2 (1), 3 (1), 5 (1)

Order 25; period 60; source v31/DEGREE_PROFILE_MODELS.json, record 30.

$$B=2^{n+23},\quad a(n)=0\ (n<11).$$

$$a(n)=\left\lfloor\frac{B^{n-11}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 11).$$

$$\begin{aligned}R(x)&=9+17x+19x^{2}+17x^{3}+14x^{4}+9x^{5}\\&+4x^{6}+x^{7}\end{aligned}$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{11}\Phi_{2}(x)^{4}\Phi_{3}(x)^{2}\Phi_{4}(x)\\&\times \Phi_{5}(x)\end{aligned}$$


### T32 — k=8; children counts: 2 (1), 3 (3)

Order 25; period 12; source v31/DEGREE_PROFILE_MODELS.json, record 31.

$$B=2^{n+23},\quad a(n)=0\ (n<12).$$

$$a(n)=\left\lfloor\frac{B^{n-12}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 12).$$

$$\begin{aligned}R(x)&=12+15x+30x^{2}+36x^{3}+40x^{4}+32x^{5}\\&+28x^{6}+18x^{7}+8x^{8}+x^{9}\end{aligned}$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{12}\Phi_{2}(x)^{5}\Phi_{3}(x)^{2}\Phi_{4}(x)\\&\times \Phi_{6}(x)\end{aligned}$$


### T33 — k=8; children counts: 2 (1), 4 (2)

Order 30; period 24; source v31/DEGREE_PROFILE_MODELS.json, record 32.

$$B=2^{n+28},\quad a(n)=0\ (n<11).$$

$$a(n)=\left\lfloor\frac{B^{n-11}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 11).$$

$$R(x)=\sum_{j=0}^{12} c_jx^j.$$

```text
  0-12   5, 2, 9, 7, 13, 8, 13, 11, 7, 7, 5, 2, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{11}\Phi_{2}(x)^{5}\Phi_{3}(x)^{2}\Phi_{4}(x)^{2}\\&\times \Phi_{6}(x)\Phi_{8}(x)\end{aligned}$$


### T34 — k=8; children counts: 2 (1), 7 (1)

Order 32; period 420; source v31/DEGREE_PROFILE_MODELS.json, record 33.

$$B=2^{n+28},\quad a(n)=0\ (n<10).$$

$$a(n)=\left\lfloor\frac{B^{n-10}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 10).$$

$$R(x)=2+2x+x^{2}+x^{3}+x^{4}+x^{5}+x^{6}$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{10}\Phi_{2}(x)^{4}\Phi_{3}(x)^{2}\Phi_{4}(x)\\&\times \Phi_{5}(x)\Phi_{6}(x)\Phi_{7}(x)\end{aligned}$$


### T35 — k=8; children counts: 2 (2), 3 (1), 4 (1)

Order 25; period 12; source v31/DEGREE_PROFILE_MODELS.json, record 34.

$$B=2^{n+25},\quad a(n)=0\ (n<12).$$

$$a(n)=\left\lfloor\frac{B^{n-12}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 12).$$

$$\begin{aligned}R(x)&=33+81x+148x^{2}+198x^{3}+203x^{4}\\&+162x^{5}+102x^{6}+47x^{7}+15x^{8}+x^{9}\end{aligned}$$

$$Q(x)=\Phi_{1}(x)^{12}\Phi_{2}(x)^{5}\Phi_{3}(x)^{2}\Phi_{4}(x)^{2}$$


### T36 — k=8; children counts: 2 (2), 6 (1)

Order 30; period 60; source v31/DEGREE_PROFILE_MODELS.json, record 35.

$$B=2^{n+28},\quad a(n)=0\ (n<11).$$

$$a(n)=\left\lfloor\frac{B^{n-11}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 11).$$

$$\begin{aligned}R(x)&=5+7x+12x^{2}+13x^{3}+14x^{4}+11x^{5}\\&+12x^{6}+7x^{7}+6x^{8}+x^{9}+2x^{10}\end{aligned}$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{11}\Phi_{2}(x)^{5}\Phi_{3}(x)^{2}\Phi_{4}(x)^{2}\\&\times \Phi_{5}(x)\Phi_{6}(x)\end{aligned}$$


### T37 — k=8; children counts: 2 (3), 3 (2)

Order 31; period 12; source v31/DEGREE_PROFILE_MODELS.json, record 36.

$$B=2^{n+35},\quad a(n)=0\ (n<13).$$

$$a(n)=\left\lfloor\frac{B^{n-13}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 13).$$

$$R(x)=\sum_{j=0}^{15} c_jx^j.$$

```text
  0-15   55, 208, 583, 1152, 1928, 2657, 3267, 3459, 3329, 2770, 2056, 1280, 668, 263, 74, 11
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{13}\Phi_{2}(x)^{6}\Phi_{3}(x)^{3}\Phi_{4}(x)^{2}\\&\times \Phi_{6}(x)\end{aligned}$$


### T38 — k=8; children counts: 2 (3), 5 (1)

Order 33; period 60; source v31/DEGREE_PROFILE_MODELS.json, record 37.

$$B=2^{n+35},\quad a(n)=0\ (n<12).$$

$$a(n)=\left\lfloor\frac{B^{n-12}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 12).$$

$$R(x)=\sum_{j=0}^{16} c_jx^j.$$

```text
  0-16   12, 35, 88, 154, 239, 315, 380, 397, 389, 329, 258, 176, 111, 54, 25, 7, 1
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{12}\Phi_{2}(x)^{5}\Phi_{3}(x)^{3}\Phi_{4}(x)^{2}\\&\times \Phi_{5}(x)\Phi_{6}(x)\end{aligned}$$


### T39 — k=8; children counts: 2 (4), 4 (1)

Order 37; period 24; source v31/DEGREE_PROFILE_MODELS.json, record 38.

$$B=2^{n+42},\quad a(n)=0\ (n<13).$$

$$a(n)=\left\lfloor\frac{B^{n-13}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 13).$$

$$R(x)=\sum_{j=0}^{21} c_jx^j.$$

```text
  0-15   29, 97, 293, 591, 1084, 1635, 2344, 2922, 3532, 3794, 3981, 3726, 3410, 2753, 2171, 1478
 16-21   953, 501, 241, 81, 22, 2
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{13}\Phi_{2}(x)^{6}\Phi_{3}(x)^{3}\Phi_{4}(x)^{3}\\&\times \Phi_{6}(x)\Phi_{8}(x)\end{aligned}$$


### T40 — k=8; children counts: 2 (5), 3 (1)

Order 32; period 12; source v31/DEGREE_PROFILE_MODELS.json, record 39.

$$B=2^{n+36},\quad a(n)=0\ (n<14).$$

$$a(n)=\left\lfloor\frac{B^{n-14}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 14).$$

$$R(x)=\sum_{j=0}^{16} c_jx^j.$$

```text
  0-16   66, 267, 807, 1711, 3051, 4475, 5816, 6528, 6633, 5900, 4700, 3209, 1884, 880, 320, 76, 9
```

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{14}\Phi_{2}(x)^{6}\Phi_{3}(x)^{3}\Phi_{4}(x)^{2}\\&\times \Phi_{6}(x)\end{aligned}$$


### T41 — k=8; children counts: 2 (7)

Order 32; period 8; source v31/DEGREE_PROFILE_MODELS.json, record 40.

$$B=2^{n+32},\quad a(n)=0\ (n<15).$$

$$a(n)=\left\lfloor\frac{B^{n-15}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 15).$$

$$R(x)=\sum_{j=0}^{16} c_jx^j.$$

```text
  0-16   23, 64, 211, 307, 584, 639, 865, 757, 930, 706, 728, 472, 346, 155, 64, 12, 1
```

$$Q(x)=\Phi_{1}(x)^{15}\Phi_{2}(x)^{7}\Phi_{4}(x)^{3}\Phi_{8}(x)$$


### T42 — k=8; children counts: 3 (1), 6 (1)

Order 26; period 60; source v31/DEGREE_PROFILE_MODELS.json, record 41.

$$B=2^{n+20},\quad a(n)=0\ (n<10).$$

$$a(n)=\left\lfloor\frac{B^{n-10}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 10).$$

$$R(x)=2+x^{3}$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{10}\Phi_{2}(x)^{4}\Phi_{3}(x)^{2}\Phi_{4}(x)\\&\times \Phi_{5}(x)\Phi_{6}(x)\end{aligned}$$


### T43 — k=8; children counts: 3 (2), 4 (1)

Order 24; period 12; source v31/DEGREE_PROFILE_MODELS.json, record 42.

$$B=2^{n+20},\quad a(n)=0\ (n<11).$$

$$a(n)=\left\lfloor\frac{B^{n-11}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 11).$$

$$R(x)=5+3x+5x^{2}+6x^{3}+6x^{4}+2x^{5}+3x^{6}$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{11}\Phi_{2}(x)^{5}\Phi_{3}(x)^{2}\Phi_{4}(x)\\&\times \Phi_{6}(x)\end{aligned}$$


### T44 — k=8; children counts: 4 (1), 5 (1)

Order 26; period 60; source v31/DEGREE_PROFILE_MODELS.json, record 43.

$$B=2^{n+22},\quad a(n)=0\ (n<10).$$

$$a(n)=\left\lfloor\frac{B^{n-10}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 10).$$

$$R(x)=2+2x+2x^{2}+2x^{3}+x^{4}$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{10}\Phi_{2}(x)^{4}\Phi_{3}(x)^{2}\Phi_{4}(x)^{2}\\&\times \Phi_{5}(x)\end{aligned}$$


### T45 — k=8; children counts: 8 (1)

Order 37; period 840; source v31/DEGREE_PROFILE_MODELS.json, record 44.

$$B=2^{n+31},\quad a(n)=0\ (n<9).$$

$$a(n)=\left\lfloor\frac{B^{n-9}R(1/B)}{Q(1/B)}\right\rfloor\bmod B\quad(n\ge 9).$$

$$R(x)=1$$

$$\begin{aligned}Q(x)&=\Phi_{1}(x)^{9}\Phi_{2}(x)^{4}\Phi_{3}(x)^{2}\Phi_{4}(x)^{2}\\&\times \Phi_{5}(x)\Phi_{6}(x)\Phi_{7}(x)\Phi_{8}(x)\end{aligned}$$


## Explicit cyclotomic factors

$$\Phi_{1}(x)=1-x$$

$$\Phi_{2}(x)=1+x$$

$$\Phi_{3}(x)=1+x+x^{2}$$

$$\Phi_{4}(x)=1+x^{2}$$

$$\Phi_{5}(x)=1+x+x^{2}+x^{3}+x^{4}$$

$$\Phi_{6}(x)=1-x+x^{2}$$

$$\Phi_{7}(x)=1+x+x^{2}+x^{3}+x^{4}+x^{5}+x^{6}$$

$$\Phi_{8}(x)=1+x^{4}$$

$$\Phi_{9}(x)=1+x^{3}+x^{6}$$

$$\Phi_{10}(x)=1-x+x^{2}-x^{3}+x^{4}$$

$$\begin{aligned}\Phi_{11}(x)&=1+x+x^{2}+x^{3}+x^{4}+x^{5}+x^{6}+x^{7}\\&+x^{8}+x^{9}+x^{10}\end{aligned}$$

$$\Phi_{12}(x)=1-x^{2}+x^{4}$$

$$\begin{aligned}\Phi_{13}(x)&=1+x+x^{2}+x^{3}+x^{4}+x^{5}+x^{6}+x^{7}\\&+x^{8}+x^{9}+x^{10}+x^{11}+x^{12}\end{aligned}$$

$$\Phi_{14}(x)=1-x+x^{2}-x^{3}+x^{4}-x^{5}+x^{6}$$

$$\Phi_{15}(x)=1-x+x^{3}-x^{4}+x^{5}-x^{7}+x^{8}$$

$$\Phi_{16}(x)=1+x^{8}$$

$$\begin{aligned}\Phi_{17}(x)&=1+x+x^{2}+x^{3}+x^{4}+x^{5}+x^{6}+x^{7}\\&+x^{8}+x^{9}+x^{10}+x^{11}+x^{12}+x^{13}\\&+x^{14}+x^{15}+x^{16}\end{aligned}$$

$$\Phi_{18}(x)=1-x^{3}+x^{6}$$

$$\begin{aligned}\Phi_{19}(x)&=1+x+x^{2}+x^{3}+x^{4}+x^{5}+x^{6}+x^{7}\\&+x^{8}+x^{9}+x^{10}+x^{11}+x^{12}+x^{13}\\&+x^{14}+x^{15}+x^{16}+x^{17}+x^{18}\end{aligned}$$

$$\Phi_{20}(x)=1-x^{2}+x^{4}-x^{6}+x^{8}$$

$$\begin{aligned}\Phi_{21}(x)&=1-x+x^{3}-x^{4}+x^{6}-x^{8}+x^{9}-x^{11}\\&+x^{12}\end{aligned}$$

$$\begin{aligned}\Phi_{22}(x)&=1-x+x^{2}-x^{3}+x^{4}-x^{5}+x^{6}-x^{7}\\&+x^{8}-x^{9}+x^{10}\end{aligned}$$

$$\begin{aligned}\Phi_{23}(x)&=1+x+x^{2}+x^{3}+x^{4}+x^{5}+x^{6}+x^{7}\\&+x^{8}+x^{9}+x^{10}+x^{11}+x^{12}+x^{13}\\&+x^{14}+x^{15}+x^{16}+x^{17}+x^{18}+x^{19}\\&+x^{20}+x^{21}+x^{22}\end{aligned}$$

$$\Phi_{24}(x)=1-x^{4}+x^{8}$$


## Verification
- Formula records: 288
- Distinct normalized rational functions: 262
- Manifest entries verified (v32 / v31): 27 / 19
- Exact denominator products: 288
- Archived coefficient replays: 18,460
- Binomial-lane replays: 18,460
- Floor formula evaluations: 1,440
- New profile lane exports: 45
- Inherited OEIS term replays: 160

Only inherited OEIS source matches are named. No new corpus scan, Lean verification, novelty review or runtime claim. The earlier graph and array catalogues are retained unchanged in the collection.
