# Sparse index sets, Riordan lifts and universal recurrence packets

**Author: Komorebi P.**  
**Status:** exact algebraic operator constructions with explicitly qualified OEIS provenance.

## 1. Sparse index pullback

Let the requested index set for the target sequence \(b\) be \(I_b\subset\mathbb N_0\), finite. Suppose a certified target formula contains source calls \(a_{m_i n+r_i}\), with \(m_i\ge1,r_i\ge0\) in *local* index coordinates. The exact required set is

\[
I_a=\bigcup_i\{m_i n+r_i:n\in I_b\}.
\]

When a formula contains multiple inputs, take their union separately for each source sequence. Under composition the affine index maps compose as

\[
(p(mn+r)+q)=(pm)n+(pr+q).
\]

This is a set-theoretic equality, requiring no interpolation or finite matching. The compiler re-parses its whitelisted arithmetic AST, recomputes the affine maps, verifies that the supplied certificate records those maps exactly, and recomputes the normal form of the **complete** identity over rational exponential-polynomial expressions. A coefficient coincidence at 20 or 100 indices is never used as an all-index proof.

## 2. Finite indexed-workload optimization

Each atomic task is \((v,n)\). A direct action computes a task using a current exact source formula. A transfer action produces \((b,n)\) only after every certified predecessor \((a,m_i n+r_i)\) is available. Source fingerprints are checked before planning and again at execution, with optional database checks of the original OEIS formula text. Supplying a cache with a forged value fails by default even if its source hash is rewritten to appear current.

For a finite task closure \(V\), finite action set \(E\), and nonnegative declared costs, represent the available tasks by a bitmask. Every valid transition increases the number of available tasks. Therefore the state graph is acyclic. Dijkstra's algorithm finds a minimum sum of declared action costs among its valid state paths. This is a **finite exactness theorem**: action-set incompleteness, state caps, approximate cost models, and performance of a particular implementation are outside the guarantee. Large task closures are rejected explicitly rather than silently truncated.

**Example.** Let \(T_n=n(n+1)/2\), \(B_n=T_{2n}-T_n\), and \(D_n=B_{n+1}-B_n=3n+2\). At one requested \(D_{11}\), the two-hop route requires only \(T_{11},T_{12},T_{22},T_{24}\), followed by \(B_{11},B_{12}\) and \(D_{11}\), seven computed values in total. A full source prefix would have 25 values \(T_0,\ldots,T_{24}\). A sensible cost model still prefers the direct formula \(D_{11}=35\), and the regression suite checks that choice.

## 3. Shared recurrence packet bank

For a monic recurrence polynomial

\[
P(X)=X^d-c_1X^{d-1}-\cdots-c_d,
\]

the quotient ring \(\mathbb Z[X]/(P(X))\) contains exact remainders \(K_n=X^n\bmod P(X)\). For every solution of the recurrence,

\[
a_n=\sum_{j=0}^{d-1}[X^j]K_n\,a_j.
\]

The same \(K_n\) works for every initial vector with the same recurrence. For sparse indices, cache \(X^{2^j}\bmod P(X)\) once. For increasing index gaps \(\delta\), the identity

\[
K_{n+\delta}\equiv K_nK_\delta\pmod P
\]

permits sparse hopping without rebuilding full binary powers. This remains valid when \(P\) has repeated or zero roots because no division or diagonalization is used. The packet bank dynamically chooses between a direct binary decomposition and a cheaper gap composition based on modular multiplication counts. The complexity is \(O(d^2\log n)\) ring arithmetic in the traditional schoolbook model, **not a fixed-bit-cost bound**. Actual big-integer multiplication costs must still be measured.

For an extracted formula \(\sum_\lambda Q_\lambda(n)\lambda^n\), the factor \((S-\lambda)^{\deg Q_\lambda+1}\) is an all-index annihilator of each component. Their product is therefore an annihilator of the sum. Only integral-rate, integral-recurrence, integer-initial-value cases are promoted into the current packet implementation.

## 4. Formal Riordan operator from the uploaded archive

The historical archive's independently retained formula is

\[
\mathcal R_{c,s,r,t}[A](x)=(1-cx)^{-s} A\!\left(\frac{x^r}{(1-cx)^t}\right),
\quad c\in\mathbb Z,\ s\ge0,\ r,t\ge1.
\]

With \(A(x)=\sum_{k\ge0} a_kx^k\), the coefficient identity is

\[
\boxed{b_n=\sum_{k=0}^{\lfloor n/r\rfloor}
 a_k\,c^{n-rk}\binom{s+tk+n-rk-1}{n-rk}}
\]

when \(s+tk\ge1\); if \(s+tk=0\), the binomial coefficient factor is interpreted as \(\delta_{n,rk}\). It follows by exact formal binomial expansion. This endpoint matters for the formal identity at \(s=k=0\).

When \(r=t=1\), the substitutions \(x\mapsto x/(1-cx)\) and \(x\mapsto x/(1+cx)\) invert each other, and the multiplicative weights cancel, proving

\[
\mathcal R_{-c,s,1,1}\circ\mathcal R_{c,s,1,1}=\operatorname{Id}.
\]

When \(r>1\), \(x^r\) ramifies the substitution, and an inverse on *all* of \(\mathbb Q[[x]]\) does not follow from this calculation. No inverse is admitted for those seven archived cases.

The original v0.8 release recorded 41 source/target rational OGF matches. A new, independent standard-library implementation here re-derived **all 41 exact identities in \(\mathbb Q(x)\)** and compared source OGF coefficients, target OGF coefficients and independently computed transformed coefficients at 25 local indices each. This is **2,050** source/target term checks plus **1,025** transform checks. All passed. Their original source association is a mathematical premise when sourced only from OEIS asserted generating functions; current stored term agreement is not its independent proof.

## 5. Quadratic polyphase transfer

For \(q\ge0\) and \(c\in\mathbb Z\), expand in the quadratic algebra \(\mathbb Z[\sqrt q]\):

\[
(c+\sqrt q)^n=B_n+\sqrt q D_n,
\]
\[
B_n=\sum_k\binom n{2k}c^{n-2k}q^k,
\quad D_n=\sum_k\binom n{2k+1}c^{n-2k-1}q^k.
\]

The pair multiplies according to

\[
(B,D)(B',D')=(BB'+qDD',BD'+DB').
\]

Therefore a single binary exponentiation evaluates both channels, and conjugation proves the exact norm identity

\[
B_n^2-qD_n^2=(c^2-q)^n.
\]

It also follows that \(B,D\) both satisfy

\[
u_{n+2}=2c\,u_{n+1}+(q-c^2)u_n.
\]

The even channel is the Riordan specialization \(\mathcal R_{c,1,2,2}[1/(1-qx)]\), and the odd channel is the degree-one shift of \(\mathcal R_{c,2,2,2}[1/(1-qx)]\). This recovers Pell-type sequences from the power source \(q^k\). The independent current-OEIS excerpt replay passed 30 and 27 indices for the two documented specializations.

## 6. Provenance and limits

The historical sample came from the user-supplied `Komorebi_OEIS_All_Versions_Through_v0_8.zip` (SHA-256 `ddffa4423a6001c82bcc3eda97d06557ca1e62358db2ab285060caf385b72244`), with original audit at `current/komorebi_oeis_v08/EXACT_RESULTS_V08.md`. Its data collection contained 96 sampled records, **not** the full official OEIS. This release uses the separately retained 99,999-sequence snapshot (`a121d7a6a5b6aa78a5a333fe748b604f170511bf8250ca16533f58cbcfa9e9f5`) and preserves both evidence lineages.

The older archive also records a Riccati projective matrix lift, a companion matrix EGF correspondence, and a non-computational Fibonacci-to-Euler Möbius expression. Those have not been imported into the active sparse proof graph in this release. In particular, the Fibonacci-to-Euler expression algebraically collapses to an elementary complex exponential and is not a demonstrated Euler-number speedup.

The provided timing receipt separately measures sparse recurrence packet reuse and quadratic powering against explicit comparators. It is not evidence of optimal big-integer arithmetic or a general advantage for each of the 110 indexed transfers. Source verification can cost more than the actual arithmetic for simple polynomial formulas.
