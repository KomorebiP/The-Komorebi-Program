# Komorebi OEIS Transfer Compiler v1.2
## Directed proof-certified hypergraphs and exact workload planning

**Author: Komorebi P.**  
**Research date:** 22 November 2026  
**Sources:** the retained first-99,999-record official OEIS source snapshot and the v0.9 source-bound hyperedge ledger. OEIS Foundation Inc. data are attributed under CC BY-SA 4.0. Exact source attribution: <https://oeis.org/> and <https://github.com/oeis/oeisdata>.

## Scope and evidence boundaries

All-index statements here concern the **admitted, explicitly extracted mathematical formula expressions**, not independent proofs that every OEIS entry agrees with its candidate expression at all indices. Every formula model is rechecked against the current finite OEIS source excerpt before admission. Numeric matches alone are not accepted as proof. Raw OEIS program text and arbitrary formula text are never executed.

This release combines the v1.1 reversible gauge network with all-index, directed, potentially multi-input formula identities. It does not claim these identities are historically novel, or that its abstract minimum-work score predicts true runtime.

## I. Exact indexing and horizon theorem

Let the target sequence have OEIS mathematical offset \(o_a\), and an input sequence have offset \(o_b\). A formula contains the input \(b(mn+c)\). When the target's **local** index is \(t=n-o_a\), the source's local index is

\[
 j=m t+r,\qquad r=m o_a+c-o_b.
\]

If \(m\ge 1\) and \(r\ge0\), this input call is defined over every local \(t\ge0\). To compute \(a(0),\ldots,a(N)\) in local indices it is sufficient to obtain the input prefix through

\[
 M_b(N)=\max_{(m_i,r_i)\text{ referencing }b}(m_iN+r_i).
\]

This is an exact index-domain result, not a sequence identity or a performance claim. The evaluator computes the requisite source prefix and checks every output against an independent exact formula implementation.

### Verified source audit

- 539 of 539 retained full-source formula identities were re-derived as canonical exponential-polynomial equalities over \(\mathbb Q\).
- 387 are unary and 152 have at least two distinct input sequences.
- 429 require the same local prefix horizon and are immediately eligible for the v1.2 shared-workload optimizer: 312 unary and 117 multi-input.
- 110 have source calls at strictly later local indices: 75 unary and 35 multi-input. Those require typed horizon propagation and are supported for **single-edge execution**, but **not** yet included in the same-horizon global optimizer.
- 539 identities were independently evaluated for local indices 0 through 20 against exact source expressions, producing **11,319 agreeing integers** and zero mismatches.

The prior v1.1 audit had retained 378 aligned relationships and excluded 161 for textual shifts or offset uncertainty. Correct mathematical-offset normalization shows that 51 of the excluded relationships are actually aligned. The remaining 110 have positive shifts or polyphase maps and can be evaluated with explicitly extended input prefixes. The total 539 are **already algebraically known identities of extracted formulas**, not 539 newly proved OEIS conjectures.

### Examples

\[
 \mathrm{A003222}(n)=\mathrm{A013730}(n)-\mathrm{A002943}(n)
 =2^{3n+1}-2n(2n+1).
\]

\[
 \mathrm{A071237}(n)=\mathrm{A000217}(n)\,\mathrm{A002522}(n)
 =\frac{n(n+1)(n^2+1)}2.
\]

The second is a **two-input product hyperedge**: both factors must already be available for this action. Neither hyperedge may be reversed unless a separate exact inverse is proved.

## II. All-index source proof gate

For each admitted hyperedge the compiler checks these properties:

1. The raw OEIS `%F` entry's `formula_id`, target ID, text hash, and exact extracted RHS agree with the archived record.
2. Every referenced input has a current, unconflicted, normalized formula in \(\mathbb{Q}[n]\)-linear combinations of integer exponentials. The source-hash and current term-prefix hash are recorded.
3. Every dependency call passes the safe AST whitelist and is resolved to a valid affine **local** index map. No arbitrary source program runs.
4. A symbolic RHS transformation yields exactly the target's canonical exponential-polynomial coefficients. This is an all-index identity within that algebra, not a finite fit.
5. Independent exact value checks, currently for indices 0–20 in the all-edge replay, provide an implementation error control.

The joint one-input gauge engine independently revalidates its rational successive-term coboundary identities. It admits 642 compatible edges in the combined graph. Two overlapping formula models with inconsistent symbolic forms have their mixed routes excluded instead of equated by finite matching.

## III. Directed shared-computation theorem

Let \(V\) be a **finite selected node set**, and let each action \(e\) have a target \(v_e\), a set of prerequisites \(I_e\subseteq V\setminus\{v_e\}\), and a nonnegative declared work score \(w_e\). Direct calculation is an action with \(I_e=\varnothing\). A cached, source-fingerprint-verified prefix belongs to the initial set \(S_0\).

A legal action may be executed in state \(S\) if

\[
 I_e\subseteq S,\quad v_e\notin S;
 \qquad S\longrightarrow S\cup\{v_e\}\quad\text{at cost }w_e.
\]

For target set \(T\), finding the minimum sum of action scores is equivalent to a shortest-path problem from \(S_0\) to any state containing \(T\) in the directed state graph with vertices \(2^V\).

**Proof.** A legal computation DAG can be topologically ordered, giving a path of subset states of identical score. Conversely, every admissible subset-state path is a topological execution of a legal computation DAG, because it only uses inputs already present. Nonnegative edge costs permit Dijkstra's algorithm to return a shortest path. Therefore the planner is optimal **within the enumerated finite action set and declared additive score model**. \(\square\)

The algorithm enforces explicit limits on \(|V|\) and expanded states. If the state budget is exceeded, it raises an exception instead of reporting an unproved optimum. The full global hypergraph, omitted operations, bit complexity, scheduling, memory pressure, and actual runtime are outside the stated optimum.

The current planner admits 429 same-horizon directed hyperedges and 642 invertible gauge actions (in both directions) plus one direct source-evaluation action per selected formula model. Query-local backward slicing limits the state space; each query reports its selected nodes and action counts. Costs are transparent heuristics, and actual runtimes are separately checked.

## IV. Exact cache and empirical selector

An admitted cache prefix is bound to a current raw-source SHA-256, current integer-term-excerpt SHA-256, the chosen formula identity, its canonical expression fingerprint, its index offset, and the cached integer digest. A changed formula or stored term excerpt invalidates the cache.

The empirical selector evaluates both the proposed shared DAG and independent exact formulas, checks every output integer for equality, then times both with repeated runs. The calibration cost is reported and is **not** free. The selected winner is specific to a machine and workload, not a performance guarantee for other indices.

Three independent 301-term, three-sequence examples were tested. One subtraction workload was faster through the shared DAG in the recorded run, while product and rational-combination workloads were slower. See `outputs/hypergraph-benchmark-v12-full.json` for exact times and verified output digests. Source loading and proof replay are additional startup costs, not included in these execution-only timings.

## V. Reproduction

Use the archived `oeis-full.sqlite3` from the previously released first-99,999-record OEIS artifact; the source database is intentionally **not** duplicated in this small compiler package.

```text
python -B tools/sequence_hypergraph_workload.py \
  --db oeis-full.sqlite3 \
  --hyperedges outputs/verified-formula-hyperedges-v09.jsonl \
  --gauges outputs/structured-gauges.jsonl \
  --extra outputs/chain-anchors.jsonl \
  --targets A003222 A002943 A013730 --nmax 300 \
  --output outputs/example-v12-plan.json

python -B tools/benchmark_sequence_hypergraph_workload.py \
  --db oeis-full.sqlite3 \
  --hyperedges outputs/verified-formula-hyperedges-v09.jsonl \
  --gauges outputs/structured-gauges.jsonl \
  --extra outputs/chain-anchors.jsonl \
  --nmax 300 --runs 5 \
  --output outputs/hypergraph-benchmark-v12-full.json

python -B tools/render_sequence_hypergraph_atlas.py \
  --ledger outputs/v12-certified-hyperedges.jsonl \
  --output exact-hypergraph-atlas-v1.2.html

python -B -m unittest discover -s tools -p test_sequence_hypergraph_workload.py -v
```

The offline tests use a wholly synthetic, independently constructed SQLite fixture and do not download OEIS data. Full 539-edge source replay requires the retained 99,999-entry snapshot and matching v0.9 proof ledger.

## VI. Remaining gaps

1. **Variable-horizon optimal planning.** A composed path of shifted or polyphase hyperedges has node-specific demands. Its true score cannot be modeled as a single shared \(N\). Extend the search state to include required prefix horizons before promoting the remaining 110 edges into multi-step optimization.
2. **Bit-aware cost.** Large integers, factorials, rational reduction, and memory reuse dominate practical cost. The present model does not predict those reliably.
3. **Broader formula classes.** Hypergeometric, holonomic, algebraic-series and nonholonomic objects require additional exact certificate engines beyond exponential-polynomial identities.
4. **Full-source corpus coverage.** The archived dataset covers 99,999 records, not the complete contemporary OEIS. It does not supply an all-index OEIS identification for every stored expression.

**Release status:** Reproducible research compiler, v1.2. No historical novelty or universal-optimality assertion.
