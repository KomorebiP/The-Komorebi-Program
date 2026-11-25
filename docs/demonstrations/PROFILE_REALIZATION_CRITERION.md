# Finite profile realization of rooted graph moments

**Author: Komorebi P.**  
**Version:** 3.1, 2026-11-25  
**Status:** mathematical proofs and exact finite computational checks. Not Lean certified or independently peer reviewed.

Predecessor: [Saturated walk lattices and finite realization classification, v3.0](https://github.com/KomorebiP/The-Komorebi-Program/blob/main/docs/demonstrations/LATTICE_REALIZATION_CLASSIFICATION.md). All six entries of its checksum manifest were checked and matched; its checker was not rerun here. This continuation replaces the abstract complementary-lattice completion criterion with a finite integer-profile criterion for connected simple graphs, even when the ambient order is unspecified. It also classifies all source Smith groups at bipartite cyclic rank three.

## 1. Finite vertex profile theorem

Let m_n be a rooted return-walk sequence of a finite connected simple undirected graph. Let r be its Hankel rank, let M(x)=x^r+sum_{j=0}^{r-1} M_j x^j be its monic minimal recurrence polynomial, and put H=(m_{i+j})_{0<=i,j<r}. The arguments also apply as an existence criterion to a proposed sequence with m_0=1, m_1=0, a positive definite H, and a monic integral minimal recurrence M of degree r. Define Q to have ones on its first superdiagonal, zero entries elsewhere in its first r-1 rows, and last row (-M_0,...,-M_{r-1}). The distinguished root profile is t_*=H e_0. The sequence is determined by this recurrence and its first r values. If r=1, a connected simple graph can only be the single vertex, with m_0=1 and all later moments zero.

For a realization A and root o, put W=(e_o^T A^i)_{0<=i<r}. Its columns are the walk profiles t_v=((A^i)_{ov})_{0<=i<r}. The first r rows span the cyclic space, so WW^T=H and QW=WA. All t_v are nonnegative integral. The root column is t_*, has first entry one, and every other profile has first entry zero. When r>=2, each nonroot second entry is zero or one, because the graph is simple. The matrix W^T H^{-1} W is the orthogonal projection onto the row space of W. Its diagonal entries lie between zero and one. Thus every column satisfies

$$t_v^\top H^{-1}t_v\le1.$$

Equivalently, H-t_v t_v^T is positive semidefinite. No profile can vanish in a connected graph: if a column of the first r rows vanishes, every later walk row vanishes at that vertex by recurrence, contradicting reachability. In particular the root eccentricity is at most r-1. Every nonzero integral profile has squared Euclidean norm at least one, so

$$r\le N\le\operatorname{tr}H=\sum_{i=0}^{r-1}m_{2i}.$$

This is an ambient-order bound derived solely from the return sequence. Without connectedness, arbitrarily many disconnected vertices could be added. The bound is not necessarily sharp.

### 1.1 Exhaustive finite profile construction

For r>=2 define the finite set of nonroot candidates t by:

- t belongs to Z^r, with nonnegative coordinates, and is nonzero;
- t_0=0 and t_1 is zero or one;
- t^T H^{-1}t<=1;
- Qt has nonnegative coordinates.

These constraints are necessary, not sufficient. The ellipsoid is bounded because H is positive definite; coordinate i is bounded above by floor(sqrt(H_ii)) by Cauchy-Schwarz. Enumerate nonnegative integer multiplicities n_t satisfying

$$\boxed{H=t_*t_*^\top+\sum_t n_ttt^\top.}$$

Every multiset is finite and the trace identity bounds its size. It remains to impose local adjacency constraints. Include t_* with multiplicity one, discard types with multiplicity zero, and denote the resulting list of distinct types by t^1,...,t^s. For each vertex of type t^i choose a nonnegative integral configuration d=(d_1,...,d_s) with

$$\sum_jd_jt^j=Qt^i,\qquad 0\le d_j\le n_{t^j}-\delta_{ij}.$$

These equations are finite. Choose a multiset of n_{t^i} configurations for each type, allowing vertices of the same profile to have different neighbor-count vectors. For each i, the list of d_i across vertices of type i must be a graphical degree sequence for a simple graph. For each i<j, the list of d_j on type i and the list of d_i on type j must be jointly bipartite graphical. These conditions are decidable by the classical Erdos-Gallai and Gale-Ryser criteria. Explicitly, a nonnegative degree list a_1>=...>=a_n is graphical iff its total is even and for each k=1,...,n,

$$\sum_{i=1}^k a_i\le k(k-1)+\sum_{i=k+1}^n\min(k,a_i).$$

Two nonnegative bipartite degree lists a (sorted) and b are jointly graphical iff their totals agree and for each k=1,...,len(a), sum_{i=1}^k a_i<=sum_j min(k,b_j). The degree bounds above exclude impossible loops or multiple edges. One can alternatively check the within-type lists by Havel-Hakimi and the between-type lists by integral bipartite flow.

**Theorem (necessary and sufficient).** A candidate multiset is realizable by a connected rooted simple graph with the prescribed return sequence exactly when such configuration lists exist. Every simple-graph realization arises from this construction.

**Proof.** Necessity follows from the original walk rows and the neighbor counts in the actual graph. For sufficiency, give vertices the selected configurations. For each type build a simple graph realizing its internal degree list, and for each pair of types independently build a simple bipartite graph realizing the two degree lists. These edge sets are disjoint, hence their union is simple and undirected. Let W be the matrix of its assigned profiles. The local equations give QW=WA. The zeroth row is the root indicator. Induction through the first r-1 shift equations gives that row i is e_o^T A^i, and the last equation gives the recurrence for the next row. Multiplication by A propagates this recurrence forever. The root column agrees with m_0,...,m_{r-1}, so all rooted moments equal the specified sequence. Every profile is nonzero, so every vertex is reached by some walk from the root; the graph is connected. The Gram identity gives the specified H and rank. Conversely every realization determines its profiles, their multiplicities, its configurations, and each constituent edge set. Thus enumerating all realizations of the degree lists (rather than only testing existence) recovers all rooted graphs up to relabeling. QED.

This is a finite decision and enumeration theorem, not a polynomial-time algorithm. The multiplicity search, configuration search and output of all graphs can be large. No arbitrary upper order cutoff or complementary lattice enumeration is required. A graphicality check on aggregate counts alone is insufficient; per-vertex configurations are needed.

### 1.2 Test a specified saturated lattice

Use the abstract monomial coordinates of v3.0, where L=Z^r with bilinear form H. For a frame W define C=span_Z{t_v} in Z^r. The rational map u -> W^T u is an isometry for H. Its integral saturation consists of the coordinates u for which W^T u is integral, namely

$$S=C^\vee=\{u\in\mathbb Q^r:u^\top C\subseteq\mathbb Z\}.$$

Here the coordinate dual uses the ordinary coordinate pairing, not the H-metric dual. The source group S/L is the character dual of Z^r/C and has the same invariant factors. If a particular invariant isotropic subgroup of the discriminant group from v3.0 is prescribed, take its overlattice S in monomial coordinates and retain exactly those multiplicity frames whose column span equals S^vee in the ordinary coordinate pairing. Necessity follows from the definition of saturation, and sufficiency follows from the isometry and the construction above. This gives an exact finite simple-graph filter for a specified candidate S at any ambient order, or at a specified order by requiring the sum of multiplicities to equal it. It does not claim a closed arithmetic condition avoiding all combinatorial graphicality constraints.

## 2. Exact rank-three bipartite classification

Let a connected rooted bipartite graph have cyclic rank three. By the bipartition sign involution, its rooted cyclic spectrum is symmetric about zero. Rank three and real symmetry imply three distinct active eigenvalues 0 and +/-sqrt(c). Thus M=x^3-cx, where c is a positive integer by monicity and integrality of the minimal polynomial. Put b=m_2 (the degree of the root). Then m_4=bc and

$$m_{2n}=bc^{n-1}\ (n\ge1),\quad m_0=1,\quad m_{2n+1}=0.$$

The positive definite moment matrix has determinant b^2(c-b), so c>b. Every vertex is at distance at most two. The root is adjacent to all b vertices in the opposite part, denoted B. Every other vertex in the root's part has a nonempty neighbor subset S of B. Write n_S for its multiplicity. The recurrence A^3 e_o=c A e_o is exactly the condition

$$\boxed{\sum_{S\ni j}|S|n_S=c-b\quad(j\in B).}$$

Indeed A^2e_o equals b at the root, |S| at the corresponding nonroot vertex on its side, and zero on B. At j in B, A^3e_o is b plus the sum of the degrees of adjacent nonroot vertices. Thus this condition is necessary and sufficient. Conversely any integer b>=1, c>b and any nonnegative multiplicities satisfying it give a connected bipartite graph of cyclic rank exactly three: the first three walk rows have independent supports after subtracting b times row zero from row two; the recurrence holds. In particular every such pair (b,c) is realizable using singleton subsets. The full graph classification is the list of these multiplicities up to permutations of B, because a rooted isomorphism permutes B and preserves each subset of B.

### 2.1 Complete arithmetic classification

Put g=gcd{|S|:n_S>0}. Subtract b times the zeroth walk row from the second walk row. The three rows are now disjointly supported: the root indicator, the indicator of B, and the positive degree vector on the nonroot vertices in the root's part. The first two are primitive, and the third has content g. Their nonzero source Smith factors are (1,1,g), and the nonzero Gram Smith factors are (1,b,b(c-b)), since summing the subset equations over j gives sum_S |S|^2 n_S=b(c-b). The latter entries already satisfy the divisibility chain. A saturated basis is obtained by dividing the last row by g; its Gram diagonal is (1,b,b(c-b)/g^2). The source group is cyclic of order g. Zero factors pad the profiles to the ambient order if the full rooted walk matrix is used.

**Theorem (exact possible defect groups).** The possible g are precisely

$$\boxed{1\le g\le b,\quad g\mid(c-b),\quad g^2\mid b(c-b).}$$

Necessity: each |S| lies in [1,b], each subset equation is a sum of multiples of g, and the sum of the squares is a multiple of g^2. Sufficiency: set d=(c-b)/g. Repeat the ordered list of b vertices d times, then partition the resulting list into consecutive blocks of length g. The divisibility hypotheses imply that the partition is exact. Since g<=b, each block contains distinct labels. Use every block as a neighbor subset, allowing repetitions. Every opposite-part vertex appears d times, and each occurrence contributes g to its subset equation, so the total is gd=c-b. All nonroot degrees on the root's side equal g, hence their gcd equals g. This explicitly constructs every allowable group. QED.

For any realization with prescribed g, the number N of vertices satisfies

$$N\le1+b+\frac{b(c-b)}{g^2},$$

because each additional vertex contributes at least g^2 to the sum of squared degrees. The uniform-block construction attains this bound for each allowable g. The unrestricted maximum is therefore 1+b+b(c-b), attained at g=1. This is much sharper than the general trace bound. No general minimum-order formula for b>2 is asserted here.

### 2.2 Explicit smallest collision and exact order set when b=2

For b=2, write t=n_{\{1,2\}}. The two singleton multiplicities must both equal c-2-2t. Thus t ranges from zero through floor((c-2)/2), and each t gives exactly one rooted graph up to isomorphism. Its order is

$$N=2c-1-3t.$$

For b=2,c=4 there are exactly two connected rooted realizations: t=1 gives C4, order four and g=2; t=0 gives a tree of order seven with two root neighbors and two leaves attached to each neighbor, g=1. Both have scalar moments 1,0,2,0,8,0,32,0,128,... and Gram factors (1,2,4). The saturated Gram diagonals are (1,2,1) and (1,2,4), respectively. This gives a scalar-equivalent realization family of different ambient orders and classifies all of its connected members. For b=2,c=5 the exact possible orders are six and nine.

For b=4,c=8 the admissible g are 1,2,4; their maximal realizable orders are 21,9,6. At g=4 the construction is K_{2,4}, rooted in its two-vertex part.

## 3. Exhaustive continuation of the seven-vertex witness

Take the common sequence from v3.0, with minimal polynomial

$$M=x^7-9x^5-4x^4+18x^3+8x^2-8x-2$$

and moments m_0,...,m_12 = (1,0,3,4,17,38,122,316,936,2550,7332,20368,57864). The root profile is (1,0,3,4,17,38,122). The exact rational ellipsoid enumeration returns 18 nonroot candidate types. The complete Gram-multiplicity enumeration has four frames (see SEVEN_VERTEX_FRAMES.txt for all candidates). Two frames of order seven pass all local constraints. Both have seven distinct columns; W is square and invertible, so the adjacency is uniquely W^{-1}QW for the fixed profile ordering. Their column multisets match the two known graphs from v3.0 exactly. One more seven-vertex frame fails local constraints (its uniquely prescribed operator also has nonzero diagonal entries); an eight-vertex frame fails local constraints as well.

For the latter, the profile (0,0,0,1,1,8,13) requires the neighbor-profile sum (0,0,1,1,8,13,58). No allowed subset of the other seven profiles has this sum. In particular the two possible neighbors supplying the unit at index two have profiles (0,0,1,1,8,14,58) and (0,0,1,1,7,12,49). The former exceeds the required index-five entry. The latter leaves (0,0,0,0,1,1,9), which cannot be assembled from the remaining profiles because every nonzero candidate with initial three zero entries has positive index-three entry. This gives an explicit local rejection, independently of the general degree-sequence check.

Thus the original pair are exactly the two finite connected rooted simple graphs of any order realizing the common scalar sequence, up to rooted isomorphism. Unrelated disconnected components remain invisible. This is an exact finite enumeration certificate, not a census over all graph orders or a general claim that scalar moments determine graph topology.

### 3.1 Completeness of the ellipsoid search

The checker uses rational Schur complements. For each successive coordinate k, with prefix z, set mu=H_{k,<k} H_{<k,<k}^{-1}z and sigma=H_{kk}-H_{k,<k}H_{<k,<k}^{-1}H_{<k,k}>0. The new prefix energy is the previous energy plus (t_k-mu)^2/sigma. These energies are the quadratic forms from the inverses of the leading principal blocks. The final energy is t^T H^{-1}t. Since each contribution is nonnegative, no feasible full profile has a prefix energy exceeding one. The exact integer recursion uses a rational enclosing interval, then tests the energy exactly. It therefore neither discards a feasible type nor accepts one outside the ellipsoid. The Gram search recursively tries every allowed multiplicity from zero up to the minimum residual bound in a nonzero entry of tt^T; all terms are nonnegative. Each local configuration search analogously exhausts all bounded nonnegative degree counts. These finite search procedures prove completeness of the enumeration when they terminate.

## 4. Verification and remaining boundaries

The final checker passed 13,854 counted exact comparisons (see verification.log). It covers every root of all connected unlabeled graphs through order six, including the singleton: 810 root cases, 642 singular. It checks 4,676 profiles for the ellipsoid and 4,676 local-balance equations; 116 direct type-enumeration and local-configuration checks each; 74 distinct moment-sequence classes through order five by independently matching the feasible frame sets of order at most five against the graph atlas (90 candidate decisions); 142 explicit uniform-subset witnesses for b=1,...,9 and c-b=1,...,10; and 248 exhaustive labeled-neighbor subset multisets for b=1,...,4 and c-b=1,...,5. The seven-vertex witness is checked over all frames with no ambient cutoff. Four additional examples have their complete frame-order sets checked. These are overlapping finite comparisons, not independent theorems. The first streaming terminal invocation was unavailable and did not execute; the non-streaming checker and expanded rerun succeeded. Python 3 with NetworkX 3.6.1 and SymPy 1.14.0 was used. The predecessor manifest matched, but its verification program was not rerun in this continuation.

The v3.0 completion gap is resolved as a finite profile-and-graphicality criterion for connected simple graphs of any finite order; the specified saturated lattice can be tested by its column lattice. The rank-three bipartite arithmetic classification has an explicit constructive proof. Efficient general enumeration, simpler necessary and sufficient conditions in higher cyclic rank, mixed-product bad-prime classification, literature-wide priority, independent peer review and Lean certification remain outstanding. The proof uses classical moment/Krylov linear algebra and degree-sequence realization theorems. No complexity breakthrough or novelty claim is made.
