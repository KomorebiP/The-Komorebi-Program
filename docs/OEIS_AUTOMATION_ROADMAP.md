# OEIS automation: reproducible acquisition, exact expression proofs, and open gaps

**Author: Komorebi P.**
**Checkpoint: 23 November 2026**
**Status: Implemented offline gap scanner, restricted exact rational-expression kernel, bounded-order C-finite bridge certificates, CI workflow. The full OEIS harvest and any production website integration are not claimed executed.**

## Mathematical and evidentiary separation

The Komorebi Sequence Network has 916 OEIS nodes and 1,559 archived transfer *views* (539 formula hyperedges, 975 tail hypergeometric gauges, 41 rational-OGF Riordan maps, four quadratic directed views). The pinned source formula-text manifest has 8,853 `%F` lines from 845 of those 916 entries, with the original CC BY-SA 4.0 source attribution. These numbers describe the existing published snapshot, not the full OEIS, not independent proofs of every named sequence, and not 1,559 independent theorem discoveries.

The code maintains five independent statuses:

1. `source_text`: original OEIS `%F` or `%Y` text, revision and SHA recorded. Never executable code.
2. `lexical_lead_not_a_transfer`: a textual cross-reference, or an external sequence needed to expand the graph. No identity follows.
3. `exact_rational_expression_identity`: a proved equality of a restricted parser's expressions in the field `Q(n)` (or an exact affine polynomial relation). This needs review for original expression domains.
4. `all_index_formula_identity`: evidence inherited unchanged from the existing curated transfer ledger, not an OEIS identification proof.
5. `oeis_identification_verified`: **not automatically assigned by this program.** Requires independent proof of a recurrence/OGF with initial data or equivalent OEIS definition.

Cross-component membership uses the *undirected incidence graph* of directed/hyperedge formula relationships, solely to prioritize review. It does not assert invertibility, canonical equivalence, or recoverability through every directed edge. For actual route optimization, keep the directed hypergraph and guard edge domains, index maps, valuations, reconstruction fibers, and computational complexity.

## Running the implemented tools

No third-party Python package is required. To generate a complete review of the **existing pinned public network and formula index** from a checkout of the Komorebi repository:

```sh
PYTHONPATH=tools python -m unittest discover -s tools -p test_oeis_gap_automation.py -v
python tools/oeis_gap_automation.py audit \
  --network manifests/sequence-transfer-network.json \
  --formulas manifests/sequence-network-formula-text.json \
  --recurrence-seeds manifests/oeis-cfinite-recurrence-seeds.json \
  --out verification/oeis-gap-discovery/curated
```

When a recurrence registry is supplied, the output also contains `cfinite_recurrence_certificates.json`. The seed registry currently records ten explicit constant-coefficient sequence definitions across orders 2–5; the engine proves ten directed all-index abstract recurrence identities, including **two formula bridges between different components** of the pinned network. These are familiar classical identities, not historically new discoveries. Source-definition identification requires its own review.

The output contains `audit.json`, `review_queues.json`, `cross_component.csv`, `new_id_frontier.csv`, `in_component.csv`, and `outside_to_network.csv`. Every record includes evidence status, source ID, referenced ID, fields, formula excerpt, component IDs, heuristic priority, and a next review action. The report records input SHA-256 hashes. CSV contains original source excerpts and should be handled as untrusted, attributed text.

For the **full OEIS formula corpus**, independently clone a revision of `https://github.com/oeis/oeisdata` (main records under `seq/A123/A123456.seq`, not the `stripped.gz` bulk terms export). A pinned SHA should be recorded. Git LFS is not required for the `.seq` text. Then:

```sh
OEIS_REV=$(git -C /path/to/oeisdata rev-parse HEAD)
python tools/oeis_gap_automation.py ingest --oeis-dir /path/to/oeisdata \
  --revision "$OEIS_REV" --db /path/to/oeis-source.sqlite3
python tools/oeis_gap_automation.py audit \
  --network manifests/sequence-transfer-network.json \
  --source-db /path/to/oeis-source.sqlite3 \
  --recurrence-seeds manifests/oeis-cfinite-recurrence-seeds.json \
  --out /path/to/oeis-full-review
```

This is a bounded-memory scanner over the official source files. Repeated ingestion skips unchanged source files by content SHA and changes only their affected SQLite rows. It preserves original `%F` and `%Y` lines, original OEIS offsets as raw `%O`, the source file path, and the revision for changed entries. Partial imports never delete records. When source snapshots differ in revision, the scanner does not pretend the combined graph was certified against the newer OEIS data.

The new `oeis-gap-discovery.yml` workflow automatically runs curated checks on relevant PRs and pushes, and uploads the review queue as a workflow artifact. The full OEIS clone is *manual opt-in* via `workflow_dispatch` input `full_oeis_harvest=true`, since it is resource-intensive. Neither workflow silently pushes generated claims into published pages or upgrades a candidate to a theorem.

## Exact proof engine: present scope

A strict Python AST whitelist parses only simple `a(n) = ...` expressions with rational arithmetic, the variable `n`, bounded integer exponents, and fixed-lower-argument `binomial(n,k)` for small nonnegative integer `k`. There is no `eval`, no imports, no attribute access, no arbitrary function calls, and no execution of OEIS code. Exact `Fraction`-polynomial arithmetic implements rational functions in `Q(n)` with Euclidean GCD reduction and cross-multiplication checks.

On cross-reference leads that have parseable formula candidates for *both* endpoints, the scanner tries exact expression equality and a restricted affine polynomial transfer:

\[
T(n) = cS(n) + b n + a, \quad a,b,c\in\mathbb{Q}.
\]

It accepts this identity only after exact algebraic checking of all coefficients, with small coefficient/degree caps. For example, `S(n)=n(n+1)/2` and `T(n)=3S(n)-2n` produce an exact polynomial identity; this alone is not a proof that two particular OEIS entries satisfy the formulas for all `n`. When a source expression has a removable pole, the actual source domain still matters. The audit is a *candidate proof assistant*, not a universal theorem prover.

## Automatic bounded-order recurrence transfer bridge

For two sequences satisfying the *same* constant-coefficient recurrence of order `d` and given their first `d` values, the engine seeks

\[ T(n)=\sum_{j=0}^{d-1} c_j S(n+j). \]

It solves the `d` equations for `n=0,...,d-1` by exact rational Gaussian elimination, solves compatible singular shift-orbits with a canonical free-variable choice, and reports inconsistent systems without pretending other transforms cannot exist, and derives an all-index proof by recurrence induction. The registry also includes polynomial sequences of degrees 2–4; finite-difference recurrences make their transfer certificates routine. Applied to the four stated seed definitions, it automatically generates

\[ L_n=2F_{n+1}-F_n, \qquad 5F_n=2L_{n+1}-L_n,\]
\[ C_n=P_{n+1}-P_n,\qquad 2P_n=C_{n+1}-C_n.\]

Here `P=A000129` and `C=A001333` are the stated Pell and companion sequences. The **Fibonacci/Lucas pair links two previously separate network components**. These are exact conditional recurrence theorems. The seed OEIS identification has to be established separately, and mathematical novelty is not claimed.

## Automated next stages (not yet implemented)

| Priority | Gap | Mechanizable advance | Exact acceptance gate |
|---|---|---|---|
| P0 | Source identification and general C-finite discovery | Parse recurrences and OGFs together with offsets/initial coefficients; verify enough conditions to make an induction or formal-series proof | Independently certified defining recurrence/OGF and initial conditions, with exact domain |
| P0 | OEIS corpus coverage | Perform one full pinned `oeisdata` ingest and compare lineage by source file SHA; incremental refreshes thereafter | Source revision, file count, formula count and source SHA receipt |
| P1 | Transfer grammar | Extend the restricted parser to factorial lanes, Pochhammer ratios, polynomial exponentials, hypergeometric shifts, and holonomic linear operators | Exact all-index symbolic identities; singular indices and parameters checked |
| P1 | Nontrivial bridge search | Candidate generation from cross-references, canonical OGF signatures, recurrence/operator normal forms, and characteristic polynomials | Independently replayed operator proof plus OEIS premises |
| P1 | Graph route optimization | Directed hypergraph dynamic programming with target-index sets, precision contracts, and shared source DAGs | A reproducible, certified lower cost than the baseline on named queries |
| P1 | Precision-aware transfer | Connect v1.7 regular atlas and Hensel-branch tools through a typed contract interface | Query-specific exact residue/Smith certificate; no unsupported singular extension |
| P2 | Automatic singular handling | Stratify zero-Jacobian sets; use Newton/Hensel regularity where available; record unresolved strata | Proof that the branch atlas covers the requested admissible domain |
| P2 | Independent proof replay | Generate proof objects for polynomial/rational identities and a small Lean checker, before adding wider algebra | Lean kernel replay without admitted placeholders |
| P2 | Resource-aware discovery | Measure symbolic bit complexity, parsing rejections, and wall-clock costs; prioritize high-impact bridge candidates | Holdout benchmarks and exact result checks |
| P3 | Website access | Keep source text and proof statuses separated, add filters for verified relations, conjectural leads, and blockers | On-site accessibility, cross-browser tests, stable indexed link URLs |

## Implementation notes and limitations

- This tool does *not* prove an arbitrary OEIS formula by parsing it; the parser intentionally rejects most unrestricted OEIS syntax.
- Formula syntax that happens to resemble Python code is only parsed into a restricted AST; neither source imports nor arbitrary function calls can run.
- A citation in an OEIS formula can point to an unrelated object; cross-reference scores are strictly review heuristics.
- An undirected connected component can contain irreversible transformations; the component size is not a measure of bidirectional computability.
- The full OEIS clone was not downloaded in this local checkpoint, and full-corpus candidate counts are therefore not reported as verified output.
- Source text is OEIS Foundation material under CC BY-SA 4.0; preserve authorship and attribution when distributing derived indices. License compatibility for larger repackaged corpora should be reviewed.
- v1.7 precision-aware branch and gluing research exists as a separate archived implementation. It is not secretly imported as production code by this script.

## Release rule

A new transfer enters the public "proved formula" graph only when it has a theorem statement, explicit parameter/index/valuation hypotheses, exact evidence receipt, source provenance, and (where applicable) a separate named-sequence identification proof. A failed parser or budget is `unresolved`, never "no transfer exists". An inconsistent recurrence shift-span linear system rules out only that restricted shift-span representation, not arbitrary sequence transfers. A symbolic equality in `Q(n)` cannot be promoted by finite term matching alone.
