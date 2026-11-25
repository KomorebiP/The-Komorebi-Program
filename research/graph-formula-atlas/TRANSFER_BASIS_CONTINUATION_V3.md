# Fixed-width array continuation and global rank 223

Author: Komorebi P.

## Certified inventory

This checkpoint extends the rank-193 predecessor without changing its immutable source catalogues or previously certified rows. The atlas inventory remains 537 records. The constant rational span has 488 represented records and exact rank 223; its dependence dimension is 265. The two new layers add 21 and nine independent functions. Exact modular elimination on the first 320 coefficients at primes 1000003 and 1000033 gives ranks 214 and 223 in the corresponding layers. The final largest pivot index is 222. Every new basis function has an identity transfer row; all predecessor spanning identities are retained.

The 99 fixed-width finite-state/block models now have 81 expanded, reduced rational generating functions and 18 explicitly deferred expansions. Across the 81 models, the sums of the original state counts, equitable quotient dimensions, and minimal eventual recurrence orders are 124278, 13395, and 9491, respectively. The state reductions concern summed dimensions, not measured wall-clock speed. The three passes performed 13395 exact residual checks and 161 independent array-evaluator comparisons, with no reconstruction failures. One attempted browser evaluation in the third pass hit the prior resource budget and was not counted as a comparison.

## Sparse transition theorem

For binary forbidden-word and sliding-window models of window length L, a history h of L-1 rows fixes the admissible next bit at each column. A precomputed table maps each length-(L-1) prefix to the subset of {0,1} that completes an allowed vertical word. For diagonal models intersect the vertical subset with the corresponding NW-SE diagonal subset whenever a complete diagonal fits. The resulting requirements are two masks O and Z, recording mandatory ones and mandatory zeros. If O and Z intersect, there is no admissible next row. Otherwise a horizontally admissible row r extends h exactly when (r & O) = O and (r & Z) = 0. This is necessary and sufficient because all newly completed windows end in the new row and the row list already enforces horizontal windows. Cache the candidate list by the mask pair. The resulting row-history edges coincide with the original transfer definition, not an approximation. Block-sum models retain direct compatible-row checks.

The subsequent equitable partition and exact residual/Cayley-Hamilton certificates have the same proof as the predecessor. CRT and shortened modular Berlekamp-Massey samples propose recurrences only; acceptance still requires exact residuals for the full quotient dimension and a coprimality witness for the reduced numerator and denominator.

## Reproduction

Run from the repository root with Node.js:

- node tools/compile_graph_array_state_rational_v2.js rebuilt-v2.json
- node tools/compile_graph_atlas_state_basis_v2.js rebuilt-basis-v2.json
- node tools/compile_graph_array_state_rational_v3.js rebuilt-v3.json
- node tools/compile_graph_atlas_state_basis_v3.js rebuilt-basis-v3.json

The continuation scripts use the retained predecessor certificate JSON files. Replay the earlier compilers to independently regenerate those predecessor files.

## Remaining fixed-width expansions

- A184213: quotient budget; quotient dimension 1072; raw state count 4096.
- A184214: row budget.
- A184215: row budget.
- A184216: row budget.
- A202469: edge budget; raw state count 22201.
- A202470: state budget; raw state count 75076.
- A202569: quotient budget; quotient dimension 2570; raw state count 35937.
- A202613: quotient budget; quotient dimension 779; raw state count 961.
- A202614: quotient budget; quotient dimension 1736; raw state count 2116.
- A202615: quotient budget; quotient dimension 3791; raw state count 4624.
- A202721: state budget; raw state count 175616.
- A202896: quotient budget; quotient dimension 1366; raw state count 2116.
- A202897: quotient budget; quotient dimension 2936; raw state count 4624.
- A203047: quotient budget; quotient dimension 7928; raw state count 46656.
- A203353: quotient budget; quotient dimension 1058; raw state count 4624.
- A203354: quotient budget; quotient dimension 2523; raw state count 12100.
- A203405: quotient budget; quotient dimension 1190; raw state count 4624.
- A203406: quotient budget; quotient dimension 3050; raw state count 12100.

The other 31 atlas records outside the current transfer matrix are 29 variable-width array models and two connected labeled-graph parity models. No new OEIS bindings, literature-priority claims, or unbounded runtime guarantees are asserted. The research branch is not the live publication.
