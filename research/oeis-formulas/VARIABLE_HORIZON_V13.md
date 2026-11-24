# Komorebi OEIS Variable-Horizon Transfer Compiler, v1.3

**Author: Komorebi P.**  
**Research status:** Reproducible exact formula compiler, not a proof of every identified OEIS sequence identity.

## 1. The need for source-specific horizons

An exact indexed formula can express an output sequence at local index \(n\) through source sequences at local indices \(m_j n+r_j\), where \(m_j\geq1\) and \(r_j\geq0\). A request for an output prefix \(0\leq n\leq N\) then requires the source prefix through

\[
H_j(N)=\max_{\text{references to source }j}(m_jN+r_j).
\]

The maximum, **not a sum**, is necessary when several arguments share a source. For composable maps \(f(n)=mn+r\) and \(g(k)=pk+q\),

\[
g(f(n))=pmn+(pr+q).
\]

These are *local* coordinates. A dependency appearing in an OEIS raw formula with target mathematical offset \(o_t\), source offset \(o_s\), and source argument \(m\,n_{\mathrm{math}}+c\) has source-local index

\[
m n_{\mathrm{local}}+(m o_t+c-o_s).
\]

The compiler reconstructs this affine map from the whitelisted source-expression AST before executing a transfer. Any negative local-index base, nonpositive integer slope, or unsupported expression is rejected.

### Real two-hop example

Two source-linked all-index **formula identities** are

\[
\mathrm{A005449}(n)=\mathrm{A000217}(2n)-\mathrm{A000217}(n),
\]
\[
\mathrm{A016789}(n)=\mathrm{A005449}(n+1)-\mathrm{A005449}(n).
\]

At requested output horizon \(N=20\), the explicit route needs the intermediate A005449 through \(21\), and A000217 through \(42\). The resulting formula is \(3n+2\). All 21 target outputs agree exactly. The cost-aware planner **rejects this unnecessarily expensive route** and computes the simple linear target directly.

## 2. Finite optimality theorem

Fix a finite node set \(V\), a finite admissible horizon set \(L_v\) for every \(v\in V\), a finite set of source-checked direct/gauge/hyperedge actions, and a nonnegative additive **full-prefix recomputation** cost \(w_e(H)\) for each action producing prefix \(0..H\). The state \(s=(s_v)_{v\in V}\) records the largest available horizon tier for each node, with \(s_v=0\) for unavailable. An action may upgrade its target's tier only if each prerequisite's already available prefix covers its certified affine-index demand. A longer result **replaces** the shorter result and pays the full stated action cost; this model does not assume free incremental continuation.

Every permitted transition strictly increases one coordinate. Therefore all legal finite computations correspond to directed paths in this state graph. Conversely every state path is a legal topologically ordered sequence of exact computations, because source prefixes are available before consumption. Dijkstra's algorithm returns a globally minimal sum of the declared costs **within this explicitly enumerated finite state graph**.

This theorem does not imply fastest wall-clock execution, minimum bit complexity, an optimum over omitted operations or horizon tiers, nor a solution for the whole OEIS corpus. The planner raises `PlanningBudgetExceeded` if its horizon-tier or state-search bound is exceeded rather than reporting an unproved optimum. For \(h_v=|L_v|\), the naive state count can reach \(\prod_v(h_v+1)\), so search limits are essential.

## 3. All-index certificate admission

An admissible hyperedge is first rederived against its current raw OEIS formula text and the exact, extracted exponential-polynomial models. Exact symbolic equality of canonical \(\mathbb{Q}\)-exponential-polynomial expressions, and separately rechecked source identities, justify the all-index formula transfer. At runtime the compiler recalculates its affine argument maps and independently rechecks the same symbolic identity before evaluation. Source hashes, evaluator fingerprints, and input prefix lengths are enforced.

**This proves identities among extracted mathematical formula expressions.** The underlying OEIS sequence record is associated with those expressions by exact *finite reference-term checks*. For every transferred identity, an independent OEIS all-index identification remains outside the certified scope unless separately available.

Similarly, cached values are not automatically correct merely because the checksum matches. By default the v1.3 executor checks all supplied cached values against the current exact source formula, including coherently modified values with a recomputed checksum. Trusted-cache use can explicitly disable this expensive verification; that mode provides only change detection, not protection against a maliciously forged cache.

## 4. Official-source audit

Source: the retained 99,999-sequence OEIS `.seq` snapshot, as archived in the preceding releases. Snapshot SQLite SHA-256: `a121d7a6a5b6aa78a5a333fe748b604f170511bf8250ca16533f58cbcfa9e9f5`.

- 99,999 OEIS records retained; SQLite integrity check returned `ok`.
- 3,403 source-linked formula models rechecked against available finite OEIS terms.
- 539 exact source-formula hyperedge certificates rederived.
- 110 contain nontrivial affine index maps, comprising 75 one-input and 35 multiple-input identities.
- 110/110 indexed transfer formulas independently replayed at local indices 0 through 20: **2,310 exact evaluations, zero failures**.
- 110/110 bounded, real-source horizon-aware optimizer queries executed and their output prefixes independently checked: **2,310 additional exact value comparisons, zero failures**.
- For the 110 individual requests, the cost heuristic selected 27 indexed transfers and preferred independent direct evaluation in 83 cases.
- The 27 indexed choices had median heuristic work-score reduction of approximately 2.076×. This is **not a runtime ratio**.
- A source-revalidated Catalan-to-central-binomial gauge produced both 21-term prefixes exactly, selecting a direct Catalan prefix followed by the certified gauge.
- The two inconsistent v1.2 representation overlaps (`A011557`, `A053310`) remain excluded from mixed-formula paths.

Reproducible full-data receipt: `outputs/variable-horizon-real-audit-v13.json`. The `source_db_sha256`, `raw_source_certificate_replay`, selected routes, source-index demands, and replay hashes enable further auditing.

## 5. Execution-time calibration

The supplemental benchmark compared exact independent source formulas against the selected variable-horizon DAG on 301-term real-source prefixes. The observations were mixed, and **all competing integer values agreed exactly**:

| Target | Planner choice | Direct ÷ shared elapsed-time ratio | Measured winner |
|---|---|---:|---|
| A006331 | indexed transfer | 0.34× | direct |
| A086653 | indexed transfer | 1.29× | shared |
| A047732 | indexed transfer | 0.63× | direct |
| A016789 | direct | 0.96× | direct |

These are medians of **three** runs in the measured environment. Startup, source loading, ledger replay, and the initial cross-evaluation were excluded. The benchmark includes all runtime proof checks inside the shared executor and should be repeated before making performance claims for another machine or workload. The optional `measured_variable_strategy()` explicitly calibrates both methods and chooses the observed winner.

## 6. Reproduce

From the compiler root, with a source database matching the SHA-256 above:

```bash
python -B -m unittest discover -s tools -p test_sequence_variable_horizon.py -v
python -B -m unittest discover -s tools -p test_sequence_variable_horizon_atlas.py -v
python -B tools/audit_sequence_variable_horizon.py \
  --db oeis-full.sqlite3 \
  --hyperedges outputs/verified-formula-hyperedges-v09.jsonl \
  --extra outputs/chain-anchors.jsonl \
  --gauges outputs/structured-gauges.jsonl \
  --nmax 20 --output outputs/variable-horizon-real-audit-v13.json
python -B tools/render_sequence_variable_horizon_atlas.py \
  --audit outputs/variable-horizon-real-audit-v13.json \
  --output variable-horizon-atlas-v1.3.html
python -B tools/benchmark_sequence_variable_horizon.py \
  --db oeis-full.sqlite3 \
  --hyperedges outputs/verified-formula-hyperedges-v09.jsonl \
  --extra outputs/chain-anchors.jsonl \
  --targets A006331 A086653 A047732 A016789 \
  --nmax 300 --runs 3 \
  --output outputs/variable-horizon-benchmark-v13.json
```

The small offline regression tests need **no external OEIS data**. The full-data audit needs the exact archived SQLite snapshot because source-record and formula receipts are intentionally bound to it.

## 7. Next steps

1. Support explicit finite **sparse** index sets rather than requiring every intervening prefix term. This is useful when the target asks for just one large-index value and the transfer only needs a few source values.
2. Introduce bit-complexity and measured-kernel cost estimates for large integers, and account for proof replay and cache validation overhead.
3. Extend the proof-admission machinery to P-recursive, algebraic generating-function, and nonholonomic dependencies currently outside the exponential-polynomial identity checker.
4. Import and normalize the remaining OEIS corpus beyond the archived 99,999 records. Neither this artifact nor the cited tests establish full OEIS coverage.

**Novelty:** This is a research software construction applying established algebraic techniques. Source and performance evidence support the implementation claims above, not a general claim of new theorems about all OEIS entries.
