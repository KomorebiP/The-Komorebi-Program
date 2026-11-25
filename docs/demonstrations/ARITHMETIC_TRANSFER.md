# Arithmetic realization of recurrent and graph-walk transfers

**Author: Komorebi P.**  
**Version:** 2.2, 2026-11-24  
**Status:** mathematical proofs and exact integer/rational tests; not Lean certified or independently peer reviewed.

Predecessor: [Relative walk transfers and polynomial realization](GRAPH_TRANSFER_CONTINUATION.md). This continuation addresses the integer-solvability and finite-precision gaps.

## 1. Arithmetic transfer theorem

Let $a$ be an integer-valued nonzero recurrent sequence with monic minimal annihilator $M\in\mathbb Z[x]$ of degree $D$ over $\mathbb Q$. Let $f\in\mathbb Z[x]$. Write $N$ for the minimal polynomial of $f$ in $\mathbb Q[x]/(M)$ and $r=\deg N$. Multiplication by $f$ on the integral quotient has a monic integral characteristic polynomial divisible by $N$. Gauss's lemma gives $N\in\mathbb Z[y]$.

For an integer-valued target $b$ satisfying $N(E)b=0$, define $T_{ij}=[E^jf(E)^ia]_0$, with $0\le i<r$, $0\le j<D$, and $\beta=(b_0,\ldots,b_{r-1})^\top$. The previous theorem gives full row rank of $T$. Since $M$ is monic integral, reduction modulo $M$ preserves integral coefficients, and matching the first $r$ target terms implies equality at all indices.

Compute Smith normal form

$$UTV=[\operatorname{diag}(s_1,\ldots,s_r)\mid0],\quad s_i>0,\quad s_i\mid s_{i+1}.$$

The matrices $U,V$ are unimodular. Set $z=U\beta$. An integral multiplier exists if and only if $s_i\mid z_i$ for every $i$. Its coefficient vector is $V(z_1/s_1,\ldots,z_r/s_r,w_{r+1},\ldots,w_D)^\top$ with arbitrary integral free coordinates. Moreover,

$$\boxed{q_{\min}=\operatorname{lcm}_{i=1}^r\frac{s_i}{\gcd(s_i,z_i)}.}$$

This is the least possible common denominator of a rational multiplier: a positive integer $q$ works exactly when $q\beta$ is in the integral image, equivalently $s_i\mid qz_i$ for all $i$. A degree-restricted column submatrix uses the same formula for its nonzero pivots, provided the remaining transformed target coordinates vanish; otherwise no rational solution exists at that degree.

Over $\mathbb Z/p^h\mathbb Z$, let $e_i=\min(h,v_p(s_i))$. A target is attainable precisely when $p^{e_i}\mid z_i$. Each attainable target has exactly $p^{h(D-r)+\sum_i e_i}$ preimages, and the image has $p^{hr-\sum_i e_i}$ elements. These counts follow by solving each scalar Smith congruence and counting free coordinates. This is coefficient ambiguity, not recovery of an unknown graph.

## 2. Closed Smith profile for cyclic Chebyshev coordinates

Let $a_n=(C_m^n)_{00}$, $m\ge3$, and $c_j(x)=2T_j(x/2)$, where $T_j$ is the Chebyshev polynomial of the first kind. Take $f(x)=c_q(x)+\eta$ with $q\ge0$ and $\eta\in\mathbb Z$. Put $L=m/\gcd(m,q)$ (including $q=0$), $D=\lfloor m/2\rfloor+1$ and $r=\lfloor L/2\rfloor+1$.

**Theorem.** The Smith invariants are

$$\begin{cases}
(1,\underbrace{2,\ldots,2}_{(L-1)/2}),&L\text{ odd},\\
(1,\underbrace{2,\ldots,2}_{L/2-1},4),&L\text{ even}.
\end{cases}$$

**Proof.** In the cyclic group algebra put $x=S+S^{-1}$, $S^m=1$, and let $\ell$ extract the constant cyclic coefficient. Then $\ell(x^n)=a_n$ and $c_j(x)=S^j+S^{-j}$. All distinct cycle Fourier eigenvalues occur in $a_n$, giving degree $D$. The basis $1,c_1,\ldots,c_{D-1}$ is monic triangular, hence an integral unimodular change of basis. Its elements are orthogonal under $\ell(PQ)$ because their cyclic supports are disjoint and symmetric. The squared norms are $d_0=1$, $d_j=4$ for $2j=m$, and $d_j=2$ otherwise.

The distinct Fourier values of $f$ are $\eta+2\cos(2\pi j/L)$, giving degree $r$. The monic triangular row basis $1,c_1(y-\eta),\ldots,c_{r-1}(y-\eta)$ maps to $1,S^{iq}+S^{-iq}$. The displacements $j_i=\min(iq\bmod m,(-iq)\bmod m)$ are distinct for $0\le i<r$, with the half-turn present exactly when $L$ is even. Therefore the transformed transfer matrix is a rectangular diagonal matrix up to column permutation, with pivots $d_{j_i}$. They satisfy the Smith divisibility chain. QED.

For an admissible target, set $z_0=b_0$, $z_i=[c_i(E-\eta)b]_0$ for $1\le i<r$. A constructive rational multiplier is

$$P(x)=z_0+\sum_{i=1}^{r-1}\frac{z_i}{d_{j_i}}c_{j_i}(x).$$

Unused source basis elements give the kernel. There are no odd-prime denominator obstructions in this family; the minimum denominator divides 4, or 2 when $L$ is odd. This includes the binomial lift $f=x+2$ and stride two $f=x^2=c_2(x)+2$, not arbitrary polynomial coordinate changes.

## 3. Exact minimum denominator of cycle-to-path endpoints

Let $b_n=(P_{m-1}^{2n+m-2})_{1,m-1}$. In the lifted transfer $b_n=\ell(P(x)(x+2)^n)$, the least common denominator is **exactly 2 for every $m\ge3$**.

The upper bound follows from the all-order integral filter for $2b$ in [Cycle–Path Walk Transfers, Section 11](CYCLE_PATH_TRANSFERS.md#11-unified-linear-transfer-for-both-parities). For the lower bound, every positive-length return walk pairs with its reflection reversing all steps; the first steps are distinct. Thus $a_k$ is even for every $k>0$ and $a_0=1$. An integral $P$ consequently satisfies $\ell(P)\equiv P(0)\pmod2$. The target lacks the base 4 because all squared path eigenvalues are below 4. The source base 4 arises only from the cycle eigenvalue 2, with weight $1/m$. Independence of distinct exponential sequences implies $P(2)=0$. Hence $\ell(P)\equiv P(2)=0\pmod2$, contradicting $b_0=1$. This excludes every degree.

For odd $m$ the original stride-two transfer $b_{n+1}=\ell(P(x)x^{2n})$ also requires denominator exactly 2. The base 4 arises only from 2 because $m$ is odd. Here $b_1=m-2$ is odd; the same parity contradiction applies, and the earlier integer filter for $2b_{n+1}$ supplies the upper bound. In particular the factor two in the motivating A094233/A005023 identity cannot be removed by choosing a different integral polynomial of any degree. Other operator classes are not excluded.

For example $m=9$, $f=x+2$, the pivots are $(1,2,2,2,2)$. From $b=(1,7,34,143,560,\ldots)$ the transformed target is $z=(1,5,8,0,-14)$. Hence $P=1+\tfrac52 c_1+4c_2-7c_4$ has minimum denominator 2. This is the lifted formula for $b_n$, distinct from the original unlifted formula for $b_{n+1}$.

## 4. Exact logarithmic-derivative precision

For $p$ prime, $N\ge1$, $h\ge1$, $d\ge1$, consider the group of normalized truncated series modulo $(p^h,t^{N+1})$ and the map

$$\Gamma_d(B)=dtB'(t)/B(t).$$

The earlier relative tree transfer has $d=2$ and the general simple-path factor has $d=1$. The logarithmic derivative uses a unit series inverse, not division by integers.

Two normalized series $B,C$ have the same image exactly when $\Gamma_d(C/B)=0$. If $C/B=1+\sum_{n=1}^Nu_nt^n$, this is equivalent to $dn u_n\equiv0\pmod{p^h}$ for every $n$. Multiplication by $B$ identifies the kernel with every nonempty fiber. Therefore the exact fiber cardinality is

$$\boxed{p^{\sum_{n=1}^N\min(h,v_p(dn))}.}$$

The image cardinality is the total number $p^{hN}$ of sources divided by this number. If the source precision is $p^{H'}$ with $H'\ge h$, multiply the fiber size by $p^{(H'-h)N}$.

The sharp uniform precision for recovering a normalized integral series modulo $p^H$ from its image through degree $N$ is

$$\boxed{h_{\min}=H+v_p(d)+\lfloor\log_p N\rfloor},\qquad H\ge1.$$

Sufficiency follows from the independent congruences on the ratio coefficients: at this precision they all vanish modulo $p^H$. For necessity, take $j=p^{\lfloor\log_pN\rfloor}$ and compare $1$ with $1+p^{H-1}t^j$. Their images agree modulo $p^{H+v_p(dj)-1}$ but the sources differ modulo $p^H$. The degree-$j$ image coefficient separates them at one more digit. Thus the bound is sharp on unrestricted normalized series, not necessarily on graph-derived series. For $p=2,d=2,N=8,H=10$, the required precision is $h=14$; the image modulo $2^4$ has fibers of size $2^{15}$.

## 5. Verification and research boundaries

The companion v2.2 archive contains the exact checker, execution log, expanded proof note, SHA-256 manifest, and continuation handoff. It uses Python 3 and SymPy 1.14.0. The actual run passed 11,155 counted assertions, including 490 cyclic coordinate cases (orders 3–30), 184 independent Smith forms (orders through 18), lifted minimum-denominator tests for every order 3–100, odd stride-two tests, 80 general full-row-rank integer matrices, and 18 exhaustive small logarithmic-derivative settings with explicit precision-collision witnesses. These are overlapping finite tests, not independent theorems.

Smith normal form, Chebyshev identities, and logarithmic derivatives are classical tools. This note proves their stated arithmetic consequences. No literature-wide novelty, Lean certification, complexity improvement, graph-specific sharp precision bound, or OEIS submission is claimed. Next targets are closed arithmetic invariants for distance-regular graphs and general polynomial coordinate maps, and precision on graph-constrained families.
