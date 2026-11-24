# OEIS Formula Hyperedge Compiler, v0.9

**Author: Komorebi P.**  
**Date:** 22 November 2026  
**Source:** Official OEIS `oeisdata` repository snapshot `12ede576d2f5b5c96c54d315a558be3ac56ee474`. OEIS Foundation Inc. data are used with attribution under CC BY-SA 4.0.

## Objective and evidence hierarchy

The primary objective is to assemble usable mathematical sequence formula representations, then compile **exact transfer hyperedges** among many sequences. Data collection, parsing, finite checks, formal-expression identities, global identification with the OEIS entry, and actual speedup are distinct evidentiary levels.

The first 100 `seq/Axxx` shards provided **99,999 real OEIS records** (not the full OEIS). The GitHub build artifact was downloaded and its source metadata and ZIP integrity checked. The archived SQLite passed the GitHub Action's integrity check.

| Item | Count | Status |
|---|---:|---|
| OEIS records | 99,999 | Official source snapshot |
| Original formula lines | 154,844 | Retained source text, not executed |
| Program blocks | 133,958 | Retained text, not executed |
| Finite-checked normalized formula records | 4,180 | Exact numerical prefix checks |
| Canonical exponential-polynomial formula sequences | 3,121 | Exact structural symbolic definitions |
| Formula identities from unary operators | 6,719 | All-index conditional formula identities |
| Exact rational basis dimension | 146 | All-index Q-linear identities for 3,121 formula functions |
| OEIS formula lines mentioning at least one other OEIS ID | 45,826 | Textual dependency candidates |
| Those lines with multiple distinct referenced IDs | 16,234 | Textual hyperedges |
| Restricted arithmetic formulas accepted | 10,359 | Parsed, not necessarily true |
| Finite-checked candidate formula dependencies | 4,840 | 233,726 exact finite checks |
| **Promoted exact formula hyperedges** | **539** | Exact all-index formula identities, source record SHA-receipted |
| Of which use multiple OEIS input entries | **152** | Exact formula hyperedges |
| Hyperedge certificate replays | **539 / 539** | Hash and symbolic replay successful |
| Independently proved global OEIS identifications | **0 claimed** | Not performed |

The 539 hyperedges are **not** disjoint from the 6,719 unary formula identities in any mathematically meaningful novelty accounting. They are a different search mechanism and can overlap. No pairwise novelty or runtime optimality claims follow.

## Exact algebra and proof scope

Suppose extracted source sequence formulas have finite exponential-polynomial representations over Q:

\[
a_n=\sum_i P_i(n)\lambda_i^n,\qquad
b_n=\sum_j Q_j(n)\mu_j^n,\qquad \lambda_i,\mu_j\in\mathbb Z\setminus\{0\}.
\]

They are closed under exact pointwise products:

\[
(a\odot b)_n = \sum_{i,j}P_i(n)Q_j(n)(\lambda_i\mu_j)^n.
\]

They are also closed under affine polyphase extraction for nonnegative integer residue, using the actual mathematical offsets:

\[
a_{mn+r}=\sum_i\lambda_i^r P_i(mn+r)(\lambda_i^m)^n,
\quad m\in\mathbb Z_{\ge1},\ r\in\mathbb Z_{\ge0}.
\]

Together with exact Q-linear combinations, integer polynomial terms, constant rational division, and bounded integer powers, these give an all-index formula algebra for a restricted grammar. Formulas are parsed using Python's AST as *data*, with an allowlist of mathematical operations; they are never executed as Python code. Missing references, nonlinear index maps, floor division without an integrality proof, unsupported functions, negative-domain references, and nonconstant denominators are rejected for all-index promotion.

Every candidate `a(n) = expression` is transformed into a canonical rate-polynomial normal form. Two expressions are considered algebraically equal only when every rational coefficient is identical for every exponential rate. **Matching a finite window does not produce an algebraic certificate.** Each certificate records the original OEIS formula line hash, normalized source-record hashes, mathematical offsets, source and target formulas, and independent post-derivation exact value controls.

Proofs prove that the supplied *formula expressions* agree at every local index. OEIS entries may include many alternative definitions, and the normalized expression has only been compared against a finite prefix from that entry. Independent all-index OEIS identification remains an outstanding obligation.

## Worked example

A062074 has an OEIS formula line linking its terms with A000578 and A000244:

\[
\mathrm{A062074}(n)=\mathrm{A000578}(n)\mathrm{A000244}(n)=n^3 3^n.
\]

This is structurally certified because both input expressions have accepted exact symbolic forms and the target expression has identical canonical polynomial coefficients at rate 3. The sampled OEIS terms agree but are not substituted for this formula-level proof.

## Reproduction

With `oeis-real-99999.sqlite3` from the corresponding 99,999-record GitHub source artifact and the Python sources in this release:

```bash
python -B tools/sequence_oeis_formula_dependencies.py --db oeis-real-99999.sqlite3 --output research/oeis-formulas/oeis-formula-dependency-hyperedges.jsonl --summary research/oeis-formulas/oeis-formula-dependency-summary.json
python -B tools/sequence_oeis_hyperedge_proofs.py --db oeis-real-99999.sqlite3 --source research/oeis-formulas/oeis-formula-dependency-hyperedges.jsonl --output research/oeis-formulas/verified-formula-hyperedges.jsonl --summary research/oeis-formulas/verified-formula-hyperedges-summary.json
python -B tools/sequence_oeis_hyperedge_proofs.py --db oeis-real-99999.sqlite3 --source research/oeis-formulas/oeis-formula-dependency-hyperedges.jsonl --output research/oeis-formulas/verified-formula-hyperedges.jsonl --replay-only
python -B tools/render_oeis_dependency_atlas.py --db oeis-real-99999.sqlite3 --source research/oeis-formulas/oeis-formula-dependency-hyperedges.jsonl --summary research/oeis-formulas/oeis-formula-dependency-summary.json --proofs research/oeis-formulas/verified-formula-hyperedges.jsonl --output oeis-formula-dependency-atlas.html
PYTHONPATH=tools python -B -m unittest discover -s tools -p 'test_*.py' -q
```

The optional source-free atlas browser uses embedded JSON, has no CDN dependencies, and prints user-provided titles through `textContent` rather than HTML injection.

## Immediate next research program

1. Obtain remaining OEIS source shards and normalize more than the currently parseable subset. Many useful formula fields are non-C-finite, including Pochhammer, exact finite sums, algebraic generating functions, partitions, and Euler zigzag numbers.
2. Promote rational ratio, P-recursive, algebraic and D-finite expressions to formally checkable transfer operators, with domain and singularity conditions explicit.
3. Compose *proven formula hyperedges* into a directed operator graph, maintaining source SHA receipts and detecting cycles. Current finite candidate edges must not be promoted without proofs.
4. Establish exact arithmetic cost models and benchmark discovered routes. Proving a representation is mathematically exact does not guarantee computational benefit.
