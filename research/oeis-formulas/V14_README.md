# Komorebi OEIS Sparse Transfer Compiler v1.4

**Author: Komorebi P.**  
**Research date: 22 November 2026**

This release continues the v1.3 variable-horizon compiler with *individual-index* computation DAGs and recovers rigorously specified transfer operators from the user-provided historical `Komorebi_OEIS_All_Versions_Through_v0_8.zip`. It supplements, rather than replaces, the source-backed 99,999-entry database. It does not copy that 520 MB database into this package.

## Verified outcomes

- **110/110** all-index indexed hyperedge certificates independently replayed at one sparse index each, after re-certifying all 539 source-formula hyperedges against the retained SQLite snapshot.
- **41/41** historical Riordan rational generating function identities independently proved in exact `Fraction` polynomial arithmetic, and checked against 25 consecutive terms from the current OEIS source excerpt for both source and target, plus the transformed output. This is **3,075** exact cross-version comparisons. **34** maps have formal unramified inverses, and **7** are ramified, without general inverses.
- **2** historical quadratic-channel pairs reproduced at **30** and **27** stored indices respectively (Pell/Pell-Lucas and related recurrence pairs).
- **244** Python tests passed locally, plus the independent **26 tests** in the uploaded historical v0.8 archive. Existing legacy tests emitted nonfatal SQLite connection ResourceWarnings.
- Node.js syntax and simulated offline-DOM tests passed on the searchable atlas (153 records).

All-index certificates concern the **mathematical formulas or OGFs**. Associating these with the named OEIS entries through their retained terms is a **finite check**, not an independent proof of every infinite OEIS entry's description.

## Noteworthy calculations

The formal Riordan operator

\[
\mathcal R_{c,s,r,t}[A](x)=(1-cx)^{-s}A\left(\frac{x^r}{(1-cx)^t}\right)
\]

is evaluated at requested terms without collecting irrelevant output indices. The source indices required for target degree \(n\) are contained in \(\{0,\ldots,\lfloor n/r\rfloor\}\), with zero-weight terms pruned. For \(r=t=1\), the inverse is \(\mathcal R_{-c,s,1,1}\). This is not a general inverse for \(r>1\).

A quadratic channel shares one exponentiation:

\[
(c+\sqrt q)^n=B_n+\sqrt q D_n,\qquad B_n^2-qD_n^2=(c^2-q)^n.
\]

For \((c,q)=(1,2)\) this matches OEIS A001333 and A000129 over the stored prefixes. \((c,q)=(2,3)\) gives A001075 and A001353. The mathematical identity is valid for every \(n\), independently of the finite OEIS comparisons.

The sparse hypergraph optimizer treats \((\mathrm{sequence},n)\) as a task. For a certified indexed formula \(b_n=F(a_{m_1n+r_1},\ldots)\), it requests only the individual source indices. A finite AND/OR task graph is built and solved with Dijkstra. Its minimum-cost guarantee is **only for the finite enumerated actions and user-specified additive costs**. It does not assert globally optimal wall-clock time.

For C-finite sources, the sparse packet bank shares polynomial residues \(X^{2^k}\bmod P(X)\) across many indices and across different sequences using the same recurrence polynomial. Exact residue arithmetic is used. All source formulas and index maps are checked; user-supplied code from OEIS is never executed.

## Timing receipts

- At \(n=900\), the archived quadratic pair `(c,q)=(1,2)` was approximately **864.1x** faster than computing its two exact binomial sums separately (medians of seven local runs). This is **not** a benchmark against optimized Pell software.
- For Fibonacci and Lucas at ten sparse indices from 3000 to 5002 (20 outputs), a shared packet bank was approximately **6.48x** faster than independently recomputing each recurrence jump (medians of seven local runs). All outputs agreed exactly.

The 110 real-corpus sparse transfer audit used **explicit illustrative operation scores** that favor transfers to exercise their execution and provenance, not measured timing. It therefore makes **no** speedup claim for those 110 requests.

## Reproduce

Python 3.10+ standard library for the new algorithms (the retained older tooling has its own dependencies); Node.js 18+ for the browser smoke test:

```sh
PYTHONPATH=tools python -B -m unittest discover -s tools -p 'test_*.py' -q
node tools/test_sequence_sparse_browser.cjs
PYTHONPATH=tools python -B tools/benchmark_sequence_sparse_v14.py --runs 7 --output outputs/reproduced-benchmark.json
```

Replaying the *real source* audit additionally requires the prior matching `oeis-full.sqlite3` snapshot with SHA-256:

`a121d7a6a5b6aa78a5a333fe748b604f170511bf8250ca16533f58cbcfa9e9f5`.

```sh
PYTHONPATH=tools python -B tools/audit_sequence_sparse_index.py \
  --db /path/to/oeis-full.sqlite3 \
  --ledger outputs/v12-certified-hyperedges.jsonl \
  --output outputs/replayed-sparse.json --limit 110
```

The historical archive's 41-row file is included in `research/oeis-formulas/archive-v08/`. To reprove it on the current source:

```python
from sequence_archive_v08_riordan import replay_riordan_archive,verify_quadratic_oeis_channels
report = replay_riordan_archive('research/oeis-formulas/archive-v08/v08_riordan_certificates.csv', '/path/to/oeis-full.sqlite3')
```

Documentation and all mathematical proof boundaries are in `research/oeis-formulas/SPARSE_AND_RIORDAN_V14.md`. Original source: user upload `Komorebi_OEIS_All_Versions_Through_v0_8.zip`, SHA-256 `ddffa4423a6001c82bcc3eda97d06557ca1e62358db2ab285060caf385b72244`.

## Next steps

Implement direct cost benchmarks for non-C-finite Riordan kernels and algebraic OGFs; extend the sparse-index planner beyond exponential-polynomial formula hyperedges; and continue importing the OEIS source beyond the retained 99,999-record snapshot. Preserve unverified formulas and source references alongside proved transfers without promoting them prematurely.
