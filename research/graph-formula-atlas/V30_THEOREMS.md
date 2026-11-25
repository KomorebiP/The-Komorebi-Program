# Constrained Array Realization Calculus v30

Author: Komorebi P.

## Scope and lineage

This continuation implements the mathematical framework of the immutable predecessor `PREDECESSOR.zip` (Constrained Array Consolidation). It concerns finite constraint models with heterogeneous finite alphabets and nonnegative integral weights, arbitrary finite motifs on open rectangles, and fixed-width homogeneous strips. Mathematical statements distinguish unrestricted finite constructions from the resource guards in the implementation. No new OEIS source identification, Lean verification, literature priority, universal efficient algorithm, or general inverse eigenvalue solution is claimed. The predecessor's 168 accepted array IDs and 71,803-ID semantic union are retained, not increased. The original source attribution and license are in `source_receipts/` and the predecessor.

## 1. Weighted local factorization over integers

Let V be a finite variable set, with each variable v ranging over a finite domain D_v. A factor f on scope S is a nonnegative integer table, with absent entries interpreted as zero. The total weight is W(x)=product_f f(x|S); the partition function is Z=sum_x W(x). The support consists of assignments of positive weight. The zero model is detected separately.

For any nonzero table f, write g=gcd of its positive entries and t=f/g. For a cut A|B of its scope, let m_A,m_B be its unnormalized marginals and z=sum t. The exact cut criterion is

    z t(a,b) = m_A(a) m_B(b).

If the product of the marginal support sizes equals the support size of t and the equality holds at every present entry, it holds at every entry. The support containment is automatic and equality of cardinalities proves the rectangular support. Divide each marginal by the gcd of its entries to form primitive integer factors u,v. The product u*v is primitive: for any prime, choose one entry not divisible by that prime in each factor. Since the primitive t is rationally proportional to the primitive product, the proportionality scalar is 1 (compare gcd after clearing denominators). Thus t=u*v, exactly, without rational factor tables.

Recursively testing cuts yields the unique finest product partition. For uniqueness, normalize any nonzero nonnegative table to a probability distribution. If it is independent across two partitions, marginalize the second factorization on each block of the first, then multiply these marginals. This proves independence across their common refinement. Hence the finest partition exists and each recursive product split is consistent with it. Empty factors contribute scalars. Empty tables make the model zero. The local compiler caches repeated normalized factor tables, carries every extracted scalar, and connects only variables in the irreducible factor scopes. The resulting disjoint components give a safe global decomposition, but need not yet be the globally finest one.

## 2. Global replica obstruction (new exact test)

For a cut A|B, view W as a matrix M with rows indexed by assignments of A and columns by assignments of B. Define

    S = sum_(a,b) W(a,b)^2,
    C = sum_(a,a',b,b') W(a,b) W(a',b) W(a',b') W(a,b'),
    Delta = S^2 - C.

Then S=tr(M M^T) and C=tr((M M^T)^2). Expanding shows

    Delta = 2 sum_(a<a', b<b') [M_ab M_a'b' - M_ab' M_a'b]^2.

Equivalently this is twice the sum of products of pairs of squared singular values. Therefore Delta>=0 and Delta=0 iff rank(M)<=1. For a nonzero model this means rank exactly one. Because W is nonnegative, one can choose a positive anchor entry W(a0,b0), and the vanishing minors give

    W(a,b) W(a0,b0) = W(a,b0) W(a0,b).

This proves weighted factorization, including zeros, not merely pairwise correlation cancellation. Compute S by squaring every original factor table and applying the finite partition compiler. Compute C on two copies of every variable, multiplying four copies of each original factor with replica selections (A0,B0),(A1,B0),(A1,B1),(A0,B1). The sum over replicated assignments is C exactly. There is no need to construct the dense global W table; the replica network may itself still be expensive. The result is algebraic, not a new claim about the known matrix rank or purity identity.

Testing every bipartition of a nontrivial block, with recursion after a valid cut, produces the globally finest weighted partition by the uniqueness argument in section 1. Already-certified local components may be processed separately. A cut budget may halt the search; retained splits remain valid, but the result is explicitly marked incomplete. Other frontier resource limits raise an error. The algorithm is complete with unbounded resources, not polynomial in general. The zero model has no distinguished positive product decomposition.

### Anchored reconstruction

Let B_1,...,B_k be any certified product partition of a nonzero model and x_* a positive-weight assignment, with w_*=W(x_*). Define the restricted model W_j(x_j)=W(x_j,x_* outside B_j). Then

    W(x) * w_*^(k-1) = product_j W_j(x_j),
    Z * w_*^(k-1) = product_j Z_j.

Proof: write W=product_j f_j(x_j) over the positive-support factors. Each restricted W_j contains the anchor values of all other factors. Multiplying counts each other anchor value exactly k-1 times. The support also factors, so its cardinalities multiply without normalization. In the implementation each W_j is obtained by slicing the original factor tables; pinned variables are removed and scalar factors retained. No full weight table need be materialized. The normalization divides every resulting weighted count exactly. The `GlobalCompiled` engine implements counts, support ranking, unranking, exact one-site marginal masses, weighted sampling via independent component tickets, and convolution of additive-score histograms. Empty-variable positive models are handled as constant weights.

Example: f(x,y)=1 when x=y and 2 otherwise; g(x,y)=2 when x=y and 1 otherwise. Both are indecomposable locally, but f*g=2 identically. The local graph connects x and y; the replica obstruction is zero and the global compiler splits them. The independent audit also verifies a connected equality chain forced to one assignment by a unary constraint.

## 3. Separator realization and exact interface rank

Partition the variables as A union S union B, disjoint, and suppose no factor touches both A and B. Write

    W(a,s,b)=W_A(a,s) W_S(s) W_B(b,s),
    Z=sum_s W_S(s) Z_A(s) Z_B(s).

Assign a factor to A or B if it touches that side, and to S otherwise. For each separator assignment, sum independently over A and B; then sum over S. This is the conditional version of the disjoint-component product. It provides a general composition operation for connected systems. The marginalized weight matrix on A and B is

    M_ab=sum_s W_S(s) W_A(a,s) W_B(b,s).

It is a sum of at most d=product_(v in S)|D_v| outer products. Its rational rank is at most d; exact rank is the minimum number of unrestricted rational rank-one terms, by elementary rank factorization. Nonnegative rank or integral reconstruction may require more terms, and is not claimed equal to rational rank. The implemented `separator_tensor` returns the separator weights and the two restricted partition vectors. It validates the separator condition and independently checks conditional slices; it does not claim optimal separator discovery.

## 4. Complete finite frontier transfer

Take any ordering v_1,...,v_N of the variables. Charge each factor at the last variable in its scope. At layer i retain the values of exactly those assigned variables that occur in a factor not yet charged. Write F_i for this live frontier. On assigning the next variable a, evaluate all newly completed factors, multiply their values to obtain arc weight w, and forget values no longer needed. Reject weight-zero transitions. The successor state is the assignment to F_(i+1). Constant factors are carried separately.

Every full feasible assignment has exactly one labeled path in this layered directed acyclic graph, and every such path gives exactly one feasible assignment. The product of its arc weights, times the constant scalar, is W(x): each factor is charged exactly once, and each charged factor has all its variables available. Thus the sum of path weights is Z, and the count of positive paths is the support cardinality. Unreachable states need not be materialized. This proves completeness for finite domains and arbitrary finite factor scopes, not just lattice problems.

For uniform alphabet bound b and frontier width omega=max |F_i|, the number of potential states per layer is at most b^omega, and at most b outgoing assignment labels per state. Up to the cost of charging factors and integer arithmetic, the time is O(N b^(omega+1)); retaining the whole DAG for reversible coding costs at most O(N b^(omega+1)) stored transitions. The partition alone permits rolling layers. This is an order-dependent upper bound, not a complexity lower bound or an assertion of optimal width. Disjoint local/global components may dramatically reduce omega. The implementation has explicit reachable-state and transition-trial guards, and is intended as a reference correctness engine rather than a high-performance replacement for the predecessor C++ kernels.

### Backward recurrence and reversible coding

Let T_i(s) count suffixes and M_i(s) sum their weights. At a terminal state T_N=M_N=1. Recursively

    T_i(s) = sum_(a,t,w) T_(i+1)(t),
    M_i(s) = sum_(a,t,w) w M_(i+1)(t).

Given the domain's fixed value order, assign consecutive rank intervals of lengths T_(i+1)(t) to the feasible outgoing labels. Select the interval containing an input rank, subtract its starting rank, and continue. The reverse computation adds the lengths of the preceding intervals. Induction on the remaining layers proves a bijection between support assignments and integers from 0 through support cardinality minus 1. Across independent components use mixed-radix arithmetic. The fixed-length information capacity in bits is floor(log2 support cardinality), distinct from entropy under a nonuniform measure.

For weighted sampling, use intervals of length w M_(i+1)(t) and divide the selected local ticket by w before proceeding. Exactly w tickets map to each suffix ticket; induction proves each configuration has ticket multiplicity W(x), with constant scalar accounted for at the start. A uniformly random integer ticket in [0,Z) therefore samples the desired distribution exactly. This is an integer multiplicity sampler, not a claimed bijection between weighted tickets and configurations.

### Exact probability and additive statistics

Forward prefix weights times an arc weight times the backward suffix weight give the total mass of all assignments taking that arc. Summing by the assigned value gives all one-site marginal masses in one forward/backward pass. Arbitrary evidence is implemented by unary pinning, giving probability Z_evidence/Z for Z>0. Joint or conditional probabilities follow from this operation; computing each requested joint can require another compilation.

For a nonnegative integer additive observable g(x)=sum_v g_v(x_v), the histogram polynomial is H(t)=sum_x W(x)t^g(x). Choose an integer B>Z. Replace the unary weight of every variable by an additional B^(g_v(a)) factor, and evaluate the same partition compiler. The resulting integer is H(B). Every coefficient is <=Z<B, so repeated base-B division recovers the full histogram exactly, including its zeros. Moments and cumulants follow from the polynomial by ordinary differentiation, where defined. This does not bound the bit cost of a large-degree histogram. The global anchored engine convolves component histograms and divides by the common anchor normalization.

## 5. Arbitrary finite motifs and the boundary rule

An original motif is a finite list of distinct integer offsets with a nonnegative integer table. Instantiate it at every translate wholly contained in the rectangular domain, then factor the table. The original boundary criterion is essential: a smaller factor may fit in an extra translate where the original motif would not have fit. Such a constraint must not be added. Negative offsets, holes, multivalued alphabets, non-square motifs and directional asymmetry are allowed. For example, the pattern pair 000/001 reduces to forbidding 00 on the first two positions, but a row of length two contains no original triple and is not restricted. The exact general model also allows irregular domains supplied directly as finite variable sets with explicit factor instances. The rectangle helper uses open boundaries; periodic constraints must be instantiated separately.

The prior lattice coset, monotone and independent-set formulas remain special optimizations. They are not prerequisites for the new compiler. All previously established formulas and inherited evidence statuses remain in the predecessor.

## 6. Exact homogeneous strip automaton

Fix alphabet b, width W, and finitely many translation-invariant motifs; optional unary weights depend on column and symbol, not height. Let R be the largest vertical span of any motif fitting the width. When appending a row, test just those original motifs whose largest row is the appended row. The state is the last min(R,h) rows, including short warm-up states. The weight of a transition multiplies the new row's site weights and the completed factors. Multiple row choices reaching the same state contribute their sum to the adjacency. Retain only reachable states, starting at the empty history. Row histories form a finite set of size at most sum_(j=0)^R b^(W*j). Every height h has exactly the desired weighted count

    a(h)=e_empty^T T^h 1,    G(x)=e_empty^T (I-xT)^(-1) 1.

The proof is the same one-charge-per-factor path bijection; short histories preserve open boundaries, including height zero. No claim of finite recurrence is made for growing width or arbitrary time-dependent factors. The strip code constructs full row histories and then quotients them. It does not automatically produce the optimal symbolic polyphase product representation for all fixed widths; the finite rectangle engine does perform canonical local factorization first.

### Weighted quotient and minimal scalar recurrence

Initialize all states in one class (terminal weight 1). Repeatedly split classes according to the total outgoing weights into every current class. At a stable partition, row sums into each target class are independent of the representative. Hence the quotient matrix intertwines the class-constant subspace and preserves every marked initial-to-total count. This is an exact equitable quotient, not necessarily a minimum positive realization.

Let D be the quotient dimension. The minimal scalar annihilator exists by Cayley-Hamilton. It is a monic divisor in Q[E] of the monic integral characteristic polynomial, hence integral by Gauss's lemma. The compiler discovers a candidate from modular Berlekamp-Massey and CRT, with exact rational fallback. It uses a finite prefix of length >=2D. For an order r candidate Q=[1,q_1,...,q_r], test D consecutive exact integer residuals starting at index r. The residual sequence is a linear functional of powers of the D-state matrix and therefore obeys its characteristic recurrence. These D zeros imply all subsequent residuals vanish. Minimality is independently certified by a nonsingular r-by-r leading Hankel minor modulo a checked prime, or exact rational rank. A sequence of smaller order would have Hankel rank at most that smaller order. Retain trailing zero entries of Q when the forward annihilator contains x factors (finite transients). The ordinary numerator P is the first r coefficients of Q(x)G(x), giving the certified rational generating function.

With a uniform integer bound b^(Wh) on unweighted counts, or a corresponding exponential bound for fixed integral weights, the predecessor's exact coefficient-packing floor/remainder construction supplies a direct a(h) formula. A formula of this type is not by itself a speedup or a low-complexity elementary expression.

## 7. Positive single-mark graph construction and obstruction

For any monic integral annihilator p of degree r, use the v29 transpose companion M and the embedding Jx=(-w^T x,x), with w_j=1+max(0,p_(j-1)), g=w^T M, beta=1+max(0,max_j ceil(g_j/w_j)), K=beta+w_r. Form columns B_0=K e_0+J e_r and B_j=w_j B_0+J M e_j. The first row is (beta,w_1 beta-g_1,...,w_r beta-g_r), the last row is (1,w_1-p_0,...,w_r-p_(r-1)), intermediate rows are shifts. Every entry is nonnegative. Directly BJ=JM and (B-KI)e_0=J e_r. The canonical impulse with initial coordinates (0,...,0,1) is (E-K)c for c(n)=(B^n)_(1,0). If the ordinary numerator of the target is P, use the Laurent numerator N(x)=x^(r-1)P(1/x), padding P to r coefficients. The target is N(E)(E-K)c exactly. The new compiler constructs sparse columns, verifies every intertwining column, and replays the sequence. This is the inherited all-index theorem, now automated for new strip models.

The graph-size lower bound r follows from Cayley-Hamilton for a single marked walk count followed by fixed polynomial shifts. For an r-vertex realization, the characteristic polynomial must equal p. Newton identities compute its required moments s_n. A nonnegative integer adjacency counts rooted closed edge walks with parallel edges interpreted as distinct. Primitive cyclic orbits give

    o_n=(s_n-sum_(d|n,d<n)d o_d)/n >=0.

A negative o_n rules out r vertices; the r+1 construction is then sharp. Passing the finite obstruction check is not a positive realization at size r. The compiler reports the interval [r,r+1] unless a certified obstruction closes it. It does not solve the classical real NIEP or the three inherited unresolved widths 4,6,10. Graph loops and weights are permitted. The large graph constructions are not needed to evaluate the reduced counts.

## 8. Verification, source interpretation and reproducibility

`verify_framework.py` independently enumerates finite models, checks two-by-two minors without using the replica formula, tests exact global decomposition, primitive integer factors, weighted tickets, support codes, conditional probabilities, histograms, arbitrary motif boundaries, separator slices and rank bounds. It independently compares fixed-height finite models to the strip automaton, checks exact recurrence residuals and Hankel ranks, and verifies sparse graph lifts. Its deterministic report is `AUDIT.json`.

`oeis_adapter.py` lowers the retained conservative grammar into the generic motif model. The retained prefixes (source credit OEIS Foundation Inc., CC BY-SA 4.0, pinned revision c5bd71de9eee0894df1301baa4f43f6431d8a08d) were copied unchanged from the predecessor compiler; the `OEIS_REPLAY.json` audit independently evaluates the first two terms where within the resource guard, with at least one term for every one of the 168 accepted IDs. These are new implementation comparisons, not new OEIS admissions or proofs of every source interpretation. A synthetic positive/mismatch/offset fixture checks scanner rejection behavior. The full corpus is absent. The generic scanner can be run against a local checkout with receipt hashes and finite-match status, but no full-corpus scan was completed. The eight-term generic replay hit the execution timeout and supplies no additional accepted comparisons. The source data and original formula catalog remain unchanged in the predecessor.

## 9. Mathematical boundary of completion

This framework is complete as an exact finite representation and reconstruction calculus: arbitrary finite factors can be evaluated by the frontier fallback, the globally finest nonzero weighted factorization has a complete finite criterion, and every fixed-width homogeneous model has a rational generating function with finite all-index certificates. It is not a promise of efficient evaluation, a uniformly small transfer matrix, an elementary closed form, a solution of arbitrary infinite systems, or resolution of general graph minimization. For example, a Boolean CNF formula is a finite constraint model with one indicator factor per clause. Counting its satisfying assignments is exactly the partition function at unit weights, so arbitrary finite instances include the general counting satisfiability problem. Exact methods may require exponential work. Literature comparisons, performance benchmarks with bit complexity, Lean formalization, broader semantic parsing and new corpus admissions are separate future tasks.
