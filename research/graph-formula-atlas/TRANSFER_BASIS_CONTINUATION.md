# Global rational transfer basis: rank 193

Author: Komorebi P.

## Scope

The 537-record atlas is the maintained publication inventory. This research continuation covers 458 of those records, not a new inventory of OEIS admissions.

- 363 graph/tree core and nonbipartite-complement models: rank 107.
- Add 40 fixed-width reduced array models and four graph-walk models: rank 142, with nine additional exact dependencies.
- Add 51 fixed-width finite-state/block models: rank 193.

The 458 x 193 transfer matrix has 265 dimensions of constant rational linear dependence. These are linear identities between generating functions, not necessarily combinatorial bijections. For every target, the sparse row specifies a positive integer denominator D and integer multipliers c_j such that D G_target = sum_j c_j B_j. Every array or walk uses its original index convention, with zero padding before its initial offset.

## Proof and certificate structure

The original 181 core dependence certificates and 75 complement transfer rows are retained from TRANSFER_BASIS.json. The nine additional dependencies in ENLARGED_TRANSFER_BASIS.json are checked by clearing the original common polynomial denominator (degree 600) and comparing exact integer polynomials, using 606 coefficient coordinates. The three compact parity tensor models do not need expanded characteristic polynomials for the independence witness: their exact strip recurrences supply the modular coefficients.

For fixed-state arrays, let M be the row-history transition matrix and U the zero-one membership matrix of an equitable partition. Refinement starts with one class and splits by the counts of outgoing edges into every current class. Stable classes define K by M U = U K. Since the all-ones vector is U 1 and the row vector of class sizes is 1^T U = c^T, the full count is exactly c^T K^n 1. This is an all-index identity. Modular Berlekamp-Massey and CRT propose an integer scalar recurrence. For a quotient of dimension s, checking s consecutive exact residuals starting at a recurrence order L suffices: the residual is c^T K^(n-L) times a fixed vector, hence Cayley-Hamilton propagates zero residuals to every later index. The numerator includes the finite prefix and zero padding before index 1. Modular coprimality with preserved degrees certifies reduced rational denominators, and thus minimal eventual scalar recurrence order.

The 51 new rational functions have independent coefficient vectors together with the 142 predecessor basis functions. Exact modular Gaussian elimination at primes 1000003 and 1000033 gives rank 193 in the first 256 coefficient positions; in both cases the largest pivot index is 192. A nonzero minor over either field gives a rational independence witness because the original coefficients are integers. The predecessor spanning certificates plus the 51 identity rows prove the upper bound 193. A duplicated basis vector is rejected by the independence check.

## Verification and remaining scope

- 51 fixed-state scalar rational functions certified; 3446 exact residual checks, 102 independent calculator comparisons, zero reconstruction failures within the attempted expansion budget.
- Aggregate state counts for those 51 models decrease from 13632 to 3446 under equitable partition refinement. The minimal scalar recurrence dimensions may be smaller still.
- 48 other fixed-width finite-state models are explicitly resource-deferred, not failed mathematical claims.
- 29 variable-width array models and two connected labeled-graph parity models lie outside the present rational basis.
- No new OEIS bindings, asymptotic complexity superiority, or literature priority is asserted.

Reproduce from a checkout with Node.js:
    node tools/compile_graph_atlas_state_basis.js rebuilt-state-basis.json
    node tools/compile_graph_array_state_rational.js rebuilt-state-rational.json

The original seven archived atlas sources remain unchanged. This research branch is separate from the already merged publication revision.
