# Cycle–Path Walk Transfers

**Author: Komorebi P.**  
**Version:** 2.0, 2026-11-24 (consolidated theorem and verification edition)  
**Status:** mathematical proof with exact integer verification; not Lean-certified or peer reviewed.

## Abstract

Given the return-walk sequence of a simple cycle of known order, explicit sequence transforms produce every entry of every adjacency matrix power of the path obtained by removing one vertex. The construction consists of a binomial lift to a doubled cycle and an antisymmetric boundary projection expressed by Chebyshev polynomials. Endpoint enumeration simplifies to a two-term transfer for odd cycle orders. For even orders a direct stride-two polynomial transfer is obstructed by missing spectral support, but the binomial lift removes the obstruction. The cycle sequence is also recoverable from path traces. This is an explicit sequence-level formulation of classical discrete reflection and spectral methods within Realization Calculus; no priority claim is made for the reflection principle.

## Unified formula map

Use $a_n=A_m(n)$, $b_n=B_{m-1}(n)$, $h_n=H_m(n)$, and $v_n=\operatorname{tr}(P_{m-1}^{2n})$. The core equivalence is

$
a\ \longleftrightarrow\ h\ \longleftrightarrow\ v\
\longleftrightarrow\ b.
$

The binomial lift and the affine trace transfer are invertible. The logarithmic-derivative transfer between traces and endpoint counts is triangular and invertible over normalized rational series. For graph inputs, all recovered values are integers. The linear Chebyshev projection additionally reconstructs every path matrix entry. The following sections present complete proofs, the original OEIS example, parity-dependent compression and the obstruction, the equally long prefix transfer, a uniform lifted filter, explicit matrix coefficients, and the general spectral criterion.

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

$$
\begin{aligned}
2b(n+1)={}&16a(2n)-24a(2n+1)\\
&-64a(2n+2)-6a(2n+3)\\
&+21a(2n+4).
\end{aligned}
$$

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

### Family-level OEIS correspondence

Three existing arrays cover the whole family:

- [A199571](https://oeis.org/A199571): the underlying array $w(m,k)$ equals $A_m(k)$ for $m\geq3$.
- [A259475](https://oeis.org/A259475): zero-based square-array row $m-2$ equals $B_{m-1}(n)$.
- [A198632](https://oeis.org/A198632): its underlying array of total closed path walks gives $V(p,h)=\operatorname{tr}(P_p^{2h})$.

For the endpoint array, define $F_0(t)=F_1(t)=1$ and $F_{p+1}(t)=F_p(t)-tF_{p-1}(t)$, as in A259475. The tridiagonal determinant recurrence gives $\det(I-zP_p)=F_p(z^2)$, and the endpoint cofactor is $z^{p-1}$. Consequently

$
\sum_{n\geq0}B_p(n)t^n=\frac{1}{F_p(t)}.
$

Since row $r$ of A259475 has generating function $1/F_{r+1}(t)$, the stated row correspondence follows. In particular, row 4 is A003462 shifted by one, not A003432 (the maximum-determinant sequence named in the retrieved cross-reference). The latter appears to be an OEIS cross-reference typo.

Section 6 gives an additional array-level transfer:

$
V(m-1,h)=m\sum_{j=0}^h\binom hj2^{h-j}w(m,j)-4^h.
$

### Independent OEIS data audit

The [source audit checker](../../examples/check_cycle_path_oeis.py) compares retrieved OEIS records with exact walk enumeration. It passed 868 checks: 96 cycle terms, 85 path terms, 83 endpoint transfers compared with OEIS target terms, 16 original five-term transfers evaluated using only the retrieved source and target terms, and 588 reciprocal-determinant coefficient checks against direct walks (cycle orders 3 through 30, indices 0 through 20). The last group is not downloaded OEIS data.

Run with Python 3, without optimization: `python -B examples/check_cycle_path_oeis.py`.

Source audit date: 2026-11-24. Some live pages returned HTTP 403; indexed and internal-format records were used instead. The original A094233/A005023 identity was not present in either retrieved entry's formula fields. Absence of every other family transfer has not been exhaustively established. No OEIS submissions or edits were made.

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

## 10. Reversible triangular transfer: cycle moments and endpoint counts

The earlier transfers are linear in the source sequence, but may require source terms beyond the destination index. The following alternative is nonlinear and triangular. It reconstructs the endpoint sequence and the cycle sequence from equally long prefixes, for both odd and even cycle orders.

Write $a_n=A_m(n)$, $b_n=B_{m-1}(n)$, and $h_n=H_m(n)$, with $H_m$ the binomial lift in Section 3. Define $g_n=mh_n-4^n$ for $n\geq1$. Then

$$
\boxed{2n b_n=\sum_{k=1}^n g_k b_{n-k}},\qquad b_0=1.
$$

The inverse uses only the endpoint sequence:

$$
\begin{aligned}
g_n&=2n b_n-\sum_{k=1}^{n-1}g_k b_{n-k},\\
h_0&=1,\qquad h_n=(g_n+4^n)/m,\\
a_n&=\sum_{j=0}^n\binom nj(-2)^{n-j}h_j.
\end{aligned}
$$

All divisions are exact over the integers on the specified cycle and path inputs. In particular, the first $N+1$ terms of either sequence determine the first $N+1$ terms of the other, given $m$.

### Proof and closed form

Let $F_p(t)=\det(I-zP_p)$ with $t=z^2$, as in Section 7, and let $\mathcal B_m(t)=\sum_{n\geq0}b_nt^n=1/F_{m-1}(t)$. The squared nonzero eigenvalues of $P_{m-1}$, counted once per opposite pair, are

$$
\mu_j=2+2\cos(2\pi j/m),\qquad
1\leq j\leq\lfloor(m-1)/2\rfloor.
$$

An unpaired zero eigenvalue, when present, contributes a factor of one to the determinant. Thus $F_{m-1}(t)=\prod_j(1-\mu_jt)$, and

$$
\det(I-t(2I+C_m))=(1-4t)F_{m-1}(t)^2.
$$

Indeed, the eigenvalues of $2I+C_m$ are $4$, two copies of each $\mu_j$, and one zero if $m$ is even. This determinant identity gives the generating-function transfer

$$
\boxed{\mathcal B_m(t)=
\exp\left(\frac12\sum_{n\geq1}
\frac{mh_n-4^n}{n}t^n\right)}.
$$

The exponential is formal over $\mathbb Q[[t]]$; no analytic convergence assumption is needed. To see the same identity directly, the binomial lift yields $mh_n=\operatorname{tr}((2I+C_m)^n)$, so $g_n=2\sum_j\mu_j^n$ for $n\geq1$. Taking the logarithm of $1/F_{m-1}(t)$ now gives the displayed series.

Logarithmic differentiation gives $2t\mathcal B_m'(t)=\mathcal B_m(t)\sum_{n\geq1}g_nt^n$. Coefficient comparison proves the forward recurrence. Solving for the newest $g_n$ gives the inverse recurrence, and binomial inversion recovers $a_n$. QED.

Over normalized rational series, the two triangular formulas are mutually inverse, since the coefficient of $a_n$ in the forward equation for $b_n$ is $m/(2n)$ and all other terms use earlier coordinates. Integer preservation is asserted only on the graph-derived sequences, not arbitrary integer inputs.

### Example: cycle 8 and path 7

The source cycle prefix is $a=(1,0,2,0,6,\ldots)$ (full-length moments, with odd positions zero). The lifted values are $h_1=2$, $h_2=6$, $h_3=20$. Therefore $g_1=12$, $g_2=32$, $g_3=96$. The forward recurrence gives

$$
b_1=6,\qquad b_2=26,\qquad b_3=100.
$$

These are the first nontrivial terms of A005022, and the inverse recovers $a_1=0$, $a_2=2$, $a_3=0$. This is not a fixed stride-two polynomial transfer and therefore does not contradict the obstruction in Section 5.

### OEIS scope and verification

The triangular equations apply directly between the underlying cycle array of [A199571](https://oeis.org/A199571) and row $m-2$ of [A259475](https://oeis.org/A259475). They also factor through the closed-path trace array [A198632](https://oeis.org/A198632), since $g_n=\operatorname{tr}(P_{m-1}^{2n})$ for $n\geq1$. In this way the endpoint counts alone recover the entire path trace sequence; the known order supplies its zeroth term. The order itself is recoverable from the endpoint sequence by $m=b_1+2$, because $a_1=0$.

The [triangular transfer checker](../../examples/check_cycle_path_triangular.py) independently enumerates graph walks and verifies forward and inverse recovery for cycle orders 3 through 100, indices 0 through 60. It also tests truncated prefixes and compares 54 endpoint values with the published square-array rows 1 through 9 of A259475.

```sh
python -B examples/check_cycle_path_triangular.py
```

The development run returned 13,382 explicit comparisons: 5,978 forward, 5,978 inverse, 1,372 prefix-level comparisons and 54 OEIS term comparisons, in addition to internal exact-division checks. The proof above, rather than the finite tests, establishes the unrestricted identity.

The determinant and logarithmic-derivative identities use classical spectral and symmetric-function methods. This extension identifies a different, reversible transfer class and a finite-prefix sufficiency result. It makes no claim of literature-wide priority or lower computational complexity. No Lean certification is claimed.

## 11. Unified linear transfer for both parities

The fixed-stride obstruction in Section 5 is a restriction on the *unlifted* cycle sequence. After the binomial lift, one integer polynomial filter works for every order.

Let $a_n=A_m(n)$, $h_n=H_m(n)$, $b_n=B_{m-1}(n)$. Write $c_d(x)=2T_d(x/2)$, with $c_0=2$, $c_1=x$, and $c_{d+1}=xc_d-c_{d-1}$. Define $J_m(y)$ by

$$
J_m(x^2)=x^{m-2}\bigl(c_{m-2}(x)-c_m(x)\bigr).
$$

This defines an integer polynomial uniquely, because $c_d$ has parity $d$. Set $r=\lfloor m/2\rfloor$ and

$$
M_m(x)=
\begin{cases}
(x-2)(U_r(x/2)+U_{r-1}(x/2)),&m=2r+1,\\
(x^2-4)U_{r-1}(x/2),&m=2r.
\end{cases}
$$

Both polynomials are monic, with precisely the distinct eigenvalues of the simple cycle as their roots. The even case follows from the roots $2\cos(\pi j/r)$ of $U_{r-1}(x/2)$ for $1\le j<r$, together with $2,-2$. Define

$$
R_m(y)=\operatorname{rem}_{M_m(y-2)}J_m(y).
$$

**Theorem.** For all $m\ge3$ and $n\ge0$,

$$
\boxed{2b_n=[R_m(E)h](n)},\qquad \deg R_m\le\lfloor m/2\rfloor.
$$

**Proof.** In Section 2 take $i=1$, $j=m-1$, and $k=2n+m-2$. Twice the resulting entry is $[J_m(E^2)A_{2m}](2n)=[J_m(E)h](n)$. The sequence $h$ consists of diagonal moments of $2I+C_m$, whose distinct-eigenvalue polynomial is $M_m(y-2)$. It annihilates $h$, so polynomial reduction leaves the output unchanged. Its degree is $r+1$, giving the stated degree bound. Monicity ensures integer remainders. QED.

The following coefficient vectors are in ascending powers of $y$, including a zero constant where appropriate. These filters output $2b_n$ from $h_n,h_{n+1},\ldots$; unlike the $Q_m$ of Section 4, they do not output $2b_{n+1}$ from the unlifted sequence at stride two.

| $m$ | Coefficients of $R_m$ |
|---:|---|
| 3 | 4, -1 |
| 4 | 0, 4, -1 |
| 5 | -4, 9, -2 |
| 6 | 0, -12, 11, -2 |
| 7 | 8, -46, 31, -5 |
| 8 | 0, 32, -72, 36, -5 |
| 9 | -20, 197, -272, 112, -14 |
| 10 | 0, -100, 385, -370, 126, -14 |
| 11 | 56, -834, 1873, -1401, 414, -42 |
| 12 | 0, 336, -1924, 2944, -1773, 456, -42 |
| 13 | -168, 3514, -11472, 13255, -6743, 1551, -132 |

For $m=6$, the identity is $2b_n=-12h_{n+1}+11h_{n+2}-2h_{n+3}$. At $n=0$ the lifted terms $2,6,20$ give $-24+66-40=2$. At $n=1$ the terms $6,20,70$ give $-72+220-140=8$. Thus $b_0=1$ and $b_1=4$.

For $m=8$, the identity is $2b_n=32h_{n+1}-72h_{n+2}+36h_{n+3}-5h_{n+4}$. At $n=0$ the terms $2,6,20,70$ give $64-432+720-350=2$. At $n=1$ the terms $6,20,70,252$ give $192-1440+2520-1260=12$. Thus $b_0=1$ and $b_1=6$.

### Explicit scalar-to-matrix transfer coefficients

Let $d_s=[x^s](c_{|i-j|}(x)-c_{i+j}(x))$. For a fixed path order $m-1$, define the integer matrix rows indexed by $(k,i,j)$ and columns indexed by $u\ge0$:

$$
\mathsf L_{(k,i,j),u}=
\sum_{\substack{0\le s\le i+j\\ k+s\ \mathrm{even}\\(k+s)/2\ge u}}
d_s\binom{(k+s)/2}{u}2^{(k+s)/2-u}.
$$

Then

$$
\boxed{2(P_{m-1}^k)_{ij}
=\sum_{u=0}^{\lfloor(k+i+j)/2\rfloor}
\mathsf L_{(k,i,j),u}a_u.}
$$

This is the explicit transfer matrix obtained by substituting the binomial lift into the Chebyshev projection. Each row is finite. The order is supplied, and the formula recovers the walk matrix, not an unknown graph topology. For $m=5,k=3,i=1,j=2$, the Chebyshev difference is $(4x-x^3)/2$. Hence $(P_4^3)_{12}=(4h_2-h_3)/2=(24-20)/2=2$.

## 12. Closed forms and a unified generating-function diagram

Let $\mathcal A(t)=\sum_{n\ge0}a_nt^n$, $\mathcal H(t)=\sum_{n\ge0}h_nt^n$, $\mathcal B(t)=\sum_{n\ge0}b_nt^n$, and $\mathcal V(t)=\sum_{n\ge0}\operatorname{tr}(P_{m-1}^{2n})t^n$. All identities below are formal power-series identities.

The cycle itself has the finite counting formula

$$
a_k=\sum_{\substack{0\le j\le k\\m\mid(2j-k)}}\binom{k}{j},
$$

because a walk consists of $j$ clockwise steps and $k-j$ counterclockwise steps and returns precisely when its net displacement is divisible by $m$. Its equivalent Fourier expression is $a_k=m^{-1}\sum_{j=0}^{m-1}(2\cos(2\pi j/m))^k$, with the zeroth powers interpreted as 1.

The binomial, trace and logarithmic-derivative transfers are

$$
\begin{aligned}
\mathcal H(t)&=\frac{\mathcal A(t/(1-2t))}{1-2t},\\
\mathcal A(t)&=\frac{\mathcal H(t/(1+2t))}{1+2t},\\
\mathcal V(t)&=m\mathcal H(t)-\frac1{1-4t},\\
\mathcal V(t)&=(m-1)+2t\,\mathcal B'(t)/\mathcal B(t).
\end{aligned}
$$

The constant term of the trace series is $m-1$, not zero. The two binomial formulas follow by summing the binomial transform and its inverse. The trace and logarithmic-derivative formulas follow from Sections 6 and 10.

Equivalently, if $g_k=mh_k-4^k$ for $k\ge1$, the exponential transfer has the fully finite coefficient form

$$
\boxed{
b_n=\sum_{\substack{r_1,\ldots,r_n\ge0\\
\sum_{k=1}^n kr_k=n}}
\prod_{k=1}^n\frac{1}{r_k!}
\left(\frac{g_k}{2k}\right)^{r_k}.
}
$$

The empty product and sum over the empty tuple give $b_0=1$. The formula is obtained by multiplying the series for $\exp(g_kt^k/(2k))$. For instance $b_1=g_1/2$, $b_2=g_2/4+g_1^2/8$, and $b_3=g_3/6+g_1g_2/8+g_1^3/48$. For $m=8$ these give 6, 26 and 100. Rational summands need not individually be integers; the graph-derived sum is an integer.

The reciprocal determinant also supplies a coefficient recurrence with no spectral quantities:

$$
F_p(t)=\sum_{j=0}^{\lfloor p/2\rfloor}(-1)^j\binom{p-j}{j}t^j,\qquad
b_n=\sum_{j=1}^{\min(n,\lfloor p/2\rfloor)}
(-1)^{j+1}\binom{p-j}{j}b_{n-j},
$$

where $p=m-1$. The first equality follows from the recurrence for $F_p$ and Pascal's identity. The second follows by multiplying $\mathcal B F_p=1$.

### Special mixed-dilation formulas: cycle 8 and path 7

For this subsection only, write $a(n)=\mathrm{A063376}(n)=2^n+4^n$ for $n\ge0$ and $b(n)=\mathrm{A005022}(n)$. Thus this $a(n)$ is the shifted even bisection, not the full cycle moment. Let $f(n)=4a(n)-a(n+1)$ and $d(n)=b(n+2)-4b(n+1)+2b(n)$. Then

$$
2b(n)=\sum_{j=1}^{\lfloor(n+2)/2\rfloor}\binom{n+2}{2j}f(n+1-j),
$$

$$
4a(n)=d(n)+d(2n).
$$

Indeed $f(n)=2^{n+1}$, and the reciprocal path determinant gives

$$
b(n)=\frac{(2+\sqrt2)^{n+2}+(2-\sqrt2)^{n+2}-2^{n+3}}4.
$$

Expanding the two radical powers proves the forward formula; applying the polynomial $x^2-4x+2$ kills both radical bases and gives $d(n)=4\cdot2^n$, proving the reverse formula. For example, $2b(2)=6f(2)+f(1)=48+4=52$. Also $d(0)=26-24+2=4$ and $d(1)=100-104+12=8$, $d(2)=364-400+52=16$, so $a(0)=2$, $a(1)=(8+16)/4=6$. The boundary term $a(-1)=1$ must be supplied separately. This is a different transfer class from the obstructed fixed-stride operator.

### Small cases and OEIS normalization

The following prefixes use the mathematical endpoint index $n=0$ for every row. They are generated by the universal formulas, not estimates.

| Path / cycle | $b_0,b_1,b_2,b_3,b_4$ |
|---|---|
| 2 / 3 | 1, 1, 1, 1, 1 |
| 3 / 4 | 1, 2, 4, 8, 16 |
| 4 / 5 | 1, 3, 8, 21, 55 |
| 5 / 6 | 1, 4, 13, 40, 121 |
| 6 / 7 | 1, 5, 19, 66, 221 |
| 7 / 8 | 1, 6, 26, 100, 364 |
| 8 / 9 | 1, 7, 34, 143, 560 |
| 9 / 10 | 1, 8, 43, 196, 820 |
| 10 / 11 | 1, 9, 53, 260, 1156 |
| 11 / 12 | 1, 10, 64, 336, 1581 |
| 12 / 13 | 1, 11, 76, 425, 2109 |

In addition to the individual entries in Section 7, A094811 gives $B_7(n)$ at its index $n+2$, and A094256 gives $B_8(n)$ at its index $n+1$ (including the shortest walk). The entire table belongs to the row-indexed array A259475. The A003432 cross-reference there appears to be a typo for A003462; the current records were checked again for this revision. No OEIS edits were submitted.

## 13. General finite spectral transfer theorem

The cycle/path results are a concrete instance of a general classification for scalar observables of finite real symmetric matrices. Let $a_n=u^\top A^nv$ and $b_n=s^\top B^nt$. Write their active spectral expansions as $a_n=\sum_{\lambda\in S_a}\alpha_\lambda\lambda^n$ and $b_n=\sum_{\mu\in S_b}\beta_\mu\mu^n$, retaining only nonzero weights. For a positive integer stride $q$, a fixed polynomial transfer $b_n=[P(E)a](qn)$ for all $n\ge0$ exists over the reals if and only if

$$
S_b\subseteq\{\lambda^q:\lambda\in S_a\}.
$$

To prove necessity, group terms by the powered eigenvalue and use independence of the sequences $\mu^n$ on distinct nodes (the Vandermonde determinant, with $0^0=1$ at index zero). For sufficiency, select one active source node in each powered class, assign it the value $\beta_\mu/\alpha_\lambda$ with zero for absent target weights, set the remaining node values to zero, and interpolate. The zero source/target case is interpreted separately as the zero transfer. When $S_a$ is nonempty the degree is at most $|S_a|-1$. More explicitly, for $P(x)=\sum_{j=0}^d c_jx^j$, the finite transfer system is

$$
\sum_{j=0}^{d}M_{\mu j}c_j=\beta_\mu,\qquad
M_{\mu j}=\sum_{\lambda^q=\mu}\alpha_\lambda\lambda^j.
$$

The target weight is zero at absent target nodes. This system describes degree-constrained existence and nonuniqueness, including collisions under powering. If the matrices and observable vectors are rational, rational coefficients exist whenever real coefficients do: at degree $|S_a|-1$ the equations for the first $|S_a^q\cup S_b|$ sequence indices form a consistent rational linear system; equality at those indices implies equality at every index by the Vandermonde argument. This does not imply integral coefficients or a computational advantage. The even-cycle obstruction is exactly a failure of this containment condition; lifting replaces the admissible spectral nodes.

## 14. Consolidated reproducibility record

The [unified checker](../../examples/check_cycle_path_unified.py) adds the following exact comparisons to the three earlier programs:

| New check | Count |
|---|---:|
| Cycle binomial counting formula, orders 3–100 | 3,038 |
| Reduced all-order lifted polynomial filters | 3,038 |
| Displayed filter coefficient vectors | 11 |
| Explicit scalar-to-matrix transfer rows, orders 3–16, lengths 0–8 | 11,151 |
| Finite partition formula, orders 3–100, indices 0–8 | 882 |
| Mixed-dilation order-8 identities, indices 0–40 | 82 |
| **New comparisons** | **18,202** |

All four programs were rerun with assertions enabled for version 2.0:

```sh
python -B examples/check_cycle_path.py
python -B examples/check_cycle_path_oeis.py
python -B examples/check_cycle_path_triangular.py
python -B examples/check_cycle_path_unified.py
```

Their counted comparisons total 218,546 (186,094 + 868 + 13,382 + 18,202), with overlapping mathematical cases across programs, not 218,546 independent theorems. All passed. The spectral classification in Section 13 is proved algebraically, not presented as a separate software or Lean certification. The scope remains simple cycles and paths of known order, and scalar transfers for finite real symmetric matrices. Classical reflection, determinant identities, Chebyshev recurrences and spectral interpolation are the underlying methods. No literature-wide priority claim, Lean verification, or computational complexity improvement is established.
