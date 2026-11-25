# Rank-271 formal-series transfer certificate and the final square-array question

Author: Komorebi P.

## 1. Certified scope

The retained atlas has 537 records, of which 506 have rational ordinary generating functions under the retained zero-padding index convention. The complete rational span has dimension 241. The preceding formal-series certificate represented 517 records with rank 252.

This continuation adds sixteen antidiagonal directions and three square-array directions, giving 536 represented series with exact constant rational rank 271. The 265 preceding dependence dimensions are preserved. The full atlas rank belongs to {271, 272}. The only unresolved record is A202427. No new OEIS bindings or literature-priority claims are made.

## 2. Antidiagonal slice annihilator

Let f_r(i,j) be a retained antidiagonal rectangle count, and let a_r(n) be its flattened sequence, where ell=i+j-1 and n=ell(ell-1)/2+i. The preceding boundary-block lemma implies that any rational ordinary generating function of a constant linear combination of antidiagonal sequences has polynomially bounded coefficients: at the first d positions of arbitrarily late diagonals (for any fixed d), all these counts are exp(O_d(sqrt(n))). An invertible recurrence companion on the eventual tail then has no contributing characteristic roots of modulus greater than one.

For fixed i, the functions f_r(i,j), j>=1, are rational sequences in j with finite integer linear realizations. For direct transfer formulas, transpose the rectangle to put i+L-1 on the width axis and j+L-1 on the height axis, or i+1 and j+1 for block formulas. NW-SE diagonals are preserved by transposition. The exact equitable quotient gives a dimension bound D_r. For a boundary-factorized independent-set formula, the tensor product of the Fibonacci and fixed-width strip recurrences has dimension at most twice the strip order. For the two parity-product independent-set models, use the symmetric fourth power of one fixed strip companion when the two widths agree, or the tensor product of their symmetric squares when they differ. Doubling the dimension handles interleaved even and odd j. The proper strip rational functions were certified in the predecessor, so these companions give all-index integer realizations. The two binomial antidiagonal models are polynomials in j on each parity lane, with degree bounds 2(i+2) and i+2, respectively.

Fix i and let D be the maximum of these realization dimensions and the binomial lane annihilator multiplicities; the tested values D=36,63,180 for i=1,2,3 cover the latter. Put

    L = lcm(1,2,...,2D),
    H(E) = E^D (E^L - 1)^D.

Here E shifts j forward. If a constant rational linear combination of the flattened antidiagonal series is rational, its coefficients, and thus each fixed-height slice, are polynomially bounded. The slice characteristic polynomial divides the least common multiple of the component characteristic polynomials. All its nonzero characteristic roots are algebraic integers, and all their algebraic conjugates occur in the rational characteristic polynomial. Polynomial growth forces every conjugate to have modulus at most one. Kronecker's theorem therefore makes each nonzero root a root of unity. For a root of order d the minimal polynomial has degree phi(d)<=D. If p^a divides d, then phi(p^a)<=D and p^a<=2D, so d divides L. Root multiplicity is at most D because the slice annihilator is an LCM, not a product. The zero root is killed by E^D. Thus H(E) annihilates every polynomially bounded slice combination, including its possible finite transient. The two binomial slice sequences are killed separately by H.

For the other 18 antidiagonal functions, compute their exact coefficient vectors modulo each of the primes 1000003 and 1000033. Modular Berlekamp-Massey proposes a recurrence from 2D_r coefficients. Verification of at least D_r consecutive residuals after the proposed order certifies that recurrence for all subsequent j by Cayley-Hamilton on the original integer realization reduced modulo the prime. Polynomial modular exponentiation computes H(E) in that recurrence quotient, without explicitly forming its huge shift degree. The resulting 96-by-18 filtered coefficient matrix from three slices has rank 18 at both primes. Indeed its first 18 rows already have rank 18. A duplicate-column control is rejected. The matrix is an exact reduction of the integer H(E)-filtered vectors, so the nonzero modular minor proves rational independence of those 18 directions modulo rational flattened series. The two remaining binomial antidiagonal directions are independent modulo the rational span by the predecessor balanced-diagonal growth and boundary-block argument. This proves joint independence of all twenty, not just each individual nonrationality claim.

Checks: 324 independent small rectangle comparisons, 7952 modular recurrence residual checks, two rank witnesses, zero reference-budget skips in this pass. The direct proof and certificate together extend the represented span to 533 records of rank 268.

## 3. Exact strip bounds for square models

Write Z(m,h) for independent-set counts on the rectangle with horizontal, vertical and NW-SE diagonal adjacency, and C_k(m) for the square binary constraint of at most one 1 in every horizontal and vertical window of length k.

A positive comparison vector v for a nonnegative matrix M with Mv<=u v gives spectral radius at most u and bounds every fixed-width strip count by a constant times u to the height. Similarly Mv>=l v gives a lower strip count of a positive constant times l to the height, because the boundary all-ones vectors bound v above and below by positive scalar multiples. The proposed vectors were obtained by normalized integer iteration; acceptance uses only exact integer row inequalities. Their construction does not rely on a floating-point eigenvalue estimate.

The following certificates hold:

- C3 strip of width 12, with 9089 compatible two-row histories: Mv <= (226/5)v.
- Triangular independent-set strip of width 10, with 144 row states: Mv <= (3199/100)v.
- Triangular independent-set strip of width 16, with 2584 row states: Mv >= 230v.

The respective minimum integer inequality margins are 48722, 3939 and 10310. The full 11817 positive-vector row checks are preserved with the vectors and reproducible integer adjacency construction.

Partition a large square or rectangle into fixed-width strips, ignoring crossing constraints for upper bounds. For a lower bound on triangular independent sets, fill width-16 strips independently and separate them by one all-zero column. The discarded width at the edge and the multiplicative constants per strip contribute only O(m+h) to the base-two logarithm. Consequently, for large squares,

    log2 C3(m) <= (log2(226/5)/12)m^2 + O(m),
    log2 Z(m,m) >= (log2(230)/17)m^2 - O(m),
    log2 Z(m,m) <= (log2(3199/100)/10)m^2 + O(m).

The corresponding triangular bounds hold for the four parity rectangles in A202484, whose areas sum to m^2. The inequalities

    (226/5)^17 < 230^12,
    (3199/100)^2 < 2^10

are checked by exact integer cross multiplication. Thus both the full triangular count and the four-rectangle triangular count lie strictly above C3 in bulk growth and strictly below the connected labeled-graph n^2/2 tier.

C3 strictly dominates C4. Work on the same m by m square and retain all C3 constraints throughout. Initially also impose all C4 constraints. Partition the square into disjoint 10 by 10 boxes. In each box relax the C4 constraints wholly internal to it, one box at a time. Given any exterior configuration previously admitted, the local completion with two ones at positions (4,3),(4,6) (zero-based) and zeros elsewhere is newly allowed. It satisfies C3, violates an internal C4 window, and has a three-cell zero margin so it satisfies every cross-box C4 constraint. The number of prior completions is at most 2^100, so each relaxation increases the global count by a factor at least 1+2^(-100). The final configurations are C3-admissible. It follows that C3(m)/C4(m) >= (1+2^(-100))^floor(m/10)^2. The side lengths for A202413 and A203040 differ by one, but adding one row and column costs at most 2^(2m+1), which cannot overcome this quadratic exponential gap. The independent spacing-four grid lower bound makes the C4 tier superexponential relative to factorial or exponentially bounded sequences.

## 4. Uniform exceptional-zero-line bound

Let m=n+2. In any finite binary line avoiding both 001 and 100, either there are no adjacent zeros, or the whole line is zero. Indeed a run of at least two zeros adjacent to any 1 produces one of the forbidden words. The statement also holds for a line of length two.

In an A202583 configuration mark all horizontal, vertical and NW-SE diagonal lines of length at least two that contain adjacent zeros. They are entirely zero. Let U be their union. All zeros outside U form an independent set in the triangular graph and avoid the closed neighborhood of U: an adjacent pair with at least one endpoint outside U would force its line to be marked. Thus, for a fixed marked line set, the number of choices is at most Z(G_m minus N[U]).

The triangular grid has a proper three-coloring by (row+column) mod 3. Hence Z(G_m[U]) >= 2^(|U|/3). Independent sets on U and on G_m minus N[U] combine freely, giving

    Z(G_m minus N[U])/Z(G_m) <= 2^(-|U|/3).

Every vertex belongs to at most three marked lines, so |U| >= (sum of their lengths)/3. Summing over all possible marked line sets gives

    A202583(n)/Z(m,m) <= product_over_lines (1+2^(-length/9)).

The product is bounded uniformly in m: there are 2m horizontal/vertical lines of length m and at most two diagonal lines of each length. The product over all diagonal lengths converges, and (1+2^(-m/9))^(2m) is uniformly bounded. Conversely every triangular independent set chosen as the zero set satisfies the forbidden words. Therefore

    Z(m,m) <= A202583(n) <= K Z(m,m)

for an absolute constant K.

The predecessor's parity decomposition A202484 is the product of independent-set counts in four rectangles partitioning the m by m square; equivalently it is the independence count after deleting all edges crossing the two central cuts. The cut graph has strictly more configurations than the full grid by an exponential-in-m factor. To see this, select disjoint 4 by 4 boxes along the vertical central cut, away from the horizontal cut and the outer boundary. Each box has an interior horizontal edge crossing the cut. Delete these selected edges one at a time. For every previously admitted exterior configuration, the local pattern containing both endpoints of the selected edge and zeros elsewhere is a newly allowed independent set after deletion. Its endpoints lie in the interior, so it creates no exterior conflict. Each deletion gives a factor at least 1+2^(-16), since prior local completions number at most 2^16. There are Omega(m) such boxes. The fully cut graph has at least as many configurations. Consequently A202484(n)/Z(m,m) grows exponentially in m, and A202484(n)/A202583(n) tends to infinity.

The 8188 exhaustive finite-line checks in the compiler are controls on the elementary line classification, not a substitute for its all-length proof.

## 5. Rank-271 conclusion

The strict growth hierarchy among the newly added and predecessor superexponential directions is now

    A184208 >> A202398 >> connected labeled total
    >> A202484 >> A202583 >> A202413 >> A203040
    >> labeled parity difference >> every exponentially bounded sequence.

The first two comparisons, the n^2/2 growth for connected labeled totals, and the factorial parity difference follow from the predecessor proofs. The strict separation of A202484 and A202583 occurs at boundary rather than bulk scale. The other new comparisons follow from Sections 3 and 4. Every nonzero constant rational combination of these directions has a dominating highest nonzero scale and cannot be canceled by exponentially bounded series. The square binomial and complete antidiagonal tiers remain independent modulo the rational span as proved previously and in Section 2. Therefore adding A202413, A202484 and A202583 gives a 536-record span of exact rank 271. The new transfer rows are identity rows for the added independent functions; no earlier dependence certificates are altered.

## 6. Final unresolved record and a sufficient closing lemma

A202427(n) = 2 F_(n+3)^2 Z(n+1,n+1) is the sole unrepresented direction. Put m=n+2. In terms of the triangular partition function its count is the extreme four-rectangle split of an m by m square: one isolated corner, two independent paths of length m-1, and the (m-1) by (m-1) triangular interior. A202484 is the balanced four-rectangle split of the same square. A202583 is comparable to the full uncut square.

The two known triangular directions have the same bulk entropy; their ratio is separated by the cut argument. The last direction A202427 has the same bulk entropy as these two, by the area-O(m) boundary comparison. A proof of

    2 F_(m+1)^2 Z(m-1,m-1)
      / [Z(h,h) Z(h,k) Z(k,h) Z(k,k)] -> infinity,

where h=floor(m/2), k=ceil(m/2), would place it above the other two triangular directions and close the full atlas rank at 272. This is sufficient, not necessary. In the opposite direction a strict separation from both A202484 and A202583 would also suffice. Another possibility is a direct proof excluding a constant rational relation between the three triangular series modulo lower-growth series. Finite numerical ratios suggest a boundary effect, but do not prove it. No such all-index boundary comparison is claimed here.

Reproduction:
    node tools/compile_graph_atlas_antidiagonal_basis.js rebuilt-antidiagonal-basis.json
    node tools/compile_graph_atlas_square_separation.js rebuilt-square-basis.json

These scripts read the preserved predecessor certificates and source catalogues. Rebuild those predecessors for a complete independent replay. The proof is written mathematics with exact arithmetic certificates, not Lean verification. The research branch remains separate from the live atlas.
