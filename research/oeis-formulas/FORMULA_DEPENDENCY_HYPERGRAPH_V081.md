# OEIS formula dependency hypergraph v0.8.1

**Author: Komorebi P.** — 22 November 2026.

**Attribution:** Original formula lines from The Online Encyclopedia of Integer Sequences, OEIS Foundation Inc., CC BY-SA 4.0. Source revision `12ede576d2f5b5c96c54d315a558be3ac56ee474` (first 24,999 source records). This is an independent indexed derivative, not an OEIS publication.

## New data layer

Some formula lines refer to other OEIS sequences explicitly, so they define *textual dependency hyperedges* before they are known to be true transfer identities. A single formula can depend on multiple entries, e.g. `a(n)=A000129(n)*A002203(n)`. Unlike the earlier unary transfer miner, these relations are extracted directly from attributed source formula lines, and multi-input references are retained without breaking them into unrelated pairwise claims.

Counts from the first 24,999 official OEIS records:

| category | observed | evidence class |
|---|---:|---|
| OEIS formula lines with ≥1 referenced ID | 15,055 | textual |
| Reference-ID occurrences across those lines | 24,348 | textual |
| Lines referencing ≥2 distinct OEIS IDs | 4,955 | textual hyperedge |
| Distinct OEIS IDs referenced | 9,185 | textual |
| Formula lines accepted by the restricted arithmetic AST | 2,958 | syntax only |
| Formula lines with matching exact finite terms | 1,034 | finite checked, not proof |
| Independently compared exact finite values | 42,813 | finite checked |
| Finite checked lines that reference ≥2 distinct IDs | 301 | finite checked hyperedge |

## Extraction and verification

`tools/sequence_oeis_formula_dependencies.py` scans only stored `%F` records. It collects distinct `Axxxxxx` identifiers and a SHA-256 receipt of the original full line. A restricted integer/rational arithmetic grammar recognizes `n`, integer constants, `+`, `-`, `*`, `/`, `//`, bounded integer exponentiation, and calls to `Axxxxxx(integer_index_expression)`. Crucially, it uses an explicit AST evaluator, **never Python `eval` or source-code execution**. Unsupported symbols and functions remain textual only.

For parseable expressions, each reference term is read by **its mathematical OEIS index** using its own declared offset. We require at least 12 exact initial terms plus eight additional held-out values for a finite positive observation. Mismatched candidates are not promoted. A missing reference sequence, insufficient term window, an unsupported operator, or an out-of-range shift produces an unresolved record rather than a fabricated result.

Every output line is labeled `textual_dependency_unverified`, `parsed_but_unverified`, `parsed_but_out_of_corpus`, or `finite_checked_formula_hyperedge`. **None of these labels means a full mathematical proof.** In particular, source documentation may quote an OEIS ID without asserting the identity, and a finite match does not prove an infinite sequence identity.

## Architecture

For an expression with several dependencies, the preferred representation is a directed hyperedge

\[
(A_{i_1},\ldots,A_{i_k}) \xrightarrow{\;\text{formula expression}\;} A_j.
\]

The raw text source and source line SHA are kept. Algebraic normalization, proof promotion, and computational cost certification occur separately. This preserves information from the original source without conflating a dependency citation with an executable exact formula.

## Reproduce

```bash
python -B tools/sequence_oeis_formula_dependencies.py --db oeis-real-24999.sqlite3 --output research/oeis-formulas/oeis-formula-dependency-hyperedges.jsonl --summary research/oeis-formulas/oeis-formula-dependency-summary.json
python -B tools/render_oeis_dependency_atlas.py --db oeis-real-24999.sqlite3 --source research/oeis-formulas/oeis-formula-dependency-hyperedges.jsonl --summary research/oeis-formulas/oeis-formula-dependency-summary.json --output oeis-formula-dependency-atlas.html
PYTHONPATH=tools python -B -m unittest discover -s tools -p 'test_*.py' -q
```
