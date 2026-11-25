# Distance-regular graph transfers: explicit arithmetic and polynomial coordinates

**Author: Komorebi P.**  
**Version:** 2.4, 2026-11-24  
**Status:** algebraic proofs with exact computational checks. Not Lean certified or independently peer reviewed.

Predecessor: [Arithmetic reconstruction on distance-regular graphs](DISTANCE_REGULAR_TRANSFER.md). Its checksum manifest and all 25,116 counted comparisons were independently rerun for this continuation.

## 1. Explicit orthogonal basis and Smith form

Let $G$ be a finite connected simple distance-regular graph of diameter $d\ge1$, valency $k$, adjacency matrix $A$, and intersection numbers $a_i,b_i,c_i$. Put $m_n=(A^n)_{oo}$ and $\ell(x^n)=m_n$. Define

$$B_i=\prod_{j=0}^{i-1}b_j,\qquad C_i=\prod_{j=1}^{i}c_j,\qquad s_i=B_iC_i,$$

with empty products equal to one. The shell sizes satisfy $k_i=B_i/C_i$. The monic polynomials are $p_0=1$, $p_1=x$, and

$$p_{i+1}=(x-a_i)p_i-b_{i-1}c_i p_{i-1},\qquad 1\le i\le d.$$

Counting neighbors gives the distance matrix recurrence $AA_i=b_{i-1}A_{i-1}+a_iA_i+c_{i+1}A_{i+1}$, with missing boundary terms omitted. Induction proves $p_i(A)=C_iA_i$ for $i\le d$ and $M(A)=0$ for $M=p_{d+1}$. Disjoint nonempty distance shells imply $\ell(p_ip_j)=\delta_{ij}s_i$, which also proves that $M$ is the minimal moment annihilator and the minimal polynomial of $A$.

For the moment matrix $H_{ij}=m_{i+j}$ and the coefficient matrix $W$ whose columns are $p_j$ in increasing monomial powers, $W$ is unimodular and

$$W^\top H W=\operatorname{diag}(s_0,\ldots,s_d).$$

The positive entries satisfy the Smith divisibility chain. At distance $i$, the walk-count transfer is $\ell(x^n p_i)/B_i$. Its denominator $B_i$ is optimal: nondegeneracy of the pairing makes $p_i/B_i$ the unique reduced representative modulo $M$, and monic reduction of an integer polynomial cannot introduce a denominator.

For finite-prefix recovery, monic Gram-Schmidt on moments $m_0,\ldots,m_{2d}$ gives $p_i,s_i$. For $i<d$, $a_i=\ell(xp_i^2)/s_i$. Starting with $b_0=k=m_2$, compute $c_i=s_i/(s_{i-1}b_{i-1})$, then $b_i=k-a_i-c_i$ for $i<d$. At the last shell $b_d=0$, $a_d=k-c_d$. This reconstructs the intersection array given the diameter, not an unknown graph topology.

## 2. Worked cube example

For the cube $Q_3$, $b=(3,2,1,0)$, $c=(0,1,2,3)$ and all $a_i=0$. Hence $B=(1,3,6,6)$, $C=(1,1,2,6)$ and $s=(1,3,12,36)$. The moments begin $1,0,3,0,21,0,183,0,1641$.

$$p_2=x^2-3,\quad p_3=x^3-7x,\quad M=x^4-10x^2+9.$$

For example $m_6=10(21)-9(3)=183$. At distances one, two and three the walk counts are respectively $m_{n+1}/3$, $(m_{n+2}-3m_n)/6$ and $(m_{n+3}-7m_{n+1})/6$. Substitution gives two length-two walks at distance two, six length-three walks at distance three and sixty length-five walks at distance three.

$$H=\begin{pmatrix}1&0&3&0\\0&3&0&21\\3&0&21&0\\0&21&0&183\end{pmatrix},\quad W=\begin{pmatrix}1&0&-3&0\\0&1&0&-7\\0&0&1&0\\0&0&0&1\end{pmatrix}.$$

Direct multiplication gives the Smith profile $(1,3,12,36)$ and determinant 1296. For instance $\ell(p_2^2)=21-6(3)+9=12$, $\ell(p_3^2)=183-14(21)+49(3)=36$ and $\ell(p_1p_3)=21-7(3)=0$. The successive norm ratios are 3,4,3, giving $c_1=1,b_1=2,c_2=2,b_2=1,c_3=3$. Parity and the terminal condition give $a_i=0$.

For Hamming $H(2,3)$, $b=(4,2,0)$, $c=(0,1,2)$, $a=(0,1,2)$, $p_2=x^2-x-4$, $B=(1,4,8)$, $s=(1,4,16)$. Its moments begin $1,0,4,4,36,100$. The distance-two length-two count is $(36-4-16)/8=2$.

For Johnson $J(5,2)$, $b=(6,2,0)$, $c=(0,1,4)$, $a=(0,3,2)$, $p_2=x^2-3x-6$, $B=(1,6,12)$, $s=(1,6,48)$. Its moments begin $1,0,6,18,138,762$. The distance-two length-two count is $(138-54-36)/12=4$.

## 3. Arbitrary polynomial coordinates

Let $f\in\mathbb Z[x]$. Write $D=d+1$ and let $N(y)$ be the minimal polynomial of $f$ in $\mathbb Q[x]/(M)$, of degree $r$. It is monic integral by Gauss's lemma applied to the characteristic polynomial of multiplication by $f$ in the integral quotient. Since $M$ has distinct real roots, $r$ is the number of distinct values of $f$ on those roots.

For $0\le n<r$, form the integer coordinate matrix

$$f(x)^n\bmod M=\sum_{j=0}^d F_{nj}p_j(x).$$

The rows are independent by the minimality of $N$. For a multiplier $P=\sum_j u_jp_j$, the output sequence $\ell(Pf^n)$ is annihilated by $N(E)$. Orthogonality shows that its first $r$ terms are given by the transfer matrix

$$\boxed{T=F\operatorname{diag}(s_0,\ldots,s_d).}$$

It has full row rank. Equality of the first $r$ terms is sufficient for equality of recurrent sequences annihilated by $N(E)$. The kernel has dimension $D-r$ over $\mathbb Q$.

Let $\Delta_k(T)$ be the gcd of the absolute $k$-row, $k$-column minors, with $\Delta_0=1$. Factoring the column scales gives the exact determinantal divisor formula

$$\boxed{\Delta_k(T)=\gcd_{|I|=|J|=k}\left(|\det F_{I,J}|\prod_{j\in J}s_j\right).}$$

The Smith invariants are $\Delta_k/\Delta_{k-1}$. Prime-by-prime, $v_p(\Delta_k)$ is the minimum of $v_p(\det F_{I,J})+\sum_{j\in J}v_p(s_j)$ over nonzero minors.

For an integer-valued admissible target with first $r$ terms $\beta$, let $L=T\mathbb Z^D$. The least common denominator of a rational multiplier is the order of the coset $\beta+L$ in $\mathbb Z^r/L$. The indices of $L$ and $L+\mathbb Z\beta$ give

$$\boxed{q_{\min}=\frac{\Delta_r(T)}{\Delta_r([T\mid\beta])}.}$$

Thus integrality is equivalent to equality of the two determinantal divisors. For the distance-$i$ observable $(f(A)^n)_{uv}$, $\beta=Te_i/B_i$, so $q_{\min}$ divides $B_i$. If $f$ separates the spectrum, $r=D$ and the representative is unique, hence $q_{\min}=B_i$. Spectral collisions can reduce it.

For Smith invariants $t_1,\ldots,t_r$, every attainable target modulo $p^h$ has exactly $p^{h(D-r)+\sum_i\min(h,v_p(t_i))}$ coefficient preimages. If $r=D$, the sharp uniform precision for recovering the reduced multiplier modulo $p^H$ is $H+v_p(t_r)$. If $r<D$, unrestricted full coefficient recovery is impossible even with exact data.

## 4. Affine and separating coordinates

For $f(x)=ax+b$, $a\ne0$ integral, the polynomials $a^ip_i((y-b)/a)$ are monic integral in $y$. They supply a unimodular row basis change, taking $T$ to the diagonal $a^is_i$. Its Smith invariants are

$$\boxed{|a|^i s_i,\quad 0\le i\le d.}$$

The precision overhead is $d\,v_p(a)+v_p(s_d)$. Translation has no effect, whereas scaling can alter arithmetic without changing rank.

If the values of $f$ on the roots $\lambda_0,\ldots,\lambda_d$ of $M$ are all distinct, evaluation of the monic basis and of the powers of $f$ at the roots gives a ratio of Vandermonde determinants:

$$\boxed{\det F=\prod_{i<j}\frac{f(\lambda_j)-f(\lambda_i)}{\lambda_j-\lambda_i}.}$$

The ratio is a nonzero integer, and $|\det T|=|\det F|\prod_i s_i$. At every prime not dividing $\det F$, the local Smith invariants agree with the original profile. This controls the total determinant; individual invariants at exceptional primes still require the minors formula.

## 5. Explicit coordinate collisions and arithmetic distortion

On $Q_3$, use $p=(1,x,x^2-3,x^3-7x)$ and $s=(1,3,12,36)$.

For $f=x^2+2x$, the values on $-3,-1,1,3$ are $3,-1,3,15$, so $r=3$. The matrices are

$$F=\begin{pmatrix}1&0&0&0\\3&2&1&0\\33&28&14&4\end{pmatrix},\quad T=\begin{pmatrix}1&0&0&0\\3&6&12&0\\33&84&168&144\end{pmatrix}.$$

Subtract three times row one from row two, thirty-three times row one from row three, then fourteen times the new row two from row three. Subtract twice column two from column three and permute columns. The Smith form has invariants $(1,6,144)$ and one free column. The distance-one and distance-two targets both have first terms $(0,2,28)^\top$; hence the transfer $p_2/6$ can be replaced with $p_1/3$. The equation $6u_1+12u_2=2q$ requires $3\mid q$, and $q=3$ works. Thus the minimum denominator drops from six to three. The two distinct distance observables have merged under the coordinate change.

For $f=x^3$, all four modes remain distinct, but

$$T=\begin{pmatrix}1&0&0&0\\0&21&0&36\\183&0&1092&0\\0&14763&0&29520\end{pmatrix}.$$

Its Smith invariants are $(1,3,1092,29484)$ and $\det F=74529=3^2\cdot7^2\cdot13^2$. The annihilator is $N(y)=y^4-730y^2+729$. The integer recurrent target with first terms $(0,0,1,0)^\top$ and annihilator $N$ has unique multiplier $(x^2-3)/1092$. This gives actual new denominator obstructions at 7 and 13 without rational information loss. The graph-derived distance targets still have denominators $(1,3,6,6)$.

| Coordinate | Smith invariants on $Q_3$ | Minimum distance denominators |
| --- | --- | --- |
| $x$ | 1,3,12,36 | 1,3,6,6 |
| $2x+1$ | 1,6,48,288 | 1,3,6,6 |
| $x^2$ | 1,12 | 1,1,6,1 |
| $x^2+2x$ | 1,6,144 | 1,3,3,6 |
| $x^3$ | 1,3,1092,29484 | 1,3,6,6 |

The square coordinate has zero odd-distance observables. For all bipartite distance-regular graphs the earlier stride-two profile remains $(s_0,s_2,\ldots,s_{2\lfloor d/2\rfloor})$.

## 6. Verification and boundaries

The detailed v2.4 standalone archive includes the expanded proof, copied predecessor checker, new polynomial-coordinate checker, actual execution log, dependency versions and SHA-256 manifest. The new execution passed 20,770 counted comparisons in 240 coordinate cases across 24 graph or intersection-array cases (8 Hamming, 6 Johnson, 7 cycles and 3 named graphs), using ten polynomials each. Checks include independent Smith forms, weighted and augmented minors, denominator attainment and rejection, spectral rank, and 11,300 comparisons with direct full adjacency matrix powers on five small graphs. The explicit cubic target was separately checked by symbolic linear algebra and is not included in that count. The predecessor's 25,116 checks also passed on rerun. Counts overlap and are not independent theorems.

These identities refine arithmetic realization beyond spectral rank. A universal simple product for arbitrary nonlinear coordinate Smith invariants remains open in this program; the weighted-minors theorem is exact but need not be computationally cheap. Association-scheme extensions, graph-constrained sharp precision, Lean certification, independent peer review and a literature-wide priority assessment remain outstanding. No OEIS submission has been made.
