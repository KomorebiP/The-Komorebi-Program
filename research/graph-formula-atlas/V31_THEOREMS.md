# Structural-core realization calculus v31

Author: Komorebi P.

Scope: unlabeled nonplane rooted and unrooted finite trees. A rooted leaf has zero children; an unrooted leaf has degree one. Unrooted counts below use at least two leaves, excluding the isolated vertex. The original archive is preserved byte for byte as PREDECESSOR.zip; its internal checksum manifest passed. The new mathematics builds on its fixed-leaf Burnside argument, not on extrapolated OEIS terms. Classical ingredients include tree dissymmetry, Burnside, cyclotomic factorization, and the plane-tree cycle lemma. No literature-priority claim is made.

## 1. Universal cyclotomic denominator

Let T_k(x) count rooted trees by vertex count with exactly k leaves. Delete unary vertices and keep the rooted branching core H. The remaining vertices consist of k leaves and b internal vertices of outdegree at least two, hence b<=k-1. Each edge has a nonnegative subdivision length, and a stem above the core root has another length. Isomorphism classes correspond precisely to orbits of edge-length assignments under Aut(H), with stem fixed. Burnside gives

    T_k(x) = sum_H x^|V(H)| / ((1-x)|Aut(H)|)
                     * sum_g prod_{edge cycles C of g} (1-x^|C|)^(-1).

There are finitely many H. For d>=2 consider the edge cycles whose lengths are divisible by d. Orient edges away from the root and identify each edge with its child. Vertex orbits under g form a rooted quotient tree; parent maps take a child orbit onto its parent orbit, so parent orbit length divides child orbit length. The d-divisible orbits form a forest closed under descendants. Give an orbit weight w=|orbit|/d, a positive integer. An internal orbit has child weights summing to at least 2w because every vertex of the core branches into at least two children. If a subtree has total leaf weight W and root weight w, its orbit count is at most 2W-w: this follows by induction, since a leaf contributes 1<=w, and 1+sum(2W_i-w_i)<=2W-w using sum w_i>=2w>=w+1. Summing over forest roots yields at most 2 floor(k/d)-1 orbits when the forest is nonempty. The pole at a primitive d-th root therefore has order at most 2 floor(k/d)-1. No d>k occurs. At 1 there are at most 2k-2 edge cycles plus the stem, and the binary cores with identity automorphisms attain 2k-1. Positive Laurent coefficients at 1 prevent cancellation of this leading term.

With Phi_1 normalized as 1-x, write

    Q*_k(x)=prod_{d=1}^k Phi_d(x)^(2 floor(k/d)-1).

Then Q*_k T_k is an integer polynomial of degree <= deg Q*_k. The degree bound follows term by term: sum of the edge-cycle lengths is |V(H)|-1, and the stem contributes one. Integrality follows by multiplying the integer formal series by the integer denominator. The degree of Q* is

    D_k = k(k+1) - sum_{d=1}^k phi(d),

using sum_{d|n} phi(d)=n. This is an a priori quadratic upper bound on the stable minimal scalar recurrence order. The actual order is the degree of the reduced denominator; for rooted trees it is also the minimal order after shifting to any strictly positive index, since the possible polynomial part is constant. All coefficient values at positive indices are quasipolynomials. The least eventual quasipolynomial period is exactly lcm of the d for which the reduced denominator contains Phi_d: any period P has poles only among P-th roots, and the partial fractions yield a quasipolynomial of this lcm. This is a least period, not merely a period bound.

## 2. Cyclotomic leading-pole filters

Let zeta be primitive d-th root, d>=2, k=ad+b, a>=1, 0<=b<d, and c_a=(2a-3)!!/a! (with (-1)!!=1). Define the truncated series M_d(y) in Q(zeta)[y]/(y^d) by M_0=1, M_1=T_1(zeta), and M_j=T_j(zeta)/zeta for 2<=j<d; these are regular because j<d. Write H_1(y)=1. Recursively define

    H_d(zeta,y) = zeta M_d(y)/(1-zeta M_d(y))
                  * sum_{j|d,j>1} H_{d/j}(zeta^j,y^j)/j  mod y^d.

The constant 1-zeta is nonzero, so this is well-defined. For d/j=1 the corresponding summand uses H_1. The exact leading-pole identity is

    lim_{x->zeta} (1-x^d)^(2a-1) T_(ad+b)(x)
        = c_a [y^b] H_d(zeta,y).

Proof: the rooted multiset equation is T=x(y-1+M), M=exp(sum_{j>=1}T(x^j,y^j)/j). Apply the denominator bound from section 1 at x^j: its root order is d/gcd(d,j). At leaf index k'=j*l a singular summand T_l(x^j) has pole order at most 2 floor(k'/lcm(j,d))-1, including order d/gcd(d,j)=1. A product of two or more singular factors at total index ad+b has pole order at most 2a-2, since the sum of the floor quotients is <=a. For a single singular factor to attain 2a-1 its index must be ad+b' with 0<=b'<=b and lcm(j,d)=d, hence j divides d. The remaining regular factors use total leaf index less than d, yielding M_d(y). For j|d, 1-(x^j)^(d/j)=1-x^d, so the singular leading coefficients use exactly the same normalization. At j=d they reduce to lim_(x->1)(1-x)^(2a-1)T_a(x)=c_a, from the binary-core identity (section 4 below). At j=1 they give the unknown H_d itself. Induct on d and then b (or solve the triangular coefficient system); isolating that term gives the displayed recursion. Thus the normalized leading coefficient vanishes exactly when H_{d,b} vanishes in Q[z]/Phi_d(z), uniformly over all a. This does not determine the subleading pole order when the leading coefficient vanishes.

For d=3, T_1=x/(1-x) and T_2=x^3/((1-x)^2(1-x^2)). At a primitive cube root zeta, the y^2 coefficient of zeta M/(3(1-zeta M)) is

    zeta^3/(3(1-zeta)^4) * (1+zeta+zeta^2)/(1-zeta^2)=0.

Hence the top allowed primitive-cube-root pole cancels in T_(3a+2) for every a>=1. For k<=24 the only top-pole cancellations found were these seven cases, and each loses exactly one order at Phi_3. The latter exact deficit and the absence of other cancellations are certified in this range only, not asserted globally. In particular T_5 has least period 20 rather than 60. For the rooted models in the computed range the reduced degree is D_k-2 when k>=5 and k=2 mod 3, and D_k otherwise. Further d and lower-order Laurent terms are open classification tasks.

## 3. Exact quasipolynomial compilation

Given reduced T=P/Q with Q=prod Phi_d^e_d, polynomial division leaves a proper fraction plus a polynomial part S. By polynomial CRT over Q, its unique primary fraction with denominator f_d=Phi_d^e_d has numerator

    N_d=(P_remainder * (Q/f_d)^(-1)) mod f_d.

Define L_d=N_d*((1-x^d)/Phi_d)^e_d, degree less than d*e_d. Then T=S+sum L_d/(1-x^d)^e_d. To compute its nth coefficient put q=floor(n/d), r=n mod d, L_d=sum_j l_(d,j) x^j. The contribution is exactly

    sum_{j=0}^{e_d-1} l_(d,r+d*j) binom(q-j+e_d-1,e_d-1).

The binomial top is nonnegative for n>=0; if top is less than bottom the contribution is zero. Add [x^n]S. This is a direct all-index formula using bounded-size residue lanes, even if the common period is huge. For rooted trees S is constant; for unrooted trees S has degree at most one. The integer coefficient arrays in the JSON are scaled by a positive denominator for each lane. The inverse is computed by Euclidean inversion modulo Phi_d and Newton lifting (g -> g(2-ag)) modulo successive powers. This is not an empirical interpolation.

For A055278 (original vertex index n>=4), the exact expression is

    288 a(n)=6n^4-40n^3+108n^2-120n+23+9(-1)^n+32 r(n),
    r(n)=-1,1,0 for n=0,1,2 mod 3 respectively.

It follows by expanding the three residue lanes of T_3. All 47 models through 24 leaves have explicit lane formulas. The rooted 24-leaf model, for example, has least period 5354228880 but a reduced denominator of degree 420; the factored lane representation avoids storing billions of polynomials.

## 4. Two leading asymptotic coefficients for rooted trees

Write A_k=(2k-3)!!/k!. For k>=2,

    t_k(n) = A_k n^(2k-2)/(2k-2)!
              + B_k n^(2k-3) + O_k(n^(2k-4)),
    B_k = A_k/(2k-3)! * [-(2k-1)/2+(k-2)/3+k(k-1)/(4(2k-3))].

Proof: full binary cores give the leading pole at 1, coefficient A_k, since labelling their leaves gives (2k-3)!! distinct cores with labelled leaves and k!/|Aut(H)| labellings of each shape. To reach one order below the leading pole only three contributions are possible: expanding x^(2k-1) in the binary identity term (coefficient -(2k-1)A_k); cores with one ternary branch and all other branches binary (coefficient (k-2)A_k/3, since contracting any one of k-2 internal edges has precisely three labelled binary refinements); binary automorphisms swapping exactly one pair of edges (necessarily the two leaf edges of a cherry, since every moved internal vertex would move descendants too). The total weighted number of cherries is choose(k,2)(2k-5)!!/k!, and the factor 1/2 comes from 1-x^2. For k=2 use (-1)!!=1; there are no ternary cores. Finally the subleading power of n from [x^n](1-x)^(-(2k-1)) contributes (2k-1)A_k/(2(2k-3)!). Other roots of unity have pole order <=2floor(k/2)-1 and do not contribute to the two highest powers. This proves the coefficient. The leading coefficient simplifies to 1/(2^(k-1)(k-1)!k!). Both asymptotic coefficients are checked exactly for k=2..24 from the rational generating functions.

## 5. Unrooted trees with a fixed number of leaves

Let U_k(x) count unrooted unlabeled trees with k>=2 vertices of degree one. Put T(x,y)=sum T_k(x)y^k. A rooted planted branch uses the original T: a vertex with no children has degree one after the parent edge is attached. Vertex-rooted unrooted trees have a root with either one child (root itself is a leaf), or at least two children. For k>=2 their GF is [y^k](xyT+x(M-1-T)). Edge-rooted trees are unordered pairs of planted branches, with GF (T^2+T(x^2,y^2))/2; directed-edge-rooted trees are ordered pairs, with GF T^2. The tree dissymmetry identity (root at a vertex plus root at an undirected edge, minus root at a directed edge) follows from the unique center of a tree and pairing noncentral roots with a directed edge along or away from the center. Substituting x(M-1)=T-xy gives, for k>=2,

    U_k(x)=(1-x)T_k(x)+xT_(k-1)(x)
           - (1/2)sum_{i=1}^{k-1}T_i(x)T_(k-i)(x)
           + (1/2) 1_{2|k} T_(k/2)(x^2).

Independently suppress every degree-two vertex of an unrooted tree. For k>=3 the core has <=2k-2 vertices and <=2k-3 edges. Burnside applies to the edge subdivision lengths with no stem. Center the core at its fixed center vertex or midpoint of its center edge. Noncentral edges have the same parent-orbit argument as section 1; the central edge, when present, is fixed, and cannot contribute to d>=2. Thus the same bound on primitive d poles holds, while the pole order at 1 is 2k-3, attained by degree-three cores. For k=2 the graph is a path and U_2=x^2/(1-x). The numerator bound now permits degree one greater than denominator degree (one vertex more than edge lengths); after shifting to n>=2, the reduced denominator gives the exact minimal scalar order. The least eventual period is again the lcm of the active d.

For k>=3 the leading term is

    u_k(n) ~ n^(2k-4)/(2^(k-2)(k-2)!k!).

Indeed labelling the leaves of degree-three unrooted cores gives (2k-5)!! labelled shapes, obtained by adding a new leaf on any edge; divide by k! and then (2k-4)!. The path k=2 has constant count 1 for n>=2 and is exceptional. In particular U_3=x^4/((1-x)(1-x^2)(1-x^3)). All 23 unrooted models through 24 leaves were compiled by the dissymmetry formula and the denominator theorem. No OEIS ID is assigned to a new unrooted model without a source receipt.

## 6. Prescribed branching-degree profile

Fix nonnegative integers b_j for j>=2, of finite support, and put k=1+sum(j-1)b_j and r=k+sum b_j. Count rooted nonplane trees with k leaves, exactly b_j vertices with j children, and arbitrary unary vertices. All branching cores now have exactly r vertices. The same finite-core Burnside argument yields rationality, with maximum pole order r at 1 and, for d>=2, bound min(2 floor(k/d)-1, floor((r-1)/d)), since each divisible edge cycle uses at least d edges. The bound is zero for d>k. The leading term is exactly

    t_profile(n) ~ n^(r-1)/(k! prod_j b_j! (j!)^b_j).

Proof: ordering the children of a nonplane core H gives prod(j!)^b_j / |Aut(H)| distinct plane trees. The number of plane rooted trees with this profile is (1/r) multinomial(r;k,b_2,b_3,...). To see it, write the outdegrees in preorder: their increments degree-1 sum to -1; exactly one cyclic shift has all proper prefix sums nonnegative, and such a word reconstructs the plane tree by the open-child-slot rule. The sum -1 prevents periodic repetitions of the word. Divide this plane count by prod(j!)^b_j, then divide by (r-1)! for the leading coefficient. All other poles have order less than r. This gives a factorial constant even without computing the core types. The case of all unary trees, k=1,r=1, is included.

The separate compiler enumerates every reduced core with <=8 leaves. For a core root with identical child core types H_i of multiplicity m_i, form the multiset series of size m_i from the subdivided rooted child series (which includes its unary stem); multiply them, then multiply by x/(1-x) for the root and its stem. This is a direct enumeration of all extensions and is equivalent to the Burnside argument. It computes 45 profile rational models from 405 reduced core shapes, independently verifies the factorial leading coefficients using automorphism orders, and recomposes the original rooted leaf-count series by summing profiles.

## 7. Verification method

`core_calculus.py` computes exact integer series by the rooted multiset recursion in the predecessor (using carry-free coefficient packing for nonnegative convolutions). Because the universal denominator and numerator degree bounds are proved, the first D+1 coefficients (D+2 for unrooted) determine the numerator exactly. All further residual checks are independent verification, not the mathematical basis for fitting an unbounded recurrence. Exact division by each known cyclotomic factor certifies the reduced denominator. The script independently compares leading-pole filters with evaluations of the unreduced rational numerator at the primitive root, and checks both asymptotic coefficients. `export_quasipolynomials.py` performs the remaining lane compilation and replays the full independent integer series. For small trees the independent canonical-tree enumerator lists every rooted tree through 12 vertices and deduplicates unrooted trees via minimum rooted canonical encoding over vertices. `degree_profile.py` independently uses reduced branching cores rather than the multiset recursion in leaf count, then compares with the full rooted series and directly enumerated profiles.

The predecessor's twelve rational models and all 160 archived OEIS terms are reproduced. Source IDs and offsets are retained from its receipts; no new OEIS identification is claimed. OEIS reference data in the bundled predecessor retain their attribution and CC BY-SA 4.0 terms. The mathematical identities are written proofs, not Lean-checked declarations. See AUDIT.json and PROFILE_AUDIT.json for exact run totals.
