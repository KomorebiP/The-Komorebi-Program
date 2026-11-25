# Graph-native defect reconstruction and polynomial saturation ladders

**Author: Komorebi P.**  
**Version:** 2.9, 2026-11-25  
**Status:** algebraic proofs and exact finite computational tests. Not Lean certified or independently peer reviewed.

Predecessor: [Unequal-depth isotropic Gram splitting, v2.8](UNEQUAL_GRAM_SPLITTING.md). All five predecessor checksums matched; its checker was not rerun.

## 1. Integral root-deletion theorem

Let $A$ be a symmetric integral matrix of order $N\ge2$, with the root listed first. Write

$$A=\begin{pmatrix}\alpha&v^\top\\v&B\end{pmatrix},\qquad n=N-1.$$

For a simple graph $\alpha=0$, $B$ is the root-deleted adjacency matrix and $v$ records its neighbors. Let $W$ have rows $e_o^\top A^i$, $0\le i<N$, and $C$ have rows $v^\top B^j$, $0\le j<n$. If $m_i=(A^i)_{oo}$, the root-first walk row is $(m_i,r_i)$. Block multiplication gives

$$r_{i+1}=m_iv^\top+r_iB,\qquad r_i=\sum_{j=1}^i m_{i-j}v^\top B^{j-1}.$$

Since $m_0=1$, there is a lower unit triangular integral matrix $U$ with entries $U_{i0}=m_i$ and $U_{ij}=m_{i-j}$ for $1\le j\le i$ (and $U_{00}=1$). Therefore

$$\boxed{W=U(1\oplus C)},\qquad WW^\top=U(1\oplus CC^\top)U^\top.$$

These identities preserve integral Smith profiles, including singular cases. The root contributes one unit factor.

## 2. Recover source defect data from the graph recurrence

Work over $R=\mathbb Z_{(p)}$ and assume $C$ is nonsingular. Define

$$L_h=\{z\in R^n:Cz\in p^hR^n\},\qquad E_h=(L_h+pR^n)/pR^n.$$

Here $E_h$ consists of the residues that lift to the kernel modulo $p^h$. A local Smith decomposition shows that if the source depths are $a_i$, then

$$\dim_{\mathbb F_p}E_h=\#\{i:a_i\ge h\},\qquad h\ge1.$$

Indeed in the local Smith basis the condition on the $i$th coordinate is divisibility by $p^{\max(0,h-a_i)}$. The following algorithm recovers this flag without using a source Smith decomposition as an algorithmic primitive.

Start with $M_0=I$. Given an integer matrix $M_h$ whose columns form a basis of $L_h$ over $R$, form the residual $R_h=p^{-h}CM_h\bmod p$. Its entries can be computed from the root-deleted recurrence, without storing the full walk matrix. Let $V_h$ be an integer lift of a finite-field basis whose first $k_h$ columns span $\ker R_h$. Then

$$\boxed{M_{h+1}=M_hV_h\operatorname{diag}(I_{k_h},pI_{n-k_h}).}$$

A vector $M_hu$ belongs to $L_{h+1}$ exactly when $R_hu=0\bmod p$. Hence the displayed matrix is an $R$-basis of the next lattice. Take $E_h=\operatorname{im}(M_h\bmod p)$ and continue until $E_h=0$. Nonsingularity ensures termination.

Starting from the deepest nonzero space, extend a basis of $E_{h+1}$ to one of $E_h$ using actual columns of $M_h$ as lifts $z_i$. Assign depth $a_i=h$ to each new direction and include depth-zero directions. The resulting $Z=(z_i)$ is invertible over $R$. Every $Cz_i/p^{a_i}$ is integral, and their matrix has unit determinant because $\sum_i a_i=v_p(\det C)$. Thus

$$C=P D_0 Z^{-1},\qquad P=CZD_0^{-1}\in\operatorname{GL}_n(R),\qquad D_0=\operatorname{diag}(p^{a_i}).$$

For the positive-depth columns $Z_+$, the pairing $K=Z_+^\top Z_+$ supplies the v2.7-v2.8 defect presentation. Only $K_{ij}\bmod p^{\min(a_i,a_j)}$ is relevant. This constructs valid source defect data from the graph recurrence by finite-field elimination and divisible integer operations. The basis and pairing are not canonical. The existence of Smith form is used in the proof, but not in the flag algorithm. No overall bit-complexity improvement is asserted.

## 3. Direct polynomial Gram algorithm

Let

$$f=\det(xI-A),\quad g=\det(xI-B),\quad s=v^\top\operatorname{adj}(xI-B)v=(x-\alpha)g-f.$$

The bordered determinant gives the last equality. The integral Bezoutian result of v2.7 and $(f,g)=(g,s)$ give

$$\boxed{\operatorname{coker}(WW^\top)\cong\mathbb Z[x]/(g,s).}$$

Put $I=(g,s)$ and $I_h=(I:p^h)=\{u:p^hu\in I\}$. The reduction of $I_h$ in $\mathbb F_p[x]$ has a monic generator $d_h$, since $g$ is monic and belongs to every $I_h$. If $b_i$ are the Gram Smith exponents, interpreting zero Smith factors as infinite exponents, then

$$\boxed{\deg d_h=\#\{i:b_i>h\}.}$$

Proof: multiplication by $p^h$ identifies $\mathbb Z[x]/I_h$ with $p^hM$ for $M=\mathbb Z[x]/I$. Reduction by $p$ gives $p^hM/p^{h+1}M\cong\mathbb F_p[x]/(d_h)$. Each free summand contributes one dimension, as does each cyclic $p$-primary summand of exponent greater than $h$. All other summands contribute zero.

Consequently $d_{h+1}\mid d_h$, and the number of exponents equal to $h\ge1$ is $\deg d_{h-1}-\deg d_h$. The degree stabilizes at $\deg\gcd_{\mathbb Q[x]}(g,s)$, the free rank. Each irreducible factor $\phi$ contributes $\deg(\phi)\operatorname{ord}_{\phi}d_h$ to the layer dimension, by the Chinese remainder decomposition.

### Explicit colon step

Suppose $I_h$ has generators $u_0=g,u_1,\ldots,u_t$. Over $\mathbb F_p[x]$, compute their monic gcd $d$ and a Bezout relation $d=\sum_i\bar c_i\bar u_i$. Lift the coefficients and put $D=\sum_i c_i u_i$. Lift $\bar q_i=\bar u_i/d$ to integer polynomials $q_i$. Then

$$R_i=(u_i-q_iD)/p\in\mathbb Z[x],\qquad
\boxed{I_{h+1}=(D,R_0,\ldots,R_t).}$$

Indeed $I_h=(D,pR_0,\ldots,pR_t)$. If $pw=aD+p\sum b_iR_i$, reduction modulo $p$ gives $\bar a d=0$ in the integral domain $\mathbb F_p[x]$. Therefore $p$ divides $a$, and $w$ belongs to the displayed ideal. The reverse inclusion follows immediately from $D,pR_i\in I_h$. Retain $g$ as a generator and reduce the others modulo the monic $g$; discard zero or duplicate remainders.

This gives a descending polynomial gcd ladder at every prime, including bad primes, without forming $W$ or computing its Smith decomposition. Singular cases are covered by the free-rank stopping condition. Generator counts and coefficients may grow, so no complexity advantage is claimed.

## 4. Explicit witnesses

For the v2.8 graph with edges 01,05,12,15,23,24,34,45,46, rooted at 4, the ladder at two is

$$x^3,\ x^3,\ x^2,\ 1.$$

This predicts positive Gram exponents $(2,3,3)$. At three the ladder is $x-1,x-1,1$, giving exponent two. The complete Gram Smith profile is $(1,1,1,1,4,8,72)$. The new flag algorithm recovers depths $(2,1,1)$ and one valid pairing

$$K=\begin{pmatrix}24&1&5\\1&1&0\\5&0&2\end{pmatrix}.$$

These give the same Gram profile as the different Smith basis in v2.8.

### Scalar-only source recovery is impossible

Consider two seven-vertex simple graphs (labels 0 through 6):

- Graph I, root 1: edges 01,04,05,12,15,23,25,34,46.
- Graph II, root 3: edges 01,06,12,13,14,23,34,45,56.

Their sorted degree sequences $(1,2,3,3,3,3,3)$ and $(2,2,2,2,3,3,4)$ show they are nonisomorphic. Both have the identical full and root-deleted characteristic polynomials

$$f=x^7-9x^5-4x^4+18x^3+8x^2-8x-2,$$
$$g=x^6-6x^4+8x^2-2x-1.$$

The Laurent expansion of $g/f$ gives their equal rooted return moments at every length. Both walk matrices are nonsingular, with determinants 4 and -4 in the given label order. Exact Smith computation gives

$$\operatorname{SNF}(W_{\rm I})=(1,1,1,1,1,1,4),$$
$$\operatorname{SNF}(W_{\rm II})=(1,1,1,1,1,2,2).$$

Both Gram matrices are identical and have profile $(1,1,1,1,1,4,4)$. The common ladder at two is $x^2+1,x^2+1,1$. The modular flag returns depths $(2)$ and pairing $K=(36)$ for Graph I, versus depths $(1,1)$ and pairing $K=\left(\begin{smallmatrix}3&1\\1&4\end{smallmatrix}\right)$ for Graph II. The first has complete splitting, while the second has individual doubling. Therefore even the entire scalar return sequence, and both characteristic polynomials, cannot determine the source defect depths or full source pairings. Their dimensions can differ. The Gram obstruction is determined; its source-level realization is not.

This example was found by comparing rooted moment prefixes in the graph atlas and was verified by exact polynomial equality and Smith computations. The search stopped after finding a witness; minimality is not established.

## 5. Verification and remaining boundaries

The companion v2.9 archive contains an expanded proof, checker, execution log, requirements, checksums and continuation handoff. Its actual execution passed 2,766 counted comparisons across 162 cases: all 137 roots of the 30 connected unlabeled simple graphs of orders 2 through 5, five explicit witnesses, and 20 signed symmetric integral matrices. These include 505 polynomial saturation profiles, 820 saturation layers, 184 source flags and pairing-derived profiles each, 260 flag layers, 162 checks each of the root factorization, Gram congruence, root and root-Gram Smith profiles and polynomial presentation, and three rooted cospectral witness comparisons. Independent Smith computations are reference tests, not algorithm steps.

The source flag algorithm requires a nonsingular source in this edition. The Gram polynomial ladder already covers singularity. A structural classification of source lattices that realize one scalar Gram sequence, and treatment of singular or rectangular sources with a nonunimodular saturation, remain further work. No independent peer review, Lean certification, overall complexity improvement or literature-wide novelty is claimed.
