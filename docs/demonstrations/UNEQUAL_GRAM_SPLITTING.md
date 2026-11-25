# Unequal-depth isotropic Gram splitting

**Author: Komorebi P.**  
**Version:** 2.8, 2026-11-25  
**Status:** algebraic proofs and exact computational checks; not Lean certified or independently peer reviewed.

Predecessor: [Isotropic Gram obstructions, v2.7](https://github.com/KomorebiP/The-Komorebi-Program/blob/main/docs/demonstrations/ISOTROPIC_GRAM_OBSTRUCTION.md). The five predecessor checksums matched; its checker was not rerun here.

## 1. Defect data and truncation

Work over the discrete valuation ring $R=\mathbb Z_{(p)}$, with valuation $v=v_p$ and $v(0)=+\infty$. Let $W$ be a nonsingular square integral matrix of order $n$, with local Smith decomposition $W=UD_0V$ where $U,V$ are invertible over $R$. Keep the $k$ strictly positive depths $a_i$, put $D=\operatorname{diag}(p^{a_i})$, and let $Z$ consist of the corresponding columns of $V^{-1}$. Write $K=Z^\top Z$. The v2.7 defect presentation identifies the nonunit Smith factors of $H=WW^\top$ with those of

$$J=\begin{pmatrix}D&-K\\0&D\end{pmatrix}.$$

All results below hold for this presentation even with arbitrary integral local $K$, not necessarily a realized kernel Gram matrix. The $k=0$ case is unimodular and is treated separately. The presentation has size $2k$; discard its zero valuations and pad with zeros to order $n$ when recovering $H$. We do not claim an arbitrary abstract $K$ is realizable with a specified ambient dimension.

Only the entry residues $K_{ij}\bmod p^{\min(a_i,a_j)}$ matter. Indeed, a change $K\mapsto K+DX+YD$ is realized by invertible block triangular row and column operations on $J$. Every change in the stated entry ideals has this form, entry by entry. In particular the relevant pairing data are finite, even when the local bases are rational.

## 2. Closed weighted-minor formula at all unequal depths

For subsets $R_1,S_1\subseteq\{1,\ldots,k\}$ of equal cardinality $j$, put $v_{R_1,S_1}=v(\det K_{R_1,S_1})$, with the empty minor having value zero. Form the multiset

$$\mathcal A_{R_1,S_1}=\{a_i:i\notin R_1\}\uplus\{a_i:i\notin S_1\}.$$

For $0\le\ell\le2k$, let $c_\ell(R_1,S_1)$ be the sum of the $\ell-j$ smallest elements of this multiset. If $\ell-j<0$ or $\ell-j>2k-2j$, set $c_\ell=+\infty$. Then the order-$\ell$ determinantal divisor valuation and the ordered Smith exponents of $J$ are

$$d_\ell=\min_{R_1,S_1}\{v_{R_1,S_1}+c_\ell(R_1,S_1)\},\qquad b_\ell=d_\ell-d_{\ell-1}\quad(1\le\ell\le2k).$$

**Proof.** An order-$\ell$ minor selects upper rows $I$, lower rows $L$, left columns $A$ and right columns $B$. For a nonzero determinant, $A\subseteq I$ and $L\subseteq B$, because the left columns and lower rows have only their diagonal entries available. Expand along the left columns and then the lower rows. The resulting determinant, up to sign, is

$$p^{\sum_{i\in A}a_i+\sum_{i\in L}a_i}\det K_{I\setminus A,B\setminus L}.$$

The surviving row and column sets have equal size $j$. Conversely, every pair $R_1,S_1$ of size $j$ and every choice of $A\subseteq R_1^c$, $L\subseteq S_1^c$ with $|A|+|L|=\ell-j$ arises from a minor, by taking $I=R_1\cup A$, $B=S_1\cup L$. The minimum diagonal contribution is exactly $c_\ell$. The determinantal divisor characterization of Smith form now proves the result. The empty choice gives $d_0=0$. QED.

This is a finite formula using only minors of $K$, not minors of $H$ or generic Smith reduction of $J$. At full order $d_{2k}=2\sum_i a_i$. The formula can be exponential in $k$ if minors are enumerated; Section 5 avoids that enumeration.

## 3. Two interacting defects, and pairing patterns

Let $a\le b$ be the two positive depths and $K$ a symmetric two-by-two matrix. Put $u=v(K_{11})$, $v_0=v(K_{12})$, $w=v(K_{22})$, and $t=v(\det K)$. Specializing Section 2 gives

$$d_1=\min(a,u,v_0,w),$$
$$d_2=\min(2a,b+u,a+v_0,a+w,t),$$
$$d_3=\min(2a+b,2b+u,a+b+v_0,2a+w),\qquad d_4=2(a+b).$$

The four exponents are consecutive differences. Zero entries and singular pairings are included via the infinity convention.

If $K$ is diagonal, its directions split independently as $(\min(a_i,v(K_{ii})),2a_i-\min(a_i,v(K_{ii})))$. If an isolated two-direction block is $\left(\begin{smallmatrix}0&c\\c&0\end{smallmatrix}\right)$, the defect presentation permutes into two independent triangular two-by-two blocks with diagonal depths $a_i,a_j$. Each block gives the pair $(s,a_i+a_j-s)$, where $s=\min(a_i,a_j,v(c))$. Thus a unit off-diagonal interaction gives two exponents $a_i+a_j$. These rules apply to disjoint blocks of the truncated pairing, after the allowed entrywise reductions of Section 1.

Entrywise valuations alone are not sufficient. For $p=5$, depths $(1,2)$, compare

$$K_1=\begin{pmatrix}1&1\\1&2\end{pmatrix},\qquad K_2=\begin{pmatrix}1&1\\1&6\end{pmatrix}.$$

Every entry has valuation zero in both matrices, but their determinants have valuations zero and one. The defect exponents are respectively $(0,0,2,4)$ and $(0,1,1,4)$. Both are genuine pairings of primitive columns: take $Z=(e_1,e_1+e_2+t e_3)$ for $t=0,2$, complete it to the unimodular matrix $V^{-1}=(e_3,Z)$, and use $W=\operatorname{diag}(1,5,25)V$. The ambient Gram profiles are $(0,2,4)$ and $(1,1,4)$. Thus no formula depending only on the depths and the separate entry valuations can classify all interactions. Minor cancellations are intrinsic.

## 4. Sharp maximum exponent without minors

Since

$$J^{-1}=\begin{pmatrix}D^{-1}&D^{-1}KD^{-1}\\0&D^{-1}\end{pmatrix},$$

its largest Smith exponent is the least nonnegative $e$ for which $p^eJ^{-1}$ is integral over $R$. Therefore

$$\boxed{b_{\max}=\max\left(\max_i a_i,\ \max_{i,j}(a_i+a_j-v(K_{ij}))\right).}$$

This is invariant under the entry reductions of Section 1: a discarded high-valuation entry can contribute no more than $\max(a_i,a_j)$. The result gives the sharp uniform precision $H_0+b_{\max}$ for recovering unrestricted Gram-multiplier coefficients modulo $p^{H_0}$ from their image. Necessity follows by varying the coordinate of a largest Smith factor by $p^{H_0-1}$; sufficiency follows from the diagonal Smith congruences. This concerns coefficient recovery, not reconstruction of an unknown graph. In particular $\max_i a_i\le b_{\max}\le2\max_i a_i$.

## 5. Full profile from precision-dependent negative pivots

For $h\ge1$ put $m_i=\min(h,a_i)$ and $r_i=h-m_i$. The equations for the kernel of $J$ modulo $p^h$ are $Dy=0$ and $Dx=Ky$. The first says $y_j=p^{r_j}z_j$, with $z_j$ ranging modulo $p^{m_j}$. The second is solvable exactly when $(K\operatorname{diag}(p^{r_j})z)_i=0\bmod p^{m_i}$. Each such $y$ has exactly $p^{\sum_i m_i}$ compatible $x$.

Let $C_h$ be the base-$p$ logarithm of the order of the image of the scaled matrix

$$Q_h=\operatorname{diag}(p^{-m_i})K\operatorname{diag}(p^{r_j})$$

in $\mathbb Q^k/R^k$. Its domain can be taken as $R^k$ because increasing $z_j$ by $p^{m_j}$ changes the image by an integral vector. Then the kernel length is

$$L_h=\log_p|\ker(J\bmod p^h)|=2\sum_i m_i-C_h.$$

Equivalently, the lattice index of $\bigl[\operatorname{diag}(p^{m_i})\mid K\operatorname{diag}(p^{r_j})\bigr]$ gives

$$C_h=\max_{R_1,S_1}\left(\sum_{i\in R_1}m_i-\sum_{j\in S_1}r_j-v_{R_1,S_1}\right).$$

To see this, expand its full-order minors along the selected diagonal columns. The minimum valuation is $\sum_i m_i-C_h$, the index of the lattice generated by these columns. The empty pair makes the maximum nonnegative. This describes exactly the interactions visible at each precision.

There is no need to enumerate minors to compute $C_h$. Pick an entry of $Q_h$ of smallest valuation $e$. If $e\ge0$, the remaining block has zero image in $\mathbb Q^k/R^k$; stop. Otherwise permute it to the leading position and perform row and column elimination. All elimination ratios are in $R$ because the pivot has minimum valuation. These transformations are invertible over $R$ and preserve the image length in the quotient. The isolated pivot contributes $-e$; the Schur complement is processed in the same way. All remaining entries have valuation at least $e$, by the nonarchimedean triangle inequality. Induction proves that $C_h$ is the sum of the negatives of the selected negative valuations. Zero entries have infinite valuation. This procedure uses at most $k$ pivots and $O(k^3)$ arithmetic operations per queried precision, ignoring bit complexity.

Finally, for a finite Smith profile $b$,

$$L_0=0,\qquad L_h=\sum_\ell\min(h,b_\ell),\qquad L_h-L_{h-1}=\#\{\ell:b_\ell\ge h\}.$$

The last quantity is monotone nonincreasing in $h$. Binary search over $0\le h\le b_{\max}$ recovers each exponent (the $j$th largest is the largest $h$ with at least $j$ exponents at least $h$). At most $O(k\log(1+b_{\max}))$ queries suffice. This replaces generic Gram Smith reduction or exhaustive minor enumeration by negative-pivot elimination on $k$-by-$k$ matrices, once the source Smith defect data are supplied. It does not eliminate the cost of obtaining those data or establish an overall bit-complexity improvement.

## 6. Unequal splitting in actual graphs

Use the seven-vertex simple graph with edges 01,05,12,15,23,24,34,45,46, rooted at 4. The rooted walk matrix $W$ has integral Smith factors $(1,1,1,1,2,2,12)$ and $H=WW^\top$ has $(1,1,1,1,4,8,72)$. At two the source depths are $(1,1,2)$. A Smith decomposition yields the primitive pairing

$$K=\begin{pmatrix}595&90&-420\\90&22&-89\\-420&-89&376\end{pmatrix}\longmapsto\begin{pmatrix}1&0&0\\0&0&1\\0&1&0\end{pmatrix},$$

where the arrow is the entrywise truncation of Section 1. The diagonal unit block gives $(0,2)$ and the cross block gives $(0,3)$ twice. After discarding zeros, the predicted exponents are $(2,3,3)$, not $(2,2,4)$. Their sums both equal eight. The largest exponent is three, one digit smaller than naïve doubling.

| Precision $h$ | $C_h$ | Actual $L_h$ | Naïve doubled $L_h$ |
|---:|---:|---:|---:|
|1|3|3|3|
|2|2|6|6|
|3|0|8|7|
|4|0|8|8|

The modular ranks of $W$ and $H$ at two are both four; no extra rank drop is visible in the field. The characteristic polynomials are $f=x^7-9x^5-4x^4+17x^3+10x^2-4x-2$ and $g=x^6-5x^4-2x^3+4x^2+2x$. Their gcd modulo two is $x^3$, confirming the Gram rank but not the higher-depth distribution. The first difference in kernel lengths appears modulo eight, where the actual kernel has twice the size predicted by doubling.

For comparison, edges 01,04,06,12,15,16,23,34,35 rooted at 2 give source factors $(1,1,1,1,1,2,4)$ and Gram factors $(1,1,1,1,1,4,16)$. Depths $(1,2)$ and pairing $\left(\begin{smallmatrix}8&-11\\-11&25\end{smallmatrix}\right)$ give nonunit exponents $(2,4)$ by Section 3. Unequal depths alone do not force splitting.

## 7. Verification and remaining boundary

Run `python -B check_unequal_gram.py` with the packages in requirements.txt. The exact checker passed 9,311 counted comparisons, including 424 abstract or realized defect profiles, 196 independent ambient Gram comparisons, 3,436 weighted-minor kernel lengths, 3,436 negative-pivot kernel lengths, 424 full negative-pivot profile recoveries, 111 two-defect formulas and eight exhaustive modular kernel counts. The rooted graph-atlas search stopped after 2,204 root cases when it found both an unequal-depth splitting example and an unequal-depth doubling example; it is not an exhaustive classification through seven vertices. The two explicit cancellation witnesses were checked with unimodular ambient realizations. The additional characteristic-polynomial and precision-table calculations were separately evaluated and are not counted in the 9,311 comparisons.

The all-depth algebraic extraction gap from v2.7 is closed in terms of the source Smith defects and the truncated pairing. A formula using only the source Smith depths and entrywise valuations cannot exist in this generality, as proved by the cancellation witnesses. Recovering the truncated pairings directly from graph structure without obtaining the source defect data, extensions to nonunimodular rectangular saturations, mixed-product bad-prime structure, and literature-wide novelty remain further work. The arguments use elementary minors, local lattice theory and valuation pivoting. No independent peer review, Lean certification or complexity breakthrough is claimed.
