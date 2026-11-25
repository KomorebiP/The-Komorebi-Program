# Minimum-order realization of bipartite cyclic rank four

**Author: Komorebi P.**  
**Version:** 3.3, 2026-11-25  
**Status:** algebraic and combinatorial proofs, exact finite tests. Not Lean certified or independently peer reviewed.

Predecessor: [Bipartite cyclic rank four, v3.2](https://github.com/KomorebiP/The-Komorebi-Program/blob/main/docs/demonstrations/RANK_FOUR_REALIZATION.md). All seven predecessor checksums matched. The predecessor checker was not rerun here.

## 1. Exact composition-capacity reduction

Use the notation of v3.2. The scalar parameters are integers b,e,q with b,e positive and 0<q<be. The inner incidence P has one nonzero binary row per distance-two vertex, with row neighbor set S_i contained in the b root neighbors. Put a_i=|S_i|, t_j=sum_{i:j in S_i} a_i, and D_i=e a_i-sum_{j in S_i}t_j. The inner data must satisfy sum_i a_i^2=q and D_i>=0. A multiset of outer neighbor subsets realizes the graph precisely when each row receives weighted load D_i, with weight of a subset T equal to sum_{i in T}a_i. The source factors are (1,1,g,k), where g=gcd_i a_i and k is the gcd of all t_j-t_1 and all outer weights.

Group the inner vertices by weight w, with I_w={i:a_i=w} and n_w=|I_w|. An outer composition is a nonzero vector c=(c_w) with 0<=c_w<=n_w. Its weight is H_c=sum_w w c_w. Let N_c be its multiplicity and d_ic the number of neighbors of inner vertex i among the outer vertices of that composition.

**Theorem.** A set of multiplicities N_c is realizable if and only if there are nonnegative integer d_ic satisfying

$$\sum_c H_c d_{ic}=D_i,\qquad \sum_{i\in I_w}d_{ic}=c_w N_c,\qquad 0\le d_{ic}\le N_c.$$

Necessity is immediate from incidence counts. For sufficiency, fix w,c. Construct a binary matrix with row degrees d_ic on I_w and N_c columns, all of degree c_w. These degrees are realizable precisely under the given bounds and total sum. One proof is to process rows, choosing d_ic distinct columns of currently smallest degree at each step. The column degrees remain balanced (their spread is at most one) by induction; the final sum is c_w N_c, so every column has degree c_w. The choices for different w,c concern disjoint blocks of the incidence matrix and can be made independently. Each outer vertex then has composition c and weight H_c; the weighted load equation holds at every inner vertex. Hence the v3.2 recurrence holds. There is no further graphicality constraint for these blocks. This construction uses a labeled binary incidence matrix, with repeated columns allowed because the outer vertices themselves are distinct. The root and inner edges are already supplied.

The number of possible outer compositions is at most product_w(n_w+1)-1, instead of 2^|X|-1 labeled nonempty subsets. This can be dramatically smaller for repeated weights; it need not be small in every case. The energy condition

$$\sum_c H_c^2N_c=\sum_i a_iD_i=eq-\sum_j t_j^2$$

is obtained by multiplying each row load by a_i and summing. It bounds all multiplicities, and the capacities bound every d_ic. Thus the construction is a finite exact integer optimization, without enumerating labeled outer subsets. For a prescribed k, impose

$$\gcd\bigl((t_j-t_1)_j,(H_c)_{N_c>0}\bigr)=k.$$

Minimize sum_c N_c. Enumerate the admissible P from v3.2 and minimize 1+b+|X|+sum_c N_c over P with the desired g. This gives the exact minimum graph order for every feasible source group (g,k). Dropping the source-group restriction gives the scalar minimum. Every feasible minimum is accompanied by an explicit graph. This is not an efficient universal algorithm, nor is it a divisibility-only criterion; the inner subset enumeration is still required in this edition.

Example: b=2,e=4,q=4. Exact enumeration and constructive minima give

| Source (g,k) | Minimum order |
|---|---:|
| (1,1) | 12 |
| (1,2) | 9 |
| (1,4) | 7 |
| (2,2) | 6 |

The previously rejected pair (2,4) remains impossible. The minimum across all groups is six. These are exhaustive for this triple: all inner possibilities are included and all weighted outer counts are bounded by the energy identity.

## 2. Uniform inner weights and closed minima

Suppose g=b. Then q=b^2 n, n=|X|, P is all-one, s=e-bn>0, and k=bh. Each outer vertex has a neighbor subset of the n inner vertices, and its weight divided by b is its subset size. Each inner vertex must receive total subset-size load s. The exact gcd of the subset sizes must be h. The admissibility conditions from v3.2 are 1<=h<=n, h|s, h^2|ns. This includes all leaf-rooted graphs (b=1). Write F_h(n,s) for the minimum number of outer subsets (counting repetitions). Then N_min=1+b+n+F_h(n,s).

For h<=n<2h the only possible size is h, so F_h=ns/h^2, attained by the uniform block construction of v3.2.

**Two-size theorem.** Suppose 2h<=n<3h and the admissibility conditions hold. Put d=s/h and C=nd/h. Then

$$u=\min\left(\left\lfloor\frac{C-2}{4}\right\rfloor,\left\lfloor\frac{n\lfloor d/2\rfloor}{2h}\right\rfloor\right),\qquad \boxed{F_h(n,s)=C-3u}.$$

Proof: the only sizes are h and 2h. Let v count size-h subsets and u count size-2h subsets. The energy identity is v+4u=C. Exact gcd h requires v>0. In fact v cannot be one: at each inner vertex the number of size-h incidences has parity d. If v=1 and d is even, every such incidence vanishes; if d is odd, every inner vertex must lie in the sole size-h subset, contrary to n>=2h. Thus v>=2. If x_i is the size-2h incidence degree of vertex i, its size-h degree is d-2x_i. Necessary and sufficient conditions for the two uniform incidence blocks, by Section 1, are

$$\max(0,\lceil(d-v)/2\rceil)\le x_i\le\min(u,\lfloor d/2\rfloor),\qquad \sum_i x_i=2hu.$$

For v>=2 and 2h<=n these lower bounds on the sum are automatic: if d>v, multiply by two and use n(d-v+1)<=nd-hv=4hu, because (n-h)v>=n. If d<=v, the lower bound is zero. The upper bound from x_i<=u is automatic since 2h<=n; the remaining upper bound is 2hu<=n floor(d/2). The possible integer sums of n numbers in a common integer interval comprise the entire interval of sums, so these conditions suffice. Therefore the largest feasible u is exactly the displayed minimum of the two floors. It is nonnegative since C>=2. Each additional size-2h subset decreases v+u by three, proving optimality. To construct an attaining graph, allocate x_i in their intervals to total 2hu and use the two uniform incidence constructions. QED.

For n=2, this specializes to F_1(2,s)=2s-3 floor((s-1)/2), and F_2(2,s)=s/2 for even s (otherwise infeasible).

### Three inner vertices

For n=3 the complete explicit answer is as follows. For h=2, F_2=3s/4 when 4|s, otherwise infeasible. For h=3, F_3=s/3 when 3|s, otherwise infeasible. For h=1 write s=3t+r, 0<=r<3. Then

| r | F_1(3,s) |
|---|---|
| 0 | t+4 if t>=2; t+5 if t=1 |
| 1 | t+2 if t>=2; t+3 if t=0 or 1 |
| 2 | t+3 |

Proof for h=1: choose z size-three subsets, leaving common load R=s-3z. The largest number x of size-two subsets is floor(3 floor(R/2)/2). Necessity follows by bounding pair incidence at each vertex by floor(R/2). Sufficiency follows by cycling among the three possible pairs, whose degree sequence is balanced and hence has maximum ceil(2x/3)<=floor(R/2). Fill each remaining load by singleton subsets. The outer count is z+3R-3x. Exclude R=0 (all triples); if z=0 and singleton count 3R-4x is zero, decrease x by one to enforce gcd one. If z>0 and R>0 the gcd is already one. Write z=t-j, R=r+3j. Increasing j by four increases R by twelve, x by nine, and the unadjusted count by five. A gcd-one adjustment at the endpoint can only increase the count. Thus evaluate j=1,2,3,4 for r=0 and j=0,1,2,3 for r=1,2, retaining j<=t and applying the stated endpoint correction. These evaluations give the table. Cases h=2,3 follow from the single-size rule and admissibility. QED.

## 3. Bounded residual formula and exact eventual periodicity

For every admissible n,s,h, put L=h floor(n/h) and P=L^2/gcd(n,L). If L=h the single-size formula is already exact. Otherwise let s0 be the representative of s modulo P in {1,...,P}. It is admissible since P is divisible by h and nP by h^2. The uniform size-h construction at s0 uses n s0/h^2 subsets. Adding a uniform size-L construction at load P uses nP/L^2 subsets and preserves gcd h. Thus for s=s0+tP the energy excess

$$E=L^2 F_h(n,s)-ns$$

satisfies 0<=E<=E0=n s0((L/h)^2-1). Here each non-L subset of size w contributes L^2-w^2 to E. Therefore every optimum has at most

$$B=\left\lfloor\frac{E0}{L^2-(L-h)^2}\right\rfloor$$

non-L subsets. This bound depends on n,h and the residue, not on s. It gives the following exact residual formula at every admissible s in the residue class, not merely for large s.

Enumerate multisets of at most B nonempty subsets of [n], each of size a positive multiple of h less than L, with total cost E' = sum (L^2-w^2)<=E0. For each multiset let u_i denote its weighted load on vertex i and U=sum_i u_i. The remaining size-L subsets must number M=(ns-U)/L^2. The multiset is feasible precisely when

- each s-u_i is nonnegative and divisible by L;
- M is a nonnegative integer and each (s-u_i)/L<=M;
- the gcd of its subset sizes, together with L if M>0, is exactly h.

The two degree conditions for the size-L block suffice by Section 1. The total degree is LM, and all columns have degree L. The gcd condition is necessary and sufficient for the desired source group. At least one candidate is feasible by the construction proving E0. Hence

$$\boxed{F_h(n,s)=\frac{ns+\min E'}{L^2}}$$

where the minimum runs over these feasible residual multisets. This is a bounded search independent of growing s within a residue, although the bound B can be large. The composition-capacity algorithm can also be used to aggregate the residual multiset search.

**Eventual exact affine periodicity.** Put T1=B(L-h)+1. For n>L additionally put T2=ceil(B(L-h)^2/(n-L)); for n=L omit T2. For every admissible s>=T=max(T1,T2) in the residue class (using T1 alone when n=L), feasibility of every candidate in the residual formula is independent of the size of s in that residue. Indeed u_i<=B(L-h) and U<=B(L-h)^2. The strict bound s>=T1 gives positive remaining loads and hence M>0 whenever it is integral. Divisibilities depend only on s mod P, since L|P and L^2|nP. The capacity inequality is equivalent to

$$(n-L)s\ge U-Lu_i.$$

For n>L the threshold T2 ensures it; for n=L it is independent of s. The gcd restriction is likewise now independent of s. Thus the optimum residual cost is a constant E_res beyond T, and

$$\boxed{F_h(n,s+P)=F_h(n,s)+\frac{nP}{L^2}.}$$

This provides a finite explicit threshold, and a finite computation of the exact intercept in every admissible residue class. It is not asserted that this threshold is optimal, that P is the least period, or that one universal elementary formula covers arbitrary n,h. The proof also shows that the excess is nonincreasing along the progression even before stabilization, by appending the uniform size-L construction.

## 4. Verification

Run `python -B check_minimum_order.py` with Python 3, NetworkX 3.6.1 and SymPy 1.14.0. The final run passed **1,362 counted comparisons**. The checker compares the composition solver with independent recursive labeled-subset enumeration on 273 fixed P cases, spanning b=1..3, e=1..4, q=1..5 (admissible triples only). It constructs 208 minimizing witnesses for fixed P and feasible k, checks each witness size, direct adjacency recurrence, and exact source Smith form. Aggregating P gives minima for 37 scalar triples and the table in Section 1. It tests 60 two-inner and 90 three-inner formulas (s=1..30), 27 two-size formula cases using a separate integer degree DP with n up to 8, and 80 bounded-residual comparisons (n<=4,s<=8). Counts overlap; they are not independent mathematical theorems. These checks are finite; the proofs give the unrestricted results. The periodicity threshold is established by the algebraic argument; a separate large-s test of every threshold is not included. The predecessor manifest matched but its checker was not rerun.

## 5. Remaining boundary

We have an exact constructive minimum-order test for all rank-four bipartite scalar triples and their source groups, closed formulas for the uniform cases described above, and an exact eventual periodic law for all uniform cases. The scalar and group conditions of v3.2 remain in force. A short divisibility-only characterization of general nonuniform groups, a closed elementary minimum-order expression for general nonuniform P, and complexity bounds remain open in this program. Next targets: apply the composition-capacity reduction jointly to the inner and outer incidences, and study periodicity in e for nonuniform data. No literature-wide priority, computational complexity breakthrough, Lean certification or independent peer review is claimed.
