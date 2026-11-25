# Local arithmetic of Cartesian products and rooted equitable walk transfers

**Author: Komorebi P.**  
**Version:** 2.6, 2026-11-25  
**Status:** algebraic proofs and exact computational checks. Not Lean certified or independently peer reviewed.

Predecessor: [Association schemes, Cartesian products and arithmetic coordinate compression, v2.5](https://github.com/KomorebiP/The-Komorebi-Program/blob/main/docs/demonstrations/ASSOCIATION_SCHEME_PRODUCT_TRANSFERS.md). All seven files listed in the predecessor checksum manifest matched. Its checker was not rerun in this continuation.

## Abstract

For products of complete graphs, we give a weighted Newton interpolation construction of the local Smith profile of the unrestricted multiplier transfer at primes not dividing any factor order. It accommodates collisions between subset sums. We also give a determinant formula for the scalar multiplier Gram matrix at every prime and closed Smith profiles and minimum target denominators at every prime for two factors. For rooted equitable partitions of arbitrary connected simple graphs, we establish the exact transfer matrices and optimal denominator classification. Rooted equitable distance partitions inherit the previous distance-regular product formulas without global regularity. A five-vertex graph demonstrates that the Smith invariants of a Gram matrix need not be the squares of the original Smith invariants, even though its determinant is squared.

## 1. Mixed Cartesian product coordinates

Let $G=K_{q_1}\square\cdots\square K_{q_d}$, where $d\ge1$ and $q_j\ge2$. Let $X_j$ be the independent adjacency operator of factor $j$, $X_S=\prod_{j\in S}X_j$ and $A=\sum_j X_j$. The integral relation lattice has basis $X_S$ for all subsets, and $X_j^2=(q_j-2)X_j+(q_j-1)I$. Write $D=2^d$, $k_S=\prod_{j\in S}(q_j-1)$ and $K=\operatorname{diag}(k_S)$. The root moment functional $\ell(Q)=Q_{oo}$ satisfies $\ell(X_S X_T)=\delta_{ST}k_S$.

The joint eigenvalue tuple indexed by $S$ uses $q_j-1$ at coordinates in $S$ and $-1$ elsewhere. The eigenvalue of $A$ is $\lambda_S=-d+\sum_{j\in S}q_j$. Put $\Lambda=\{\lambda_S\}$, $r=|\Lambda|$, and $Q_*=\prod_j q_j$. The probability weight of tuple $S$ in the root spectral measure is

$$\omega_S=\frac{\prod_{j\notin S}(q_j-1)}{Q_*}.$$

All weights are positive. The rank of the scalar observation is $r$ and its minimal annihilator is the monic integer polynomial $\prod_{\lambda\in\Lambda}(x-\lambda)$.

Let $F$ be the $r\times D$ integer matrix of the first $r$ powers of $A$ in the relation basis. As in v2.5, write $T=FK$ for the unrestricted relation multiplier transfer and $H=FKF^\top$ for the scalar polynomial multiplier Gram matrix. Both have rank $r$, and $H$ is positive definite. The entry-functional target for relation $S$ is $Fe_S$, not $FKe_S$.

### 1.1 Exact good-prime Smith profile by weighted Newton ordering

Fix a prime $p\nmid Q_*$. For each distinct node $\lambda$ let

$$w_\lambda=\min_{S:\lambda_S=\lambda}v_p(\omega_S)=\min_{S:\lambda_S=\lambda}\sum_{j\notin S}v_p(q_j-1).$$

Choose distinct nodes sequentially. At step $i=0,\ldots,r-1$ select a remaining node $\lambda_i$ minimizing

$$e_i=w_{\lambda_i}+\sum_{j<i}v_p(\lambda_i-\lambda_j).$$

Ties may be settled arbitrarily. **Theorem.** The valuations of the nonzero Smith invariants of $T$, in increasing order, are exactly $e_0,\ldots,e_{r-1}$. The kernel over the rationals has dimension $D-r$, independently of these valuations.

**Proof.** Let $E$ denote the square joint evaluation matrix whose rows are tuples and columns are $X_S$. It is the Kronecker product of the $2\times2$ evaluation matrices with rows $(1,-1),(1,q_j-1)$, so it is invertible over $\mathbb Z_{(p)}$ when $p\nmid Q_*$. Let $V_{n,S}=\lambda_S^n$ and $\Omega=\operatorname{diag}(\omega_S)$. The identities $FE^\top=V$ and $K=E^\top\Omega E$ imply $T=V\Omega E$. Right multiplication by $E^{-1}$ does not change its local Smith invariants. Columns at coincident nodes are scalar multiples of the same power vector. By choosing a weight of least valuation in each group and eliminating all other columns using local integral column operations, we reduce to a weighted Vandermonde matrix on distinct nodes, with weights of valuations $w_\lambda$ and additional zero columns.

Replace the monomial row basis by the monic Newton polynomials $n_i(x)=\prod_{j<i}(x-\lambda_j)$. This is a unimodular integer row change. Order columns by the greedy selection. The resulting matrix has zeros in row $i$ at columns $j<i$, and its diagonal entry in row $i$ has valuation $e_i$. By the minimizing rule, every remaining entry in that row is divisible by the diagonal entry in $\mathbb Z_{(p)}$. Clear the entries to the right by subtracting local integral multiples of the pivot column. The pivot column has zeros below row $i$, so later rows are unchanged. The successive minima cannot decrease because adding a selected node adds a nonnegative valuation to every remaining score. Therefore the diagonal is already in Smith divisibility order up to local units. QED.

The rule requires pairwise node differences and at most $O(r^2)$ valuation additions if scores are updated after each choice. It is not a claim about total bit complexity or the cost of generating the $2^d$ nodes. For primes dividing $Q_*$ the change of basis $E$ is not locally unimodular; the proof does not apply there.

### 1.2 Restricted Gram determinant at every prime, including collisions

Define the aggregate spectral numerator $W_\lambda=\sum_{S:\lambda_S=\lambda}\prod_{j\notin S}(q_j-1)$. Then the root spectral weight at $\lambda$ is $W_\lambda/Q_*$. The square Vandermonde matrix $V_0$ on the distinct nodes satisfies $H=V_0\operatorname{diag}(W_\lambda/Q_*)V_0^\top$. Hence

$$\boxed{\det H=\frac{\prod_{\lambda<\mu}(\mu-\lambda)^2\prod_{\lambda\in\Lambda}W_\lambda}{Q_*^r}.}$$

This determinant formula holds also at bad primes. In particular its valuation is twice the sum of pairwise node-difference valuations, plus the sum of aggregate numerator valuations, minus $r v_p(Q_*)$. Note the distinction: unrestricted Smith at a good prime uses a **minimum** among colliding weights, while the restricted Gram uses their **sum**. The determinant only controls the sum of the restricted Smith valuations, not each invariant separately.

## 2. All-prime closed formulas for two factors

Let $G=K_q\square K_r$ with $q,r\ge2$, $q\ne r$. In this section $r$ denotes the second factor order, not the observation rank. Put $u=q-1$, $v=r-1$, $\delta=v-u=r-q$ (signed), $\sigma=q+r$, $a=u+v$, $g=\gcd(u,v)$, $h=\gcd(|\delta|,2g)$. The four distinct scalar eigenvalues are $-2,q-2,r-2,q+r-2$. Let $X,Y$ be the two coordinate adjacency operators.

The independent basis is $(I,X,Y,XY)$ and $K=\operatorname{diag}(1,u,v,uv)$. The coefficients of $1,A,A^2,A^3$ form the matrix

$$F=\begin{pmatrix}1&0&0&0\\0&1&1&0\\a&u-1&v-1&2\\(u-1)u+(v-1)v&(u-1)^2+u+3v&(v-1)^2+v+3u&3(u+v-2)\end{pmatrix}.$$

Subtract the constant terms from rows three and four, subtract $(u-1)$ times row two from row three, and subtract $((u-1)^2+u+3v)$ times row two from row four. The last two rows are now $(0,0,\delta,2)$ and $(0,0,\delta(u+v-4),3(u+v-2))$. Subtract $(u+v-4)$ times the new row three from row four. The integral unimodular row operation gives

$$F'=\begin{pmatrix}1&0&0&0\\0&1&1&0\\0&0&\delta&2\\0&0&0&\sigma\end{pmatrix}.$$

Thus $[L:\mathbb Z[A]]=|\delta|\sigma=|r^2-q^2|$, and the Smith profile of $F$ is $(1,1,\gcd(\delta,2),|\delta|\sigma/\gcd(\delta,2))$ (all gcds are nonnegative). This is the coordinate lattice index, distinct from the moment transfer profile.

### 2.1 Unrestricted relation multiplier Smith profile

The bottom block of $F'K$ is

$$T_3=\begin{pmatrix}u&v&0\\0&\delta v&2uv\\0&0&\sigma uv\end{pmatrix}.$$

The first determinantal divisor is $g$. The second is $uv\gcd(\delta,2u,2v,\sigma u,\sigma v)=uv h$. To see the equality, use $\gcd(u,v)=g$, and note that $\delta$ and $\sigma$ have the same parity, so adjoining $\sigma g$ to $\delta$ and $2g$ does not reduce the gcd. The determinant has absolute value $|\delta|\sigma(uv)^2$. Consequently the exact all-prime Smith profile is

$$\boxed{\operatorname{SNF}(T)=\left(1,g,\frac{uvh}{g},\frac{|\delta|\sigma uv}{h}\right).}$$

### 2.2 Restricted scalar polynomial multiplier Smith profile

Apply the same unimodular row change on both sides of $H$. Its lower block is

$$H_3=\begin{pmatrix}a&\delta v&0\\\delta v&\delta^2v+4uv&2\sigma uv\\0&2\sigma uv&\sigma^2uv\end{pmatrix}.$$

Let

$$G_1=\gcd(a,\delta v),\quad G_2=uv\gcd\bigl(\sigma\gcd(\sigma,2)\gcd(|\delta|v,a),\delta^2+4a\bigr).$$

The first divisor of $H_3$ is $G_1$: any common divisor of $a,\delta v$ divides $2uv=av-\delta v$, hence divides all displayed entries except possibly $\sigma^2uv$. When $\sigma$ is even this last entry is divisible as well; when $\sigma$ is odd, $a$ and $G_1$ are odd and $G_1\mid uv$. The nonzero cofactors up to sign are $uv$ times

$$\delta^2\sigma^2 v,\quad |\delta|\sigma^2 v,\quad 2|\delta|\sigma v,\quad a\sigma^2,\quad 2a\sigma,\quad \delta^2+4a.$$

Their gcd gives exactly $G_2$. The determinant is $\delta^2\sigma^2(uv)^2$. Therefore

$$\boxed{\operatorname{SNF}(H)=\left(1,G_1,\frac{G_2}{G_1},\frac{\delta^2\sigma^2(uv)^2}{G_2}\right).}$$

When $q=r$, the scalar rank is three rather than four. With $u=v$ the Hamming specialization from v2.5 gives unrestricted profile $(1,u,2u^2)$ and restricted profile $(1,2u,4u^2)$. No singular denominator formula with $\delta=0$ is used.

### 2.3 Exact optimal scalar transfer denominators

The target walks along relation $X$ have multiplier $X/u$, along $Y$ have $Y/v$, and along $XY$ have $XY/(uv)$. These are the unique rational multipliers in the full relation algebra because the scalar eigenvalues separate. Express them in the integral row basis $F'$ of the scalar polynomial lattice. Solving $F'^\top c=e_S/k_S$ gives

- For $X$: $c=(0,1/u,-1/(u\delta),2/(u\delta\sigma))^\top$.
- For $Y$: $c=(0,0,1/(v\delta),-2/(v\delta\sigma))^\top$.
- For $XY$: $c=(0,0,0,1/(uv\sigma))^\top$.

The least common denominators, preserved by the unimodular basis change, are

$$\boxed{D_X=\frac{u|\delta|\sigma}{\gcd(\sigma,2)},\qquad D_Y=\frac{v|\delta|\sigma}{\gcd(\sigma,2)},\qquad D_{XY}=uv\sigma.}$$

For the first two expressions, take the lcm of $u|\delta|$ (respectively $v|\delta|$) and the denominator of the last coefficient. Their least common multiple removes exactly the factor $\gcd(\sigma,2)$. Monic reduction modulo the scalar annihilator preserves integrality, so allowing arbitrarily high polynomial degree cannot reduce these denominators.

| Factors | Unrestricted Smith | Restricted Smith | $D_X,D_Y,D_{XY}$ |
|---|---|---|---|
| 2,3 | 1,1,2,10 | 1,1,2,50 | 5,10,10 |
| 2,5 | 1,1,4,84 | 1,1,4,1764 | 21,84,28 |
| 3,4 | 1,1,6,42 | 1,1,42,42 | 14,21,42 |
| 4,6 | 1,1,30,150 | 1,2,30,1500 | 30,50,150 |

The explicit table is independently checked in the audit below. In particular, the original K2 x K3 example is the first row of an infinite all-prime family, not an isolated obstruction.

## 3. Arbitrary rooted equitable partitions

Let $G$ be a finite connected simple undirected graph, not necessarily regular. Fix a root $o$. Let $C_0=\{o\},C_1,\ldots,C_{t-1}$ be an equitable partition: each vertex of $C_i$ has the same number $Q_{ij}$ of neighbors in $C_j$. Set $k_i=|C_i|$ and $K_C=\operatorname{diag}(k_i)$. Write $A$ for the adjacency matrix. Edge counting gives $K_C Q=Q^\top K_C$.

Let $w_n(i)=(A^n)_{vo}$ for any $v\in C_i$. The partition indicator matrix intertwines $A$ and $Q$, so $w_n=Q^n e_0$ is the vector of per-vertex walk counts, not the vector of total walks into cells. Let $m_n=w_n(0)$ and $r=\dim\operatorname{span}_{\mathbb Q}\{w_n:n\ge0\}$. The first $r$ vectors are independent by minimality of the root annihilator. This annihilator is monic integral: it is a divisor over Q of the monic integral characteristic polynomial of $Q$, so Gauss's lemma applies. Form $W_{ni}=w_n(i)$ for $0\le n<r$.

The unrestricted domain here is the lattice of integral cell-constant vectors, not necessarily an algebra of matrices. A vector with values $c_i$ in cell $C_i$ has observations $\langle A^ne_o,c\rangle=\sum_i k_i w_n(i)c_i$, so

$$\boxed{T_C=WK_C.}$$

If the vector is restricted to $P(A)e_o$ for an integer polynomial $P$, the first $r$ powers span this lattice by monic reduction. In this basis the matrix is

$$\boxed{H=WK_CW^\top=(m_{i+j})_{0\le i,j<r}.}$$

The last equality follows from symmetry of $A$ and the identity $m_{i+j}=\langle A^ie_o,A^je_o\rangle$. The matrix is positive definite, so each target $\beta_i=We_i$ has a unique reduced rational scalar polynomial with coefficient vector $H^{-1}\beta_i$. Since all future profile vectors satisfy the same recurrence, this reconstructs the walk sequence at every length. This is a transfer using the given partition or graph, not a claim that scalar root moments alone reveal an unknown vertex or graph.

For a full-row-rank integer matrix $M$, let $I(M)=[\mathbb Z^r:M\mathbb Z^{\#\text{columns}}]$, equivalently the gcd of its maximal minors or the determinant of a column-lattice Hermite basis. Then

$$q_C(i)=\frac{I(T_C)}{I([T_C\mid\beta_i])},\qquad q_A(i)=\frac{I(H)}{I([H\mid\beta_i])}.$$

Because $e_i/k_i$ in the cell domain attains the target and the polynomial domain is contained in it, $q_C(i)\mid k_i$ and $q_C(i)\mid q_A(i)$. If $r=t$, both W and $K_C$ are invertible, and

$$q_C(i)=k_i,\quad q_A(i)=k_i\,\operatorname{ord}(e_i+W^\top\mathbb Z^t).$$

Here the order is in the finite quotient $\mathbb Z^t/W^\top\mathbb Z^t$. To prove the second formula, let $h$ be the least denominator of $W^{-\top}e_i$, so $z=hW^{-\top}e_i$ is integral. It is primitive: a common divisor of its entries must divide $h$ by $W^\top z=h e_i$, and if greater than one contradicts minimality of $h$. Thus the vector $z/(h k_i)$ has least denominator $h k_i$. This proves the formula. The determinant is $\det H=(\det W)^2\prod_i k_i$ in the full-rank case, but the individual Smith factors need not square.

## 4. Rooted equitable distance partitions: exact product formulas

Assume only that the distance shells $C_i$ around the chosen root are equitable. Let $d$ be its eccentricity. The quotient is tridiagonal, with entries $c_i,a_i,b_i$ counting neighbors toward, within, and away from the root. No assumption that the degrees $a_i+b_i+c_i$ are equal is needed. All $b_i$ for $i<d$ and all $c_i$ for $i>0$ are positive, by connectedness and equitability. Put

$$B_i=\prod_{j=0}^{i-1}b_j,\qquad C_i^*=\prod_{j=1}^i c_j,\qquad k_i=B_i/C_i^*.$$

The shell sizes identity follows from $k_{i-1}b_{i-1}=k_ic_i$. Define monic polynomials $p_0=1$, $p_1=x-a_0=x$, and

$$p_{i+1}=(x-a_i)p_i-b_{i-1}c_i p_{i-1}\quad(1\le i\le d).$$

The shell indicator vectors $\mathbf1_i$ satisfy $A\mathbf1_i=b_{i-1}\mathbf1_{i-1}+a_i\mathbf1_i+c_{i+1}\mathbf1_{i+1}$ with missing terms omitted. Induction gives $p_i(A)e_o=C_i^*\mathbf1_i$ for $0\le i\le d$, and $p_{d+1}(A)e_o=0$. Orthogonality of shell vectors gives

$$\langle p_i(A)e_o,p_j(A)e_o\rangle=\delta_{ij}B_iC_i^*.$$

The cyclic rank is $d+1$, and the monic basis change is unimodular. Hence

$$\boxed{s_i=B_iC_i^*=\prod_{j=1}^i b_{j-1}c_j,\qquad (A^n)_{ov}=\frac{[p_i(E)m]_n}{B_i}\quad(v\in C_i).}$$

The Smith divisibility chain follows from $s_i/s_{i-1}=b_{i-1}c_i$. The scalar optimal denominator is $B_i$, since its unique reduced multiplier is $p_i/B_i$ and $p_i$ is monic. In the cell-constant domain the optimal denominator is $k_i$ and the extra scalar denominator is $C_i^*$. The root annihilator is not necessarily the minimal polynomial of the entire graph, unlike the distance-regular theorem.

### 4.1 Example: irregular complete bipartite graph

Take $K_{3,4}$ rooted in its part of size three. The graph is not regular. The shell sizes are $(1,4,2)$, $b=(4,2,0)$, $c=(0,1,4)$, $a=(0,0,0)$. Thus $p_2=x^2-4$, $p_3=x^3-12x$ and the Smith profile is $(1,4,32)$. The moments start $(1,0,4,0,48,0,576)$. The two-step count to either other vertex in the root's part is $(48-4\cdot4)/8=4$. The minimum cell-domain denominator is two, while the minimum scalar polynomial denominator is eight.

In a rooted tree whose distance partition is equitable, every vertex outside the root has one parent, so $c_i=1$. Then $s_i=B_i=k_i$ and the two multiplier domains have exactly the same optimal denominators. This is an additional class beyond distance-regular graphs.

## 5. Explicit failure of squaring Smith invariants

Use the five-vertex graph with edges $(0,1),(0,3),(0,4),(1,2),(2,3),(3,4)$ rooted at zero, and the discrete equitable partition. Its root distance partition is not equitable (the distance-one vertices have differing degrees). Direct walk enumeration gives

$$W=\begin{pmatrix}1&0&0&0&0\\0&1&0&1&1\\3&0&2&1&1\\2&5&1&6&4\\15&3&11&7&8\end{pmatrix},\quad \det W=-5,$$

$$H=WW^\top=\begin{pmatrix}1&0&3&2&15\\0&3&2&15&18\\3&2&15&18&82\\2&15&18&82&130\\15&18&82&130&468\end{pmatrix}.$$

Independent exact Smith computation yields $\operatorname{SNF}(W)=(1,1,1,1,5)$ and $\operatorname{SNF}(H)=(1,1,1,5,5)$. The latter is NOT $(1,1,1,1,25)$. Both products agree with $\det H=25$. A direct modular explanation is that the right kernel of $W$ over $\mathbb F_5$ is the line generated by $z=(0,1,3,3,1)^\top$: $Wz=0$ modulo five, and the Smith form of $W$ gives nullity one. Its squared norm is $20=0$ modulo five. Thus $z$ lies in $(\ker W)^\perp=\operatorname{im}W^\top$. The restriction of $W$ to this four-dimensional image has one-dimensional kernel, so $WW^\top$ has rank three over $\mathbb F_5$. The two positive Smith valuations must sum to two because the determinant is 25; they are therefore both one. The general assertion about squaring Smith invariants was an unsuccessful candidate tested during this continuation and has been rejected, not retained as a theorem.

For the walks from vertex zero to vertex one the unique scalar multiplier is

$$P(x)=\frac{5-17x-23x^2+2x^3+4x^4}{5}.$$

For $m_0,\ldots,m_5=(1,0,3,2,15,18)$, substitution at $n=1$ gives $(0-51-46+30+72)/5=1$. The optimal cell denominator is one and scalar denominator is five. This is a compression obstruction for a rooted irregular graph, not a distance-regular example.

## 6. Verification, limitations and next target

Run `python -B check_local_smith_equitable.py` in this directory. The final log records 37,750 counted exact comparisons, including 199 mixed product cases and 314 rooted partition cases (124 rank deficient), 1,770 good-prime Smith profile comparisons, 2,189 all-prime determinant-valuation comparisons, and 16,006 explicit scalar walk-transfer comparisons against adjacency enumeration. The rooted graph cases comprise the connected graph atlas through order five, plus K3,4, the seven-leaf star, the balanced binary tree of height three, and P8. For small graphs the discrete partition and the stable refinement of the singleton root partition are both checked. The 152 rooted equitable-distance cases count partition-root runs, including repetitions. Mixed product tests use exact tensor relation multiplication, not full graph construction. The first run failed on the naive squared-Smith prediction for the five-vertex example; the failure log is retained and the corrected final checker tests the explicit rejection. Counts are finite comparisons, not independent universal theorems.

The main algebraic proofs establish the unlimited cases within their hypotheses. At bad primes dividing one or more factor orders, the good-prime Newton rule is not asserted for general products of three or more factors. Individual restricted Gram Smith factors also remain open in general; the determinant identity alone is insufficient. More broadly, the rooted equitable theorem assumes the partition or rooted walk profiles are supplied. It is not an unknown-topology reconstruction theorem. The local Newton elimination and lattice methods use classical tools. Lean certification, independent peer review, a literature-wide novelty audit, and graph-constrained sharp precision remain outstanding.
