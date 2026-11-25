# Isotropic Gram obstructions in arithmetic graph transfers

**Author: Komorebi P.**  
**Version:** 2.7, 2026-11-25  
**Status:** Algebraic proofs and exact finite computational checks. Not Lean certified or independently peer reviewed.

Predecessor: [Local arithmetic of Cartesian products and rooted equitable walk transfers](LOCAL_SMITH_EQUITABLE.md), Section 5.

## 1. Local Gram splitting and the exact doubling criterion

Let $W$ be a nonsingular square integral matrix, $H=WW^\top$, and work over $R=\mathbb Z_{(p)}$. Write its local Smith decomposition $W=UDV$, with $U,V$ unimodular and $D=\operatorname{diag}(p^{a_i})$, $a_1\le\cdots\le a_n$. Put $C=VV^\top$. Then $H$ is equivalent to $DCD$. Denote its ordered Smith exponents by $b_i$.

For any matrix $W$, including rectangular and singular cases, if $L$ is its row space modulo $p$, then

$$\operatorname{rank}_{\mathbb F_p}(WW^\top)=\operatorname{rank}_{\mathbb F_p}W-\dim(L\cap L^\perp).$$

Indeed $\operatorname{im}W^\top=L$ and $\ker W=L^\perp$. It is the radical of the restricted form, not merely the presence of self-isotropic vectors, that causes extra modular rank loss.

**Theorem.** For the square nonsingular case,

$$\sum_{i=1}^k b_i\ge 2\sum_{i=1}^k a_i,\qquad \sum_i b_i=2\sum_i a_i.$$

Moreover $b_i=2a_i$ for all $i$ if and only if each leading principal block $C_{[1,k],[1,k]}$ has unit determinant at every strict jump $a_k<a_{k+1}$.

**Proof.** The valuation of each order-$k$ minor of $DCD$ is its corresponding row and column sums of the $a_i$ plus the valuation of the minor of $C$. Minimizing gives the inequality. At full order equality follows from unimodularity of $C$. At a strict jump the first $k$ indices are the unique minimal weight row and column sets, giving the necessity and sufficiency of the unit determinant for equality at that boundary. Between such boundaries the $a_i$ are constant. Monotonicity of the $b_i$ bounds each cumulative sum above by its linear interpolation between the boundaries; the lower bound is exactly that interpolation. Hence equality at all boundaries implies equality everywhere.

Intrinsically, for the row lattice $\mathcal L$ of $W$, put

$$L_t=\{p^{-t}w\bmod p:w\in\mathcal L\cap p^tR^n\},\quad t\ge0.$$

This is the span of rows of $V$ with $a_i\le t$ modulo $p$. Thus exact doubling occurs if and only if every Smith filtration subspace is nondegenerate. The proof works at two as well as odd primes.

## 2. General defect presentation

Let $k$ be the number of positive $a_i$, $D_+=\operatorname{diag}(p^{a_i}:a_i>0)$, and let $Z$ be the corresponding columns of $V^{-1}$. Define $K=Z^\top Z$. The nonunit local Smith factors of $H$ are exactly those of the smaller presentation

$$\boxed{\begin{pmatrix}D_+&-K\\0&D_+\end{pmatrix}.}$$

The matrix has size $2k$, and the result permits unequal positive depths. For $k=0$ the Gram matrix is unimodular.

**Proof.** In the standard unimodular ambient lattice use the basis $e'_i=V^\top e_i$ and its dual $e_i'^*=V^{-1}e_i$. The row lattice has basis $p^{a_i}e'_i$, and its dual has basis $p^{-a_i}e_i'^*$. The discriminant quotient $\mathcal L^*/\mathcal L$ has presentation $DCD$. Its generators can be taken to be $x_i=e'_i\bmod\mathcal L$ and $y_i=p^{-a_i}e_i'^*\bmod\mathcal L$ on positive indices. Their relations are $p^{a_i}x_i=0$ and $p^{a_i}y_i=\sum_j(C^{-1})_{ji}x_j$. The positive-index submatrix of $C^{-1}$ is $K$. These relations give a surjection from the displayed presentation to the discriminant quotient. Both modules have length $2\sum_i a_i$, by their determinants, so it is an isomorphism.

If all positive depths equal $a$, let $\kappa_j$ be the Smith factors of $K$ and $t_j=\min(a,v_p(\kappa_j))$, with valuation of zero interpreted as infinity. Then the Gram exponents are obtained from the pairs

$$\boxed{(t_j,2a-t_j)}$$

by discarding zeros, sorting and padding with zeros to order $n$. To prove this, unimodularly diagonalize $K$ using independent left and right operations, applying their inverse operations to the complementary blocks to preserve the two scalar blocks $p^aI$. The resulting independent two-by-two blocks have first invariant of valuation $t_j$ and determinant valuation $2a$.

In particular, for one positive exponent $a$ and $n\ge2$, choose any primitive kernel lift $Wz=0\bmod p^a$. The Gram exponents consist of $n-2$ zeros and

$$\boxed{t,\ 2a-t},\qquad t=\min(a,v_p(z^\top z)).$$

Indeed $Vz$ is a unit multiple of the final standard coordinate modulo $p^a$, so the truncated norm valuation is well-defined. For $n=1$ the sole Gram exponent is $2a$.

At precision $p^h$, the one-defect Gram transfer kernel has size $p^{\min(h,t)+\min(h,2a-t)}$. The sharp uniform precision needed to recover an unrestricted coefficient vector modulo $p^H$ is $H+2a-t$. Splitting changes the distribution and low-precision ambiguity even though the total determinant valuation is conserved.

For $W=\begin{pmatrix}b&-1\\25&0\end{pmatrix}$ the Smith factors are $(1,25)$ and a primitive kernel lift is $(1,b)^\top$. At $b=1,2,7$ its norm is $2,5,50$, giving Gram factors $(1,625),(5,125),(25,25)$ respectively.

## 3. Rooted graph Gram matrices: the polynomial ideal description

For any symmetric integral matrix $A$ of order $n$ and coordinate root $o$, let $W$ have rows $e_o^\top A^i$ for $0\le i<n$ and $H=WW^\top$. No nonsingularity assumption is needed here. Define

$$f(x)=\det(xI-A),\qquad g(x)=\det(xI-A_{-o}).$$

The full integral Gram cokernel has the exact description

$$\boxed{\operatorname{coker}H\cong\mathbb Z[x]/(f,g).}$$

Thus the Gram Smith factors, including zero factors, equal those of multiplication by $g$ modulo $f$ in the integral monomial basis.

**Proof.** Write $m_j=e_o^\top A^je_o$. The resolvent cofactor identity gives $g(x)/f(x)=\sum_{j\ge0}m_jx^{-j-1}$. Form the Bezout polynomial

$$B(x,y)=\frac{f(x)g(y)-g(x)f(y)}{x-y}.$$

The divided difference of the Laurent series yields $\sum_{i,j\ge0}m_{i+j}x^{-i-1}y^{-j-1}$. Multiplying by $f(x)f(y)$ and taking polynomial parts gives $B(x,y)=\sum_{i,j<n}m_{i+j}q_i(x)q_j(y)$, where $q_i$ is the polynomial part of $f(x)x^{-i-1}$. Their coefficient matrix is $J_0=(f_{i+j+1})_{0\le i,j<n}$ with $f_s=[x^s]f$, a unimodular matrix because its reverse diagonal consists of ones and the entries beyond it vanish. The Bezout matrix is therefore $J_0HJ_0^\top$.

Modulo $f(y)$ the Bezout polynomial equals $g(y)(f(x)-f(y))/(x-y)$. The kernel for $g=1$ has coefficient matrix $J_0$, so its remainder after multiplication by $g(y)$ has matrix $J_0M_g^\top$, where $M_g$ is multiplication by $g$ modulo $f$. Consequently $M_g=J_0H$. The multiplication cokernel is exactly the stated polynomial quotient.

Consequences:

$$\boxed{\operatorname{rank}_{\mathbb F_p}H=n-\deg\gcd(\bar f,\bar g).}$$

At arbitrary precision, the size of $(\mathbb Z/p^h)[x]/(f,g)$ is $p^{\sum_i\min(h,b_i)}$, interpreting zero Smith factors as infinite exponents. Successive differences of the logarithmic sizes count the number of exponents at least $h$. The resultant alone gives only the determinant and cannot determine this distribution.

Let $U$ be the rooted cyclic subspace over $\mathbb F_p$, $m_o$ its minimal polynomial, and $N=\bar f/\gcd(\bar f,\bar g)$. A polynomial annihilates the moments precisely when its product with $\bar g/\bar f$ has no negative Laurent terms, so $N$ is the minimal moment annihilator. Equivalently it annihilates the quotient of $U$ by its radical, because pairing a cyclic vector with all cyclic vectors detects exactly that radical. Thus the radical has characteristic polynomial $m_o/N$. It is contained in $U$ and $U^\perp$, whose characteristic polynomials are $m_o$ and $\bar f/m_o$ respectively. Hence

$$m_o/N\mid\gcd(m_o,\bar f/m_o).$$

For a one-dimensional modular source kernel, the extra Gram rank loss corresponds precisely to a squared common linear factor of the full and root-deleted characteristic polynomials.

**Squarefree prime screen.** If $W$ is nonsingular and $\bar f$ is squarefree, then the Gram Smith exponents double at $p$. Indeed the row lattice is stable under $A$ by Cayley-Hamilton, so every filtration subspace $L_t$ is invariant modulo $p$. Over a splitting field the distinct eigenlines of the symmetric matrix are mutually orthogonal and nondegenerate. Each invariant subspace is a direct sum of eigenlines by spectral interpolation, hence nondegenerate. Apply the exact doubling criterion. Thus splitting primes must divide the characteristic discriminant, but this necessary condition is not sufficient.

## 4. Actual graph examples

The original graph has root 0 and edges 01,03,04,12,23,34. Its polynomials are

$$f=x^5-6x^3-2x^2+4x,\quad g=x^4-3x^2+1.$$

Modulo five their gcd is $(x-3)^2$, giving Gram rank three. The rooted walk matrix has rank four modulo five and its only nonunit Smith factor is 5. The resultant is 25. Thus the Gram factors are $(1,1,1,5,5)$. The kernel lift $(0,1,3,3,1)^\top$ has norm 20, confirming the one-defect depth rule.

Two actual seven-vertex graphs give higher-depth splitting. Vertex order is increasing in both cases.

- Root 1, edges 01,04,05,12,15,23,25,34,46. Source factors $(1,1,1,1,1,1,4)$, kernel lift $(2,0,1,2,1,1,-1)^\top$ modulo four of norm 12. Thus $p=2,a=t=2$ and Gram factors $(1,1,1,1,1,4,4)$.
- Root 5, edges 01,04,12,14,15,23,34,35,36,46,56. Source factors $(1,1,1,1,1,1,24)$, kernel lift $(-2,1,1,1,3,0,-2)^\top$ modulo eight of norm 20. Thus $p=2,a=3,t=2$, with two-adic Gram exponents 2 and 4. The complete integral Gram factors are $(1,1,1,1,1,4,144)$.

## 5. Verification and remaining boundaries

The standalone v2.7 research archive contains the expanded proof, executable checker, actual log, requirements and checksum manifest. The completed run passed 10,217 counted exact comparisons: 380 constructed square matrices with prescribed exponents, 378 defect presentations, 281 equal-depth profiles, 380 flag criteria, 810 rooted cases across all 143 connected unlabeled graphs through order six, 138 Bezout congruences, 3,254 finite-field gcd rank comparisons, 396 squarefree screens, the original counterexample and higher-depth witnesses, among other overlapping checks. The two seven-vertex witnesses were obtained by a search stopped when both splitting types were found; order seven was not exhaustively checked.

These proofs establish exact local classification by a defect presentation and by a polynomial ideal for rooted graphs. A simpler formula for unequal-depth cases directly from graph structure, local polynomial subresultant shortcuts, and extension to rectangular lattices with nonunimodular saturation remain further work. The methods are classical lattice duality, Smith form, and Bezoutian identities; no literature-wide novelty, computational complexity improvement, Lean certification or independent peer review is claimed. The predecessor checker was not rerun for this continuation.
