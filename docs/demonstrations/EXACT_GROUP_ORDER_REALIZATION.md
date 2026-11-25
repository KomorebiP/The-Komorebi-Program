# Exact Smith-group feasibility and universal minimum-order periods

**Author: Komorebi P.**  
**Version:** 3.5, 2026-11-25  
**Status:** Mathematical proofs and exact finite computational tests. Not Lean certified or independently peer reviewed.

Predecessor: [Parametric minimum order and joint incidence compression, v3.4](https://github.com/KomorebiP/The-Komorebi-Program/blob/main/docs/demonstrations/PARAMETRIC_ORDER_REALIZATION.md). All seven predecessor checksum entries matched; its checker was not rerun. This continuation proves an elementary eventual feasibility criterion and an explicit common period and optimal slope for every prescribed rank-four Smith pair. It also gives exact all-parameter formulas for the largest possible second factor, and explicit examples with both minimal and nonminimal universal periods.

## 1. Normalization and necessary residue conditions

Use the connected simple bipartite cyclic-rank-four model of v3.2. The scalar parameters satisfy $b,e\ge1$, $0<q<be$, with cyclic polynomial $M(x)=x^4-(b+e)x^2+be-q$. The nonzero source Smith factors are $(1,1,g,k)$. For the binary inner incidence matrix $P$, write $S_i$ for the nonempty neighbor subset of inner vertex $i$, $a_i=|S_i|$, $t_j=\sum_{i:j\in S_i}a_i$, and $B_i=\sum_{j\in S_i}t_j$. Each outer vertex has weight equal to the sum of $a_i$ over its inner neighbors. The outer weighted load at inner vertex $i$ must be $e a_i-B_i$. We have $q=\sum_i a_i^2=\sum_jt_j$ and $k=\gcd((t_j-t_1)_j,\text{outer weights})>0$.

A necessary preliminary domain is $1\le g\le b$, $g^2\mid q$, $g\mid k$. Set

$$n=q/g^2,\qquad h=k/g,\qquad w_i=a_i/g,\qquad d_j=t_j/g.$$

Then $\gcd_i w_i=1$, $\sum_iw_i^2=n$, $\sum_jd_j=gn$, and $0\le d_j\le\sum_iw_i\le n$. The normalized outer weights are the sums of $w_i$ over their neighbor subsets. Both those weights and the absolute differences $|d_j-d_1|$ are at most $n$, so $1\le h\le n$. All $d_j$ have one common residue $r$ modulo $h$, chosen in $0\le r<h$.

**Theorem 1 (elementary eventual feasibility).** In the preliminary domain, a necessary condition at every scalar-admissible $e$ is the existence of an integer $0\le r<h$ such that

$$\begin{aligned}
gn&\equiv br\pmod h,\\
e&\equiv gr\pmod h,\\
ne&\equiv 2rgn-br^2\pmod{h^2},\\
br&\le gn\le b\left(r+h\left\lfloor\frac{n-r}{h}\right\rfloor\right).
\end{aligned}$$

These conditions are sufficient whenever $e\ge E_*$, where

$$E_*=\begin{cases}
\max(gn+1,\lceil gn^2/(n-h)\rceil),&h<n,\\
gn+1,&h=n.
\end{cases}$$

If any preliminary domain condition fails, no realization exists. If the residue test fails at a particular $e$, no realization exists there. Below $E_*$, a passing residue test alone is not asserted sufficient, except in the special cases proved below. The eventual feasible set is therefore completely described by congruences of modulus at most $h^2$ and the displayed bounds.

**Proof of necessity.** The common residue and bounds on $d_j$, together with their sum, give the first congruence and capacity bound. Divide each inner weighted load equation by $g$. Its right side is $e w_i-\sum_{j\in S_i}d_j$, which is divisible by $h$ because each normalized outer weight is divisible by $h$. Since $|S_i|=g w_i$, this implies $h\mid (e-gr)w_i$ for every $i$, and the gcd of the $w_i$ proves the second congruence. The normalized energy identity is

$$\sum_{\text{outer }y} H_y^2=ne-\sum_jd_j^2,$$

where $H_y$ is the normalized outer weight. The left side is divisible by $h^2$. Writing $d_j=r+h z_j$ gives $\sum_jd_j^2\equiv 2rgn-br^2\pmod{h^2}$, proving the third congruence.

**Proof of sufficiency.** Choose $b$ numbers $d_j=r+h z_j$ in $[0,n]$ summing to $gn$. They exist because the first congruence and capacity bound say that $(gn-br)/h$ is a nonnegative integer not exceeding $b\lfloor(n-r)/h\rfloor$; distribute this integer among $b$ bounded coordinates. Construct a binary incidence matrix with $b$ row degrees $d_j$ and $n$ columns each of degree $g$. The uniform-column block lemma from v3.3 gives this matrix because $d_j\le n$ and the total degree is $gn$. Equivalently, assign each row to the specified number of columns of currently smallest degree. The spread of column degrees remains at most one, so the final column degrees all equal $g$. These columns are the inner vertices; all $a_i=g$.

Define $B'_i=\sum_{j\in S_i}d_j$, so $0\le B'_i\le gn$, $\sum_iB'_i=\sum_jd_j^2$, and $B'_i\equiv gr\pmod h$. Use only outer subsets of size $h$; their normalized weights are $h$. Required row degrees are $u_i=(e-B'_i)/h$, and the number of columns is $F=(ne-\sum_j d_j^2)/h^2$. Both are positive integers at the threshold. For $h<n$, the capacity $u_i\le F$ is equivalent to $(n-h)e\ge\sum_jd_j^2-hB'_i$; the right side is at most $gn^2$. Thus the threshold suffices. For $h=n$, the common residue condition forces either all $d_j=r$ with $r>0$, or all $d_j\in\{0,n\}$. In the former case all $B'_i=gr$; in the latter exactly $g$ rows have degree $n$, all columns use those rows, and $B'_i=gn$. The required degrees are constant, equal to $F$, so the full size-$n$ subsets work. The uniform-column lemma now constructs the outer incidence in both cases. At least one outer vertex exists and every outer weight is exactly $gh=k$, while the root-neighbor differences are divisible by $k$. Therefore the second source factor is exactly $k$, not a multiple. The first source factor is exactly $g$. The v3.2 incidence criterion proves connectivity, the specified scalar recurrence and cyclic rank four. QED.

## 2. Optimal slope and eventual uniformity for every pair

Fix $b,q,g,k$ satisfying the preliminary domain, and suppose some residue passes Theorem 1. Write $N(e)$ for the minimum graph order at that exact source group, undefined when infeasible. Define

$$L=h\lfloor n/h\rfloor,\qquad P=L^2/\gcd(n,L),\qquad C=n/\gcd(n,L),\qquad \rho=n/L^2.$$

Every normalized outer weight is at most $L$. The normalized energy identity and $\sum_jd_j^2\le gn^2$ give the lower bound $F\ge(ne-gn^2)/L^2$ for the number $F$ of outer vertices. In particular the asymptotic order cannot have slope below $\rho$.

At any uniform-inner realization, a homogeneous increment by $P$ is obtained by adjoining $C$ outer subsets, all of size $L$, each inner vertex occurring $P/L$ times. The column construction is valid because $P/L$ and $C$ are integers, $nP/L=LC$, and $P/L\le C$. It raises each normalized inner load by $P$, changes $e$ by $P$, and preserves the exact group because $h\mid L$. Moreover $h\mid P$ and $h^2\mid nP$, so Theorem 1's residue test is unchanged under translation by $P$. For every feasible $e\ge E_*$ choose $e_0\in[E_*,E_*+P-1]$ congruent to $e$ modulo $P$. Construct a uniform graph at $e_0$ using Theorem 1 and append the pump $(e-e_0)/P$ times. With $U_0=n(E_*+P-1)/h^2$, its order is at most

$$N(e)\le1+b+n+\rho e+U_0.$$

This proves the exact slope $\rho$ on all eventual feasible parameters.

**Theorem 2 (uniformity of every eventual minimizer).** For sufficiently large feasible $e$, every minimizing realization has all inner weights equal to $g$. In fact choose

$$T_U=\max\left(E_*,1+\left\lfloor\frac{n-1+U_0+2gn/L}{2/L-\rho}\right\rfloor\right).$$

This threshold suffices. To prove it, note $L>n/2$ for every $1\le h\le n$: if $j=\lfloor n/h\rfloor$, then $n<(j+1)h\le2jh=2L$. Thus $2/L>\rho$. If some normalized inner weight $w_i\ge2$, its normalized load is $e w_i-\sum_{j\in S_i}d_j\ge w_i(e-gn)\ge2(e-gn)$ for $e\ge E_*$. Every adjacent outer vertex supplies at most $L$, and each is adjacent to the inner vertex at most once. Consequently that graph has order at least $1+b+1+2(e-gn)/L$. By the strict inequality encoded in $T_U$, this exceeds the constructed uniform upper bound. This proves the assertion, even when nonuniform data admit outer weights as large as $L$. In particular, the previous LP minimum and competition among nonuniform slopes are unnecessary for the global eventual optimum. QED.

## 3. Bounded residual intercept formula and exact period

Retain only uniform inner data. A signature consists of $d_j\in[0,n]$ with sum $gn$, and the $n$ inner subsets of size $g$ giving those degrees (or their compressed signatures from v3.4). Write $B'_i$ for their normalized sums and $S_d=\sum_jd_j^2$. For any such fixed inner data satisfying the residue test at $e\ge E_*$, the construction at $e_0$ in Section 2 works with those very same inner subsets. Appending size-$L$ subsets gives an outer cost whose excess $L^2F-(ne-S_d)$ is at most

$$E_0=n(E_*+P-1)((L/h)^2-1).$$

Thus a fixed-signature optimum has at most

$$B=\left\lfloor\frac{E_0}{L^2-(L-h)^2}\right\rfloor$$

non-$L$ outer subsets if $L>h$; put $B=0$ if $L=h$. Every smaller allowed size is a positive multiple of $h$ at most $L-h$. Enumerate the finite collections of at most $B$ such subsets (repetitions allowed), or use composition-capacity compression. Let $u_i$ be their normalized loads, $U=\sum_i u_i$, $m$ their count, and $E'=L^2m-U$ their excess. Retain $E'\le E_0$. The remaining size-$L$ columns must number

$$M=(ne-S_d-U)/L^2.$$

The residual collection is feasible if and only if $M$ and all $(e-B'_i-u_i)/L$ are nonnegative integers, the latter are at most $M$, and the gcd of all $d_j-d_1$, the residual sizes, and $L$ if $M>0$ is $h$. The uniform-column lemma proves sufficiency; no other graphicality condition is needed. The minimum total order is

$$N(e)=1+b+n+\frac{ne+\min(E'-S_d)}{L^2},$$

where the minimum ranges over all uniform inner signatures and feasible residual collections. This formula is valid for $e\ge T_U$ on the feasible domain. The search is bounded independently of increasing $e$.

For an explicit eventual stabilization threshold put

$$T_R=gn+B(L-h)+1$$

and, if $n>L$, also require $e\ge T_C=\lceil(gn^2+B(L-h)^2)/(n-L)\rceil$. For $n=L$ omit $T_C$. Above these thresholds the remaining loads are positive, so any integral feasible $M$ is positive. The capacity condition becomes $(n-L)e\ge S_d+U-L(B'_i+u_i)$. For $n>L$ it follows from $T_C$, since $S_d\le gn^2$ and $U\le B(L-h)^2$. For $n=L$ it is independent of $e$. Integrality conditions depend only on $e$ modulo $P$ because $L\mid P$ and $L^2\mid nP$. The exact gcd test is likewise independent of $e$ within its residue. Thus the minimizing excess minus $S_d$ is a fixed number on each feasible residue above the maximum of $T_U,T_R,T_C$ (when applicable).

**Theorem 3 (universal exact eventual period).** For every fixed eventually feasible group, on all sufficiently large feasible parameters,

$$N(e+P)=N(e)+C,\qquad P=L^2/\gcd(n,L),\quad C=n/\gcd(n,L).$$

Feasibility is also invariant under this translation throughout the tail. The proof gives an explicit finite computation of every residue intercept. The threshold and period are not necessarily optimal.

For the least eventual translation period $P_{\min}$, the slope gives the arithmetic bounds

$$\frac{L^2}{\gcd(n,L^2)}\mid P_{\min}\mid \frac{L^2}{\gcd(n,L)}.$$

Indeed an order increment over period $t$ must be the integer $\rho t$. The eventual function $L^2 N(e)-ne$, assigning infinity to infeasible residues, is a finite cyclic word of length $P$. Its translation stabilizer is a subgroup of the cyclic group, so its least positive period divides $P$ and can be found by testing divisors against the finite residue intercepts. A period here means preservation of the domain and one constant integral order increment on every feasible residue. In particular the displayed universal $P$ is least whenever $\gcd(n,L^2)=\gcd(n,L)$. This includes $h\mid n$ ($L=n$, period $n$) and $n\equiv1\pmod h$ with $h>1$ ($L=n-1$, period $(n-1)^2$). Section 5 gives an example where the universal period is not least. No formula solely in terms of $n,h$ for the least period in every case is asserted.

## 4. Exact all-parameter classification for the maximal second factor

Take $h=n$, equivalently $k=q/g$. At any feasible scalar parameter, all inner weights must equal $g$: otherwise $\sum_i w_i<n$, so every root-neighbor difference and outer weight is smaller in absolute value than $n$, contradicting their positive gcd $n$. Hence there are exactly $n$ inner vertices. There are two possible types of root-neighbor degrees, since the $d_j$ are congruent modulo $n$.

- Zero residue: exactly $g$ of the $d_j$ equal $n$, the remainder zero. Every inner vertex uses the same $g$ neighbors, and $B'_i=gn$. This is feasible exactly when $e\ge gn$ and $n\mid e-gn$. If $e=gn$ there are no outer vertices; the scalar domain forces $b>g$ and the root-neighbor differences then have gcd $n$.
- Positive residue: require $b\mid gn$ and $r=gn/b<n$. All $d_j=r$ and $B'_i=gr$. Uniform-column incidence gives the inner data. Feasibility is exactly $e>gr$ and $n\mid e-gr$; the strict inequality is already the scalar domain. The outer vertices are full subsets of size $n$.

In either case all outer vertices are full subsets, numbering $(e-B')/n$. Thus the exact set of possible graph orders is the set of $1+b+n+(e-B')/n$ over the two feasible constants $B'=gn,gr$ just described. It is empty if neither branch works; otherwise the minimum chooses the largest feasible $B'$. This holds at every scalar-admissible parameter, not just above a threshold. It includes the case $n=1$. For example $b=4,g=2,q=8,k=4,e=4$ has two possible orders, seven and eight, with minimum seven. The proof constructs both graphs and excludes all other orders.

## 5. Two exact nontrivial period examples

### 5.1 A higher-factor group with least period sixteen

Let $b=3,g=2,q=20,k=4$. Then $n=5,h=2,L=4$. Because $b<2g$, all inner weights must be $g$ at every feasible parameter. The normalized root-neighbor degrees are congruent modulo two, sum to ten and lie in $[0,5]$. They must all be even, so up to permutation they are $(4,4,2)$. The inner subsets of size two are three copies of $\{1,2\}$ and one each of $\{1,3\},\{2,3\}$. The normalized constants $B'_i$ are $(8,8,8,6,6)$. The residue condition forces $e=4m$, and the scalar domain requires $m\ge2$.

Use $u$ outer subsets of size four and $v$ of size two. With row loads divided by two, the required degrees are $d_i=2m-4$ on three vertices and $2m-3$ on two. Then $4u+v=5m-9$. If $x_i$ are incidences in the size-four block, the capacity constraints are

$$\max(0,\lceil(d_i-v)/2\rceil)\le x_i\le\min(u,\lfloor d_i/2\rfloor),\qquad \sum_i x_i=4u.$$

The upper sum gives $u\le\lfloor(5m-10)/4\rfloor$. Choose equality, giving $1\le v\le4$ and $u\ge m-2$. For $m\ge3$ all $d_i\ge v$. The lower sum equals $5m-8-5v/2$ for even $v$, and $5m-10-5(v-1)/2$ for odd $v$, each at most $4u=5m-9-v$. Each lower bound is at most $m-2$, the upper bound for every row. For $m=2$, take $u=0,v=1$, joining the two rows of unit degree. Thus the block construction always attains the upper bound on $u$. The normalized root differences already have gcd two, so the exact group is automatic for both outer sizes. Minimizing the number $u+v$ maximizes $u$, hence

$$\boxed{N(4m)=5m-3\left\lfloor(5m-10)/4\right\rfloor\quad(m\ge2).}$$

The first orders at $e=8,12,16,20,24$ are $10,12,14,16,15$. The slope is $5/16$, and the least eventual period is sixteen with increment five by Theorem 3 and the slope divisibility bound.

### 5.2 The universal period need not be least

Let $b=g=1,q=8,k=3$. Then $n=8,h=3,L=6$, so Theorem 3 gives $P=18$, increment four. All eight inner vertices use the only root neighbor. Their common normalized load is $s=e-8>0$. All allowed outer sizes are three and six, and the energy condition requires $9\mid s$, so write $s=9m$, $m\ge1$. If $u,v$ count size-six and size-three subsets respectively, $4u+v=8m$. The exact gcd three requires $v>0$, so $v\ge4$ and $u\le2m-1$. Set $u=2m-1,v=4$. With $d=3m$, the size-six incidences at each of the eight inner vertices may range from $\max(0,\lceil(d-4)/2\rceil)$ to $\min(2m-1,\lfloor d/2\rfloor)$. The sum must be $6(2m-1)$. Multiplying both endpoints by eight bounds that sum below and above (directly for $m=1$, and by parity for $m\ge2$). Hence the two uniform-column blocks exist. The minimum order is

$$\boxed{N(8+9m)=13+2m\quad(m\ge1).}$$

Its least period is nine with increment two, strictly smaller than the universal period eighteen. The slope $2/9$ excludes any smaller positive translation period with integral increment.

## 6. Verification, lineage and remaining boundary

Run `python -B check_exact_group_order.py` with Python 3, NetworkX 3.6.1 and SymPy 1.14.0. The final run passed **9,509 counted exact comparisons** (see verification.log). It includes 91 rank-four rooted cases from the connected bipartite graph atlas through order seven; 420 residue-set comparisons against enumeration of bounded degree vectors; 815 constructed uniform graphs at the explicit feasibility threshold and 815 pumped graphs (connectivity, energy, recurrence and independently computed source Smith form for each); 478 maximal-group order checks at larger parameters; 275 exhaustive small maximal-group oracle comparisons; 213 small-instance necessity and 99 sufficiency comparisons using independent labeled subset recursion; 39 exact minimum comparisons and constructed graph checks for Section 5.1; and 40 size-capacity minima and constructed graphs for Section 5.2. The two-order example in Section 4 is also explicitly constructed and verified. Counts overlap and are not independent theorems. The initial run passed 9,218 comparisons; the expanded final count supersedes it. The atlas order test was broadened to check membership in the full maximal-group order set, rather than equality with its minimum. The general eventual uniformity and residual threshold are proved algebraically; the checker does not exhaustively evaluate all large residual searches.

The elementary eventual feasibility problem and explicit global slope and period problem from v3.4 are closed for every prescribed source Smith group in bipartite cyclic rank four. The least period is computable by finite intercept comparison but not expressed by one elementary formula in all cases. Finite exceptions below the threshold (outside the proved exact special cases) still use the v3.4 finite criterion. The stabilization bound is not optimized. Next: study exact early admissibility and intercept simplification; extend to nonbipartite rank four or bipartite rank five. No overall complexity improvement, Lean certification, independent peer review or literature-wide novelty is established.
