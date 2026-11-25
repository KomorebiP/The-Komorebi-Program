# Association schemes, Cartesian products and arithmetic coordinate compression

**Author: Komorebi P.**  
**Version:** 2.5, 2026-11-25  
**Status:** self-contained algebraic proofs and exact computational tests. Not Lean certified or independently peer reviewed.

Predecessor: [Distance-regular polynomial coordinates, v2.4](https://github.com/KomorebiP/The-Komorebi-Program/blob/main/docs/demonstrations/DISTANCE_REGULAR_POLYNOMIAL_COORDINATES.md).

## Abstract

The preceding work separated rational spectral loss, arithmetic distortion, and the least denominator for a target transfer. This continuation extends that distinction to symmetric association schemes and Cartesian products. In Hamming graphs, three nested multiplier lattices have different closed Smith profiles and different optimal denominators, despite realizing the same distance-conditioned walk sequence. For mixed Cartesian products of complete graphs, subset sums classify the rational loss of total-adjacency compression, while a Vandermonde ratio gives the integral lattice index when the spectrum separates. The two-factor example K2 × K3 introduces an unavoidable denominator five. A general symmetric tensor theorem extends the orbit-size arithmetic obstruction to repeated distance-regular factors.

## 1. Association-scheme transfer lattice

Let $A_0=I,A_1,\ldots,A_D$ be the symmetric relation matrices of a finite symmetric association scheme. They are pairwise disjoint zero-one matrices with constant row sums $k_i>0$, $k_0=1$, and their span is a commutative matrix algebra with integer structure constants. Indexing the relations by 0 through D here gives D+1 basis elements. The integral relation algebra is $L=\bigoplus_i\mathbb Z A_i$. For a fixed vertex $o$, define $\ell(P)=P_{oo}$. Disjoint supports and symmetry give

$$\ell(A_iA_j)=\delta_{ij} k_i.$$

Thus the integral Gram matrix of the full relation basis is $K=\operatorname{diag}(k_i)$. Its Smith invariants are obtained by sorting the valuations of the $k_i$ separately at each prime and multiplying the aligned prime powers. They need not occur in relation-index order. For example, the distance-relation basis of the four-cube has norms $1,4,6,4,1$ and Smith invariants $1,1,2,4,12$.

Let $G_1,\ldots,G_s\in L$ be commuting observation operators, and let $R=\mathbb Z[G_1,\ldots,G_s]\subseteq L$. This is a free finite-rank lattice of rank r. A finite spanning list consists of words $G_1^{n_1}\cdots G_s^{n_s}$ with each exponent less than the degree of the corresponding minimal polynomial: those polynomials are monic integral by the integral characteristic polynomial and Gauss's lemma. Monic reduction in each variable proves the spanning statement. A lattice basis, not merely an independent rational sublist of words, can be obtained by integer Hermite normal form.

Write the rows of $F$ for the coordinates of an integral basis of $R$ in the relation basis. For a multiplier $P\in L\otimes\mathbb Q$ with relation coefficients $u$, the sequence of observations is $\ell(PG_1^{n_1}\cdots G_s^{n_s})$. Its values on the chosen basis are

$$\boxed{\beta=T u,\qquad T=F K.}$$

If the multiplier itself must lie in $R\otimes\mathbb Q$ with basis coefficients $v$, then $u=F^\top v$ and

$$\boxed{\beta=T_R v,\qquad T_R=F K F^\top.}$$

The matrices have rank r because K is positive definite and F has independent rows. Every rational functional on $R\otimes\mathbb Q$ can therefore be realized. The first matrix has rational kernel dimension $(D+1)-r$; the second is injective. An arbitrary table of word values must first respect the rational word relations before it defines such a functional. Smith form and augmented maximal minors of the corresponding transfer matrix give integral solvability and minimum denominator, as in v2.2 and v2.4.

If a pair of vertices lies in relation i, the entry of every $Q\in R$ is its coefficient at $A_i$, namely $\ell(A_iQ)/k_i$. The multiplier $A_i/k_i$ works. If r=D+1, this is the unique rational relation multiplier; its optimal denominator in L is $k_i$. If r is smaller, the minimum denominator in L divides $k_i$. A restriction to R may increase it. When r=D+1, the finite index of R in L is $|\det F|$ and

$$|\det T_R|=[L:R]^2\prod_i k_i.$$

The determinant of T instead has only one power of this index. Over the reals the simultaneous eigenbasis identifies the observation algebra with functions on the distinct joint eigenvalue tuples of the $G_j$. Its rank equals the number of these tuples: polynomial interpolation on a finite set supplies the indicator of each distinct tuple. This rational rank statement also holds over Q by scalar extension. It does not imply equality of the integral lattices.

These formulas distinguish source information from permitted arithmetic. Restricting the multiplier changes the domain of the transfer even when the observed word sequence is unchanged. They do not recover an unknown association scheme from scalar observations.

## 2. Three multiplier lattices on Hamming graphs

Let $H(d,q)=K_q^{\square d}$, with $d\ge1,q\ge2$. Write $X_j$ for the adjacency operator of the j-th coordinate, acting as identity on all other factors. Put $A=\sum_j X_j$ and $X_S=\prod_{j\in S}X_j$. The tensor relation basis consists of all $X_S$, $S\subseteq\{1,\ldots,d\}$, and

$$X_j^2=(q-2)X_j+(q-1)I,$$
$$\ell(X_S X_T)=\delta_{ST}(q-1)^{|S|}.$$

Set $A_i=\sum_{|S|=i}X_S$, the distance-i matrix. There are three multiplier lattices in the same rational coordinate calculus:

- L: all integer combinations of the $X_S$ (independent coordinate multipliers).
- Lsym: the permutation-invariant sublattice, with basis $A_i$.
- R: the polynomial lattice $\mathbb Z[A]$, with monic basis $p_i(A)=i! A_i$ for $0\le i\le d$.

The last statement follows from the Hamming intersection numbers $b_i=(d-i)(q-1),c_i=i,a_i=i(q-2)$ and the v2.3 monic recurrence. The annihilator is monic of degree $d+1$ (eigenvalues $d(q-1)-qj$ for $0\le j\le d$); consequently the monic polynomials of degrees 0 through d span R integrally. In particular $[L_{sym}:R]=\prod_{i=0}^d i!$.

In all three cases the observed sequence is $\ell(P A^n)$, and its first $d+1$ values suffice. Use the row basis $p_i(A)$ instead of $A^i$; this is a unimodular row change. With independent columns $X_S$, the transfer entries are

$$\boxed{T_{iS}=i!(q-1)^i\,\mathbf1_{|S|=i}.}$$

For each i, subtract one representative column from the other columns of weight i. This makes the matrix diagonal with free zero columns. If the columns are $A_j$, the result is diagonal with entries $i!\binom di(q-1)^i$. If they are $p_j(A)$, the entries are $(i!)^2\binom di(q-1)^i$. The three diagonals are positive and have successive divisibility. Writing $(d)_i=d!/(d-i)!$, the Smith profiles are therefore

| Multiplier lattice | Smith invariant at i | Optimal denominator for distance i |
|---|---|---|
| L | $i!(q-1)^i$ | $(q-1)^i$ |
| Lsym | $(d)_i(q-1)^i$ | $\binom di(q-1)^i$ |
| R | $i!(d)_i(q-1)^i$ | $(d)_i(q-1)^i$ |

To prove the denominator column, fix a pair at distance i and let $w_n=(A^n)_{uv}$. Applying the same row basis change to the target yields $i!e_i$, since $p_j(A)=j! A_j$. The least integer q making q times this vector belong to the image lattice is its Smith pivot divided by the gcd with $i!$; this gives exactly the displayed denominators. Explicit attaining multipliers are $X_S/(q-1)^i$ for any S of size i, $A_i/[\binom di(q-1)^i]$, and $p_i(A)/[(d)_i(q-1)^i]$. They produce the same sequence because $A^n$ is constant on relations of the same Hamming weight.

The ranks of all three transfer matrices are $d+1$. The independent-coordinate kernel has dimension $2^d-d-1$, while both smaller lattice maps are injective. The index $\prod_i i!$ is an arithmetic obstruction internal to the invariant algebra, distinct from the rational dimension loss from forgetting coordinate labels. The first realization requires access to the joint-coordinate moment functional $\ell(X_S A^n)$; it is not a claim that the scalar sequence $\ell(A^n)$ alone supplies these mixed moments without a further transfer.

### Explicit cube example

For $d=3,q=2$, the profiles are $(1,1,2,6)$, $(1,3,6,6)$, and $(1,3,12,36)$. At distance two, the least denominators are 1, 3, 6, respectively. Attaining multipliers are $X_1X_2$, $A_2/3$, and $(A^2-3I)/6$. The first gives $\ell(X_1X_2 A^2)=2$ by choosing either ordering of the two coordinate flips. The third gives $(m_4-3m_2)/6=(21-9)/6=2$. At distance three the three denominators are 1, 1, 6, since the orbit contains only one subset but its distance polynomial is still multiplied by $3!$.

## 3. Symmetric tensor theorem for repeated distance-regular factors

Let a fixed finite distance-regular graph of diameter e have monic basis $p_j(A)=C_j A_j$, norm $s_j=B_j C_j$, and the conventions $B_0=C_0=s_0=1$ from v2.3. On the Cartesian power with d independent copies of its adjacency, the tensor monic basis is

$$P_{\alpha}=\prod_{l=1}^d p_{\alpha_l}(X_l),\quad 0\le \alpha_l\le e.$$

Monic reduction in each coordinate shows that these span the integral independent polynomial lattice. The root moment factorizes, hence $\ell(P_\alpha P_\beta)=\delta_{\alpha\beta}s_\alpha$ where $s_\alpha=\prod_l s_{\alpha_l}$. The full multivariate Gram matrix is diagonal in this basis. Its canonical Smith profile is obtained by sorting the prime valuations of the products $s_\alpha$.

Compress observations to the permutation-invariant polynomial lattice. Its basis consists of orbit sums $U_O=\sum_{\alpha\in O} P_\alpha$, for orbits O under permutations of d coordinates. Every invariant class has this symmetric integral polynomial lift, because the tensor monic basis is permuted. The fundamental theorem of symmetric polynomials over Z expresses the lift as an integer polynomial in the elementary symmetric polynomials of the X_l. Thus those d observation operators generate exactly the invariant lattice. Its rank is $\binom{d+e}{e}$, the number of multisets of d indices from 0 through e.

For a representative $\alpha\in O$, let $L_O=|O|=d!/\prod_j m_j!$, where $m_j$ counts occurrences of j. The observation rows $U_O$ and independent multiplier columns $P_\beta$ give

$$T_{O,\beta}=s_\alpha\mathbf1_{\beta\in O}.$$

If the multipliers are also invariant, the transfer matrix is diagonal with entries $L_O s_\alpha$. The canonical Smith profiles follow from these two lists of positive integers by prime-wise sorting. The kernel in the unrestricted tensor domain has dimension $(e+1)^d-\binom{d+e}{e}$.

For a pair whose coordinate distances are $\alpha$, its entry functional on the invariant observations has values $(\prod_l C_{\alpha_l}) e_O$ on the orbit basis: only one relation in the orbit sum contributes. Therefore its exact minimum denominator in the independent tensor polynomial lattice is $\prod_l B_{\alpha_l}$, and in the invariant tensor polynomial lattice it is

$$\boxed{L_O\prod_l B_{\alpha_l}.}$$

The result quantifies precisely the orbit-size obstruction induced by restricting the multiplier to an invariant lattice. It does not assume the total adjacency alone generates that invariant algebra. For a single scalar sum of the X_l, extra collisions are possible. For example, two copies of C4 have three factor eigenvalues -2,0,2, giving six unordered spectral pairs but only five distinct sums because (-2,2) and (0,0) both sum to zero.

## 4. Mixed Cartesian products of complete graphs

Let $G=K_{q_1}\square\cdots\square K_{q_d}$, $q_j\ge2$. Keep independent tensor basis $X_S$ and total adjacency A. Each coordinate has eigenvalues $-1,q_j-1$. Thus on the common eigenspace labeled by S the total eigenvalue is

$$\lambda_S=-d+\sum_{j\in S} q_j.$$

All 2^d joint spectral modes occur; in particular the scalar return moment has positive weight on every distinct sum. The rank of $\mathbb Q[A]$ equals the number r of distinct subset sums. Hence the dimension lost by this scalar compression is exactly $2^d-r$. A collision example is $(q_1,q_2,q_3)=(2,3,5)$, where $2+3=5$; the rank is seven, not eight.

Suppose all subset sums are distinct and put $D=2^d$ (new dimension notation in this section). Let F be the matrix of the coefficients of $1,A,\ldots,A^{D-1}$ in the independent relation basis. The evaluation matrix of that basis on joint eigenvalues is the tensor product of the matrices $\begin{pmatrix}1&-1\\1&q_j-1\end{pmatrix}$, each having determinant $q_j$. Its absolute determinant is $\prod_j q_j^{D/2}$ by the determinant formula for Kronecker products. The evaluation matrix of the powers of A is Vandermonde on the subset sums shifted by -d. Taking the ratio gives

$$\boxed{[L:\mathbb Z[A]]=\frac{\prod_{S<T}|\lambda_T-\lambda_S|}{\prod_j q_j^{2^{d-1}}}.}$$

The ordering S<T is any fixed ordering of the subsets. The ratio is a positive integer since F is integral and invertible over Q. This index is the full lattice obstruction, not necessarily the minimum denominator for any one target. The unrestricted mixed observation matrix is $F\operatorname{diag}(k_S)$ with $k_S=\prod_{j\in S}(q_j-1)$. In the scalar multiplier lattice, its Gram matrix is $F\operatorname{diag}(k_S)F^\top$. In particular the determinant distortion is the square of the index above, relative to the independent Gram determinant. A specific relation target has scalar multiplier coefficients $F^{-\top}e_S/k_S$; their least common denominator is optimal by uniqueness. This proves that both rank and arithmetic may be evaluated separately.

### Example: K2 × K3

With $X=X_1,Y=X_2$ we have $X^2=I$, $Y^2=Y+2I$. For $A=X+Y$, the coefficient matrix of its first four powers in the basis $(I,X,Y,XY)$ is

$$F=\begin{pmatrix}1&0&0&0\\0&1&1&0\\3&0&1&2\\2&7&6&3\end{pmatrix}.$$

Indeed $A^2=3I+Y+2XY$ and $A^3=2I+7X+6Y+3XY$. The determinant is 5. The subset sums are 0,2,3,5, and the index formula gives $(2\cdot3\cdot5\cdot1\cdot3\cdot2)/(2^2 3^2)=180/36=5$. The Smith profiles of $F\operatorname{diag}(1,1,2,2)$ and of $F\operatorname{diag}(1,1,2,2)F^\top$ are respectively $(1,1,2,10)$ and $(1,1,2,50)$. Solving in the scalar power basis gives the exact identity

$$X=(2A^3-3A^2-9A+5I)/5.$$

For a pair related by X, the row valency is one. Its walk counts therefore equal

$$w_n=(2m_{n+3}-3m_{n+2}-9m_{n+1}+5m_n)/5.$$

The moments are $1,0,3,2,19,30,143,\ldots$, giving $w_0=(4-9+5)/5=0$, $w_1=(38-6-27)/5=1$, and $w_2=(60-57-18+15)/5=0$. Because the four eigenvalues are distinct, the degree-at-most-three scalar multiplier is unique. The minimal polynomial is monic integral, so reduction of any integer polynomial preserves integrality. The displayed numerator has coefficients coprime to five, proving minimum denominator five over all degrees. This prime is absent from the two individual complete-graph valencies 1 and 2. It arises entirely from compressing the independent adjacency coordinates.

## 5. Precision consequence

For any of the full-row-rank integer transfer matrices with nonzero Smith invariants $t_0,\ldots,t_{r-1}$, the image modulo $p^h$ has size $p^{hr-\sum_i\min(h,v_p(t_i))}$. Every attainable value has $p^{h(D-r)+\sum_i\min(h,v_p(t_i))}$ preimages when the multiplier domain has rank D. For recovery of the multiplier *class modulo the exact integral kernel* to precision $p^H$, the sharp uniform data precision is $H+v_p(t_{r-1})$: transform to Smith coordinates, divide each pivot, and use a change of $p^{H-1}$ in the final coordinate as a lower-bound witness. This is unrestricted coefficient-class recovery, not a graph-constrained precision theorem.

For Hamming graphs the resulting overheads are $v_p(d!)+d v_p(q-1)$ in the independent and invariant multiplier cases, and $2v_p(d!)+d v_p(q-1)$ in the scalar polynomial case. In particular the scalar representation pays one additional factorial valuation for uniform recovery of its coefficients.

## 6. Verification, limits, and next step

Run `python -B check_product_transfers.py` with Python 3.10+ and SymPy 1.14.0. The actual successful run, recorded in `verification.log`, has 13,949 counted exact comparisons: 35 homogeneous Hamming parameter pairs (d=1..7, q=2..6); 10 mixed products, of which six have separating subset sums; eight symmetric tensor cases from four factor intersection arrays with two or three copies. The checker independently computes Smith forms and augmented lattice indices, and compares 4,070 entries with explicitly constructed Cartesian graph adjacency enumeration. Larger products use exact subset relation multiplication or tensor Gram matrices rather than full vertex enumeration. The factor arrays correspond to C5, Q3, H(2,3), and J(5,2). The first run failed on a SymPy integer passed to Python's `bit_count`; the conversion was fixed and the entire checker reran successfully. The initial error is retained in `initial_failure.log`.

The general association-scheme theorem and symmetric polynomial generation argument are established by the written proofs, not by exhaustive testing of all association schemes. No unknown graph topology is reconstructed, and no speedup or new priority claim is established. The tools (relation algebras, orthogonal bases, Smith form, symmetric polynomials, and Vandermonde evaluation) are classical. The new synthesis explicitly compares multiplier lattices and their optimal denominators. Lean certification, independent review, and a literature-wide novelty assessment remain outstanding. The next target is exact prime-by-prime Smith invariants of mixed products without enumerating minors, and integral transfer classification for equitable partitions that are not distance-regular.
