# OEIS graph realization formula catalog
Author: Komorebi P.

## Scope
This graph-focused supplement collects 64 distinct already-bound OEIS IDs: 33 reduced independence-graph formulas, 15 sliding-window independent-set formulas, four direct walk sequences, two connected labeled-graph parity sequences, and ten rooted-tree sequences. The 48 array entries are part of the existing 168-array catalog. The other 16 are inherited v19 bindings, not new corpus admissions. Every formula refers to the stated mathematical model; OEIS identification retains the finite-check evidence of the source archive. The tree formulas are formal power-series formulas, not elementary closed forms.

## 1. Definitions for the reduced graph formulas

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


## 2. Square-grid and triangular-grid parity formulas

### A202398

\[a(n)=\begin{aligned}&\mathcal I_{h}^{(0)}(h)\,\mathcal I_{k}^{(0)}(h)\\[-1pt]&\quad\times \mathcal I_{h}^{(0)}(k)\,\mathcal I_{k}^{(0)}(k)\end{aligned}\]

square; New vs v19; 8 terms checked.

### A202399

\[a(n)=\begin{aligned}&\mathcal I_{1}^{(0)}(h)\,\mathcal I_{2}^{(0)}(h)\\[-1pt]&\quad\times \mathcal I_{1}^{(0)}(k)\,\mathcal I_{2}^{(0)}(k)\end{aligned}\]

fixed width 3; Inherited; 8 terms checked.

### A202400

\[a(n)=\bigl(\mathcal I_{2}^{(0)}(h)\bigr)^{2}\,\bigl(\mathcal I_{2}^{(0)}(k)\bigr)^{2}\]

fixed width 4; Inherited; 8 terms checked.

### A202401

\[a(n)=\begin{aligned}&\mathcal I_{2}^{(0)}(h)\,\mathcal I_{3}^{(0)}(h)\\[-1pt]&\quad\times \mathcal I_{2}^{(0)}(k)\,\mathcal I_{3}^{(0)}(k)\end{aligned}\]

fixed width 5; Inherited; 8 terms checked.

### A202402

\[a(n)=\bigl(\mathcal I_{3}^{(0)}(h)\bigr)^{2}\,\bigl(\mathcal I_{3}^{(0)}(k)\bigr)^{2}\]

fixed width 6; Inherited; 8 terms checked.

### A202403

\[a(n)=\begin{aligned}&\mathcal I_{3}^{(0)}(h)\,\mathcal I_{4}^{(0)}(h)\\[-1pt]&\quad\times \mathcal I_{3}^{(0)}(k)\,\mathcal I_{4}^{(0)}(k)\end{aligned}\]

fixed width 7; New vs v19; 8 terms checked.

### A202404

\[a(n)=\bigl(\mathcal I_{4}^{(0)}(h)\bigr)^{2}\,\bigl(\mathcal I_{4}^{(0)}(k)\bigr)^{2}\]

fixed width 8; New vs v19; 8 terms checked.

### A202405

\[a(n)=\begin{aligned}&\mathcal I_{4}^{(0)}(h)\,\mathcal I_{5}^{(0)}(h)\\[-1pt]&\quad\times \mathcal I_{4}^{(0)}(k)\,\mathcal I_{5}^{(0)}(k)\end{aligned}\]

fixed width 9; New vs v19; 8 terms checked.

### A202406

\[a(n)=\begin{aligned}&\mathcal I_{h_j}^{(0)}(h_i)\,\mathcal I_{k_j}^{(0)}(h_i)\\[-1pt]&\quad\times \mathcal I_{h_j}^{(0)}(k_i)\,\mathcal I_{k_j}^{(0)}(k_i)\end{aligned}\]

antidiagonal; New vs v19; 8 terms checked.

### A202484

\[a(n)=\begin{aligned}&\mathcal I_{h}^{(1)}(h)\,\mathcal I_{k}^{(1)}(h)\\[-1pt]&\quad\times \mathcal I_{h}^{(1)}(k)\,\mathcal I_{k}^{(1)}(k)\end{aligned}\]

square; New vs v19; 8 terms checked.

### A202485

\[a(n)=\begin{aligned}&\mathcal I_{1}^{(1)}(h)\,\mathcal I_{2}^{(1)}(h)\\[-1pt]&\quad\times \mathcal I_{1}^{(1)}(k)\,\mathcal I_{2}^{(1)}(k)\end{aligned}\]

fixed width 3; Inherited; 8 terms checked.

### A202486

\[a(n)=\bigl(\mathcal I_{2}^{(1)}(h)\bigr)^{2}\,\bigl(\mathcal I_{2}^{(1)}(k)\bigr)^{2}\]

fixed width 4; Inherited; 8 terms checked.

### A202487

\[a(n)=\begin{aligned}&\mathcal I_{2}^{(1)}(h)\,\mathcal I_{3}^{(1)}(h)\\[-1pt]&\quad\times \mathcal I_{2}^{(1)}(k)\,\mathcal I_{3}^{(1)}(k)\end{aligned}\]

fixed width 5; Inherited; 8 terms checked.

### A202488

\[a(n)=\bigl(\mathcal I_{3}^{(1)}(h)\bigr)^{2}\,\bigl(\mathcal I_{3}^{(1)}(k)\bigr)^{2}\]

fixed width 6; Inherited; 8 terms checked.

### A202489

\[a(n)=\begin{aligned}&\mathcal I_{3}^{(1)}(h)\,\mathcal I_{4}^{(1)}(h)\\[-1pt]&\quad\times \mathcal I_{3}^{(1)}(k)\,\mathcal I_{4}^{(1)}(k)\end{aligned}\]

fixed width 7; New vs v19; 8 terms checked.

### A202490

\[a(n)=\bigl(\mathcal I_{4}^{(1)}(h)\bigr)^{2}\,\bigl(\mathcal I_{4}^{(1)}(k)\bigr)^{2}\]

fixed width 8; New vs v19; 8 terms checked.

### A202491

\[a(n)=\begin{aligned}&\mathcal I_{4}^{(1)}(h)\,\mathcal I_{5}^{(1)}(h)\\[-1pt]&\quad\times \mathcal I_{4}^{(1)}(k)\,\mathcal I_{5}^{(1)}(k)\end{aligned}\]

fixed width 9; New vs v19; 8 terms checked.

### A202492

\[a(n)=\begin{aligned}&\mathcal I_{h_j}^{(1)}(h_i)\,\mathcal I_{k_j}^{(1)}(h_i)\\[-1pt]&\quad\times \mathcal I_{h_j}^{(1)}(k_i)\,\mathcal I_{k_j}^{(1)}(k_i)\end{aligned}\]

antidiagonal; New vs v19; 8 terms checked.

## 3. Boundary-factorized independent-set formulas

### A202427

\[a(n)=2F_{n+3}^2\,\mathcal I_{n+1}^{(1)}(n+1)\]

square; New vs v19; 8 terms checked.

### A202428

\[a(n)=6F_{n+3}\,\mathcal I_{2}^{(1)}(n+1)\]

fixed width 3; Inherited; 8 terms checked.

### A202429

\[a(n)=10F_{n+3}\,\mathcal I_{3}^{(1)}(n+1)\]

fixed width 4; Inherited; 8 terms checked.

### A202430

\[a(n)=16F_{n+3}\,\mathcal I_{4}^{(1)}(n+1)\]

fixed width 5; Inherited; 8 terms checked.

### A202431

\[a(n)=26F_{n+3}\,\mathcal I_{5}^{(1)}(n+1)\]

fixed width 6; Inherited; 8 terms checked.

### A202432

\[a(n)=42F_{n+3}\,\mathcal I_{6}^{(1)}(n+1)\]

fixed width 7; New vs v19; 8 terms checked.

### A202433

\[a(n)=68F_{n+3}\,\mathcal I_{7}^{(1)}(n+1)\]

fixed width 8; New vs v19; 8 terms checked.

### A202434

\[a(n)=110F_{n+3}\,\mathcal I_{8}^{(1)}(n+1)\]

fixed width 9; New vs v19; 8 terms checked.

### A202435

\[a(n)=2F_{i+3}F_{j+3}\,\mathcal I_{j+1}^{(1)}(i+1)\]

antidiagonal; New vs v19; 8 terms checked.

### A202594

\[a(n)=6F_{n+3}\,\mathcal I_{2}^{(0)}(n+1)\]

fixed width 3; Inherited; 8 terms checked.

### A202597

\[a(n)=26F_{n+3}\,\mathcal I_{5}^{(0)}(n+1)\]

fixed width 6; Inherited; 8 terms checked.

### A202598

\[a(n)=42F_{n+3}\,\mathcal I_{6}^{(0)}(n+1)\]

fixed width 7; New vs v19; 8 terms checked.

### A202599

\[a(n)=68F_{n+3}\,\mathcal I_{7}^{(0)}(n+1)\]

fixed width 8; New vs v19; 8 terms checked.

### A202600

\[a(n)=110F_{n+3}\,\mathcal I_{8}^{(0)}(n+1)\]

fixed width 9; New vs v19; 8 terms checked.

### A202601

\[a(n)=2F_{i+3}F_{j+3}\,\mathcal I_{j+1}^{(0)}(i+1)\]

antidiagonal; New vs v19; 8 terms checked.

## 4. Sliding-window independent-set formulas
For rectangles with both dimensions at least $R+1$, define $J_R(H,W)$ by joining cells in the same row or column at distance between 1 and $R$. The constraint of at most one 1 in every complete length-$(R+1)$ window is equivalent to choosing an independent set in this graph: every such pair is contained in a complete window, and any violating window contains such a pair. Let
\[
S_{W,R}=\{a:0\le a<2^W,\ a\mathbin{\&}(2^j a)=0\ (1\le j\le R)\}.
\]
The integer adjacency $A_{W,R}$ has states $(a_1,\ldots,a_R)\in S_{W,R}^R$. Its entry to $(a_2,\ldots,a_R,b)$ is 1 if $b\mathbin{\&}a_j=0$ for all $j$, and 0 otherwise. Start at the all-zero tuple, and sum all terminal states. Then
\[
J_R(H,W)=e_{0}^{T}A_{W,R}^{H}\mathbf1.
\]
This explicit matrix expression, or the determinant formula below, works at every displayed index. No small-matrix or elementary-form claim is made for growing widths.

### A202413

\[a(n)=J_{2}(n+2,n+2)\]

### A202414

\[a(n)=J_{2}(n+2,3)\]

### A202415

\[a(n)=J_{2}(n+2,4)\]

### A202416

\[a(n)=J_{2}(n+2,5)\]

### A202417

\[a(n)=J_{2}(n+2,6)\]

### A202418

\[a(n)=J_{2}(n+2,7)\]

### A202419

\[a(n)=J_{2}(n+2,8)\]

### A202420

\[a(n)=J_{2}(n+2,9)\]

### A202421

\[a(n)=J_{2}(i+2,j+2)\]

### A203040

\[a(n)=J_{3}(n+3,n+3)\]

### A203041

\[a(n)=J_{3}(n+3,4)\]

### A203042

\[a(n)=J_{3}(n+3,5)\]

### A203043

\[a(n)=J_{3}(n+3,6)\]

### A203044

\[a(n)=J_{3}(n+3,7)\]

### A203047

\[a(n)=J_{3}(n+3,10)\]

## 5. All four direct graph walks
Let $C(n)=\sum_{0\le j\le n,\ 2j\equiv n\pmod9}\binom nj$, and $L_m=((1+\sqrt5)/2)^m+((1-\sqrt5)/2)^m$.

### A094233

\[a(n)=\sum_{0\le j\le n,\ 2j\equiv n\pmod9}\binom nj\]

Valid for $n\ge 0$.

### A005023

\[a(n)=(C(2n+9)-4C(2n+7))/2\]

Valid for $n\ge 1$.

### A095933

\[a(n)=2(4^n-L_{2n+1})/5\]

Valid for $n\ge 2$.

### A226493

\[a(n)=3^n+3(-1)^n\]

Valid for $n\ge 1$.

The A005023 formula follows from reflection of path walks into a doubled cycle, then the odd-cycle covering map, as in the v25 proof. The A095933 formula also gives $a(n+1)-4a(n)=2F_{2n}$. A226493 uses the total trace, not the count at a single vertex.

## 6. Connected labeled graphs with edge parity
Define
\[
G(x)=\sum_{j\ge0}2^{\binom j2}\frac{x^j}{j!},\qquad C_n=n![x^n]\log G(x).
\]
These are formal series. $C_n$ counts connected simple labeled graphs on $n$ vertices. Weight each graph by $(-1)^{\#\text{edges}}$. The unrestricted signed count is $(1-1)^{\binom n2}$, so its exponential generating function is $1+x$. Its connected signed coefficient is $(-1)^{n-1}(n-1)!$. Taking the two parity projections proves the following.

### A054939
\[a(n)=\frac{n![x^n]\log G(x)+(-1)^{n-1}(n-1)!}{2}\]

### A054940
\[a(n)=\frac{n![x^n]\log G(x)-(-1)^{n-1}(n-1)!}{2}\]
Both offsets are 1. The coefficient can alternatively be computed from a finite expression: replace $G$ by its degree-$n$ truncation, and use $\log(1+u)=\sum_{j=1}^n(-1)^{j-1}u^j/j$ through degree $n$.

## 7. Unlabeled rooted trees by leaf count
Use the formal power series $T(x,y)$ with zero constant term satisfying
\[
T(x,y)=x\left(y-1+\exp\left(\sum_{j\ge1}\frac{T(x^j,y^j)}{j}\right)\right).
\]
The exponential represents an unordered multiset of rooted children; the empty multiset is replaced by leaf weight $y$. A degree-$n$ coefficient requires only $j\le n$ and $n$ substitutions of this right-hand side starting from $T=0$. Thus the following are exact finite coefficient constructions. Their OEIS bindings retain the v19 nonplane-unlabeled interpretation and 16 finite checks each.

### A055278

\[a(n)=[x^n y^3]T(x,y)\]

Offset 4.

### A055279

\[a(n)=[x^n y^4]T(x,y)\]

Offset 5.

### A055280

\[a(n)=[x^n y^5]T(x,y)\]

Offset 6.

### A055281

\[a(n)=[x^n y^6]T(x,y)\]

Offset 7.

### A055282

\[a(n)=[x^n y^7]T(x,y)\]

Offset 8.

### A055283

\[a(n)=[x^n y^8]T(x,y)\]

Offset 9.

### A055284

\[a(n)=[x^n y^9]T(x,y)\]

Offset 10.

### A055285

\[a(n)=[x^n y^10]T(x,y)\]

Offset 11.

### A055286

\[a(n)=[x^n y^11]T(x,y)\]

Offset 12.

### A055287

\[a(n)=[x^n y^12]T(x,y)\]

Offset 13.

## 8. Exact integer evaluation and all explicit strip polynomials
### Direct integer evaluation
For any $\mathbf u^T A^m\mathbf v$ in this catalog, including the independent-set factors, let $g(z)=\mathbf u^T(I-zA)^{-1}\mathbf v$. Choose an integer $c\ge1$ bounding the row sums of $A$, and $a\ge1$ bounding $\|\mathbf u\|_1\|\mathbf v\|_\infty$. With $B=2ac^{m+1}+1$, the exact integer is
\[\left\lfloor\frac{B^{m+1}\mathbf u^T\operatorname{adj}(BI-A)\mathbf v}{\det(BI-A)}\right\rfloor\bmod B.\]
For the all-ones vectors, take $a$ equal to the state count. For A and C take $c=2^w$; for B take $c=b^w$; for I take $a=1,c=2^w$. The bound on the tail of $B^m g(1/B)$ is $ac^{m+1}/(B(1-c/B))<1$, so this is exact. It is not a claim of computational speed or small matrix size. Square arrays and flattened tables have width depending on the index; the matrix construction remains exact but does not imply a fixed-order scalar recurrence.

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


## Verification and boundaries
Fresh checks: 64 direct walk terms; 32 connected graph parity terms; 30 sliding-window terms by an independent graph-history evaluator. The 33 reduced array expressions and their rational polynomial data are copied from the existing audited 168-entry catalog; the 10 rooted-tree bindings retain the v19 checks, not a fresh tree replay. The existing source catalog and v30 archive remain unchanged. All 64 IDs are previously bound; there is no new corpus scan, Lean proof, or originality claim. The rest of the 168 array models use exact transfer-graph constructions in the complete original catalog. The graph realizations are not necessarily minimum-size or faster to evaluate. Source attribution: OEIS Foundation Inc., CC BY-SA 4.0, retained source receipts and pinned array revision c5bd71de9eee0894df1301baa4f43f6431d8a08d.
