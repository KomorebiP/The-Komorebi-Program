# Structural-core graph realization calculus v32

Author: Komorebi P.

## 0. Scope and lineage

Connected, finite, unlabeled, undirected **simple** graphs are counted up to isomorphism. A leaf is a vertex of degree one. The cycle rank is g = e - v + 1. The variable x counts vertices, not edges. The v31 predecessor is retained byte for byte in PREDECESSOR.zip, including its source receipts and licenses. Its 19 checksums were independently verified. The extracted v31_core_calculus.py is exactly the predecessor compiler, and supplies its rooted-tree series engine to the independent unicyclic construction. All proofs below are written mathematical arguments, not Lean-verified declarations. Classical ingredients are degree sums, subdivision cores, Burnside's lemma, the dihedral cycle index, cyclotomic factorization and polynomial CRT. No priority or new OEIS identification is claimed.

The isolated vertex (g,k)=(0,0) has generating function x. The class (0,1) is empty. A cycle-only graph (g,k)=(1,0) has generating function x^3/(1-x), and its bipartite subclass has x^4/(1-x^2). All other nonempty classes have either g=0,k>=2, g=1,k>=1, or g>=2,k>=0. The path class (0,2) is included in the general construction. Empty or exceptional classes must not be subjected to the general positive-power asymptotic formula without these qualifications.

## 1. Canonical finite cores

Suppress all vertices of degree two in a connected graph outside the isolated-vertex and cycle-only classes. A maximal path through degree-two internal vertices becomes an edge of a core multigraph H. A path which starts and ends at the same retained vertex becomes a loop. The core is connected, may have loops and parallel edges, and has all vertex degrees in {1,3,4,...}. A loop counts twice toward degree. Suppression preserves cycle rank and leaf count.

Write k for the number of leaves, b_j for the number of degree-j vertices (j>=3), v for the number of core vertices, e for the number of core edges, and b=sum b_j. The handshake identity gives

    sum_{j>=3} (j-2)b_j = k+2g-2.
    v = k+b; e = v+g-1.
    b <= k+2g-2; e <= D=2k+3g-3.

Equality in the last inequality holds exactly when every nonleaf core vertex has degree three. Thus for each fixed (g,k) there are finitely many core isomorphism classes, and the degree profiles themselves are given by integer partitions of k+2g-2. Fixing a profile gives the sharper edge bound e=v+g-1. The core of a path is a single edge.

Conversely, recover a graph by replacing every core edge with a path of length ell>=1, or equivalently inserting s=ell-1 internal vertices. Distinct edges have disjoint inserted vertices. For simple graphs the exact admissibility restrictions are:

* A loop requires s>=2, since its replacement must be a simple cycle of length at least three.
* In a nonloop bundle of parallel edges, at most one edge may have s=0.
* There are no other restrictions.

Every admissible expansion is simple and connected; all core vertices preserve their degrees. A graph isomorphism induces a core vertex permutation preserving the edge bundles and their lengths. Conversely, any such permutation, together with a bijection matching the equal-length paths in each bundle, extends to a graph isomorphism. In particular there is no need to distinguish orientations of a subdivided loop. This gives an exact bijection, not just a correspondence of counts.

## 2. Explicit finite-core generating function

A bundle is an unordered pair of core endpoints, possibly equal for a loop, with positive multiplicity m. Let

    J_m(x) = product_{i=1}^m (1-x^i), with J_0=1.
    A_m(x) = (x^(m-1)+x^m-x^(2m-1))/J_m(x).
    L_m(x) = x^(2m)/J_m(x).

For a nonloop bundle, the multiset of insertion counts is either a multiset of m positive integers or one zero and a multiset of m-1 positive integers. Their generating functions are x^m/J_m and x^(m-1)/J_(m-1), respectively. Adding them gives A_m. For a loop bundle, all m insertion counts are at least two, giving L_m. These partition formulas follow by writing each sorted nonnegative list as its successive nonnegative differences. A difference contributes a multiple of one of 1,...,m to the total.

Let Gamma(H) be the group of vertex permutations preserving all multiplicities, including loops. For sigma in Gamma(H), let O be an orbit of bundles under sigma, with b_O bundles, each of common multiplicity m_O. Put F_O=A_m for a nonloop orbit, and F_O=L_m for a loop orbit. An assignment fixed by sigma has the same sorted insertion multiset on every bundle in O. Its total contribution is F_O(x^b_O). Burnside's lemma on each finite coefficient therefore gives the all-index identity

    G_H(x) = x^v / |Gamma(H)| * sum_{sigma in Gamma(H)}
                    product_{bundle orbits O of sigma} F_O(x^b_O).

Sum over all core isomorphism classes with the prescribed parameters to obtain G_(g,k), or over the cores of a prescribed profile to obtain its refinement. The computation only enumerates vertex permutations and multisets of lengths, not the much larger full edge-permutation group.

## 3. Universal denominator, exact growth and recurrence bound

For any term of the preceding Burnside sum, the denominator is a product of factors 1-x^(b i), for each bundle orbit of size b and multiplicity m and for 1<=i<=m. At a primitive d-th root of unity, the pole contribution of that orbit is at most

    floor(m*gcd(b,d)/d) <= bm/d.

Since sum bm=e, the pole order is at most floor(e/d). Consequently every core generating function, and hence the whole class, has a denominator dividing

    Q*_D(x) = product_{i=1}^D (1-x^i)
            = product_{d=1}^D Phi_d(x)^floor(D/d),

where Phi_1=1-x. Its degree is D(D+1)/2. For a fixed profile replace D by its exact edge count e. A numerator degree bound before reduction is deg Q*_D + max_H(v+e). Indeed the numerator of a summand has degree at most v+2e, while its denominator has degree at least e. After summing and clearing Q*_D, the numerator is an integer polynomial, since it is the product of an integer polynomial and an integer formal series. These bounds also justify exact reconstruction from finitely many terms, with further terms reserved for independent checks.

At x=1 only terms in which every bundle is fixed can attain pole order e. Let K_H be the kernel of the action of Gamma(H) on the bundles. Since A_m and L_m each have leading coefficient 1/m! after multiplication by (1-x)^m, the mass of H is

    M(H) = |K_H| / (|Gamma(H)| * product_bundles m!).

In particular M(H)>0. The leading contribution to the coefficient at n is M(H)*n^(e-1)/(e-1)!. Other roots have pole order at most floor(e/2)<e, so do not affect this leading term. Maximal trivalent cores always exist for the nonexceptional classes: start with a single edge for trees, a loop with a leaf attached for g=1,k=1, or the two-vertex triple-edge core for g=2,k=0. A new leaf is added by subdividing one edge and attaching a leaf to the new vertex. An additional independent cycle is added by replacing an edge uv by u-a, two parallel a-b edges, and b-v. These operations preserve the degrees of existing vertices and create degree-three vertices; all resulting multigraphs have admissible simple expansions. The g>=2,k=0 construction can use a nonloop edge throughout. The path base case already has e=1.

Thus, for every nonexceptional class,

    a_(g,k)(n) ~ C_(g,k)*n^(D-1),
    C_(g,k) = sum_{H: e(H)=D} M(H)/(D-1)! > 0.

The corresponding result for a nonempty fixed profile uses e and the sum over its cores instead. The pole at 1 is exactly D for the full class and exactly e for its profile. The reduced denominator's degree is the minimal eventual scalar constant-coefficient recurrence order. Its least eventual quasipolynomial period is the least common multiple of the orders of roots of unity actually appearing as poles, not just an upper bound. For the minimal order, a smaller recurrence would give a denominator of smaller degree after discarding a finite prefix, contradicting reducedness; discarding a finite prefix cannot remove a pole at a nonzero root. For the period, residue polynomials on a period p have poles only at p-th roots, while the partial fractions at roots of unity produce a period equal to the indicated least common multiple. The finite polynomial part is separately retained to give the correct initial terms.

## 4. Bipartite transfer calculus, exact parity and a universal proportion theorem

A connected expanded core is bipartite if and only if there is a two-coloring c of its core vertices such that for each nonloop edge uv its path length ell is congruent to c(u)+c(v) modulo 2, and for each loop ell is even. The coloring is then unique up to global color reversal, since the graph is connected. Count the pair consisting of the coloring class and the sorted bundle insertion multisets. Every valid expanded graph corresponds to exactly one such pair modulo Gamma(H).

For a nonloop bundle with endpoints of the same color, all insertion counts are positive odd integers. For endpoints of opposite color, they are nonnegative even integers with at most one zero. A bipartite loop must have even length at least four, so its insertion counts are odd integers at least three. The exact bundle generating functions are therefore

    A_same,m(x) = x^m/J_m(x^2),
    A_opp,m(x) = A_m(x^2),
    L_bip,m(x) = x^(3m)/J_m(x^2).

For sigma in Gamma(H), sum over the coloring classes fixed by sigma (sigma may preserve or globally reverse the colors). Within each orbit of bundles the endpoint parity is constant. Apply the formula of section 2 with the appropriate one of these three factors and average over Gamma(H). This is a rational expression for the bipartite count, with denominator dividing

    Q_bip,D(x) = product_{i=1}^D (1-x^(2i)).

At a primitive d-th root the pole order is at most floor(e*gcd(d,2)/d) for a core of e edges. Hence only x=1 and x=-1 can contribute to growth of degree e-1. At x=1 the leading pole coefficient is M(H)*2^(-g). To prove this exactly, first note that every element of K_H fixes every coloring class: when the connected core has at least three vertices, a vertex incident to two distinct nonloop bundles must be fixed as their intersection, and then connectedness forces every vertex fixed. Such a vertex exists in a connected underlying graph on at least three vertices. For one vertex the group is trivial, and for two vertices a kernel element can at most swap the two, fixing the same/opposite coloring class. Thus each sigma contributing at order e permits all 2^(v-1) coloring classes. Each bundle of m edges contributes a factor 2^(-m) to the mass at x=1. Multiplying gives 2^(v-1-e)=2^(-g).

At x=-1 the leading coefficient for each color class differs from its positive leading coefficient at x=1 by the sign

    (-1)^(v+e+sum_{u} deg_H(u)c(u)).

Indeed each insertion count s=ell-1 has sign determined by the endpoint colors, including the odd insertion counts of loops. If there is an odd-degree vertex, summing the signs over all colorings modulo global reversal gives zero: the sign is invariant under global reversal because the total degree is even, and flipping one odd-degree vertex pairs opposite signs. If all core degrees are even the sign is constant (-1)^(g-1). These are all the possible top-order contributions at -1.

It follows for every nonempty fixed profile with at least one odd-degree vertex that

    b_profile(n)/a_profile(n) -> 2^(-g).

For an all-even profile, the bipartite count is identically zero unless n congruent to g-1 modulo two. On that parity subsequence the limiting ratio is 2^(1-g). This parity restriction is exact, because n=v+sum s has the stated parity for every admissible bipartite expansion. For the entire (g,k) class the maximal cores are trivalent with leaves of degree one, and thus have odd-degree vertices; the lower-degree cores contribute only lower-order terms. Consequently, for all nonexceptional (g,k),

    lim_{n->infinity} b_(g,k)(n)/a_(g,k)(n) = 2^(-g).

This is a limit for each sufficiently large integer n, not merely an average over parity classes. For the excluded cycle-only class the bipartite fraction alternates, so it has no such limit.

## 5. Independent unicyclic construction and closed asymptotic constant

Use the rooted-tree generating functions T_k(x) from v31. Let T(x,y)=sum_{k>=1} T_k(x)y^k mark vertices and rooted leaves. A cycle vertex together with its multiset of attached rooted trees has generating function

    B(x,y) = x + T(x,y) - xy.

The cycle vertex is never a leaf of the full graph; each attached rooted leaf has degree one in the full graph. The empty multiset contributes x, and B_1=T_1-x=x^2/(1-x); for i>=2, B_i=T_i. Put B_j^sub = B(x^j,y^j), in particular B_2^sub=B(x^2,y^2). Every unicyclic graph is uniquely a dihedral orbit of a cycle of length m>=3 with these decorated vertices.

For length m the rotation term of the dihedral cycle index is (1/(2m))*sum_{j|m} phi(j)(B_j^sub)^(m/j). For odd m, reflections contribute B*(B_2^sub)^((m-1)/2)/2. For even m, they contribute [B^2*(B_2^sub)^((m-2)/2)+(B_2^sub)^(m/2)]/4. Sum the geometric series over m>=3 and subtract the length-one and length-two rotation terms. The exact bivariate generating function is

    U(x,y) = -(1/2) sum_{j>=1} phi(j)/j * log(1-B_j^sub)
             + (1+B)^2/(4*(1-B_2^sub))
             - (1+4*B+2*B^2+2*B_2^sub)/4.

All operations are well-defined as formal series in x. At fixed positive leaf count k the log terms reduce to finite sums: the coefficient of y^k can use only j dividing k, and for each such j the positive-leaf part is expanded around the constant-in-y term x^j. Explicitly, the contribution of the rotation term is

    1/2 sum_{j|k} phi(j)/j * sum_{l=1}^{k/j} 1/l *
      [y^(k/j)] (sum_{i>=1} B_i(x^j)y^i / (1-x^j))^l.

Only i<=k/j are needed. Reflection terms are finite in each positive y degree by geometric-series expansion around x^2. This supplies an independent rational construction without enumerating general multigraph cores. The coefficient with k=0 is x^3/(1-x).

Let c_i=(2i-3)!!/i! with (-1)!!=1, and C(z)=sum_{i>=1} c_i z^i=1-sqrt(1-2z). From v31, B_i(x) has leading coefficient c_i at x=1 of pole order 2i-1 for i>=1. Hence in the rotation term only j=1 reaches the pole order 2k. Its leading coefficient is

    (1/2)[z^k](-log(1-C(z))) = 2^(k-1)/(2k).

In the reflection term, to reach order 2k all k leaves must appear in the factor (1+B)^2, with only one B factor having positive leaf count. Its leading coefficient there is 4c_k, the other factor 1/(1-x^2) contributes 1/2, and the outer 1/4 yields c_k/2. All terms with at least one positive-leaf decoration from B(x^2,y^2) have lower order; the finite short-cycle subtraction also has lower order. Therefore for every k>=1,

    u_(1,k)(n) ~ [2^(k-1)/(2k) + (2k-3)!!/(2 * factorial(k))]
                       * n^(2k-1)/(2k-1)!.

For example the constants for k=1,2,3 are 1, 1/8, 11/1440. The compiler verifies the closed constant against the exact rational function at 1, and compares the two independent constructions for k=1..4 by polynomial cross multiplication.

## 6. Sharper cyclotomic denominator for unicyclic graphs

For k>=1 let E_d(k) be the following upper bounds on pole order at primitive d-th roots:

    E_1(k) = 2k.
    E_2(k) = 2 floor(k/2).
    E_d(k) = 2 floor(k/d)-1 + 1_{d divides k},  3<=d<=k.
    E_d(k) = 0, d>max(k,2).

Thus the unicyclic reduced denominator divides product Phi_d^E_d. We prove all divisor-pole orders exactly and the entire order-two result; the bounds for the other primitive roots can have leading-coefficient cancellations in principle. Through k=24 all the displayed bounds are attained, by exact division of the compiled rational polynomials. This finite saturation does NOT prove that every bound is attained for arbitrary k.

For d>=3, in the finite rotation expansion of section 5, a term indexed by j dividing k with d dividing j has pole order at most 2k/j. If d does not divide j, the order of x^j at the root is h=d/gcd(d,j)>1. The v31 rooted-tree pole bound gives at most 2 floor(i/h)-1 for a singular factor B_i(x^j). Summing over singular factors yields at most 2 floor(k/lcm(d,j))-1, hence at most 2 floor(k/d)-1. The reflection and short-cycle terms obey the latter bound too: 1-x^2 is regular at a primitive d-th root for d>2, and each singular factor from B(x,y) or B(x^2,y^2) consumes at least d leaves for its first pole. Adding the floor bounds over factors gives the result. When d divides k, the term j=d is the unique rotation contribution with order 2k/d, while reflections and the other terms have smaller order. Let k=ad and zeta be a primitive d-th root. The nonzero leading coefficient is

    lim_{x->zeta}(1-x^d)^(2a) U_k(x)
        = phi(d) * 2^(a-1)/(2*d*a),   d>=3.

This follows from the rotation expansion and -log(1-C(z)) = -(1/2)log(1-2z), with x^d tending to 1. It proves exact order 2a, uniformly over all multiples of d.

For d=2 put t=1-x^2. The reflection term is (1+B)^2/(4(1-B(x^2,y^2))). Define D_i=binom(2i,i)/2^i; then [y^(2i)]1/(1-B(x^2,y^2)) has leading coefficient D_i and order 2i+1 in t, since sum D_i z^i=1/(1-C(z))=(1-2z)^(-1/2). In (1+B)^2, the coefficient of y^0 is (1+x)^2, which vanishes twice at -1. For a positive even b, the coefficient of y^b has pole order at most b-2: a single singular B_b is multiplied by 2(1+x), reducing its order, and any positive-leaf split among two B factors also gives order at most b-2 by the v31 bounds. For b=1 the coefficient is 2(1+x)B_1 and vanishes once. For odd b>=3, its order is at most b-2; the only contribution at that order is 2 B_1 B_(b-1). Here B_1(-1)=1/2 and the v31 leading-pole filter at -1 gives

    lim_{x->-1} t^(2j-1) B_(2j)(x) = -c_j/4,   j>=1.

The latter is the v31 formula H_(2,0)=(-1)/(1-(-1))*1/2=-1/4; the rooted-tree formula transfers to B_(2j) unchanged.

If k=2a, a>=1, these estimates show that the reflection term has pole order at most 2a-1. The unique highest rotation term j=2 gives

    lim_{x->-1} t^(2a) U_(2a)(x) = 2^(a-1)/(4a).

If k=2a+1, a>=1, rotations and the short-cycle correction have order at most 2a-1. In the reflection term the coefficient with b=1 contributes D_a/2 before the factor 1/4, because (1+x)/t tends to 1/2. The terms b=2j+1, j>=1, contribute -c_j D_(a-j)/4 before that factor. Since C(z)*(1-C(z))^(-1)=(1-C(z))^(-1)-1, the sum of c_j D_(a-j) for j=1..a equals D_a. Hence

    lim_{x->-1} t^(2a) U_(2a+1)(x) = D_a/16.

Both expressions are strictly positive. The k=1 case has no pole at -1, directly from U_1=x^4/(1-x)^2. This closes the order-two classification for all k. The implementation conservatively used exponent 2 floor(k/2)+1 in its reconstruction bound, then removed the extra factor exactly. The final reduced models use the proven sharper order.

For k>=2 the new universal denominator degree bound simplifies to

    R_k <= k(k+2)+1-1_{2 divides k}-sum_{d=1}^k phi(d).

Indeed the rooted-tree universal exponents of v31 gain one at d=1, one at d=2, and one at each d>=3 dividing k. Use sum_{d|k} phi(d)=k. Equality is certified through 24 leaves, not beyond. For k=1 the exact order is 2. These are eventual recurrence orders, allowing an initial polynomial part. The 24-leaf model has minimal eventual order 444 and least eventual period 5354228880.

## 7. Direct all-index residue formulas

For a computed reduced generating function P/Q, write P/Q=S+F/Q with deg F<deg Q. Factor Q=product Phi_d^e_d. For each primary factor f_d=Phi_d^e_d, compute

    N_d = F*(Q/f_d)^(-1) mod f_d,
    L_d = N_d*((1-x^d)/Phi_d)^e_d.

Then P/Q=S+sum_d L_d/(1-x^d)^e_d, and deg L_d<d e_d. Every inverse exists because the primary factors are pairwise coprime. Polynomial CRT proves equality by multiplication by Q. To evaluate at vertex count n, write n=dq+r, 0<=r<d, and L_d=sum l_(d,i)x^i. The contribution is

    sum_{j=0}^{min(q,e_d-1)} l_(d,r+dj) binom(q-j+e_d-1,e_d-1).

Sum the contributions and add [x^n]S. This is an explicit nonrecursive all-index formula. The lane file stores the full finite polynomial part, even if its degree exceeds one, unlike the earlier tree-only implementation. Exact primary fractions are reassembled and compared by polynomial identities; coefficient checks are additional tests. The minimal eventual period can be enormous, but its residue representation need not list a polynomial for every residue of that entire period.

## 8. Worked small examples

Unicyclic graphs with one leaf:

    U_(1,1)=x^4/(1-x)^2,
    a_(1,1)(n)=n-3 for n>=4 (zero before).

Unicyclic graphs with two leaves:

    U_(1,2)=x^5(2+2x-x^2)/((1-x)^4(1+x)^2),
    16 a_(1,2)(n)=2n^3-12n^2+15n+6+(n-6)(-1)^n, n>=2.

The count is zero at n=0,1. The latter formula follows by partial fraction expansion including the finite polynomial part -x. Initial nonzero values at n=5,6,7,8 are 2,6,13,24.

Bicyclic graphs with no leaves:

    G_(2,0)=x^4(1+x)/((1-x)^2(1-x^3)).
    q=floor((n-4)/3), n>=4.
    a_(2,0)(n)=(q+1)(2n-7-3q),

with zero before n=4. Its coefficient follows by summing 2(n-4-3j)+1 over 0<=j<=q. Its bipartite counterpart is

    G_bip,(2,0)=x^5/((1-x)(1-x^2)(1-x^3)).

The respective leading terms are n^2/3 and n^2/12; their ratio tends to 1/4 as proved independently in section 4.

For reference, the leafless classes with cycle ranks 2,3,4 have exact eventual orders 5,15,29, least eventual periods 3,12,60, and leading coefficients 1/3,37/5760,137/2322432, respectively. Their full numerators and denominators are in GRAPH_MODELS.json; bipartite versions are in BIPARTITE_MODELS.json. The model files use vertex index n starting at 0. These formulas are mathematical models, not claims of new OEIS source admissions.

## 9. Generalization boundaries and next target

The finite-core construction applies to arbitrary fixed cycle rank and leaf count and to all feasible exact branching-degree profiles. Enumeration of core representatives in the implementation is deliberately bounded. It does not provide a runtime guarantee for large simultaneous parameters. When the cycle rank or leaf count is allowed to grow without bound, the finiteness argument no longer yields a single rational generating function; one must not infer general graph-enumeration rationality. The sharper unicyclic bound uses the v31 rooted-tree pole theorem, whose assumptions and proof are retained in the predecessor.

A next target is arbitrary automorphism-invariant restrictions on the insertion lengths, in particular congruences, marked distances, girth, bounded diameter and specified block structures. Each has a finite-core formulation, but a general exact rational compiler for all such restrictions is not implemented in v32. Another target is a uniform proof of the nondivisor primitive-root pole orders beyond the computed range, and closed mass formulas for arbitrary g rather than enumeration of trivalent cores. No novelty comparison, Lean formalization, full OEIS scan or GitHub update was performed in this continuation.
