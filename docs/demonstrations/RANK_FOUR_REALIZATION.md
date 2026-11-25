# Bipartite cyclic rank four: scalar classification, sharp order, and arithmetic realization

**Author: Komorebi P.**  
**Version:** 3.2, 2026-11-25  
**Status:** Mathematical proofs and exact finite computational verification. Not Lean certified or independently peer reviewed.

Predecessor: [Finite profile realization of rooted graph moments, v3.1](https://github.com/KomorebiP/The-Komorebi-Program/blob/main/docs/demonstrations/PROFILE_REALIZATION_CRITERION.md). All six predecessor checksum entries matched. Its checker was not rerun. This continuation specializes the general profile criterion to connected simple bipartite graphs with cyclic rank four. It closes scalar-sequence admissibility and maximum order in this class, gives all source groups by finite coefficient extraction, and gives a short divisibility classification in a special case. It does not assert a simple divisibility classification for all source groups.

## 1. Scalar admissibility and two-layer incidence criterion

Let A be the adjacency of a finite connected simple bipartite graph, rooted at o. Cyclic rank means the dimension of the span of A^j e_o over the rationals. Suppose this rank is four. The minimal cyclic polynomial is monic integral because it divides the monic integral characteristic polynomial over the rationals. Symmetry makes its roots real and distinct; the bipartition sign involution negates the spectrum and fixes e_o up to sign. Thus the active roots occur in opposite pairs, with no zero (four is even), and the polynomial is x^4-c x^2+d with c,d positive integers. Write m_j=(A^j)_{oo}, b=m_2, q=m_4-b^2 and e=c-b. The first four walk rows are independent. In particular q>0, since otherwise A^2 e_o=b e_o by the squared norm identity. The recurrence at j=0 gives d=be-q>0, hence e>=1.

The exact scalar parameter domain is

    b>=1, e>=1, 1<=q<be.

All parameters are integers. The minimal recurrence and moment data are

    M(x)=x^4-(b+e)x^2+be-q,
    m_0=1, m_2=b, m_(2n+1)=0,
    m_(2n+4)=(b+e)m_(2n+2)-(be-q)m_(2n).

For incidence coordinates, every vertex is at distance at most three: a nonzero profile is forced by connectivity and the order-four recurrence. Let J, X, Y be the vertices at distances one, two, three respectively. There are b vertices in J. Let P be the 0-1 incidence matrix X by J and R the 0-1 incidence matrix X by Y. There are no other edges besides root-J, P and R. Every row of P is nonzero, every column of R is nonzero; Y can be empty. Put a=P 1, t=P^T a, h=R^T a. Then

    q=a^T a,  sum_j t_j=q,
    P t+R h=e a.                                            (1)

Indeed, A^2 e_o has root entry b and distance-two vector a. A^3 e_o has J entries b+t_j and Y entries h. At the root A^4 e_o=b^2+q, and at X its values are b a+P t+R h. This proves (1) from M(A)e_o=0. Conversely take arbitrary 0-1 P,R obeying the stated row and column conditions, q=a^T a>0, (1), and d=be-q>0. The constructed graph is connected, and the same calculation yields M(A)e_o=0. Dotting (1) with a gives

    ||t||^2+||h||^2=e q.                                     (2)

The two even walk rows have rank two because q>0. The two odd rows, after subtracting b times row one from row three, have Gram matrix [[b,q],[q,e q]] of determinant d q>0. The even and odd blocks have disjoint supports. Thus the rank is four and M is minimal. This is necessary and sufficient. It avoids the general profile and graphicality search.

## 2. Existence for every scalar triple and sharp maximum order

Write q=b l+s, 0<=s<b. Choose b nonnegative integers n_j with sum q, s equal to l+1 and the remainder equal to l. Since q<be, all n_j<=e. Construct a tree: connect the root to b neighbors, give neighbor j precisely n_j children, and give each of those children e-n_j new leaves. This has P rows with exactly one 1, t_j=n_j, and each outer vertex contributes h=1. At an inner vertex attached to j, (1) reads n_j+(e-n_j)=e. Hence it realizes the proposed scalar triple.

For any realization, |X|<=q since each a_i>=1 and q=sum a_i^2. Also |Y|<=||h||^2=e q-||t||^2. Integer nonnegative t_j sum to q; their least possible sum of squares is b l^2+s(2l+1), obtained by balancing (if two entries differ by at least two, moving one unit from the larger to the smaller reduces the sum of squares). Therefore

    N_max=1+b+q+e q-b l^2-s(2l+1).

The constructed tree attains equality. This is the maximum among connected bipartite realizations and also among connected simple realizations of the given moments: all odd rooted moments vanish, so any odd cycle in a connected realization would be reachable and would produce a positive odd return count. The exact scalar admissibility statement likewise concerns all connected simple graphs with these even moments. The case e=1 has q<b, and is especially rigid. For each inner vertex i, t_j>=a_i at every j in its P-neighbor set, so (P t)_i>=a_i^2. Equation (1) forces a_i=1, t_j=1 at every occupied neighbor, and no outer vertices. There is exactly one rooted graph up to isomorphism: q arms of length two and b-q arms of length one.

For b=2,e=3,q=4, M=x^4-5x^2+2, the maximum is eleven and moments start 1,0,2,0,8,0,36,0,164.

## 3. Source and Gram Smith factors

Define g=gcd_i a_i and k=gcd(t_j-t_1 for 1<=j<=b, h_y for y in Y), taking the nonnegative gcd. It is positive: if all the differences and h vanish, (2) and sum t=q force e q=q^2/b, contradicting d>0. All t_j and h_y are multiples of g, hence g divides k.

Unimodularly subtract b times the root row from row two and b times row one from row three. The even rows now consist of the root indicator and a on X; they give source Smith factors 1,g and Gram diagonal (1,q). The odd rows consist of (1_J,0_Y) and (t,h). Subtracting t_1 times the former from the latter, and using a unit entry to clear the first row by column operations, gives source factors 1,k. The odd Gram matrix before this last row subtraction is [[b,q],[q,e q]]. Its Smith factors are l=gcd(b,q) and d q/l, because its determinant is d q. Since l divides both q and d=be-q, the complete nonzero Smith factors form the divisibility chains

    SNF(W)=(1,1,g,k),
    SNF(WW^T)=(1,l,q,d q/l).

The first four walk rows generate all subsequent rows integrally via M, so padding by zero factors gives the full walk-matrix result. The source saturation quotient is Z/g Z plus Z/k Z. The total Gram determinant in the independent basis is d q^2. Thus the determinant gives the necessary divisibility g^2 k^2 | d q^2; this follows from the saturation determinant identity in v3.0.

Further necessary bounds are 1<=g<=b, g^2|q, g|k, 1<=k<=q. The last follows because all h and t_j are at most sum a_i<=q, so every nonzero argument in the gcd is bounded in absolute value by q. For T=t_1, all t_j are T modulo k and all h are zero modulo k. Equation (1), the sum, and the norm identity imply

    q-bT=0 mod k,
    g(e-T)=0 mod k,
    e q-2T q+b T^2=0 mod k^2.

Here g|T, and the last congruence follows by expanding sum_j(t_j-T)^2+sum_y h_y^2. Also |X|<=q/g^2 and |Y|<=||h||^2/k^2. Cauchy-Schwarz gives ||t||^2>=q^2/b, yielding

    N <= 1+b+q/g^2 + d q/(b k^2).

The maximum-order tree in Section 2 has g=k=1: if Y is nonempty a unit h supplies k=1; otherwise d>0 forces the balanced t entries to take both values, hence their difference is one.

## 4. Complete coefficient test for possible source groups

This is an exact finite arithmetic test, not a simple product or divisibility criterion. Enumerate multiplicities n_S>=0 for nonempty subsets S of the b labeled root neighbors, such that sum |S|^2 n_S=q. They determine P up to permutation of the inner vertices; retain a fixed indexing of its n=|X| rows with subsets S_i, and compute a,t as above. For each row put D_i=e a_i-sum_(j in S_i) t_j. Reject negative deficits. Every outer vertex corresponds to a nonempty subset T of [n] and has weight h_T=sum_(i in T) a_i. If its multiplicity is r_T, (1) is equivalent to

    sum_(T containing i) h_T r_T=D_i for every i.

For a positive divisor candidate u define

    C_u(P)=[z_1^D_1 ... z_n^D_n]
       product_(nonempty T, u divides h_T) (1-product_(i in T) z_i^h_T)^(-1),

and set C_u(P)=0 unless every t_j-t_1 is divisible by u and every D_i>=0. The product is formal and the coefficient finite because each weight is positive. Expanding the geometric factors counts outer subset multisets with u dividing their resulting k. Since k<=q, finite Möbius inversion gives the number of such multisets with exact k:

    E_k(P)=sum_(1<=j<=floor(q/k)) mu(j) C_(jk)(P).

Here mu is the classical arithmetic Möbius function. A pair (g,k) occurs if and only if some enumerated P with gcd row sums g has E_k(P)>0. Necessity and sufficiency follow from (1) and geometric-series expansion. The count distinguishes the chosen inner labels and is not a count of isomorphism classes across different P. If desired, introduce an extra variable multiplying the monomial in each geometric denominator to record the number of outer vertices. This yields exact attainable orders by coefficient extraction. No adjacency enumeration or degree-sequence test is needed after the subset data are selected. This method may be exponential in q and b.

A precise boundary: for b=2,e=4,q=4, the actual possible pairs are (1,1),(1,2),(1,4),(2,2). The seemingly admissible pair (2,4) passes all Section 3 necessary divisibilities and congruences with T=0 modulo 4, but is impossible. Indeed g=2 forces every a_i=2, and q=4 forces exactly one inner vertex. Its t entries are (2,2); d=4>0 forces some outer vertices, all of weight two, so k=2. The checker verifies the complete pair list by the exact coefficient criterion; the elementary argument alone excludes the false pair.

## 5. Closed classification when g=b (including roots of degree one)

If g=b then each a_i=b. Thus q=b^2 n for a positive integer n, and P is the all-one matrix. Here t_j=b n and each outer weight is b times its subset size. Put s=e-b n=d/b>0. The recurrence becomes

    sum_(T containing i) |T| r_T=s for each i in [n].

Writing k=b h, where h is the gcd of the outer subset sizes, the exact attainable h satisfy

    1<=h<=n, h|s, h^2|n s.

Necessity follows from each vertex's load and from summing the load equations. For sufficiency repeat the ordered list of n inner vertices s/h times and cut it into consecutive blocks of h distinct vertices. The divisibility hypotheses ensure exact cuts and every vertex appears s/h times. Make one outer vertex per block. Its weight is b h and all outer subset sizes are h. This realizes k=b h. The exact largest order for this source pair is 1+b+n+n s/h^2, attained by this construction since each outer subset contributes at least h^2 to the sum n s. For b=1 every realization has g=b; consequently this is a complete source-group and sharp fixed-group maximum-order classification for leaf roots.

Example: b=1,e=4,q=2, with M=x^4-5x^2+2. The two allowed h=1,2 give a tree of order eight and a five-vertex graph consisting of C4 with a pendant root. Both have moments 1,0,1,0,3,0,13,0,59,... and Gram factors (1,1,2,4). The source factors are (1,1,1,1) and (1,1,1,2). The first has two outer leaves per inner vertex, the second one outer vertex adjacent to both inner vertices. This is a rank-four scalar collision of both order and source group.

## 6. Reproducibility and boundaries

Run `python -B check_rank_four.py` without optimization (Python 3, NetworkX 3.6.1, SymPy 1.14.0). Final run: 29,819 counted comparisons, including 453 connected bipartite atlas root cases through seven vertices scanned by independent rational cyclic-rank tests; 91 of them have rank four and receive detailed checks. The checker constructs and directly enumerates 546 balanced trees for 1<=b<=7, 1<=e<=6 and 1<=q<be; 216 uniform-defect constructions; and 9,480 explicitly enumerated small two-layer graphs (outer size at most two), of which 101 pass the prescribed recurrence. The latter independently test 486 coefficient counts in 167 fixed-inner-data cases. Across 853 analyzed graphs it checks source and Gram Smith factors, moments, incidence balances, order bounds, and necessary congruences. The full counts are in verification.log. The expanded checker's first attempt failed because its explicit rejection fixture used residue T=2 rather than the valid residue T=0. This fixture error was corrected, and verification_failed.log is retained. The original run before expanding the checks had passed 28,107 comparisons; the final count supersedes it, not adds to it.

The scalar classification and sharp maximum are proved for all triples. The coefficient test gives an exact finite source-group classification; a shorter divisibility characterization for general 1<g<b or g=1,b>1, closed minimum-order formulas, and nonbipartite higher-rank classifications are outstanding. The code tests finite ranges, not a proof of novelty or a complexity breakthrough. The techniques use classical Krylov and Smith-form linear algebra, weighted subsets, and Möbius inversion. Lean certification, independent review, and literature-wide priority assessment remain outstanding.
