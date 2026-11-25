# Arithmetic reconstruction on distance-regular graphs

**Author: Komorebi P.**  
**Version:** 2.3, 2026-11-24  
**Status:** algebraic proofs and exact computational tests. Not Lean certified or independently peer reviewed.

Predecessor: [Arithmetic realization of recurrent and graph-walk transfers](ARITHMETIC_TRANSFER.md).

## 1. Integral orthogonal basis

Let $G$ be a finite connected simple undirected distance-regular graph of diameter $d\ge1$, adjacency matrix $A$, valency $k$, and intersection numbers $b_i,c_i,a_i=k-b_i-c_i$. Let $A_i$ be the distance-$i$ matrix and $k_i$ the size of a distance-$i$ shell. Set

$$C_i=\prod_{j=1}^i c_j,\quad B_i=\prod_{j=0}^{i-1}b_j,\quad C_0=B_0=1.$$

Counting edges between successive shells gives $k_i C_i=B_i$. The moment functional is $\ell(x^n)=m_n=(A^n)_{oo}$ at a fixed vertex $o$.

Define monic integer polynomials

$$p_0=1,\quad p_1=x-a_0,$$

$$p_{i+1}=(x-a_i)p_i-b_{i-1}c_i p_{i-1}\quad(1\le i\le d).$$

The distance-matrix recurrence $AA_i=b_{i-1}A_{i-1}+a_iA_i+c_{i+1}A_{i+1}$ (with absent boundary terms omitted) gives $p_i(A)=C_iA_i$ for $0\le i\le d$ and $p_{d+1}(A)=0$. Since distance shells are disjoint and the matrices symmetric,

$$\ell(p_ip_j)=\delta_{ij}C_i^2k_i=\delta_{ij}B_iC_i.$$

Thus the moment pairing is positive definite on degrees at most $d$. No annihilator of smaller degree than $p_{d+1}$ exists for the scalar moments, since it would be orthogonal to itself.

## 2. Exact Smith invariants and precision

Let $H=(m_{i+j})_{0\le i,j\le d}$. If $W$ has as its columns the monomial coefficients of $p_i$, it is integral unit upper triangular, and

$$W^\top HW=\operatorname{diag}(s_0,\ldots,s_d),$$

$$\boxed{s_0=1,\quad s_i=\prod_{j=1}^i b_{j-1}c_j.}$$

The successive ratios $s_i/s_{i-1}=b_{i-1}c_i$ are positive integers, so this is already Smith normal form.

For a target sequence annihilated by $p_{d+1}$, let $\beta$ be its first $d+1$ terms and $z=W^\top\beta$. The integral multiplier criterion is $s_i\mid z_i$ for every $i$. The least common denominator is

$$q_{\min}=\operatorname{lcm}_i\frac{s_i}{\gcd(s_i,z_i)}.$$

For a prime $p$, each attainable target modulo $p^h$ has exactly $p^{\sum_i\min(h,v_p(s_i))}$ canonical coefficient preimages. The sharp uniform precision needed in target data to recover the multiplier modulo $p^H$ is $H+v_p(s_d)$ for $H\ge1$. These statements follow by the independent Smith congruences; sharpness follows by varying the last transformed coefficient by $p^{H-1}$. They concern coefficient recovery, not topology reconstruction.

## 3. Minimum denominators for distance-conditioned walks

If $\operatorname{dist}(u,v)=i$, then

$$\boxed{(A^n)_{uv}=\frac{[p_i(E)m]_n}{B_i},\qquad n\ge0.}$$

Indeed, every power of $A$ lies in the distance algebra, so its entries are constant on distance relations. Consequently $\ell(x^np_i)=C_i(A^nA_i)_{oo}=C_i k_i(A^n)_{uv}$.

The denominator $B_i$ is minimal over all fixed polynomial multipliers. Nondegeneracy of the pairing implies that every multiplier for this target reduces to $p_i/B_i$ modulo the monic integral annihilator. Its leading coefficient is $1/B_i$. Integral polynomial reduction cannot introduce denominators, so any common denominator must be divisible by $B_i$.

For Hamming graphs $H(d,q)$, $b_i=(d-i)(q-1)$ and $c_i=i$. For Johnson graphs $J(v,k)$ with $k\le v/2$, $b_i=(k-i)(v-k-i)$ and $c_i=i^2$. These are obtained by counting changes of coordinates or exchanges of subset elements. The hypercube is the case $q=2$.

| Family | Smith invariant $s_i$ | Minimum denominator $B_i$ |
|---|---|---|
| Cycle $C_m$, $i>0$ | 2, except 4 at the even-cycle antipode | 2 |
| Hypercube $Q_d$ | $(i!)^2\binom di$ | $(d)_i$ |
| Hamming $H(d,q)$ | $(i!)^2\binom di(q-1)^i$ | $(d)_i(q-1)^i$ |
| Johnson $J(v,k)$ | $(i!)^4\binom ki\binom{v-k}i$ | $(k)_i(v-k)_i$ |

Here $(z)_i$ is a falling factorial and $s_0=B_0=1$ in every case.

For $Q_3$, the Smith profile is $(1,3,12,36)$. At distance two, $p_2=x^2-3$ and $B_2=6$. Since $m_2=3$ and $m_4=21$, the length-two transfer gives $(21-3\cdot3)/6=2$ walks.

This theorem concerns distances within a graph, not the distinct cycle-to-path target of the predecessor.

## 4. Bipartite stride-two specialization

If $G$ is bipartite, $a_i=0$, and $p_i$ has parity $i$. The spectrum is symmetric under negation and has $d+1$ distinct eigenvalues, since $A$ is symmetric with minimal polynomial $p_{d+1}$. For $f(x)=x^2+\eta$, $\eta\in\mathbb Z$, its number of distinct values is $r=\lfloor d/2\rfloor+1$.

For the rectangular transfer matrix $T_{ij}=\ell(f(x)^i x^j)$ with $0\le i<r$, $0\le j\le d$, replace the row monomials by the monic integer polynomials $p_{2i}(\sqrt{y-\eta})$. The column change to $p_j$ gives $\ell(p_{2i}p_j)$. A column permutation therefore produces a Smith profile

$$\boxed{s_0,s_2,\ldots,s_{2\lfloor d/2\rfloor}.}$$

The result is not asserted for arbitrary polynomial coordinate changes.

## 5. Finite-prefix reconstruction and the topology boundary

The moments $m_0,\ldots,m_{2d}$ determine the intersection array of a distance-regular graph of known diameter $d$.

Monic Gram-Schmidt for the moment pairing recovers $p_0,\ldots,p_d$ and $s_i=\ell(p_i^2)$. This needs no moments above degree $2d$. For $i<d$, $\alpha_i=\ell(xp_i^2)/s_i=a_i$ by the three-term recurrence. Put $\beta_i=s_i/s_{i-1}=b_{i-1}c_i$ and $k=m_2$. Starting at $b_0=k$, recover

$$c_i=\beta_i/b_{i-1},\qquad b_i=k-\alpha_i-c_i\quad(1\le i<d).$$

Finally $c_d=\beta_d/b_{d-1}$, $b_d=0$, $a_d=k-c_d$. For leading moment determinants $\Delta_i$, with $\Delta_{-1}=1$, the equivalent norm formula is $s_i=\Delta_i/\Delta_{i-1}$. The recovered array determines all distance-conditioned walk counts by Section 3.

This does not recover graph topology. The rook graph $H(2,4)$ and Shrikhande graph both have $b=(6,3,0)$, $c=(0,1,2)$, $a=(0,2,4)$. For the latter use the Cayley graph on $(\mathbb Z/4\mathbb Z)^2$ with generators $(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1)$. The differences of distinct ordered generators attain each nonzero element twice, giving common-neighbor counts of two. The rook graph has the same counts by its row-column construction. Yet its clique number is four while the Shrikhande graph's is three, since every Shrikhande neighborhood is a six-cycle. They are nonisomorphic and have identical scalar return moments and distance-conditioned walks.

## 6. Verification and research limits

The standalone v2.3 archive contains the expanded proof note, exact checker, execution log, requirements and SHA-256 manifest. Python 3 with NetworkX 3.6.1 and SymPy 1.14.0 was used. The completed run passed **25,116 counted comparisons** across 128 intersection-array cases: 19 cycles, 40 Hamming parameter pairs, 62 Johnson pairs and seven additional named graphs. It independently computed 128 square and 19 rectangular Smith normal forms. Explicitly constructed graphs were checked for their intersection arrays at every vertex, and direct adjacency enumeration was compared through length ten from one root. Larger Hamming and Johnson cases used their derived arrays instead of constructing the full graph. Tests overlap and are not independent theorems.

The underlying orthogonal polynomials, distance-matrix recurrence and Smith form are classical. No literature-wide novelty, Lean certification, independent review or graph-constrained sharp precision bound is claimed. Next: analyze the coordinate matrix of arbitrary polynomial changes in the integral orthogonal basis, then extend to association schemes and equitable partitions.
