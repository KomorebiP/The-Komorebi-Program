# Relative walk transfers and polynomial realization of recurrent sequences

**Author: Komorebi P.**  
**Continuation:** Cycle–Path Realization and Reconstruction Calculus, v2.0.  
**Status:** mathematical proofs and exact computational tests. Not Lean certified or independently peer reviewed.

Predecessor: [Cycle–Path Walk Transfers v2.0](https://github.com/KomorebiP/The-Komorebi-Program/blob/da20e784db35e19bc5a57927729107a7c6739767/docs/demonstrations/CYCLE_PATH_TRANSFERS.md).

## 1. Relative spectral transfer for arbitrary trees

Let $T$ be a finite simple tree with adjacency matrix $A_T$. For vertices $u,v$ (possibly equal), let $P$ be the unique simple path joining them, $d$ its edge length, and $F=T-V(P)$ the induced forest obtained by deleting its vertices. The empty forest has determinant 1 and traces 0. Define

$$b_n=(A_T^{2n+d})_{uv},\qquad g_n=\operatorname{tr}(A_T^{2n})-\operatorname{tr}(A_F^{2n}),\quad n\ge1,$$

with $b_0=1$ (there is exactly one shortest walk). Then the forward and inverse transfers are

$$\boxed{2nb_n=\sum_{k=1}^n g_k b_{n-k}},\qquad
\boxed{g_n=2nb_n-\sum_{k=1}^{n-1}g_k b_{n-k}}.$$

The generating function is

$$\sum_{n\ge0}b_nt^n=\exp\left(\sum_{n\ge1}\frac{g_n}{2n}t^n\right).$$

In particular, equally long positive-index prefixes of the two sequences determine one another. The relative trace $g_n$ counts closed walks of length $2n$ with a specified starting vertex whose vertex set intersects $P$. Indeed, subtracting the forest trace deletes precisely the walks avoiding all of $P$. This supplies a nonnegative integer interpretation, not just a spectral difference. All odd or too-short endpoint lengths vanish by bipartiteness and distance.

The proof follows from the more general simple-path formula in Section 2. In the case of nonzero symmetric edge weights, divide the weighted walk count defining $b_n$ by the product of the edge weights on $P$. Then the same formulas hold over any characteristic-zero field, with the weighted adjacency matrices. The nonnegative integer interpretation is asserted for unweighted walks, or nonnegative integer weights in the relative trace, not arbitrary signed weights. The weight product must be nonzero.

### Examples and recovery boundary

For $T=P_p$ with opposite endpoints, $F$ is empty. The trace becomes $g_n=\operatorname{tr}(P_p^{2n})$, exactly the previous triangular path transfer. The earlier cycle lift expresses this as $m H_m(n)-4^n$, with $m=p+1$.

For the star $K_{1,4}$, take two distinct leaves. Their unique path has two edges, and $F$ consists of two isolated vertices. The nonzero eigenvalues of the star are $2,-2$, so $g_n=2\cdot4^n$. The recurrence gives $b_1=8/2=4$ and $b_2=(8\cdot4+32)/4=16$. In general $b_n=4^n$, since its generating function is $1/(1-4t)$.

**Failure control.** The whole-graph trace and distance are insufficient by themselves, even for a fixed tree. On $P_4$, the adjacent pair $(1,2)$ has off-path forest $P_2$, while $(2,3)$ has two isolated vertices. Both have distance one, and the full second trace is 6. Their $g_1$ values are 4 and 6 respectively, so their length-three walk counts are 2 and 3. Thus no formula using only the unmarked full trace and distance can recover the marked walk sequence in all trees. The deleted-forest trace is essential in this operator class.

## 2. All finite graphs: simple-path decomposition

Let $G$ be any finite simple undirected graph, with symmetric weights $w_{ij}$ in a characteristic-zero field, adjacency $A_G$, and no self-loops. Let $\mathcal P_{uv}$ denote its simple paths from $u$ to $v$ (if $u=v$, only the trivial path is included). For a path $P$, let $d(P)$ be its length, $w(P)$ the product of its edge weights (empty product 1), and $F_P=G-V(P)$. Write $D_H(z)=\det(I-zA_H)$.

Then

$$\boxed{\sum_{k\ge0}(A_G^k)_{uv}z^k
=\sum_{P\in\mathcal P_{uv}}w(P)z^{d(P)}\frac{D_{F_P}(z)}{D_G(z)}}.$$

Each summand has an exponential relative-trace representation:

$$\frac{D_{F_P}(z)}{D_G(z)}=\exp\left(\sum_{k\ge1}\frac{\operatorname{tr}(A_G^k)-\operatorname{tr}(A_{F_P}^k)}{k}z^k\right).$$

These are formal power series; all denominators have constant term 1. Write $r_P(k)=\operatorname{tr}(A_G^k)-\operatorname{tr}(A_{F_P}^k)$, and $c_P(0)=1$ with

$$n c_P(n)=\sum_{k=1}^n r_P(k)c_P(n-k).$$

With $c_P(j)=0$ for $j<0$, the universal marked-walk transfer is

$$\boxed{(A_G^k)_{uv}=\sum_{P\in\mathcal P_{uv}} w(P)c_P(k-d(P)).}$$

The disconnected case is the empty sum. This is a multi-path transfer, not an assertion of efficient simple-path enumeration or of unique recovery of all individual relative traces from their sum.

### Proof of the determinant formula

Put $M=I-zA_G$. The coefficient of $s$ in $\det(M+s e_v e_u^\top)$ equals $\det(M)(M^{-1})_{uv}$ by the rank-one determinant identity (also valid formally). In the Leibniz expansion, terms using the inserted entry from row $v$ to column $u$ contain a unique permutation cycle going from $u$ to $v$ and closing by this inserted entry. For $u\ne v$, the rest of that cycle is a simple path $P$ from $u$ to $v$. Its permutation sign is $(-1)^{d(P)}$, and the ordinary path entries contribute $(-z)^{d(P)} w(P)$. Their signs cancel. The remaining permutation terms on the complement sum to $D_{F_P}(z)$. When $u=v$, the inserted diagonal entry is a one-cycle, giving the trivial path. Hence the coefficient of $s$ is precisely the stated path sum before division by $D_G$. The formal inverse $M^{-1}=\sum_{k\ge0}A_G^kz^k$ proves the result.

The identity $\log\det(I-zA)=-\sum_{k\ge1}\operatorname{tr}(A^k)z^k/k$ follows by formal differentiation of the determinant and use of the geometric-series inverse, together with constant term zero. Subtracting two such logarithms proves the exponential ratio, and logarithmic differentiation proves the coefficient recurrence. QED.

For a tree the sum contains one path. Both $T$ and its induced forest are bipartite, hence all odd traces vanish. Dividing by $z^d$ and (in the weighted case) $w(P)$, then substituting $t=z^2$, proves Section 1 and its inverse by coefficient comparison.

### Local factorization and last-exit interpretation

For $P=(v_0,\dots,v_d)$ let $G_j=G-\{v_0,\ldots,v_{j-1}\}$, including $G_0=G$ and $G_{d+1}=F_P$. The determinant ratio telescopes:

$$\frac{D_{F_P}}{D_G}=\prod_{j=0}^d \frac{D_{G_{j+1}}}{D_{G_j}}=\prod_{j=0}^d\left(\sum_{k\ge0}(A_{G_j}^k)_{v_jv_j}z^k\right).$$

The second equality uses the diagonal cofactor formula. Combinatorially, any walk from $u$ to $v$ determines a simple path by taking its last visit to the starting vertex and its next step, then repeating in the suffix until $v$ is reached. Each segment before a last departure is a closed walk at the current vertex in the graph with earlier path vertices removed. The final segment is a closed walk at $v$. Conversely, concatenate such closed walks and the designated path edges. Later segments avoid earlier path vertices, so the last-exit algorithm recovers exactly the same path and segments. This is a bijection, also weight-preserving. It proves the product and sum directly, and identifies $c_P$ as a nonnegative integer sequence in the unweighted case.

The determinant path identity and last-exit decomposition are classical. Their formulation here isolates the relative moments as the reversible source coordinates for each path contribution. Compare the characteristic polynomial path-deletion identities in Brouwer and Haemers, *Spectra of Graphs*, Chapter 5, and the weighted cofactor formula discussed at https://mathoverflow.net/questions/417308/how-to-determine-the-sign-for-the-sum-over-all-simple-paths-in-the-graph. These sources are contextual references; the proofs above are self-contained. No priority claim for the determinant identity or loop erasure is made.

## 3. Polynomial-coordinate transfer for all recurrent sequences

Work over a characteristic-zero field $K$. Let $a=(a_n)_{n\ge0}$ be a nonzero linearly recurrent sequence, $E$ its forward shift, and $M\in K[x]$ its monic minimal annihilating polynomial of degree $D\ge1$. Define

$$R=K[x]/(M),\qquad \ell(x^n)=a_n.$$

The functional $\ell$ is well defined because $M(E)a=0$, and its bilinear form $\langle P,Q\rangle=\ell(PQ)$ is nondegenerate. Indeed, if $\ell(PQ)=0$ for every $Q$, then $[P(E)a]_k=0$ for every $k\ge0$. Minimality implies that $M$ divides $P$, so $P=0$ in $R$.

Given a polynomial $f\in K[x]$, let $N\in K[y]$ be the monic minimal polynomial of the element $f(x)\in R$; equivalently $N$ generates the kernel of the algebra map $K[y]\to R,\ y\mapsto f(x)$. Put $r=\deg N$. We consider the coordinate-change transfer

$$b_n=[P(E)f(E)^n a]_0=\ell(P f(x)^n).$$

**Theorem.** Such a transfer exists if and only if $N(E)b=0$. One may always take $\deg P<D$. The map from $R$ onto the space of sequences annihilated by $N$ has rank $r$, with kernel dimension $D-r$. Thus the ambiguity of $P$ is measured in the quotient by $M$, not in the full polynomial ring. A degree constraint $\deg P\le d<D$ holds precisely when the first $r$ target values lie in the column space of the first $d+1$ columns of the transfer matrix below.

**Proof.** Necessity follows from $N(f)=0$ in $R$. Conversely, $N(E)b=0$ defines a linear functional on $K[y]/(N)$ via $y^n\mapsto b_n$. This quotient is isomorphic to the subalgebra $K[f]\subseteq R$. Extend the functional from this subspace to $R$. By nondegeneracy of the above bilinear form, every such extension equals $Q\mapsto\ell(PQ)$ for some $P\in R$. Restrict to $f^n$ to obtain the desired transfer. Surjectivity and rank-nullity give the dimensions, since the solution space of a monic degree-$r$ recurrence has dimension $r$. QED.

The zero source is a separate trivial case: it can only produce the zero target. For rational $a$ and rational $f$, all calculations and solutions may be taken over $K=\mathbb Q$. No integer-coefficient or complexity claim follows automatically.

### Explicit transfer matrix and minimality

For $0\le k<r$, $0\le j<D$, put

$$\mathsf T_{kj}=\ell(x^jf(x)^k)=[E^jf(E)^k a]_0.$$

The equation $\mathsf T c=(b_0,\ldots,b_{r-1})^\top$ constructs a transfer. Equality at these indices implies equality at every index by the monic recurrence. The matrix has full row rank $r$. Its first $d+1$ columns decide whether degree $d$ suffices, and the smallest such $d$ is the minimum polynomial degree. A basis of the nullspace gives all remaining ambiguity. These are finite exact algebraic tests.

### Closed-form image annihilator, including repeated roots

Over a splitting field, factor

$$M(x)=\prod_{\lambda}(x-\lambda)^{e_\lambda}.$$

For nonconstant $f$, let $s_\lambda$ be the order of vanishing of $f(x)-f(\lambda)$ at $\lambda$. Then

$$\boxed{N(y)=\prod_{\mu}(y-\mu)^{h_\mu}},\qquad
h_\mu=\max_{f(\lambda)=\mu}\left\lceil\frac{e_\lambda}{s_\lambda}\right\rceil.$$

If $f$ is constant, $N(y)=y-f$. In each local quotient $K[x]/((x-\lambda)^{e_\lambda})$, the difference $f(x)-f(\lambda)$ is a unit times $(x-\lambda)^{s_\lambda}$ (or zero in the quotient). Its least positive nilpotency exponent is $\lceil e_\lambda/s_\lambda\rceil$. Chinese remaindering gives the product with maxima over coincident image roots. This proves the formula; the polynomial descends to $K$ because it is the minimal polynomial of the original $K$-algebra element. In particular for $f(x)=x^q$ and $q\ge1$, the multiplicity at any nonzero source root is retained locally, while at zero it changes to $\lceil e_0/q\rceil$; image collisions take the maximum.

**Exact loss criterion.** The coordinate subalgebra equals $R$ exactly when $r=D$. Equivalently, $f$ is injective on the distinct roots of $M$ and $f'(\lambda)\ne0$ at every root of multiplicity greater than one. This follows by comparing the sum of the image exponents with $\sum e_\lambda$; collisions or local shrinkage strictly decrease it. It also covers the constant case (lossless only when $D=1$). Thus the lost dimension is explicitly $D-\sum_\mu h_\mu$. This is a statement about the coordinate algebra and the transfer coefficients, not about recovery of an unknown graph or arbitrary external data.

The prior symmetric-matrix criterion is the squarefree case $e_\lambda=1$, where the annihilator has the active spectral nodes as roots. With $f=x^q$ the transfer becomes $b_n=[P(E)a]_{qn}$. The cycle binomial lift is $f=x+2$, an invertible polynomial coordinate change, and a stride is $f=x^q$. Both are instances of the same algebra.

### Worked repeated-root example

Let $a_n=\binom n3 2^{n-3}$ for $n\ge3$, and zero for $n<3$. Its minimal polynomial is $(x-2)^4$ (the top coefficient functional in $K[\epsilon]/(\epsilon^4)$, where $\epsilon=x-2$). Let $f(x)=(x-2)^2+3$. Then $s_2=2$, hence $N(y)=(y-3)^2$ and $r=2$, $D-r=2$. Modulo $\epsilon^4$,

$$f^n=3^n+n3^{n-1}\epsilon^2$$

(with the second coefficient defined as zero at $n=0$). The polynomial $P=\epsilon^3$ produces $3^n$, and $P=\epsilon$ produces $n3^{n-1}$. The kernel is spanned by $1,\epsilon^2$. No polynomial multiplier can produce a sequence with minimal annihilator $(E-3)^3$, such as $n^2 3^n$. This demonstrates mode loss even without merging distinct roots: stationary coordinate maps can erase higher-order modes.

The quotient-ring duality and primary decomposition used here are classical algebra. The theorem packages them as a constructive transfer and an exact loss criterion. Priority of this formulation has not been assessed exhaustively.

## 4. Reproducibility

The companion standalone continuation archive contains the two checkers and their execution logs. From that archive, run with Python 3 and assertions enabled (do not use `-O`):

```sh
python -B check_relative_walk_transfer.py
python -B check_polynomial_realization.py
```

The relative-walk checker uses exact integers and fractions. It enumerates all 201 unlabeled trees of orders 1 through 10 by leaf extension and canonical rooted-tree encoding, checking all unordered marked pairs including equal vertices, prefix indices 0 through 8, and forbidden lengths. It also enumerates all 1,099 labeled simple graphs of orders 1 through 5 (including disconnected graphs), all unordered marked pairs, and lengths 0 through 6. It compares the relative-trace and local last-exit decompositions with direct walk enumeration. Forty deterministic signed integer weighted graphs are also checked.

The polynomial checker uses exact fractions. Across 568 test cases it constructs quotient rings from prescribed rational roots and multiplicities, tests constant, colliding, stationary and ordinary polynomial coordinate changes, checks the image annihilator and its minimality, constructs the exact transfer matrix, solves for a basis of target sequences, and tests a basis of its kernel.

| Checker | Counted exact comparisons |
|---|---:|
| Relative graph transfers | 691,639 |
| Polynomial-coordinate realization | 48,626 |
| Total new comparisons | 740,265 |

These counts exclude internal assertions not explicitly counted and include overlapping cases. They are finite reproducibility checks, not numbers of independent theorems. The logs record the actual output. The universal statements are established by the algebraic and combinatorial proofs above. No exhaustive OEIS search, new OEIS edits, Lean verification, independent peer review, computational complexity advantage, or literature-wide novelty claim is made.
