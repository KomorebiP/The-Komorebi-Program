# Complete fixed-width rational span and formal-series boundary

Author: Komorebi P.

## Scope and final inventories

This continuation preserves the 537-record publication inventory, the original source catalogues and the earlier exact spanning identities. It distinguishes three claims:

1. All 506 graph/tree, fixed-width array and direct-walk records have rational ordinary generating functions, including 18 compact finite-state realizations whose scalar denominator expansions remain deferred. Their constant rational linear span has exact dimension 241.
2. Every one of the other 31 retained sequence definitions has a nonrational ordinary generating function. This is a classification of individual series, not a claim that their linear combinations cannot be rational.
3. Eleven of these 31 nonrational functions are jointly independent modulo the 506-record rational span. Thus the 517-record represented subcollection has exact rational linear rank 252, and the full 537-record span has rank between 252 and 272 inclusive. The remaining 20 formal-series dependence questions are open.

All arrays and direct walks have zeros padded before their retained original offsets. Rational linear combinations use constant coefficients in Q, not coefficients in Q(x). No new OEIS bindings, formal Lean certification, or literature-priority claims are made.

## 1. Compact rational realizations and exact finite-field certificates

For a fixed width w, the row-history graph is finite, regardless of the height n. Its adjacency M yields the count a(n)=1^T M^n 1 for n>=1, with the appropriate initial history length. Therefore the padded generating function is

    F(x) = 1^T (I-xM)^(-1) 1 - 1^T 1.

This is an exact all-index representation even if the characteristic polynomial is too large to expand. It does not assert that the state dimension is the minimal eventual scalar recurrence order.

For the three deferred binary models A202469, A202470 and A202721, the forbidden word is the all-one word of length L. For a suffix h of L-2 rows, write S for their bitwise intersection. A transition from the history (a,h) to (h,b) is admissible precisely when a & S & b = 0, provided every row is horizontally admissible. For each suffix, form a histogram f_h(t) of the weights of predecessor rows a grouped by t=a&S. The new weight at (h,b) equals the subset sum of f_h(t) over t contained in S without the bits of b. The standard subset-zeta recurrence computes these subset sums using only addition. It is an exact rearrangement of the row-history transfer, valid over integers and finite fields alike.

The remaining eleven binary models use the exact sparse equitable quotient of the predecessor. For both methods the 256-coefficient residues at primes 1000003 and 1000033 were computed directly from the finite-state constructions. All fourteen extra functions are jointly independent with the preceding 223 basis functions: the rank is 237 over both fields, with largest pivot index 236. A nonzero finite coefficient minor modulo a prime is a nonzero integer minor, proving rational independence. All predecessor spanning identities and the fourteen identity rows prove the matching upper bound. A duplicated basis-vector control is rejected.

Verification: 27 independent exact array comparisons, one resource-budget skip, eleven exact original-edge/quotient first-moment identities, and 3713 exact subset-zeta controls. No scalar minimality claims are made for these fourteen models.

## 2. Perron separation for the last four quaternary strips

Let M_w be the symmetric compatibility matrix on rows in {0,1,2,3}^w, with an edge precisely when all adjacent 2x2 block sums are at least 7. Here w>=2. A row is active exactly when each adjacent pair of its entries has sum at least 1: otherwise no neighboring row can make that block reach 7; conversely the all-3 row is compatible with every active row. The active submatrix is irreducible and has a loop at the all-3 row, hence primitive. The remaining rows are isolated. Thus for n>=1 the count has asymptotic c_w lambda_w^n with c_w>0 and lambda_w the Perron root.

Append the digit 3 to an active width-w row. This identifies its active submatrix with a principal submatrix of the active width-(w+1) matrix. Indeed an old compatible pair has final vertical sum at least 1, because its previous vertical sum is at most 6. The appended vertical sum 6 therefore satisfies the last block condition. If a pair was incompatible, its old failed constraint remains failed. The image is a proper subset (for example the all-2 row is active and not in the image). Strict Perron monotonicity for a proper principal submatrix of an irreducible nonnegative matrix gives lambda_(w+1)>lambda_w.

At width 6, write b_n=1^T M_6^n 1. Symmetry implies b_4/b_2=||M_6^2 1||^2/||M_6 1||^2 <= lambda_6^2. Transposing the 3x6 and 5x6 rectangles permits the following exact counts at widths 3 and 5:

    b_2 = 601469417
    b_4 = 208292231201647
    b_4 - 512^2 b_2 = 50620632351599 > 0.

Hence lambda_6>512. The 131 binary fixed-width array formulas have exponential growth rate at most 512: the direct finite-state models have at most 512 horizontally admissible rows; for the reduced formulas, fixed-lower-argument binomials give polynomial factors, F_m<=2^m, and I_w(m)<=2^(wm), yielding at most 2^9 per index. These bounds are checked against the retained model descriptors. The graph/tree core has polynomial growth from cyclotomic denominators; the walk counts have exponential rate at most 4. The earlier quaternary widths 2 through 5 have strictly smaller Perron roots than width 6.

Consequently A184213 through A184216 (widths 6 through 9) are jointly independent modulo the previous span: in any nonzero combination of them, the term with largest width dominates all smaller-width and predecessor terms. This argument does not need their explicit large matrices or expanded characteristic polynomials. The all-index finite-state realizations prove rationality. Combined with the preceding 502-record rank-237 certificate this yields the complete 506 x 241 rational transfer matrix. Finite controls: 336 active-row predicates and 69888 compatibility/embedding predicates. Those checks illustrate the general proof; they are not its justification.

## 3. Rational-series obstruction lemmas

### 3.1 Asymptotic power

An eventually recurrent rational-series coefficient sequence is a finite sum of exponential-polynomial terms P_j(n) lambda_j^n with distinct nonzero lambda_j (plus a finite prefix). A nonzero sequence with a_n ~ C R^n n^alpha, C != 0 and R>0, must have alpha a nonnegative integer. Indeed the dominant root modulus is R by the limsup nth-root formula. If k is the highest polynomial degree at that modulus, the normalized leading term is a finite trigonometric sum with nonzero Cesaro mean square. It is bounded and does not tend to zero. Hence alpha=k. The same assertion applies to an even-index subsequence, since taking every second term of a rational coefficient sequence again gives a rational coefficient sequence.

A superexponential subsequence is another direct obstruction: rational-series coefficients are exponentially bounded up to a polynomial factor.

### 3.2 Antidiagonal boundary-block lemma

For a rational coefficient sequence, fix an eventual recurrence whose trailing coefficient is nonzero, deleting any finite prefix associated with zero characteristic roots. Its companion evolution on d consecutive values is invertible. Suppose there are arbitrarily late blocks of d consecutive values all of size exp(o(n)) at starting index n. Project the recurrence state onto the generalized eigenspaces of modulus >1. Applying the inverse evolution on that unstable space bounds the initial projection by a polynomial factor times an exponentially decaying factor times the subexponential block norm. Taking the block starts to infinity forces this projection to vanish. Thus every nonzero contributing characteristic root has modulus <=1 and the entire sequence is polynomially bounded. The finite-support case is already polynomially bounded.

In the retained antidiagonal indexing n=l(l-1)/2+i, j=l+1-i, the first d entries of each sufficiently large diagonal have bounded i and j=O(sqrt(n)). For every one of the twenty antidiagonal models, the displayed formula or array interpretation bounds those entries by exp(O_d(sqrt(n))) times a polynomial. On the other hand each has a superpolynomial subsequence, certified below. Thus none is rational.

## 4. Classification of all 31 nonrational definitions

Nine square models:

- A184208: choose all entries from {2,3}. This gives at least 2^((n+1)^2) admissible arrays.
- A202398, A202484: the parity factors include growing square independent-set models. On a square grid, with or without the NW-SE diagonal edges, the sites spaced by two in each coordinate may be selected independently. This gives 2^(Omega(n^2)).
- A202427: the growing interior independent-set factor gives the same lower bound.
- A202413, A203040: place optional ones only at a lattice spaced by the window length, 3 or 4. Every complete window then contains at most one 1. Again there are 2^(Omega(n^2)) choices.
- A202583: start with all ones and choose optional zeros at sites spaced by three in each coordinate. No length-three horizontal, vertical or NW-SE diagonal word has two adjacent zeros, so neither 001 nor 100 occurs. The optional choices give 2^(Omega(n^2)).
- A202092: at n=2m, the count is binom(2m+2,m+1)^4 ~ (256/pi^2) 256^m/(m+1)^2. The power -2 is forbidden for a rational-series subsequence.
- A202194: 2(n+2)^2 binom(2n+2,n+1) ~ (8/sqrt(pi)) 4^n n^(3/2). The power 3/2 is forbidden.

Twenty antidiagonal models:

Fourteen direct transfer and block models have explicit pairs of distinct closed walks of equal length k in the finite state graph obtained by transposing the i=1 rectangles. Their state definitions are exactly the retained horizontal and vertical (and, where applicable, NW-SE diagonal) constraints; transposition preserves them. At j=kt the two closed walks can be concatenated independently t times, giving at least 2^t distinct valid arrays. Since the corresponding antidiagonal index is O(j^2), this is superpolynomial in n. The certificate JSON stores both walks for every model, and the compiler verifies all edges, equal lengths and distinctness.

For A202100 and A202202 use balanced even side lengths i=j=m and the central-binomial asymptotic. For A202406, A202435, A202492 and A202601 use the growing independent-set strip factor at i=1: alternating sites of a row already give exponentially many choices in j. These six also have superpolynomial subsequences. All twenty therefore satisfy the boundary-block obstruction lemma.

Two labeled-graph parity models:

For n>=3, fix all n-1 edges incident to a given vertex. Every completion is connected, and half of the 2^binom(n-1,2) completions have each edge parity. Both counts are superexponential. More precisely, if E_n and O_n are the even and odd counts, their sum C_n has log_2 C_n = n^2/2+O(n), and their signed difference D_n=E_n-O_n=(-1)^(n-1)(n-1)! by the retained signed exponential generating function argument.

## 5. Eleven independent nonrational directions modulo the rational span

The following growth separation proves a joint rank extension, not merely individual nonrationality.

### 5.1 Superexponential square and labeled-graph tier

Write A=A184208 and B=A202398 and Z=A203040. The following strict growth scales hold as n increases.

For A, allow {2,3} at all sites and {1,2,3} at the sites spaced by two in both coordinates. Any 2x2 block contains at most one optional low site; its sum is at least 1+2+2+2=7. Thus log_2 A_n >= (1+delta)n^2-O(n) for some delta>0.

For B, the parity decomposition contains four ordinary horizontal/vertical independent-set grids with total area (n+2)^2. In each rectangle, choose black checkerboard sites arbitrarily. Select a family of white sites separated by at least four in one coordinate whenever they differ. Their black neighborhoods are disjoint and each has size at most four. Counting independent choices of these white sites gives the lower bound 2^(floor(area/2)) (1+2^(-4))^(area/16-O(perimeter)). Multiplying over the four rectangles proves log_2 B_n >= (1/2+epsilon)n^2-O(n) for some epsilon>0. The trivial upper bound is 2^((n+2)^2).

For Z, tile the (n+3) by (n+3) square by disjoint 4x4 blocks and leave O(n) boundary cells. Each complete block must be a partial permutation matrix, since each row and column can contain at most one 1. There are exactly sum_{k=0}^4 binom(4,k)^2 k! = 209 < 2^8 such matrices. Thus log_2 Z_n <= (log_2 209)/16 n^2+O(n), with coefficient strictly below 1/2. The lattice lower bound from Section 4 has a strictly positive quadratic coefficient.

The resulting hierarchy is A >> B >> C >> Z >> |D| >> every exponentially bounded sequence, where >> denotes ratio tending to infinity in absolute growth magnitude. The factorial D grows superexponentially but has log growth O(n log n). Every nonzero constant linear combination of these five directions is superexponential, by dominance of its highest nonzero tier. C and D are invertible constant linear combinations of E and O. Therefore A184208, A202398, A054939, A054940 and A203040 are jointly independent modulo exponentially bounded series, including the rational span and the six remaining proposed directions.

### 5.2 Square binomial tier

A202092 and A202194 have distinct even-index growth scales 256^m/m^2 and 16^m m^(3/2), respectively. The four antidiagonal directions below are exponentially bounded by 2^(n+O(sqrt(n))) times a polynomial: the block models have rectangle area at most n/2+O(sqrt(n)), and the binomial models have subexponential bounds. On the even subsequence these antidiagonal terms are therefore negligible compared with either square binomial term. If a combination with a nonzero square-binomial coefficient were rational after addition of antidiagonal terms, its even subsequence would have the forbidden asymptotic power of the largest nonzero square-binomial term. This is impossible by Section 3.1.

### 5.3 Antidiagonal tier

Use A184217 (quaternary blocks), A184207 (binary blocks), A202100 (four binomial parity factors), A202202 (single binomial with polynomial multiplier). Along the common subsequence i=j=m with even m, the quaternary block count is at least 2^((m+1)^2)(3/2)^(floor((m+1)/2)^2), by the separated low-site construction. The binary block count is at most 2^((m+1)^2), and at least 2^(floor((m+1)/2)^2) by optional zeros spaced by two in a background of ones. Its growth dominates both binomial counts. At these balanced even side lengths the two binomial counts have growth 16^m times an inverse-square polynomial factor and 4^m times a polynomial factor of degree 3/2, respectively. Thus any nonzero constant combination of the four antidiagonal directions grows faster than every polynomial along this common subsequence. All such combinations retain subexponential boundary blocks. The boundary-block lemma excludes rationality.

Together the three tiers certify the eleven additional basis directions. The 517 represented series have exact rank 252: 241 predecessor rational directions plus eleven independent modulo that span. There are 265 dependence dimensions among these 517, and 20 unrepresented nonrational series. The full-catalogue rank is bounded, not determined.

## 6. Reproduction and limitations

From a repository checkout:

- node tools/compile_graph_array_compact_deferred.js rebuilt-compact-models.json
- node tools/compile_graph_atlas_compact_basis.js rebuilt-compact-basis.json
- node tools/compile_graph_atlas_complete_fixed_basis.js rebuilt-fixed-basis.json
- node tools/compile_graph_atlas_formal_basis.js rebuilt-formal-basis.json

The scripts consume retained predecessor certificates and exact source definitions. Rebuild predecessors to audit them separately. The spectral and nonrational classifications also rely on the written proofs above, not solely on executable finite tests. No minimum scalar recurrence order is asserted for the 18 compact final fixed-state models. This continuation is on the research branch; it is not an assertion of current website publication.
