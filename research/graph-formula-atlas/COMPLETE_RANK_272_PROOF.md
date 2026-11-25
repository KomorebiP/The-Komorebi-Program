# Complete constant rational rank of the 537-record graph and array atlas

Author: Komorebi P.

## 1. Statement and scope

For the retained 537 mathematical sequence definitions, using their retained indices and zeros before their original offsets, let G be the vector of ordinary generating series in Q[[x]]. Then

    dim_Q span{G_1,...,G_537} = 272.

There is a constant rational transfer matrix T of size 537 x 272, with G = T B for a specified vector B of 272 linearly independent retained generating series. The nullity of the map from the 537 formal record coordinates to their span is 265. Here coefficients in the linear span are constants in Q, not rational functions of x. The rational-series subcollection comprises 506 models and has dimension 241; the other 31 models are jointly independent modulo that rational span.

This continuation relies on the predecessor rank-271 theorem and exact certificates, preserved in SQUARE_SEPARATED_TRANSFER_BASIS.json and RANK_271_ANTIDIAGONAL_AND_SQUARE_PROOFS.md, together with their earlier source chain. The new proof closes the final A202427 boundary-growth obstruction. It does not independently establish the original OEIS identifications, claim mathematical priority, or represent a Lean kernel verification.

## 2. The last three triangular-grid series

Let Z(a,b) be the independent-set count on the a by b grid with horizontal, vertical and NW-SE diagonal edges, at activity one. It is invariant under transposition. Write m=n+2, h=floor(m/2), k=ceil(m/2).

By the retained formulas,

    A(n) = A202427(n) = 2 F_(m+1)^2 Z(m-1,m-1),
    B(n) = A202484(n) = Z(h,h) Z(h,k) Z(k,h) Z(k,k).

Here F_0=0, F_1=1. Since Z(1,t)=F_(t+2), A is exactly the four-rectangle partition function obtained by deleting the seams one row and one column from the boundary of the m by m grid. B is the corresponding partition function for a central split. The predecessor proves B/A202583 -> infinity, where A202583 lies between Z(m,m) and a fixed constant times Z(m,m).

We prove A/B -> infinity by a uniform strict comparison of seam restoration factors. No infinite-volume limit, surface-pressure expansion, or unproved mixing assumption is used.

## 3. Exact conditional odds recursion with clique groups

For any finite simple graph G, denote its independent-set partition function by Z(G). Write N_G[v] for the closed neighborhood of v. For the uniform measure on independent sets,

    R_G(v) = Z(G-N_G[v])/Z(G-v),
    p_G(v) = R_G(v)/(1+R_G(v)).

Both are nonnegative, and R_G(v)<=1 because G-N_G[v] is induced in G-v.

In H=G-v, partition the neighbors of v into singleton or two-vertex clique groups C_1,...,C_s. Let H_i be H with the earlier groups removed. An independent set can contain at most one vertex of C_i. Conditioning on whether it contains one gives the exact equality

    Z(H_i)/Z(H_i-C_i)
        = 1 + sum_{u in C_i} R_{H_i-(C_i minus {u})}(u).

Telescoping these ratios gives

    R_G(v) = product_i [1 + sum_{u in C_i}
                         R_{H_i-(C_i minus {u})}(u)]^(-1).

This identity holds for every finite graph and every such clique partition. At depth zero, use the unconditional interval [0,1] for the odds. At greater depths, use the displayed recursion; the product is decreasing in every child odds argument, so the child upper endpoints give a lower endpoint and the child lower endpoints give an upper endpoint. In particular the truncated recursion bounds the true odds on every finite ambient graph sharing the explored local neighborhood, regardless of any dependence on the unexamined exterior. The procedure does not assume independence of neighboring vertices.

For nonadjacent distinct vertices u,v, conditioning on u being occupied deletes N_G[u], so

    P_G(u and v occupied) = p_G(u) p_{G-N_G[u]}(v).

Adding the edge uv to G multiplies Z(G) by one minus this joint probability. Since p<=1/2 everywhere, any such edge restoration factor belongs to [3/4,1].

The implementation keeps all intervals at scale S=10^9. If a current product factor is bounded by integer endpoints lo/S and hi/S, and the scaled sum of child odds lies in [a/S,b/S], the new scaled endpoints are

    floor(lo*S/(S+b)), ceil(hi*S/(S+a)).

Conversion to occupation probability uses the increasing map R/(1+R), rounding outward. Multiplication of intervals for joint probabilities and successive restoration factors also rounds outward. All operations in the JavaScript checker are exact BigInt operations. Thus the numerical intervals below are rigorous rational inequalities, not approximated probabilities.

## 4. Uniform local seam comparison

Define the join ratio

    J(a,b;t) = Z(a,t) Z(b,t) / Z(a+b,t).

It is at least one, since the numerator counts configurations before cross-seam edges are restored. Let P(a,b;t)=1/J(a,b;t), the product of the edge-restoration factors.

Use coordinates (column,row), with the seam between columns 0 and 1. Restore crossing edges in increasing row order, restoring (0,r)--(1,r) first and (0,r)--(1,r+1) second when the latter exists. For a non-end row r, before the first edge, precisely the crossing edges starting at rows below r in this ordering have already been restored. Before the second edge the first current edge is also present.

Consider two local templates: (i) a=1, b wide; (ii) both a and b wide. With r translated to zero, construct the finite patch from row -12 through 12 and column -11 through 12 in the wide case, or column 0 through 12 in the one-column case. Include every internal horizontal, vertical and NW-SE diagonal edge, except seam edges not yet restored. Compute the two joint-probability intervals using the clique recursion of Section 3 at depth 8. The deterministic neighborhood order is row-major and a remaining neighbor is paired with the first remaining adjacent neighbor, if one exists.

For clarity, all recursion vertices lie within graph distance 8 of the selected endpoint. Every examined neighborhood at a positive recursion depth is contained in the patch. The initially deleted closed neighborhood of u in the joint calculation is also contained there. Pair selection uses only the known edges between neighbors. Hence for a finite rectangle whose row is at least K=13 from either end, and whose wide pieces have width at least K, the entire truncated recursion is identical to this patch recursion; the depth-zero bounds remain valid in the actual finite graph. This verifies the required uniformity, not merely a finite-patch estimate.

The exact scaled joint intervals are:

| Seam type | Edge | Lower / 10^9 | Upper / 10^9 |
|---|---|---:|---:|
| One column | Horizontal | 66057496 | 75909865 |
| One column | Diagonal | 65545006 | 74518530 |
| Two wide pieces | Horizontal | 46730158 | 60093565 |
| Two wide pieces | Diagonal | 46485945 | 60272649 |

Multiplying the two restoration factors with outward rounding gives

    855228296/10^9 <= P_row(one column) <= 872727237/10^9,
    883255784/10^9 <= P_row(two wide pieces) <= 908956193/10^9.

The two edge factors use the graph just before their own restoration, as required by telescoping; they are not treated as independent events.

Consequently set u=873/1000 and l=883/1000. At every interior row of the indicated finite rectangles,

    P_row(one column) <= u < l <= P_row(two wide pieces).

The C++ calculation and an independently executed BigInt JavaScript implementation agree on the scaled endpoints. The JavaScript checker also verifies the truncated odds and joint intervals against exhaustive independent-set enumeration for every simple graph on one through five vertices, at all depths from zero through the vertex count: 1099 graphs, 32110 occupancy comparisons, and 31731 nonedge joint comparisons. These finite controls test the recursion implementation; its all-ambient-graph validity comes from Section 3.

## 5. Exponential separation of the corner and central splits

Fix K=13. For t>=2K, the t-2K interior rows contain both crossing edges. There are at most 4K other crossing edges (in fact the total is 2t-1). Every exceptional restoration factor belongs to [3/4,1].

If a=1 and b>=K, this gives

    P(1,b;t) <= u^(t-2K),
    J(1,b;t) >= u^(2K) u^(-t).

If a,b>=K, it gives

    P(a,b;t) >= (3/4)^(4K) l^(t-2K)
              >= (3/4)^(4K) l^t,
    J(a,b;t) <= (4/3)^(4K) l^(-t).

Write W=Z(m,m). By splitting first vertically and then horizontally in each resulting rectangle, and using transposition,

    A/W = J(1,m-1;m) J(1,m-1;1) J(1,m-1;m-1),
    B/W = J(h,k;m) J(h,k;h) J(h,k;k).

The factor J(1,m-1;1) is at least one. For m>=4K+2, all other factors meet the preceding width and height requirements. Since h+k=m,

    A/W >= u^(4K+1) u^(-2m),
    B/W <= (4/3)^(12K) l^(-2m).

Therefore

    A/B >= C (883/873)^(2m),

where C=(3/4)^(12K) (873/1000)^(4K+1)>0 is independent of m. This proves the required divergence. It also gives a concrete, although conservative, all-width lower bound. In particular the asymptotic conclusion is not inferred from observed ratios at small n.

## 6. Full rank conclusion

All three triangular square functions occupy the same bulk growth range. The predecessor strip bounds show this range strictly below the connected labeled total and strictly above the C3 square tier on the quadratic exponential scale. The new A has the same bulk bounds: it contains the (m-1) by (m-1) triangular interior and has only two path factors and one isolated vertex in addition. Its logarithmic bulk bounds differ from the corresponding Z(m,m) bounds by at most O(m).

Thus insert A immediately above B in the predecessor strict superexponential hierarchy:

    A184208 >> A202398 >> connected labeled total
    >> A202427 >> A202484 >> A202583 >> A202413 >> A203040
    >> absolute labeled parity difference
    >> every exponentially bounded sequence.

Here X >> Y means the ratio of their magnitudes tends to infinity. In any nonzero constant combination of these square and labeled directions, the highest nonzero growth tier dominates; it cannot be canceled by the exponentially bounded rational, square-binomial and antidiagonal directions. The invertible constant transformation from the labeled even/odd counts to their total and difference is the same as in the predecessor.

The new strict comparison therefore makes A202427 independent modulo the previously certified 536-record span. Appending its identity row to the predecessor sparse transfer matrix gives 537 rows and 272 basis columns. The predecessor spans all other records, so this is both a lower and an upper rank bound. The full rank is exactly 272 and the dependence dimension remains 265.

## 7. Reproduction and remaining engineering scope

From the repository root, run:

    node tools/compile_graph_atlas_complete_formal_basis.js rebuilt-complete-formal-basis.json

The script regenerates the local graph and its exact interval certificates, runs the exhaustive small-graph controls, and appends the final identity row to the preserved rank-271 certificate. Compare against COMPLETE_FORMAL_TRANSFER_BASIS.json. For a full replay, independently rebuild and check the earlier transfer, scalar recurrence, compact-state, spectral, antidiagonal and square-separation certificates listed in the predecessor proof notes.

The full constant rational transfer rank question is closed for the retained mathematical definitions. This does not claim minimal scalar recurrences for the 18 fixed-width models retained as compact rational realizations, a finite-state realization for any of the 31 nonrational series, unlimited calculator runtime, or a proof of new OEIS bindings. Formal Lean verification and independent mathematical review are separate obligations. This research branch has not yet been integrated into the live reader website.
