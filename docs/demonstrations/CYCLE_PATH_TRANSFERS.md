# Cycle–Path Walk Transfers

**Author: Komorebi P.**  
**Version:** 1.1, 2026-11-24 (audited revision)  
**Status:** mathematical proof with exact integer verification; not Lean-certified or peer reviewed.

## Abstract

Given the return-walk sequence of a simple cycle of known order, explicit sequence transforms produce every entry of every adjacency matrix power of the path obtained by removing one vertex. The construction consists of a binomial lift to a doubled cycle and an antisymmetric boundary projection expressed by Chebyshev polynomials. Endpoint enumeration simplifies to a two-term transfer for odd cycle orders. For even orders a direct stride-two polynomial transfer is obstructed by missing spectral support, but the binomial lift removes the obstruction. The cycle sequence is also recoverable from path traces. This is an explicit sequence-level formulation of classical discrete reflection and spectral methods within Realization Calculus; no priority claim is made for the reflection principle.

## 1. Definitions

For an integer $m\geq3$, let $C_m$ denote the adjacency matrix of the simple, undirected cycle on $m$ vertices, and let $P_{m-1}$ denote the adjacency matrix of the simple path on vertices $1,\ldots,m-1$. The cycle is indexed modulo $m$. All edges have weight one, and walks may revisit vertices and edges. A matrix power counts walks of exactly the indicated length.

$$
A_m(k)=(C_m^k)_{00},\qquad
B_{m-1}(n)=(P_{m-1}^{2n+m-2})_{1,m-1}.
$$

All indices $k,n$ are nonnegative integers. In particular $A_m(0)=B_{m-1}(0)=1$. The shortest endpoint walk has length $m-2$; the index $n$ counts additional pairs of steps. Endpoint walks of the opposite parity vanish. Write $E f(k)=f(k+1)$ for the forward shift and $T_d,U_d$ for the Chebyshev polynomials of the first and second kinds. For a polynomial $q(x)=\sum_d q_dx^d$, the notation $[q(E)f](k)$ means $\sum_d q_df(k+d)$.

## 2. Theorem: complete scalar-to-matrix reconstruction

For every $m\geq3$, $k\geq0$, and $1\leq i,j<m$,

$$
(P_{m-1}^{k})_{ij}
=\bigl[T_{|i-j|}(E/2)-T_{i+j}(E/2)\bigr]A_{2m}(k).
$$

The entire source sequence on the right is obtained from $A_m$:

$$
A_{2m}(2h)=\sum_{r=0}^{h}\binom{h}{r}2^{h-r}A_m(r),
\qquad A_{2m}(2h+1)=0.
$$

These formulas give a rational linear transfer from the scalar sequence to a matrix entry. Only the source terms through index $\lfloor(k+i+j)/2\rfloor$ are needed for that entry. The polynomials $2T_d(x/2)$ have integer coefficients, as follows from their initial values 2 and $x$ and recurrence $p_{d+1}(x)=xp_d(x)-p_{d-1}(x)$. The final division by two is exact for cycle-walk inputs. The supplied order already fixes both graph structures; the result gives an explicit enumeration transfer, not an inference of an unknown graph.

**Proof.** Let $S$ be cyclic translation on the vector space with basis indexed modulo $2m$. Then $C_{2m}=S+S^{-1}$. Reflection sends $e_i$ to $e_{-i}$ and commutes with $C_{2m}$. The vectors

$$
f_i=(e_i-e_{-i})/\sqrt2,\qquad 1\leq i<m,
$$

form an orthonormal basis of the reflection-odd subspace. In this basis the restriction of $C_{2m}$ is exactly $P_{m-1}$: the endpoints at 0 and $m$ vanish, and the other coordinates have their two ordinary neighbors. Consequently

$$
(P_{m-1}^k)_{ij}
=(C_{2m}^k)_{i,j}-(C_{2m}^k)_{i,-j}.
$$

The recurrence for $T_d$ gives $2T_d(C_{2m}/2)=S^d+S^{-d}$, including $d=0$. Since cycle walk kernels are translation invariant and symmetric, applying this polynomial to the diagonal moment gives the walk count at displacement $d$. Substitution proves the entry formula.

For the lift, $C_{2m}^2=2I+S^2+S^{-2}$. On the even-indexed vertices, the last two terms are precisely the adjacency operator of $C_m$. Taking the $(0,0)$ entry of its $h$-th binomial expansion gives the asserted transform. Odd lengths cannot return on a bipartite cycle. QED.

## 3. Theorem: universal endpoint transfer

Put $L=2n+m-2$ and $D_m(k)=A_m(k+2)-4A_m(k)$. Then

$$
\boxed{2B_{m-1}(n)=D_m(L)-D_{2m}(L).}
$$

For odd $m$, $L$ is odd, so the doubled-cycle term vanishes:

$$
2B_{m-1}(n)=A_m(2n+m)-4A_m(2n+m-2).
$$

For even $m$, define $h=n+(m-2)/2$ and $H_m(h)=\sum_{r=0}^h\binom hr 2^{h-r}A_m(r)$. Then

$$
2B_{m-1}(n)=A_m(2h+2)-4A_m(2h)-H_m(h+1)+4H_m(h).
$$

**Proof.** The cycle $C_{2m}$ has Fourier eigenvalues $\lambda_j=2\cos(\pi j/m)$, $0\leq j<2m$, each counted with its Fourier multiplicity. Its diagonal moment is the uniform average of their powers, using the usual convention that a zeroth matrix power is the identity. For the endpoint pair $(1,m-1)$, the multiplier at Fourier index $j$ is

$$
T_{m-2}(\lambda_j/2)-T_m(\lambda_j/2)
=\tfrac12(-1)^j(\lambda_j^2-4).
$$

Consequently $2B_{m-1}(n)$ is the uniform average of $(-1)^j(\lambda_j^2-4)\lambda_j^L$. The even-indexed Fourier modes are precisely those of $C_m$, and twice the even contribution minus the total equals $D_m(L)-D_{2m}(L)$. QED.

## 4. Odd cycle polynomial compression

For $m=2r+1$, the distinct eigenvalues of $C_m$ are roots of the monic integer polynomial

$$
M_m(x)=(x-2)\bigl[U_r(x/2)+U_{r-1}(x/2)\bigr].
$$

Indeed the expression in brackets, at $x=2\cos\theta$, equals $\sin(m\theta/2)/\sin(\theta/2)$ by the sine addition identity. Its roots are exactly $2\cos(2\pi j/m)$, $1\leq j\leq r$, and the recurrence for $U$ proves integrality and monicity. Thus $M_m(E)A_m=0$.

Define the integer polynomial

$$
Q_m(x)=\operatorname{rem}_{M_m(x)}\bigl(x^m(x^2-4)\bigr).
$$

Its degree is at most $r$. The endpoint theorem and the annihilator give

$$
\boxed{2B_{m-1}(n+1)=[Q_m(E)A_m](2n).}
$$

The corresponding formula for $B_{m-1}(n)$ uses the remainder of $x^{m-2}(x^2-4)$.

| Cycle order | $Q_m(x)$ |
| --- | --- |
| 3 | $2-x$ |
| 5 | $2x^2-5x+2$ |
| 7 | $9x^2-14x-8$ |
| 9 | $21x^4-6x^3-64x^2-24x+16$ |
| 11 | $55x^5+66x^4-308x^3-229x^2+242x+80$ |
| 13 | $221x^6+143x^5-1183x^4-858x^3+1471x^2+715x-242$ |

These six remainders were independently checked by exact polynomial arithmetic. In particular, the motivating transfer from A094233 to A005023 is exactly the order-9 remainder, not a fitted formula.

For clarity, write $a=\mathrm{A094233}$ and $b=\mathrm{A005023}$. The original identity holds for every $n\geq0$ (the target index is always at least 1):

$
\begin{aligned}
2b(n+1)={}&16a(2n)-24a(2n+1)\\
&-64a(2n+2)-6a(2n+3)\\
&+21a(2n+4).
\end{aligned}
$

At $n=0$, the right-hand side is $16-128+126=14$, so $b(1)=7$. At $n=1$ it is $32-384+420=68$, so $b(2)=34$.

## 5. Obstruction for even cycles

For every even $m\geq4$, no fixed polynomial $R$, even with arbitrary real coefficients, can satisfy

$$
B_{m-1}(n)=[R(E)A_m](2n)
\quad\text{for all } n\geq0.
$$

**Proof.** Such an output is a linear combination of exponentials with bases $4\cos^2(2\pi j/m)$. The path endpoint sequence has a nonzero term with base $4\cos^2(\pi/m)$, by pairing the two eigenvalues of largest absolute value in its sine basis. The corresponding endpoint weights reinforce each other at the compatible parity $L=2n+m-2$; their combined coefficient is positive. This base lies strictly between the largest squared cycle eigenvalue below 4, namely $4\cos^2(2\pi/m)$, and 4. It is therefore absent from the source's squared spectrum. Distinct exponential sequences are linearly independent by the Vandermonde determinant. QED.

This is a restriction on the operator class, not on reconstruction in general. The binomial lift in Section 2 changes the available spectral bases to $2+2\cos(2\pi j/m)$, supplying the required spectral support without any extra source sequence. No claim of a computational complexity improvement is made.

**Exact rejection example.** For $m=4$, the even moments of $C_4$ have bases 0 and 4. The polynomial $p(x)=x(x-4)$ annihilates both bases. However, the endpoint sequence on $P_3$ is $2^n$, and $[p(E)2^n](n)=-4\cdot2^n$ is nonzero. Here $E$ shifts the index of the bisection or endpoint sequence. For general even $m$, the checker uses $p(x)=2T_{m/2}((x-2)/2)-2$, which vanishes on all squared cycle eigenvalues, and checks that the target fails its annihilating recurrence.

## 6. Inverse reconstruction

The correspondence also has a trace-level inverse. For every $k\geq0$,

$$
2m A_{2m}(k)=2^k+(-2)^k+2\operatorname{tr}(P_{m-1}^k).
$$

To prove this, the path sine eigenvectors give its spectrum $\lambda_j=2\cos(\pi j/m)$ for $1\leq j<m$. The doubled cycle contains two copies of those eigenvalues and one copy each of 2 and -2. Taking the trace proves the identity. Binomial inversion of Section 2 now gives

$$
A_m(n)=\sum_{h=0}^n\binom nh(-2)^{n-h}A_{2m}(2h).
$$

Thus the scalar sequence and the path trace sequence are mutually reconstructible when the order is known. The inverse is affine in the trace data because the two boundary eigenvalues contribute known terms.

## 7. OEIS examples and indexing

The following entries are illustrations of the theorem, not independent proofs. In the table, $a$ is the named cycle entry and $b$ the named path entry. It is important to distinguish the full moment sequence from its even-length bisection.

| Path / cycle orders | Cycle entry and normalization | Path entry and normalization |
| --- | --- | --- |
| 2 / 3 | [A078008](https://oeis.org/A078008): $A_3(k)=a(k)$ | [A000012](https://oeis.org/A000012): $B_2(n)=b(n)=1$ |
| 3 / 4 | [A199573](https://oeis.org/A199573): $A_4(k)=a(k)$ | [A000079](https://oeis.org/A000079): $B_3(n)=b(n)=2^n$ |
| 4 / 5 | [A054877](https://oeis.org/A054877): $A_5(k)=a(k)$ | [A001906](https://oeis.org/A001906): $B_4(n)=b(n+1)$ |
| 5 / 6 | [A047849](https://oeis.org/A047849): $A_6(2h)=a(h)$ | [A003462](https://oeis.org/A003462): $B_5(n)=b(n+1)$ |
| 6 / 7 | [A094659](https://oeis.org/A094659): $A_7(k)=a(k)$ | [A005021](https://oeis.org/A005021): $B_6(n)=b(n)$ |
| 7 / 8 | [A063376](https://oeis.org/A063376): $A_8(2h)=a(h-1)$ | [A005022](https://oeis.org/A005022): $B_7(n)=b(n)$ |
| 8 / 9 | [A094233](https://oeis.org/A094233): $A_9(k)=a(k)$ | [A005023](https://oeis.org/A005023): $B_8(n)=b(n)$ for $n\geq1$; extend by $B_8(0)=1$ |

For the even cycles all odd moments are zero, including when an OEIS entry records only the even bisection. The special case $P_2,C_3$ gives the constant endpoint sequence 1, and $P_3,C_4$ gives $2^n$.

Here are two worked examples with the mathematical index starting at zero:

- **Path 4 / cycle 5.** $2F_{2n+2}=A_5(2n+5)-4A_5(2n+3)$. The first value is $(2-4\cdot0)/2=1$, and the next is $(14-4\cdot2)/2=3$.
- **Path 5 / cycle 6.** With $a=\mathrm{A047849}$, the formula becomes $2B_5(n)=a(n+3)-4a(n+2)-H_6(n+3)+4H_6(n+2)$. The lift gives $H_6(2)=6$ and $H_6(3)=20$, hence $2B_5(0)=22-24-20+24=2$. The sequence is $(3^{n+1}-1)/2$, which agrees with A003462 shifted by one.

For $P_7$ the endpoint sequence begins $1,6,26,100,364$; for $P_8$ it begins $1,7,34,143,560$. These normalizations are essential: A063376 records only even-length cycle counts and starts at index -1, while A005023 omits the shortest walk and starts at index 1. The OEIS mappings in the table were rechecked on 2026-11-24.

## 8. Verification and research boundary

Run the standalone [integer checker](../../examples/check_cycle_path.py) from the repository root:

```sh
python -B examples/check_cycle_path.py
```

The audited checker uses only Python's standard library. Run it without the `-O` optimization flag, which disables assertions. Its output is:

```text
{'doubling': 3220, 'endpoints': 588, 'entries': 179634, 'trace': 1148, 'inverse': 588, 'polynomial': 294, 'coefficients': 6, 'obstruction': 602, 'fixtures': 14}
PASS: 186094 exact assertions
```

| Check | Assertions |
| --- | ---: |
| Binomial lift, including zero odd moments | 3,220 |
| Endpoint transfer | 588 |
| Every entry of path powers for lengths 0 through 20 | 179,634 |
| Trace identity for lengths 0 through 40 | 1,148 |
| Inverse reconstruction from path traces | 588 |
| Odd-order polynomial transfer | 294 |
| Published polynomial coefficient vectors | 6 |
| Even-order annihilator and rejection controls | 602 |
| Cycle and path prefix fixtures | 14 |
| **Total** | **186,094** |

Cycle orders 3 through 30 are covered. The checker enumerates walks directly with integers independently of the spectral formulas. It also checks all seven displayed OEIS pairs using normalized short prefixes. Each prefix comparison and each rejection control counts as one assertion, not one assertion per term. These finite tests support reproducibility; the mathematical proofs establish the universal statements. No Lean certificate or independent peer review is claimed.

The scope is exact enumeration for paths and cycles of known order. It is not a theorem that arbitrary graphs can be recovered from return moments. More general spectral transfer classification and complexity analysis are future work.

## 9. Relation to earlier work

Reflection, discrete Fourier diagonalization, and Chebyshev representations of path and cycle walk kernels are established techniques. In particular:

- J. S. Dowker, [Heat-kernels on the discrete circle and interval](https://arxiv.org/abs/1207.2096), 2012, Section 7, gives the Dirichlet interval kernel by images with reflection boundaries at 0 and $m$. This is closely related to Section 2: the difference of the two periodic kernels gives the Dirichlet kernel, and the coefficients of the adjacency exponential give the corresponding walk counts.
- C. J. Everett and P. R. Stein, *The combinatorics of random walk with absorbing barriers*, Discrete Mathematics 17 (1977), 27–45, is a classical reference listed by the OEIS path entries.
- [OEIS A199571](https://oeis.org/A199571) tabulates cycle return-walk counts, with spectral and Chebyshev descriptions.

The focus here is the explicit composition of scalar sequence transforms, compressed integer coefficients, the even-order operator obstruction, and the bidirectional reconstruction statement as a case study of Realization Calculus. The projection is a classical method. The paper records its sequence-level consequences and does not claim to have discovered the underlying cycle-to-path reflection relation. The original order-9 relation was not present in the A094233 and A005023 formulas examined. Absence from OEIS does not establish publication novelty. A literature-wide priority review is outstanding.
