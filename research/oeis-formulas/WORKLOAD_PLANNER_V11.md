# Komorebi OEIS v1.1: exact gauge coordinates and shared-workload planning

**Author: Komorebi P.**  
**Scope:** Source-bound exact identities between admitted formula expressions. A finite OEIS match is not a proof that the database entry equals that expression at every index.

## 1. Data and admissibility

The input is the retained official OEIS first-99,999-record SQLite snapshot and the v1.0 gauge ledger. The loader reevaluates currently admitted exact source formulas, checks their SHA-256 source/evaluator fingerprints, and **re-derives every accepted rational gauge certificate**. No arbitrary OEIS `%F` line, program field, or third-party code is executed.

Of **975** source-bound gauge records, **650** are eligible for a whole-prefix query at local index `n>=0`; the other **325** require a positive tail-start index, so v1.1 excludes them until exact head/tail boundary stitching is available. The admitted 650 gauges join 288 formula models in 35 connected components. All certificates preserve OEIS offsets and are invertible with nonzero factors on the entire admitted local index domain.

The mathematically correct name for this data structure is a **multiplicative formula-transfer groupoid**, not a quotient of the entire OEIS sequence universe.

## 2. Exact transfer coordinates

A source-to-target gauge `u -> v` has the form

\[
  f_v(n)=g_{uv}(n)f_u(n),\qquad
  g_{uv}(n)=K_{uv}c_{uv}^n\frac{L_{uv}(n)}{L_{uv}(0)},
  \quad L_{uv}(n)=\prod_j(a_jn+b_j)^{e_j}.
\]

`K,c` are nonzero rationals, the `a_j` are positive integers, the `b_j` are positive integers after the full-prefix restriction, and the exponents `e_j` are integers. A gauge is accepted only after proving the rational identity

\[
  \frac{f_v(n+1)/f_v(n)}{f_u(n+1)/f_u(n)}
   =c\frac{L(n+1)}{L(n)} \quad\text{in }\mathbb{Q}(n),
\]

and matching one exact initial ratio. This is an all-index formula identity, not coefficient interpolation.

**Composition.** Along a path `u -> v -> w`, multiply the constants and exponential rates and add exponents of identical affine factors. Reversal inverts the gauge. The factor product may be rational but stays nonsingular on the admissible domain.

**Cycle check.** For a closed path `gamma`, write the product as `K_gamma*c_gamma^n*L_gamma(n)/L_gamma(0)`. It equals 1 at every index if and only if

\[
  K_\gamma=1,\qquad
  c_\gamma\frac{L_\gamma(n+1)}{L_\gamma(n)}=1\quad\text{in }\mathbb{Q}(n).
\]

A spanning forest produces one fundamental cycle per non-tree edge. Since multiplicative gauges commute and every cycle is an integral combination of the fundamental cycles, these tests imply path-independent coordinates throughout each connected component.

**Real audit:** 650 admitted edges, 288 vertices, 35 components, `650 - 288 + 35 = 397` independent cycles. **397 of 397 exact checks passed.** The resulting spanning forest stores 253 source-bound coordinate charts. This audit is a consistency test of the formula compiler and its transfer ledger; it is not 397 newly discovered independent OEIS theorems.

## 3. Exact modeled optimum for several requested outputs

Let the query request complete prefixes `f_t(0),...,f_t(N)` for target set `T`. Construct an undirected graph of the admissible invertible gauges. Give edge `e` a nonnegative estimated arithmetic score `w_e(N)`. Add a virtual root `r` with one edge `r -> v` of cost `d_v(N)` for each formula model: it means evaluating that source formula directly, either by its exact expression or by its proved rational term ratio. A source-bound, immutable cached prefix creates a cost-zero root connection.

A root-connected tree spanning every requested target specifies a computation DAG: calculate each direct base once and apply each selected gauge once, with all intermediate values shared.

**Theorem (within the declared additive model).** The minimum total source-plus-transfer score among all permitted shared rooted computation trees is the minimum Steiner tree connecting `T union {r}`. For `k=|T|<=6`, Dreyfus-Wagner subset dynamic programming returns the exact minimum of this finite model:

\[
  D[S,v]=\min_{\varnothing\ne A\subsetneq S}
        \bigl(D[A,v]+D[S\setminus A,v]\bigr),
\]

with shortest-path relaxations after each subset combination and singleton bases `D[{t},t]=0`. Reconstruct from `D[T,r]`. The implementation verifies the reconstructed cost equals the dynamic-programming optimum and rejects cycles or missing targets. Exhaustive edge-subset enumeration independently verifies the algorithm on small graphs.

**Boundary:** This is not the fastest possible algorithm in real time. The weights omit detailed integer bit complexity, cache locality, Python overhead, non-gauge transformations, and the cost of seeking other mathematical representations. The exact optimization guarantee applies only to this specific graph and score model.

## 4. Empirical check and negative controls

All result prefixes are compared against independent exact formula-ratio evaluation. Five-run medians on one CPU show the **independent-direct / shared-transfer** runtime ratio:

| Exact prefix workload | Ratio | Faster observed strategy |
|---|---:|---|
| 3 Catalan/binomial-family outputs through n=1000 | ~1.01x | Shared |
| Same 3 through n=2500 | ~0.94x | Independent |
| 5 related outputs through n=1000 | ~1.18x | Shared |
| Same 5 through n=2500 | ~1.00x | Independent (marginal) |

The actual benchmark receipt includes precise medians, source fingerprints, and hardware metadata. This comparison is deliberately **against separately streamed exact hypergeometric recurrences**, not a weaker baseline that recomputes binomial coefficients independently at each index. The empirical selector runs both candidate plans, checks equality, and selects the measured winner; the calibration runs have a real upfront cost.

### Previously computed prefixes

Saved prefixes are accepted only when their source SHA-256, evaluator SHA-256, length, and integer-value digest match the current model. An admitted prefix can be frozen as an immutable tuple and reused without rehashing it on every iteration. This can save repeated computation across related later queries; it does **not** make the original computation or the one-time cache admission free.

## 5. Reproduce

Use the official 99,999-entry OEIS data artifact from the earlier v0.9 release (place the SQLite database at `oeis-full.sqlite3`), plus the v1.0 source-bound ledgers `outputs/chain-anchors.jsonl` and `outputs/structured-gauges.jsonl`:

```bash
python -B tools/sequence_gauge_atlas.py \
  --db oeis-full.sqlite3 --extra outputs/chain-anchors.jsonl \
  --gauges outputs/structured-gauges.jsonl \
  --output outputs/exact-gauge-atlas-v11.json

python -B tools/sequence_workload_planner.py \
  --db oeis-full.sqlite3 --extra outputs/chain-anchors.jsonl \
  --gauges outputs/structured-gauges.jsonl \
  --targets A000108 A000984 A002544 --nmax 500 --evaluate \
  --output outputs/example-workload-plan.json

python -B tools/benchmark_oeis_workload_v11.py \
  --db oeis-full.sqlite3 --extra outputs/chain-anchors.jsonl \
  --gauges outputs/structured-gauges.jsonl \
  --runs 5 --output outputs/workload-benchmark-v11.json

python -B -m unittest discover -s tools -p 'test_sequence_workload_planner.py' -v
python -B -m unittest discover -s tools -p 'test_sequence_gauge_atlas.py' -v
```

All source files are Python 3.10+ standard library. The `--evaluate` mode checks selected computed values against their current exact source formula expressions. The 99,999-record source database remains separate from the small v1.1 reproducibility bundle to avoid a redundant large download.

## 6. Next construction

The current cost optimizer is restricted to full-prefix, nonsingular, invertible **one-input gauges** and a maximum of six simultaneous targets. The next mathematically significant extension is a proof-gated, directed **multi-input** planner for additive and multiplicative hyperedges, where planning becomes a directed Steiner or hypergraph covering problem. Separate algorithms will also be needed for generic D-finite, algebraic, P-recursive, and nonholonomic formula families. Numerical holdout matching never supplies the proof gate.
