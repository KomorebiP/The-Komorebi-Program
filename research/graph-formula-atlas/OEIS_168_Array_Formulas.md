# 168 OEIS array formulas
Author: Komorebi P.

**Scope.** 168 accepted bindings (101 new relative to v19), each specialized below. `*` marks new IDs. This is a catalog of explicit construction formulas, not a claim of elementary expressions for every family. Source audit: 1,347 comparisons including six for two excluded IDs; 1,341 comparisons for accepted IDs. A202583 has a partial prefix. Flattened traversal is a finite-checked convention.

## Definitions



Every entry below is specialized to its OEIS identifier and mathematical index $n\ge1$. A star marks the 101 additions relative to v19. The retained compiler accepted 168 of 170 examined IDs; A202566 and A202718 are excluded. The new catalog preserves the archive's evidence: exact construction formulas for the stated counting problem, finite agreement with the OEIS receipts, and a finitely checked antidiagonal convention for the flattened tables. A202583 has seven of eight retained terms checked.

For heights $n+2$, set
\[h=1+\lfloor n/2\rfloor,\qquad k=1+\lceil n/2\rceil.\]
For a flattened table, put
\[\ell=\left\lfloor\frac{1+\sqrt{8n-7}}{2}\right\rfloor,\quad i=n-\frac{\ell(\ell-1)}2,\quad j=\ell+1-i.\]
This visits $(1,1),(1,2),(2,1),(1,3),\ldots$. Define $h_t=1+\lfloor t/2\rfloor$, $k_t=1+\lceil t/2\rceil$ for $t=i,j$. A table indexed directly by $(i,j)$ uses those same variables without flattening.

### Reduced independent-set factors
$F_m=((1+\sqrt5)^m-(1-\sqrt5)^m)/(2^m\sqrt5)$ is the ordinary Fibonacci number. For $d=0,1$, define the row-mask set
\[S_w=\{a:0\le a<2^w,\ a\mathbin{\&}(2a)=0\}.\]
Let $M_w^{(d)}$ have rows and columns in $S_w$. The entry at $(a,b)$ is one exactly when $a\mathbin{\&}b=0$ and either $d=0$ or $(2a)\mathbin{\&}b=0$; otherwise it is zero. Let $e_0$ select the all-zero mask. Then
\[\mathcal I_w^{(d)}(m)=e_0^T(M_w^{(d)})^m\mathbf1.\]
Here $d=0$ means horizontal and vertical adjacency; $d=1$ adds NW--SE diagonal adjacency. This is an explicitly defined integer matrix power, including $\mathcal I_w^{(d)}(0)=\mathcal I_0^{(d)}(m)=1$. It counts independent sets, not arbitrary arrays.

For a matrix-free-in-$m$ evaluation, the appendix gives polynomials $P,Q$ for every fixed reduced strip used by the structural formulas. For $w\le9$, set $B=2^{w(m+1)+1}+1$. Then
\[\mathcal I_w^{(d)}(m)=\left\lfloor\frac{B^m P(1/B)}{Q(1/B)}\right\rfloor\bmod B.\]
No sequence values or algebraic roots are needed. For arbitrary $w$, use the matrix power above, or the identity\[P(z)/Q(z)=e_0^T(I-zM_w^{(d)})^{-1}\mathbf1.\] The tail after the $m$-th coefficient is less than one because the coefficient of degree $t$ is at most $2^{wt}$. Thus the floor isolates the exact coefficient as a base-$B$ digit.

### Explicit forbidden-word matrices
For $\mathcal A_w^{(d;p_1,\ldots,p_s)}$, let $\mathcal P$ be the displayed forbidden words, all of length $L$. Let $R$ contain all binary rows of length $w$ with no consecutive length-$L$ word in $\mathcal P$. A state is an ordered $(L-1)$-tuple of rows in $R$. The rows and columns of the matrix index all such states. The entry from $a=(a_1,\ldots,a_{L-1})$ to $b=(b_1,\ldots,b_{L-1})$ is one precisely when:

- $b_r=a_{r+1}$ for $1\le r<L-1$;
- in the $L$-row stack $a_1,\ldots,a_{L-1},b_{L-1}$, no complete vertical word is in $\mathcal P$;
- when $d=1$, no complete NW--SE diagonal word is in $\mathcal P$.

All other entries are zero. Every initial history is allowed, since it contains only $L-1$ rows, so for $H\ge L-1$ the rectangle count is $\mathbf1^T\mathcal A^{H-L+1}\mathbf1$. This counts the initial rows and every subsequent row exactly once. All boundary constraints require the entire original window to fit. A leading zero in a pattern label is significant.

### Sliding-window and block matrices
$\mathcal C_{w,L,K}$ means exactly the matrix in B with $d=0$ and $\mathcal P=\{p\in\{0,1\}^L:\sum p_r>K\}$. It counts arrays with at most $K$ ones per complete horizontal or vertical length-$L$ window.

For $\mathcal B_{w,b,t}$, the state set is $\{0,\ldots,b-1\}^w$. Its entry from row $a$ to row $v$ is
\[\prod_{j=1}^{w-1}\mathbf1\{a_j+a_{j+1}+v_j+v_{j+1}\ge t\}.\]
Thus $\mathbf1^T\mathcal B_{w,b,t}^{H-1}\mathbf1$ counts $H$ rows whose every complete $2\times2$ sum is at least $t$. The two retained block families use $(b,t)=(2,2)$ and $(4,7)$.

### Direct integer evaluation
For any $\mathbf u^T A^m\mathbf v$ in this catalog, including the independent-set factors, let $g(z)=\mathbf u^T(I-zA)^{-1}\mathbf v$. Choose an integer $c\ge1$ bounding the row sums of $A$, and $a\ge1$ bounding $\|\mathbf u\|_1\|\mathbf v\|_\infty$. With $B=2ac^{m+1}+1$, the exact integer is
\[\left\lfloor\frac{B^{m+1}\mathbf u^T\operatorname{adj}(BI-A)\mathbf v}{\det(BI-A)}\right\rfloor\bmod B.\]
For the all-ones vectors, take $a$ equal to the state count. For A and C take $c=2^w$; for B take $c=b^w$; for I take $a=1,c=2^w$. The bound on the tail of $B^m g(1/B)$ is $ac^{m+1}/(B(1-c/B))<1$, so this is exact. It is not a claim of computational speed or small matrix size. Square arrays and flattened tables have width depending on the index; the matrix construction remains exact but does not imply a fixed-order scalar recurrence.


### A184200

fixed width 3; Inherited; 8 terms checked; Block transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal B_{3,2,2}\bigr)^{n}\mathbf1\]

### A184201

fixed width 4; Inherited; 8 terms checked; Block transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal B_{4,2,2}\bigr)^{n}\mathbf1\]

### A184202

fixed width 5; Inherited; 8 terms checked; Block transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal B_{5,2,2}\bigr)^{n}\mathbf1\]

### A184203

fixed width 6; Inherited; 8 terms checked; Block transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal B_{6,2,2}\bigr)^{n}\mathbf1\]

### A184204

fixed width 7; Inherited; 8 terms checked; Block transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal B_{7,2,2}\bigr)^{n}\mathbf1\]

### A184205

fixed width 8; Inherited; 8 terms checked; Block transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal B_{8,2,2}\bigr)^{n}\mathbf1\]

### A184206

fixed width 9; Inherited; 8 terms checked; Block transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal B_{9,2,2}\bigr)^{n}\mathbf1\]

### A184207 *

antidiagonal; New vs v19; 8 terms checked; Block transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal B_{j+1,2,2}\bigr)^{i}\mathbf1\]

### A184208 *

square; New vs v19; 7 terms checked; Block transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal B_{n+1,4,7}\bigr)^{n}\mathbf1\]

### A184209

fixed width 2; Inherited; 8 terms checked; Block transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal B_{2,4,7}\bigr)^{n}\mathbf1\]

### A184210 *

fixed width 3; New vs v19; 8 terms checked; Block transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal B_{3,4,7}\bigr)^{n}\mathbf1\]

### A184211 *

fixed width 4; New vs v19; 8 terms checked; Block transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal B_{4,4,7}\bigr)^{n}\mathbf1\]

### A184212 *

fixed width 5; New vs v19; 8 terms checked; Block transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal B_{5,4,7}\bigr)^{n}\mathbf1\]

### A184213 *

fixed width 6; New vs v19; 8 terms checked; Block transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal B_{6,4,7}\bigr)^{n}\mathbf1\]

### A184214 *

fixed width 7; New vs v19; 8 terms checked; Block transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal B_{7,4,7}\bigr)^{n}\mathbf1\]

### A184215 *

fixed width 8; New vs v19; 8 terms checked; Block transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal B_{8,4,7}\bigr)^{n}\mathbf1\]

### A184216 *

fixed width 9; New vs v19; 7 terms checked; Block transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal B_{9,4,7}\bigr)^{n}\mathbf1\]

### A184217 *

antidiagonal; New vs v19; 8 terms checked; Block transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal B_{j+1,4,7}\bigr)^{i}\mathbf1\]

### A202092 *

square; New vs v19; 8 terms checked; Reduced parity formula.

\[a(n)=\begin{aligned}&\binom{h+h}{h}\,\binom{h+k}{k}\\[-1pt]&\quad\times \binom{k+h}{h}\,\binom{k+k}{k}\end{aligned}\]

### A202093

fixed width 3; Inherited; 8 terms checked; Reduced parity formula.

\[a(n)=\begin{aligned}&\binom{h+1}{1}\,\binom{h+2}{2}\\[-1pt]&\quad\times \binom{k+1}{1}\,\binom{k+2}{2}\end{aligned}\]

### A202094

fixed width 4; Inherited; 8 terms checked; Reduced parity formula.

\[a(n)=\binom{h+2}{2}^{2}\,\binom{k+2}{2}^{2}\]

### A202095

fixed width 5; Inherited; 8 terms checked; Reduced parity formula.

\[a(n)=\begin{aligned}&\binom{h+2}{2}\,\binom{h+3}{3}\\[-1pt]&\quad\times \binom{k+2}{2}\,\binom{k+3}{3}\end{aligned}\]

### A202096

fixed width 6; Inherited; 8 terms checked; Reduced parity formula.

\[a(n)=\binom{h+3}{3}^{2}\,\binom{k+3}{3}^{2}\]

### A202097 *

fixed width 7; New vs v19; 8 terms checked; Reduced parity formula.

\[a(n)=\begin{aligned}&\binom{h+3}{3}\,\binom{h+4}{4}\\[-1pt]&\quad\times \binom{k+3}{3}\,\binom{k+4}{4}\end{aligned}\]

### A202098 *

fixed width 8; New vs v19; 8 terms checked; Reduced parity formula.

\[a(n)=\binom{h+4}{4}^{2}\,\binom{k+4}{4}^{2}\]

### A202099 *

fixed width 9; New vs v19; 8 terms checked; Reduced parity formula.

\[a(n)=\begin{aligned}&\binom{h+4}{4}\,\binom{h+5}{5}\\[-1pt]&\quad\times \binom{k+4}{4}\,\binom{k+5}{5}\end{aligned}\]

### A202100 *

antidiagonal; New vs v19; 8 terms checked; Reduced parity formula.

\[a(n)=\begin{aligned}&\binom{h_i+h_j}{h_j}\,\binom{h_i+k_j}{k_j}\\[-1pt]&\quad\times \binom{k_i+h_j}{h_j}\,\binom{k_i+k_j}{k_j}\end{aligned}\]

### A202194

square; Inherited; 8 terms checked; Elementary binomial formula.

\[a(n)=2(n+2)^2\binom{2n+2}{n+1}\]

### A202195

fixed width 3; Inherited; 8 terms checked; Elementary binomial formula.

\[a(n)=6(n+2)\binom{n+3}{2}\]

### A202196

fixed width 4; Inherited; 8 terms checked; Elementary binomial formula.

\[a(n)=8(n+2)\binom{n+4}{3}\]

### A202197

fixed width 5; Inherited; 8 terms checked; Elementary binomial formula.

\[a(n)=10(n+2)\binom{n+5}{4}\]

### A202198

fixed width 6; Inherited; 8 terms checked; Elementary binomial formula.

\[a(n)=12(n+2)\binom{n+6}{5}\]

### A202199

fixed width 7; Inherited; 8 terms checked; Elementary binomial formula.

\[a(n)=14(n+2)\binom{n+7}{6}\]

### A202200

fixed width 8; Inherited; 8 terms checked; Elementary binomial formula.

\[a(n)=16(n+2)\binom{n+8}{7}\]

### A202201

fixed width 9; Inherited; 8 terms checked; Elementary binomial formula.

\[a(n)=18(n+2)\binom{n+9}{8}\]

### A202202 *

antidiagonal; New vs v19; 8 terms checked; Elementary binomial formula.

\[a(n)=2(i+2)(j+2)\binom{i+j+2}{i+1}\]

### A202311

fixed width 4; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{4}^{(0;001,100)}\bigr)^{n}\mathbf1\]

### A202312

fixed width 5; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{5}^{(0;001,100)}\bigr)^{n}\mathbf1\]

### A202313

fixed width 6; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{6}^{(0;001,100)}\bigr)^{n}\mathbf1\]

### A202314 *

fixed width 7; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{7}^{(0;001,100)}\bigr)^{n}\mathbf1\]

### A202315 *

fixed width 8; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{8}^{(0;001,100)}\bigr)^{n}\mathbf1\]

### A202316 *

fixed width 9; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{9}^{(0;001,100)}\bigr)^{n}\mathbf1\]

### A202317 *

antidiagonal; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{j+2}^{(0;001,100)}\bigr)^{i}\mathbf1\]

### A202371

fixed width 3; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{3}^{(0;001,111)}\bigr)^{n}\mathbf1\]

### A202372

fixed width 4; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{4}^{(0;001,111)}\bigr)^{n}\mathbf1\]

### A202373

fixed width 5; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{5}^{(0;001,111)}\bigr)^{n}\mathbf1\]

### A202374

fixed width 6; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{6}^{(0;001,111)}\bigr)^{n}\mathbf1\]

### A202375 *

fixed width 7; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{7}^{(0;001,111)}\bigr)^{n}\mathbf1\]

### A202376 *

fixed width 8; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{8}^{(0;001,111)}\bigr)^{n}\mathbf1\]

### A202377 *

fixed width 9; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{9}^{(0;001,111)}\bigr)^{n}\mathbf1\]

### A202378 *

antidiagonal; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{j+2}^{(0;001,111)}\bigr)^{i}\mathbf1\]

### A202398 *

square; New vs v19; 8 terms checked; Reduced parity formula.

\[a(n)=\begin{aligned}&\mathcal I_{h}^{(0)}(h)\,\mathcal I_{k}^{(0)}(h)\\[-1pt]&\quad\times \mathcal I_{h}^{(0)}(k)\,\mathcal I_{k}^{(0)}(k)\end{aligned}\]

### A202399

fixed width 3; Inherited; 8 terms checked; Reduced parity formula.

\[a(n)=\begin{aligned}&\mathcal I_{1}^{(0)}(h)\,\mathcal I_{2}^{(0)}(h)\\[-1pt]&\quad\times \mathcal I_{1}^{(0)}(k)\,\mathcal I_{2}^{(0)}(k)\end{aligned}\]

### A202400

fixed width 4; Inherited; 8 terms checked; Reduced parity formula.

\[a(n)=\bigl(\mathcal I_{2}^{(0)}(h)\bigr)^{2}\,\bigl(\mathcal I_{2}^{(0)}(k)\bigr)^{2}\]

### A202401

fixed width 5; Inherited; 8 terms checked; Reduced parity formula.

\[a(n)=\begin{aligned}&\mathcal I_{2}^{(0)}(h)\,\mathcal I_{3}^{(0)}(h)\\[-1pt]&\quad\times \mathcal I_{2}^{(0)}(k)\,\mathcal I_{3}^{(0)}(k)\end{aligned}\]

### A202402

fixed width 6; Inherited; 8 terms checked; Reduced parity formula.

\[a(n)=\bigl(\mathcal I_{3}^{(0)}(h)\bigr)^{2}\,\bigl(\mathcal I_{3}^{(0)}(k)\bigr)^{2}\]

### A202403 *

fixed width 7; New vs v19; 8 terms checked; Reduced parity formula.

\[a(n)=\begin{aligned}&\mathcal I_{3}^{(0)}(h)\,\mathcal I_{4}^{(0)}(h)\\[-1pt]&\quad\times \mathcal I_{3}^{(0)}(k)\,\mathcal I_{4}^{(0)}(k)\end{aligned}\]

### A202404 *

fixed width 8; New vs v19; 8 terms checked; Reduced parity formula.

\[a(n)=\bigl(\mathcal I_{4}^{(0)}(h)\bigr)^{2}\,\bigl(\mathcal I_{4}^{(0)}(k)\bigr)^{2}\]

### A202405 *

fixed width 9; New vs v19; 8 terms checked; Reduced parity formula.

\[a(n)=\begin{aligned}&\mathcal I_{4}^{(0)}(h)\,\mathcal I_{5}^{(0)}(h)\\[-1pt]&\quad\times \mathcal I_{4}^{(0)}(k)\,\mathcal I_{5}^{(0)}(k)\end{aligned}\]

### A202406 *

antidiagonal; New vs v19; 8 terms checked; Reduced parity formula.

\[a(n)=\begin{aligned}&\mathcal I_{h_j}^{(0)}(h_i)\,\mathcal I_{k_j}^{(0)}(h_i)\\[-1pt]&\quad\times \mathcal I_{h_j}^{(0)}(k_i)\,\mathcal I_{k_j}^{(0)}(k_i)\end{aligned}\]

### A202413 *

square; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{n+2,3,1}\bigr)^{n}\mathbf1\]

### A202414

fixed width 3; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{3,3,1}\bigr)^{n}\mathbf1\]

### A202415

fixed width 4; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{4,3,1}\bigr)^{n}\mathbf1\]

### A202416 *

fixed width 5; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{5,3,1}\bigr)^{n}\mathbf1\]

### A202417 *

fixed width 6; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{6,3,1}\bigr)^{n}\mathbf1\]

### A202418 *

fixed width 7; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{7,3,1}\bigr)^{n}\mathbf1\]

### A202419 *

fixed width 8; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{8,3,1}\bigr)^{n}\mathbf1\]

### A202420 *

fixed width 9; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{9,3,1}\bigr)^{n}\mathbf1\]

### A202421 *

antidiagonal; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{j+2,3,1}\bigr)^{i}\mathbf1\]

### A202427 *

square; New vs v19; 8 terms checked; Boundary factorization.

\[a(n)=2F_{n+3}^2\,\mathcal I_{n+1}^{(1)}(n+1)\]

### A202428

fixed width 3; Inherited; 8 terms checked; Boundary factorization.

\[a(n)=6F_{n+3}\,\mathcal I_{2}^{(1)}(n+1)\]

### A202429

fixed width 4; Inherited; 8 terms checked; Boundary factorization.

\[a(n)=10F_{n+3}\,\mathcal I_{3}^{(1)}(n+1)\]

### A202430

fixed width 5; Inherited; 8 terms checked; Boundary factorization.

\[a(n)=16F_{n+3}\,\mathcal I_{4}^{(1)}(n+1)\]

### A202431

fixed width 6; Inherited; 8 terms checked; Boundary factorization.

\[a(n)=26F_{n+3}\,\mathcal I_{5}^{(1)}(n+1)\]

### A202432 *

fixed width 7; New vs v19; 8 terms checked; Boundary factorization.

\[a(n)=42F_{n+3}\,\mathcal I_{6}^{(1)}(n+1)\]

### A202433 *

fixed width 8; New vs v19; 8 terms checked; Boundary factorization.

\[a(n)=68F_{n+3}\,\mathcal I_{7}^{(1)}(n+1)\]

### A202434 *

fixed width 9; New vs v19; 8 terms checked; Boundary factorization.

\[a(n)=110F_{n+3}\,\mathcal I_{8}^{(1)}(n+1)\]

### A202435 *

antidiagonal; New vs v19; 8 terms checked; Boundary factorization.

\[a(n)=2F_{i+3}F_{j+3}\,\mathcal I_{j+1}^{(1)}(i+1)\]

### A202464

fixed width 3; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{3,3,2}\bigr)^{n}\mathbf1\]

### A202465 *

fixed width 4; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{4,3,2}\bigr)^{n}\mathbf1\]

### A202466 *

fixed width 5; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{5,3,2}\bigr)^{n}\mathbf1\]

### A202467 *

fixed width 6; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{6,3,2}\bigr)^{n}\mathbf1\]

### A202468 *

fixed width 7; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{7,3,2}\bigr)^{n}\mathbf1\]

### A202469 *

fixed width 8; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{8,3,2}\bigr)^{n}\mathbf1\]

### A202470 *

fixed width 9; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{9,3,2}\bigr)^{n}\mathbf1\]

### A202471 *

antidiagonal; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{j+2,3,2}\bigr)^{i}\mathbf1\]

### A202484 *

square; New vs v19; 8 terms checked; Reduced parity formula.

\[a(n)=\begin{aligned}&\mathcal I_{h}^{(1)}(h)\,\mathcal I_{k}^{(1)}(h)\\[-1pt]&\quad\times \mathcal I_{h}^{(1)}(k)\,\mathcal I_{k}^{(1)}(k)\end{aligned}\]

### A202485

fixed width 3; Inherited; 8 terms checked; Reduced parity formula.

\[a(n)=\begin{aligned}&\mathcal I_{1}^{(1)}(h)\,\mathcal I_{2}^{(1)}(h)\\[-1pt]&\quad\times \mathcal I_{1}^{(1)}(k)\,\mathcal I_{2}^{(1)}(k)\end{aligned}\]

### A202486

fixed width 4; Inherited; 8 terms checked; Reduced parity formula.

\[a(n)=\bigl(\mathcal I_{2}^{(1)}(h)\bigr)^{2}\,\bigl(\mathcal I_{2}^{(1)}(k)\bigr)^{2}\]

### A202487

fixed width 5; Inherited; 8 terms checked; Reduced parity formula.

\[a(n)=\begin{aligned}&\mathcal I_{2}^{(1)}(h)\,\mathcal I_{3}^{(1)}(h)\\[-1pt]&\quad\times \mathcal I_{2}^{(1)}(k)\,\mathcal I_{3}^{(1)}(k)\end{aligned}\]

### A202488

fixed width 6; Inherited; 8 terms checked; Reduced parity formula.

\[a(n)=\bigl(\mathcal I_{3}^{(1)}(h)\bigr)^{2}\,\bigl(\mathcal I_{3}^{(1)}(k)\bigr)^{2}\]

### A202489 *

fixed width 7; New vs v19; 8 terms checked; Reduced parity formula.

\[a(n)=\begin{aligned}&\mathcal I_{3}^{(1)}(h)\,\mathcal I_{4}^{(1)}(h)\\[-1pt]&\quad\times \mathcal I_{3}^{(1)}(k)\,\mathcal I_{4}^{(1)}(k)\end{aligned}\]

### A202490 *

fixed width 8; New vs v19; 8 terms checked; Reduced parity formula.

\[a(n)=\bigl(\mathcal I_{4}^{(1)}(h)\bigr)^{2}\,\bigl(\mathcal I_{4}^{(1)}(k)\bigr)^{2}\]

### A202491 *

fixed width 9; New vs v19; 8 terms checked; Reduced parity formula.

\[a(n)=\begin{aligned}&\mathcal I_{4}^{(1)}(h)\,\mathcal I_{5}^{(1)}(h)\\[-1pt]&\quad\times \mathcal I_{4}^{(1)}(k)\,\mathcal I_{5}^{(1)}(k)\end{aligned}\]

### A202492 *

antidiagonal; New vs v19; 8 terms checked; Reduced parity formula.

\[a(n)=\begin{aligned}&\mathcal I_{h_j}^{(1)}(h_i)\,\mathcal I_{k_j}^{(1)}(h_i)\\[-1pt]&\quad\times \mathcal I_{h_j}^{(1)}(k_i)\,\mathcal I_{k_j}^{(1)}(k_i)\end{aligned}\]

### A202567 *

fixed width 4; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{4,4,2}\bigr)^{n}\mathbf1\]

### A202568 *

fixed width 5; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{5,4,2}\bigr)^{n}\mathbf1\]

### A202569 *

fixed width 6; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{6,4,2}\bigr)^{n}\mathbf1\]

### A202583 *

square; New vs v19; 7 terms checked (partial retained prefix); Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{n+2}^{(1;001,100)}\bigr)^{n}\mathbf1\]

### A202584

fixed width 3; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{3}^{(1;001,100)}\bigr)^{n}\mathbf1\]

### A202585

fixed width 4; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{4}^{(1;001,100)}\bigr)^{n}\mathbf1\]

### A202586

fixed width 5; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{5}^{(1;001,100)}\bigr)^{n}\mathbf1\]

### A202587

fixed width 6; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{6}^{(1;001,100)}\bigr)^{n}\mathbf1\]

### A202588 *

fixed width 7; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{7}^{(1;001,100)}\bigr)^{n}\mathbf1\]

### A202589 *

fixed width 8; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{8}^{(1;001,100)}\bigr)^{n}\mathbf1\]

### A202590 *

fixed width 9; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{9}^{(1;001,100)}\bigr)^{n}\mathbf1\]

### A202591 *

antidiagonal; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{j+2}^{(1;001,100)}\bigr)^{i}\mathbf1\]

### A202594

fixed width 3; Inherited; 8 terms checked; Boundary factorization.

\[a(n)=6F_{n+3}\,\mathcal I_{2}^{(0)}(n+1)\]

### A202597

fixed width 6; Inherited; 8 terms checked; Boundary factorization.

\[a(n)=26F_{n+3}\,\mathcal I_{5}^{(0)}(n+1)\]

### A202598 *

fixed width 7; New vs v19; 8 terms checked; Boundary factorization.

\[a(n)=42F_{n+3}\,\mathcal I_{6}^{(0)}(n+1)\]

### A202599 *

fixed width 8; New vs v19; 8 terms checked; Boundary factorization.

\[a(n)=68F_{n+3}\,\mathcal I_{7}^{(0)}(n+1)\]

### A202600 *

fixed width 9; New vs v19; 8 terms checked; Boundary factorization.

\[a(n)=110F_{n+3}\,\mathcal I_{8}^{(0)}(n+1)\]

### A202601 *

antidiagonal; New vs v19; 8 terms checked; Boundary factorization.

\[a(n)=2F_{i+3}F_{j+3}\,\mathcal I_{j+1}^{(0)}(i+1)\]

### A202609

fixed width 3; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{3}^{(0;001,010)}\bigr)^{n}\mathbf1\]

### A202610

fixed width 4; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{4}^{(0;001,010)}\bigr)^{n}\mathbf1\]

### A202611

fixed width 5; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{5}^{(0;001,010)}\bigr)^{n}\mathbf1\]

### A202612

fixed width 6; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{6}^{(0;001,010)}\bigr)^{n}\mathbf1\]

### A202613 *

fixed width 7; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{7}^{(0;001,010)}\bigr)^{n}\mathbf1\]

### A202614 *

fixed width 8; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{8}^{(0;001,010)}\bigr)^{n}\mathbf1\]

### A202615 *

fixed width 9; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{9}^{(0;001,010)}\bigr)^{n}\mathbf1\]

### A202616 *

antidiagonal; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{j+2}^{(0;001,010)}\bigr)^{i}\mathbf1\]

### A202642

fixed width 5; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{5}^{(1;000,111)}\bigr)^{n}\mathbf1\]

### A202643

fixed width 6; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{6}^{(1;000,111)}\bigr)^{n}\mathbf1\]

### A202644 *

fixed width 7; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{7}^{(1;000,111)}\bigr)^{n}\mathbf1\]

### A202645 *

fixed width 8; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{8}^{(1;000,111)}\bigr)^{n}\mathbf1\]

### A202646 *

fixed width 9; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{9}^{(1;000,111)}\bigr)^{n}\mathbf1\]

### A202647 *

antidiagonal; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{j+2}^{(1;000,111)}\bigr)^{i}\mathbf1\]

### A202719 *

fixed width 4; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{4,4,3}\bigr)^{n}\mathbf1\]

### A202720 *

fixed width 5; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{5,4,3}\bigr)^{n}\mathbf1\]

### A202721 *

fixed width 6; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{6,4,3}\bigr)^{n}\mathbf1\]

### A202772

fixed width 5; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{5}^{(1;000,011)}\bigr)^{n}\mathbf1\]

### A202773

fixed width 6; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{6}^{(1;000,011)}\bigr)^{n}\mathbf1\]

### A202774 *

fixed width 7; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{7}^{(1;000,011)}\bigr)^{n}\mathbf1\]

### A202775 *

fixed width 8; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{8}^{(1;000,011)}\bigr)^{n}\mathbf1\]

### A202776 *

fixed width 9; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{9}^{(1;000,011)}\bigr)^{n}\mathbf1\]

### A202777 *

antidiagonal; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{j+2}^{(1;000,011)}\bigr)^{i}\mathbf1\]

### A202892

fixed width 4; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{4}^{(1;001,010)}\bigr)^{n}\mathbf1\]

### A202893

fixed width 5; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{5}^{(1;001,010)}\bigr)^{n}\mathbf1\]

### A202894

fixed width 6; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{6}^{(1;001,010)}\bigr)^{n}\mathbf1\]

### A202895 *

fixed width 7; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{7}^{(1;001,010)}\bigr)^{n}\mathbf1\]

### A202896 *

fixed width 8; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{8}^{(1;001,010)}\bigr)^{n}\mathbf1\]

### A202897 *

fixed width 9; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{9}^{(1;001,010)}\bigr)^{n}\mathbf1\]

### A202898 *

antidiagonal; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{j+2}^{(1;001,010)}\bigr)^{i}\mathbf1\]

### A203040 *

square; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{n+3,4,1}\bigr)^{n}\mathbf1\]

### A203041

fixed width 4; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{4,4,1}\bigr)^{n}\mathbf1\]

### A203042 *

fixed width 5; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{5,4,1}\bigr)^{n}\mathbf1\]

### A203043 *

fixed width 6; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{6,4,1}\bigr)^{n}\mathbf1\]

### A203044 *

fixed width 7; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{7,4,1}\bigr)^{n}\mathbf1\]

### A203047 *

fixed width 10; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal C_{10,4,1}\bigr)^{n}\mathbf1\]

### A203086

fixed width 5; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{5}^{(0;000,101)}\bigr)^{n}\mathbf1\]

### A203087

fixed width 6; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{6}^{(0;000,101)}\bigr)^{n}\mathbf1\]

### A203088 *

fixed width 7; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{7}^{(0;000,101)}\bigr)^{n}\mathbf1\]

### A203089 *

fixed width 8; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{8}^{(0;000,101)}\bigr)^{n}\mathbf1\]

### A203090 *

fixed width 9; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{9}^{(0;000,101)}\bigr)^{n}\mathbf1\]

### A203091 *

antidiagonal; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{j+2}^{(0;000,101)}\bigr)^{i}\mathbf1\]

### A203349

fixed width 4; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{4}^{(1;010,101)}\bigr)^{n}\mathbf1\]

### A203350

fixed width 5; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{5}^{(1;010,101)}\bigr)^{n}\mathbf1\]

### A203351

fixed width 6; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{6}^{(1;010,101)}\bigr)^{n}\mathbf1\]

### A203352 *

fixed width 7; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{7}^{(1;010,101)}\bigr)^{n}\mathbf1\]

### A203353 *

fixed width 8; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{8}^{(1;010,101)}\bigr)^{n}\mathbf1\]

### A203354 *

fixed width 9; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{9}^{(1;010,101)}\bigr)^{n}\mathbf1\]

### A203355 *

antidiagonal; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{j+2}^{(1;010,101)}\bigr)^{i}\mathbf1\]

### A203402

fixed width 5; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{5}^{(0;000,111)}\bigr)^{n}\mathbf1\]

### A203403

fixed width 6; Inherited; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{6}^{(0;000,111)}\bigr)^{n}\mathbf1\]

### A203404 *

fixed width 7; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{7}^{(0;000,111)}\bigr)^{n}\mathbf1\]

### A203405 *

fixed width 8; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{8}^{(0;000,111)}\bigr)^{n}\mathbf1\]

### A203406 *

fixed width 9; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{9}^{(0;000,111)}\bigr)^{n}\mathbf1\]

### A203407 *

antidiagonal; New vs v19; 8 terms checked; Finite-state transfer.

\[a(n)=\mathbf1^T\bigl(\mathcal A_{j+2}^{(0;000,111)}\bigr)^{i}\mathbf1\]

## Appendix: explicit strip polynomials

Coefficients in ascending powers of z. Each numerator and denominator is explicitly specified by its complete integer coefficient list.

### d=0, w=1
P: `[1, 1]`
Q: `[1, -1, -1]`

### d=0, w=2
P: `[1, 1]`
Q: `[1, -2, -1]`

### d=0, w=3
P: `[1, 3, 1, -1]`
Q: `[1, -2, -6, 0, 1]`

### d=0, w=4
P: `[1, 4, 0, -4, 1]`
Q: `[1, -4, -9, 5, 4, -1]`

### d=0, w=5
P: `[1, 9, 11, -37, -24, 53, -15, -3, 1]`
Q: `[1, -4, -36, 0, 105, -15, -64, 20, 4, -1]`

### d=0, w=6
P: `[1, 13, 9, -137, -10, 368, -252, -15, 39, -3, -1]`
Q: `[1, -8, -62, 78, 375, -300, -486, 385, 30, -52, 2, 1]`

### d=0, w=7
P: `[1, 25, 68, -988, -1607, 16419, -5655, -87821, 131924, 38447, -181170, 57827, 75440, -37529, -13435, 7403, 1227, -518, -68, 9, 1]`
Q: `[1, -9, -203, 210, 5659, -6975, -48558, 82823, 127405, -308107, -21372, 340142, -100779, -139011, 54187, 25564, -9369, -2227, 546, 87, -9, -1]`

### d=0, w=8
P: `[1, 34, -69, -3680, 11250, 115424, -589200, -383600, 7324276, -12709710, -10338228, 46744413, -15995666, -63310147, 46773404, 43551682, -43244487, -17693860, 20228703, 4921024, -5163970, -1026276, 696368, 141170, -42654, -9508, 810, 211, -2, -1]`
Q: `[1, -21, -307, 2897, 14496, -143966, -69560, 2521758, -3420900, -14955414, 38553144, 14453733, -112214391, 38309781, 146183839, -89116906, -104112201, 74808697, 45050815, -31698675, -12536716, 7157982, 2231568, -837464, -232636, 45650, 12188, -855, -237, 3, 1]`

### d=0, w=9
P: `[1, 68, 362, -21774, -71960, 3073650, -2176298, -189454909, 695162126, 4109827910, -27269876999, -8893434356, 366882675476, -455498470953, -2351867077296, 5134807514514, 8329482679416, -26890418277749, -17376218450692, 85846736935076, 22136009758910, -184230631788252, -20274363796888, 277741924735811, 24253450247920, -298373869039940, -39452927701636, 226929233392823, 47510243148508, -119556782665954, -35700712420552, 42148804233668, 16627418754556, -9443571523947, -4806125712972, 1232811789602, 855068519680, -75588878411, -92662160860, -447546064, 6041486617, 334757312, -233547314, -18535385, 5207700, 434974, -63778, -4434, 398, 16, -1]`
Q: `[1, -21, -1132, 5920, 244380, -1259724, -19673778, 127632485, 612853063, -5597130430, -4977066279, 116262875259, -94043978188, -1228760396865, 2092683698219, 7283723918850, -17153391287480, -26617967095223, 79200771180203, 65552289065868, -233868746956342, -120623143251024, 467984535433410, 184070347186175, -650939587415509, -240265022872528, 632623890480118, 250766015181179, -425984963276799, -191883928876524, 195140774531710, 101914774321228, -59051676182704, -36502573934307, 11222413648753, 8650516718822, -1199642863344, -1332705463117, 45820109401, 130934303308, 3705746789, -8025512259, -502848618, 299141021, 22912829, -6517908, -484764, 77676, 4524, -454, -15, 1]`

### d=1, w=1
P: `[1, 1]`
Q: `[1, -1, -1]`

### d=1, w=2
P: `[1, 2, 1]`
Q: `[1, -1, -2, -1]`

### d=1, w=3
P: `[1, 4, 3, 0, -1]`
Q: `[1, -1, -5, -4, 0, 1]`

### d=1, w=4
P: `[1, 7, 10, 3, -6, -1, 3, -1]`
Q: `[1, -1, -10, -15, -4, 6, 1, -3, 1]`

### d=1, w=5
P: `[1, 12, 26, 6, -56, -27, 49, 21, -55, 34, -7, -2, 1]`
Q: `[1, -1, -21, -48, -14, 69, 38, -68, -13, 57, -37, 8, 2, -1]`

### d=1, w=6
P: `[1, 20, 66, 22, -330, -279, 738, 883, -2436, 507, 3461, -5128, 3419, -941, -190, 158, 33, -29, -6, 3, 1]`
Q: `[1, -1, -42, -147, -70, 478, 449, -1199, -732, 2727, -659, -3827, 5776, -3926, 1152, 148, -154, -32, 29, 6, -3, -1]`

### d=1, w=7
P: `[1, 33, 158, 7, -2126, -2608, 12161, 22507, -86923, -5865, 279442, -165515, -973487, 2659019, -3303195, 1990177, 188994, -1302856, 819673, 88109, -334790, 71780, 84554, -25694, -21404, 2690, 5205, 1166, -613, -538, -167, -13, 5, 1]`
Q: `[1, -1, -85, -432, -192, 3711, 5096, -21164, -27340, 112654, 37244, -477721, 464722, 897815, -3102284, 4149918, -2761082, 138325, 1353257, -942033, -64683, 365483, -80904, -92350, 27097, 23292, -2585, -5635, -1405, 561, 545, 173, 14, -5, -1]`

### d=1, w=8
P: `[1, 54, 370, -176, -12054, -19392, 165168, 423027, -2396858, -1725123, 18206974, 18440240, -264605165, 579128387, 233111349, -4183542851, 11302361177, -16291050385, 10937902079, 5536133605, -19514068594, 14576571706, 5863866841, -17263460312, 5368128503, 11431057964, -8646060777, -5962173712, 7397348672, 3170657730, -4968238783, -2231408527, 2716131027, 1911213447, -892203881, -1360206128, -236356230, 472581407, 380257091, 60725960, -103100738, -105547379, -56356440, -19303230, -3859220, -161699, 96878, -2410, -10222, -674, 609, 45, -30, -1, 1]`
Q: `[1, -1, -170, -1243, -452, 25328, 47829, -329977, -677669, 3899000, 4142351, -40598266, 22625542, 280040412, -733571937, -225285263, 5406913431, -15244941445, 23143116063, -18064627845, -2246759550, 21472294755, -18258761486, -5172378119, 19704882159, -6931675953, -12628340471, 10036097232, 6485990080, -8290578844, -3493944338, 5396581563, 2482388885, -2807416030, -2023351213, 877760575, 1366907685, 211758176, -511379314, -405881894, -67901250, 105839886, 110007288, 59224072, 20510652, 4214944, 234085, -87637, 2782, 10138, 671, -608, -45, 30, 1, -1]`

### d=1, w=9
P: `[1, 88, 848, -1511, -67308, -131180, 2202936, 7633106, -66718866, -128162253, 1344965125, 2872271032, -44337314475, 116762452685, 152625086329, -1365132369538, -252943272128, 27035433847738, -130141745080780, 336158601172596, -472565415627347, 31913686275711, 1400655259679236, -2902731893658072, 1640318448162860, 4094750144980504, -9129949657981726, 2779486462940290, 14630734942892659, -18881643365026842, -10371963145112143, 39273952525803303, -6305113848792967, -58676629458269669, 31979069502025595, 77019720231545852, -59780862569813515, -100164391441090647, 80360551579253640, 135881690216901373, -79745141543090175, -186303268648785773, 37113655627570391, 236377988927385007, 72419055217556641, -230595273627928331, -241044830903833651, 61787582436904109, 306038665965612275, 230639599039546766, -48389009700178278, -242571905788862639, -206542302852163778, -18848076897189873, 157095121368991061, 224233012879237103, 189596184668486524, 112967905339832738, 46335910241298612, 9315571708058138, -3173361834257272, -3744961955501699, -1574513709890844, -209881504281434, 133163189331475, 81032419681489, 11522585136525, -5960981518203, -2747058752500, 38253145152, 269433089272, 30245809541, -20170669223, -3367492987, 1446545714, 180823131, -108295504, 2026841, 6596206, -1506328, -55989, 133948, -38165, -228, 2877, -686, 37, 8, -1]`
Q: `[1, -1, -341, -3520, 334, 171909, 417526, -5083216, -15283855, 130485447, 272892045, -3049905478, -511179629, 55957856060, -124488945147, -538626934150, 3500468879427, -4478480115950, -29496433268727, 182611451591524, -524306069845407, 852626156042858, -440208193462827, -1464924827758540, 3885196495123007, -2982940342312306, -4230674222649921, 11825337408157360, -5401968255267581, -16816567234540602, 24983151120411597, 9585671646760248, -48126804293022820, 11682212847079777, 69385711314076868, -42509085580493654, -89871633733075620, 75307132119610574, 117589053059603490, -99278700466055506, -162855432975425412, 95541176582994872, 226961599933750196, -34278410467657420, -280799538989855391, -106868457992460011, 247136946296363469, 282871338108355230, -44674358779740500, -324196672203238169, -249495641012276252, 64768558699537498, 296803477374187509, 272395901288262463, 67831170531569559, -136563731814790740, -226356673050150368, -201657150023555253, -124871036042872432, -53901370391664446, -12735538772455692, 2148662678861166, 3630394365861038, 1638150531308210, 246442107448472, -127482845730036, -82879141747172, -12381088034848, 6019979527395, 2847346843155, -30990252773, -278159240994, -31494932814, 20838665195, 3457565706, -1496929050, -181278765, 111939979, -2570071, -6700528, 1571198, 43847, -136254, 39914, -105, -2879, 695, -38, -8, 1]`

## Verification
All 168 IDs reconciled; 101 new relative to v19; 408 independent structural source checks; 1190 exact rational strip coefficient checks. Full-prefix matrix replays for general models were not newly performed. OEIS source commit `c5bd71de9eee0894df1301baa4f43f6431d8a08d`; OEIS Foundation Inc., CC BY-SA 4.0. No new corpus coverage claimed.
