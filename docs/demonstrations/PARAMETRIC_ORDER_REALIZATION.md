# Parametric minimum order and joint incidence compression

**Author: Komorebi P.**  
**Version:** 3.4, 2026-11-25  
**Status:** Mathematical proofs and exact finite computational tests. Not Lean certified or independently peer reviewed.

Predecessor: [Minimum-order realization of bipartite cyclic rank four, v3.3](https://github.com/KomorebiP/The-Komorebi-Program/blob/main/docs/demonstrations/MINIMUM_ORDER_REALIZATION.md). All six entries of its checksum manifest matched. Its verification program was not rerun. This continuation eliminates labeled inner subset enumeration for the scalar and source-group optimization problem, proves eventual affine periodicity for arbitrary fixed inner data and for their finite union, and obtains a universal exact eventual period for the unrestricted scalar minimum and the group (1,1).

## 1. Joint composition-capacity criterion

Use the rank-four incidence model of v3.2. There are b root neighbors, a binary inner incidence P with nonzero rows, a_i=|S_i|, t_j=sum_{i:j in S_i} a_i, and q=sum_i a_i^2=sum_j t_j. Put B_i=sum_{j in S_i}t_j and D_i=e a_i-B_i. Outer vertices correspond to nonempty subsets of inner vertices and have weight equal to the sum of their a_i. Their weighted loads must equal D_i. The scalar domain is b>=1, e>=1, 0<q<be. The source factors are (1,1,g,k), where g=gcd_i a_i and k is the gcd of the t_j-t_1 and all used outer weights.

Group root neighbors by their t_j values. Write m_t for the number of neighbors with load t. Enumerate nonnegative integer histograms with sum_t m_t=b and sum_t t m_t=q. These are finite. For an inner vertex introduce a nonzero composition c=(c_t), 0<=c_t<=m_t, with weight a(c)=sum_t c_t and B(c)=sum_t t c_t. Let n_c be its multiplicity. The necessary aggregate conditions are

$$\sum_c a(c)^2 n_c=q,\qquad \sum_c a(c)c_t n_c=t m_t.$$

For each individual root neighbor j of load t and each composition c choose a nonnegative integer d_{jc}. The exact conditions are

$$\boxed{\sum_c a(c)d_{jc}=t,\qquad \sum_{j:t_j=t}d_{jc}=c_t n_c,\qquad 0\le d_{jc}\le n_c.}$$

They are necessary and sufficient for the inner incidence. For each pair (t,c), construct a binary incidence block between the m_t root neighbors and n_c inner vertices, with row degrees d_{jc} and uniform column degree c_t. The bounds and total sum suffice: assign each row to distinct columns of currently smallest degree. Their degree spread stays at most one by induction, and the final total is c_t n_c, so every column has the desired degree. Blocks concern disjoint edge sets, and their union gives the prescribed t_j and compositions. This is the same uniform-column degree lemma as v3.3. The energy equation follows by summing the aggregate equations and is retained as a useful bound.

For each feasible inner signature use the outer composition-capacity construction of v3.3. Group inner vertices by weight w, with index set I_w and size n_w. For an outer composition c with 0<=c_w<=n_w, not all zero, put H_c=sum_w w c_w. For multiplicity N_c and individual incidences d_ic, impose

$$\sum_c H_c d_{ic}=D_i,\qquad \sum_{i\in I_w}d_{ic}=c_w N_c,\qquad 0\le d_{ic}\le N_c.$$

These conditions construct the outer incidence by the same block lemma. For each feasible inner candidate, reject negative D_i, impose the desired gcds, and minimize 1+b+sum_c n_c+sum_c N_c. Inner multiplicities are bounded by q, and outer multiplicities by sum H_c^2 N_c=eq-sum t_j^2. Hence this is a finite exact optimization, without enumerating labeled neighbor subsets in either layer. A single inner witness for each signature (sorted t_j, sorted pairs (a_i,B_i)) suffices for minimum order and source-group existence: these data determine every remaining constraint and the gcd of the t_j differences. This does not enumerate every nonisomorphic incidence graph; different graphs can have the same signature. The composition and capacity search can still be large.

## 2. Homogeneous growth rate from a small rational LP

Fix an inner signature and positive candidate k, and set g0=gcd_j(t_j-t_1) (zero if all differences vanish). If k does not divide g0, that group is impossible. Restrict outer compositions to H_c divisible by k. Exact gcd k will be enforced separately. A homogeneous increment of e by a positive integer E requires extra weighted load E a_i at inner vertex i, with no change in the inner data. The minimum rational outer cost per unit of e is

$$\boxed{\rho=\min_{x_c\ge0}\sum_c x_c,\qquad \sum_c H_c c_w x_c=n_w w\quad\text{for every weight class }w.}$$

Here x_c is the number of outer vertices of composition c per unit of increment. Necessity follows by summing the homogeneous weighted loads within each weight class. Conversely any rational feasible x_c gives uniform rational degrees c_w x_c/n_w for each vertex of class w. These satisfy the capacity bounds because c_w<=n_w. Choose E clearing the denominators of x_c and c_w x_c/n_w. The integer block lemma constructs a homogeneous increment with N_c=E x_c and those degrees scaled by E. The feasible rational LP is bounded because H_c>0 and summing the equations with weights w gives sum H_c^2 x_c=q. A minimum is attained at a rational extreme point (an independent column support may be found by finite linear algebra). Clearing its denominators gives a homogeneous pump of period P0=E and cost C0=E rho. It is an actual collection of additional distinct outer vertices. Its weights need only be divisible by k, not have exact gcd k: appending it to a graph already of exact group k preserves that group. The slope depends only on the multiset of inner weights and k, not on the arrangement of the inner incidence. Infeasibility means no positive homogeneous increment exists.

## 3. Explicit finite generators for all affine parameters

Put e_min=floor(q/b)+1. Homogenize the outer composition-capacity equations with variable z>=0, writing e=e_min z+y, y>=0, and adding nonnegative slack variables s_ic with d_ic+s_ic=N_c. Use load equations

$$\sum_c H_c d_{ic}-e a_i+B_i z=0,\qquad \sum_{i\in I_w} d_{ic}=c_w N_c.$$

Together with the capacity/slack equations these define a pointed rational polyhedral cone of nonnegative variables. Integer points with z=1 represent affine realizations with k dividing the second Smith factor, and points with z=0 are homogeneous increments. The energy identity becomes

$$\sum_c H_c^2 N_c=eq-z\sum_j t_j^2.$$

In particular every nonzero cone point has e>0: e=0 forces z=y=0, all N_c=0 and hence d_ic=s_ic=0. Thus for fixed z=0 or 1 and bounded e, all variables are bounded integers.

We give an explicit finite generating bound, not merely an appeal to eventual integer programming behavior. Enumerate the primitive integral extreme rays of the cone. They can be found by enumerating supports of the homogeneous linear system with one-dimensional nullspace containing a vector positive on that support. Indeed if a positive-on-support solution has a nullspace of dimension greater than one, use a nonproportional null direction and subtract a multiple of the solution to obtain mixed signs. Moving in the two directions until a coordinate vanishes expresses the solution as a convex combination of smaller-support solutions. Induction generates the entire cone by its extreme rays. Rationality gives primitive integer ray generators.

For a ray R write e(R),z(R) for its coordinates (e is the linear combination e_min z+y). Define

$$E_0=\sum_{R:z(R)=0} e(R),\qquad E_1=E_0+\left\lceil\max_{R:z(R)>0}\frac{e(R)}{z(R)}\right\rceil.$$

If no ray has z>0, the affine slice is empty. Otherwise enumerate all integer points in z=0 with 1<=e<=E_0, and in z=1 with e_min<=e<=E_1, calling them homogeneous generators and anchors. Every z=0 point is a sum of homogeneous generators. Every z=1 point is an anchor plus a sum of homogeneous generators. Proof: express a point as a nonnegative real linear combination of rays, subtract the integer parts of coefficients times their primitive integer rays, and retain the integer residual. At z=0 its e is at most E_0. At z=1 the integer parts of positive-z rays either contribute one z=1 ray, leaving a z=0 residual, or contribute none, leaving a z=1 residual of e at most E_0+max e(R)/z(R), since the positive-z fractional terms have total z=1. Each integer ray contribution obeys the respective bound. The zero homogeneous residual need not be included. Conversely addition preserves all equations. This proves exact generation. The construction applies directly to compressed outer equations with slacks; no labeled subsets are required. It is finite but may be expensive.

Project each integer point to (e,N,h), where N=sum N_c and h is the gcd of its used weights, with empty gcd zero. For anchors include g0 in the gcd; for homogeneous generators use only their outer weights. Addition adds e and N and combines gcds by gcd. For optimization and feasibility it suffices to keep the cheapest point at each (e,h) among anchors and homogeneous generators: replacing a component by another of the same e and gcd cannot spoil its combination with the others. Thus the projection gives exact minimum costs and realizability, though not necessarily all nonminimal costs after such pruning. This is an explicit finite semilinear-type description with a gcd-state update.

## 4. Exact residue-state solution and nonuniform affine periodicity

If the homogeneous LP is infeasible, E_0=0 and all affine parameters lie within the finite anchor bound. If it is feasible, adjoin the optimal pump (P0,C0,h0) to the finite generators if needed. For each generator (E,C,h), the reduced cost

$$P_0 C-C_0 E\ge0$$

by the optimal LP slope. Use states (r,j), where r is the residue modulo P0 and j is the current gcd (0<=j<=q). Each anchor (e,N,j) initializes state (e mod P0,j) with reduced cost P0 N-C0 e. A homogeneous generator gives a directed edge

$$(r,j)\longmapsto(r+E\bmod P_0,\gcd(j,h))$$

with nonnegative reduced cost P0 C-C0 E and positive length E. Finite multsource shortest paths compute the minimum reachable e in each target state (r,k), using lengths E and anchor e as the initial length. Every feasible parameter of exact group k has a representation by such a path, and every path gives a feasible realization. If the earliest parameter in state (r,k) is e_r, then all e=e_r+jP0 for j>=0 are feasible, by appending the optimal pump. No smaller parameter in that residue is feasible. Hence the admissible parameter set is exactly a finite union of arithmetic rays, not merely eventually periodic, for this fixed signature in the pump case.

For optimal costs use lexicographic path weights (reduced cost, e), with the corresponding anchor labels. For each reachable target state (r,k), let (R_r,e_r^*) be the minimum reduced cost and the earliest e attaining it. These minima exist: all edge reduced costs are nonnegative and lengths are positive, so a lexicographically minimal path can be chosen simple, deleting repeated-state cycles. Initial costs may be negative but are finite in number, and can be shifted by one constant for a multi-source shortest-path computation. Thus all thresholds and intercepts are finite computable integers. For every e>=e_r^* in residue r,

$$\boxed{F_k(e)=\frac{C_0 e+R_r}{P_0},\qquad F_k(e+P_0)=F_k(e)+C_0.}$$

Here F_k is the minimum number of outer vertices for the fixed signature. The path attaining the label can be extended by the pump to precisely e; no better solution can exist since it would yield a lower reduced cost in the same state. Before e_r^*, a bounded dynamic program over e and gcd computes the exact minimum. This proof is valid for nonuniform data and permits absent residues and finite-only cases. It does not claim a polynomial-time algorithm; even the ray construction may be expensive.

For fixed (b,q,g,k), there are only finitely many inner signatures from Section 1. Keep those with the desired g. The total order adds the fixed offset 1+b+|X| to each outer minimum. Union their feasible parameter sets; a finite-only signature contributes only finitely many values. Taking a common multiple of their pump periods, each residue eventually has a finite list of affine cost functions. The minimum is the function with smallest slope and, among ties, smallest intercept; a finite threshold follows from their pairwise crossing points and the individual thresholds. Thus the exact group-admissibility set is a finite union of arithmetic rays and finite exceptions, and the minimum order is eventually affine on every feasible residue. This does not give a short divisibility-only characterization or necessarily a least common period.

## 5. Stronger global scalar result: least eventual period q

Let N_min(b,q;e) minimize over all connected rooted simple realizations of the bipartite rank-four scalar data. The same conclusions below apply if the exact source group is restricted to (g,k)=(1,1). The parameters b,q are fixed and e tends to infinity within the scalar domain.

**Theorem.** For sufficiently large e every minimizing realization has all inner weights equal to one. In either of the stated minimization problems,

$$\boxed{N_{\min}(b,q;e+q)=N_{\min}(b,q;e)+1.}$$

The least positive eventual translation period with constant integral order increment is q. The slope is exactly 1/q. The following explicit, nonoptimal bounds prove stabilization.

First use q inner vertices all attached to a single root neighbor, with all a_i=1 and t=(q,0,...,0). For e>=2q, choose e0=q+r with 1<=r<=q and e0 congruent to e modulo q. Attach r singleton outer neighbors to each inner vertex, then append (e-e0)/q full subsets of all q inner vertices. This realizes the exact group (1,1), since there are singleton outer weights. Its total order is

$$1+b+q+qr+(e-e_0)/q\le e/q+b+q+q^2.$$

If some a_i>=2, then q>=4 and A=sum_i a_i<=q-2 because q-A=sum_i a_i(a_i-1)>=2. Every outer weight is at most A, and sum t_j^2<=q^2. The energy identity implies for e>=q

$$N\ge b+2+\frac{eq-q^2}{(q-2)^2}.$$

This has larger slope than 1/q. In particular nonuniform weights cannot minimize whenever e>=2q and

$$e\left(\frac{q}{(q-2)^2}-\frac1q\right)>q+q^2-2+\frac{q^2}{(q-2)^2}.$$

For q<4 nonuniform weights are already impossible. This proves the asserted eventual weight-one structure for both problems, with an explicit threshold.

For weight-one inner vertices, q=|X| and each inner vertex is attached to exactly one root neighbor. Choose any histogram t_j summing to q. Its inner load constant B_i is the corresponding t_j; each t_j occurs t_j times. Appending one outer vertex adjacent to all q inner vertices raises e by q, adds one to the order, and preserves exact gcd 1 when required. We now bound the residual search uniformly over t_j and residues. If q=1 the only outer subset has size one, and N=b+e+1 in the domain. Suppose q>=2. For e>=2q choose e0 in [q+1,2q] congruent to e modulo q. At e0, singleton outer vertices realize all loads e0-B_i>=1 with exact gcd 1, at cost e0 q-sum_j t_j^2<=2q^2. Append full subsets for e-e0. For any optimum at that fixed signature the excess

$$q^2 F-(eq-\sum_j t_j^2)=\sum_{\text{outer subsets }S}(q^2-|S|^2)$$

is therefore at most 2q^2(q^2-1). Each non-full subset contributes at least 2q-1. Thus at most

$$B=\left\lfloor\frac{2q^2(q^2-1)}{2q-1}\right\rfloor$$

non-full subsets are needed at an optimum. Enumerate the bounded residual collection and let u_i be its weighted load and m its cardinality. The remaining subsets must all have size q and contain every inner vertex. Therefore the quantities B_i+u_i must have one common value C congruent to e modulo q. For e>=q+B(q-1)+1 their common value is strictly below e, so the remaining full subset count (e-C)/q is a positive integer. If exact group (1,1) is required, the additional condition is gcd(t_j-t_1, residual subset sizes, q)=1. Otherwise omit it. All feasibility conditions in this bounded residual search are now independent of e within its residue. Each candidate has cost F=m+(e-C)/q. Its minimum, including the finite choice of t_j, is an affine function of slope 1/q. Combining with the nonuniform exclusion proves the theorem, with threshold the maximum of 2q, the nonuniform exclusion bound, and q+B(q-1)+1. Residual compositions and capacities can be used in place of labeled subsets. Since an eventual constant translation of positive period P must give integer increment P/q, the proved period q is the least possible. QED.

The bound is deliberately loose; no sharp stabilization threshold is asserted. The exact group restriction (1,1) may have different intercepts than unrestricted scalar minimization. Other groups have the general residue laws in Section 4, not necessarily slope 1/q.

## 6. Explicit nonuniform examples

### Infinite family with period six

Take b=2,q=5, inner neighbor sets {0} and {0,1} in zero-based root-neighbor labels. Then a=(1,2), t=(3,2), B=(3,5), and g=k=1. The three outer subset types have weights 1,2,3. Let x,y,z be their counts. The load equations are

$$x+3z=e-3,\qquad 2y+3z=2e-5.$$

Hence z must be odd, and for e>=3 its upper bound is floor((e-3)/3), since this is no larger than floor((2e-5)/3). No realization exists for e=3,4,5. For e>=6 take z to be the largest odd integer at most floor((e-3)/3), with x=e-3-3z and y=(2e-5-3z)/2. Both are nonnegative integers. This maximizes z and minimizes x+y+z=(4e-11-7z)/2, so the exact total minimum order for this signature is

$$N=5+\frac{4e-11-7z}{2},\qquad z=2\left\lfloor\frac{e-6}{6}\right\rfloor+1,\quad e\ge6.$$

In particular N(e+6)=N(e)+5. At e=6 there are x=0,y=2,z=1 outer vertices of the respective types, so N=8. This is a minimum for the fixed signature, not the global minimum for (b,q)=(2,5).

### Isolated parameter with nonuniform weights

Take b=4,q=10 and inner neighbor sets {0},{1},{2,3},{2,3}. Then a=(1,1,2,2), t=(1,1,4,4), B=(1,1,8,8). Require exact k=3 (and g=1). The allowed outer weights are 3 and 6. A subset of weight 3 contains one vertex of each weight class; a subset of weight 6 contains all four. Each allowed subset therefore contributes equal total load to the two classes. The required totals are 2(e-1) and 2(2e-8), so equality forces e=7. The four loads are then all 6. One full subset supplies them, and gcd(3,6)=3. Its minimum order is ten, since at least one outer vertex is necessary. No homogeneous increment exists because its required class totals would be 2E and 4E. This demonstrates a finite-only feasible parameter for fixed inner data; it does not exclude other inner patterns for the same scalar triple or group.

## 7. Verification and boundaries

Run `python -B check_parametric_order.py` without optimization (Python 3; NetworkX 3.6.1, SymPy 1.14.0). The final run passed **1,667 counted exact comparisons**. It compares the compressed inner construction with exhaustive labeled inner-subset signatures in 32 (b,q) cases (b=1..4, q=1..8); 205 constructed signatures are checked including repeated small global tests. It tests 44 homogeneous LP feasibility and 23 feasible optimal slope comparisons against exact rational LPs on labeled subset columns, 55 constructed pump checks in each of three categories, 244 finite-generator cost comparisons against independent subset recursion, 178 exact earliest-residue checks, and 156 affine-tail comparisons. The finite model tests include the isolated e=7 pattern. It compares the explicit nonuniform formula for e=3..60 and constructs 55 witnesses; with the isolated witness, 56 graph recurrence and 56 direct source Smith checks pass. Finally it compares 378 scalar and exact-group minima against independent subset recursion for b,q=1..3 and e through 22, and tests 18 global leading slopes and 18 period intercepts. The counts overlap and are not independent theorems. The full count is in verification.log. The initial non-streaming run passed 1,115 comparisons; the expanded final count supersedes it. The first attempted streaming invocation did not execute; a non-streaming execution succeeded.

The checker implements the compressed inner enumeration and homogeneous LP directly. For the small-instance finite-generator tests it computes ray bounds in the equivalent labeled outer-subset cone and compares with independent subset recursion; a general implementation of extreme-ray enumeration in the compressed capacity/slack cone has not been written. The proof gives that version without labeled subsets. The global slope/period theorem for unrestricted q is algebraic; the tail checks use q<=3. The predecessor manifest matched but its checker was not rerun. The archive contains the exact checker, actual logs, dependencies, proof and handoff. No complexity breakthrough, literature-wide novelty, Lean certification or independent peer review is claimed. The remaining arithmetic problem is to simplify the exact finite criteria to direct divisibility formulas, and determine sharp least periods and intercepts for general exact groups (g,k), especially when g>1 or k>1.
