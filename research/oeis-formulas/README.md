# Komorebi OEIS formula database — initial implementation

**Author: Komorebi P.**  
**Data attribution:** The Online Encyclopedia of Integer Sequences, OEIS Foundation Inc., <https://oeis.org/>. OEIS-derived data and adaptations are made available under **CC BY-SA 4.0**. Source repository: <https://github.com/oeis/oeisdata>. Independent Komorebi code is distributed according to the host repository's code license.

This is an incremental, **standard-library-only Python/SQLite formula catalog**, designed to scale from a small independently testable seed set to the full public OEIS `.seq` export. It supplements rather than replaces the existing Komorebi Sequence Library.

## What is in this release

- 32 OEIS sequences with one safe exact evaluator each. All 32 were checked against their first 18 stored reference terms from the official OEIS repository (not a proof of infinite identity).
- A parser for OEIS's official `seq/A123/A123456.seq` format. It imports IDs, correct mathematical offsets, finite reference terms, names, the `%F` formula lines, and `%p`, `%t`, `%o` source-program sections.
- A strict distinction between **source-reported formula text** and **executable, finitely checked formula specifications**. No OEIS formula or program text is executed.
- A separate loader for Komorebi `sequence-library-data.json` exports. Preserves KSEQ, KFOR, and KOM source identities and labels finite OEIS matches as candidates, not proofs.
- An idempotent SQLite database, verification states, source attribution, SHA-256 source fingerprints, query interface, JSONL export, offline HTML browser, and regression tests.

## Quick start

Run from repository root (Python 3.10+):

```bash
python tools/oeis_formula_database.py --db oeis-formulas.sqlite3 ingest-seeds --path research/oeis-formulas/seeds.json
python tools/oeis_formula_database.py --db oeis-formulas.sqlite3 stats
python tools/oeis_formula_database.py --db oeis-formulas.sqlite3 show A000108
python tools/oeis_formula_database.py --db oeis-formulas.sqlite3 search Catalan --verified-only
python tools/oeis_formula_database.py --db oeis-formulas.sqlite3 export-jsonl --path verified.jsonl
python tools/export_formula_browser.py --db oeis-formulas.sqlite3 --output formula-browser.html
python -m unittest discover -s tools -p 'test_oeis_formula_database.py' -v
```

### Ingest the entire official OEIS formula corpus

Use the [official GitHub export](https://github.com/oeis/oeisdata), **not** `stripped.gz`/`names.gz` for full formulas; those smaller exports contain only names/term excerpts. A local clone of the `.seq` files is required for a bulk ingest. No separate LFS b-file download is necessary to import main formula fields.

```bash
# From a computer or environment with network access:
git clone --depth 1 https://github.com/oeis/oeisdata.git external/oeisdata
python tools/oeis_formula_database.py --db oeis-formulas.sqlite3 ingest-oeis --path external/oeisdata/seq
python tools/oeis_formula_database.py --db oeis-formulas.sqlite3 stats
```

The full import scans `*.seq` files incrementally, commits every 1,000 entries, and records parsing errors as samples. The database is not bounded to the initial 32 records. Repeating an unchanged `.seq` import skips it; changing an entry replaces that entry's raw formulas without overwriting curated evaluators.

If the Komorebi website has been built and `sequence-library-data.json` is available:

```bash
python tools/oeis_formula_database.py --db oeis-formulas.sqlite3 ingest-komorebi --path path/to/sequence-library-data.json
```

The generated SQLite file is local and intentionally not tracked by Git. You can distribute a generated SQLite/JSON export separately with its OEIS attribution and CC BY-SA 4.0 notice.

## Schema and verification semantics

- `sequences`: official OEIS identity, first and second mathematical offsets, exact string terms, metadata and SHA-256 of the ingested source.
- `formulas`: separate records for OEIS `%F` formulas, OEIS program sections, Komorebi source representations, and curated safe evaluators. `source_url`, license, proof status, finite verification, and complexity text are retained.
- `komorebi_records`: local archive IDs remain local IDs, not newly assigned OEIS numbers.
- `crosswalks`: `finite_match` means only equality over the reported finite excerpt. `source_claim` means an existing attribution, not independent proof.

**`finite_checked` means agreement over a finite, explicitly reported prefix only.** It must never be interpreted as proof of a formula's validity for all indices, discovery priority, or mathematical novelty. The seed's `classical_reference` flag describes its provenance as a familiar classical formula, not a formal proof certificate. Raw OEIS `%F` lines have `unreviewed` status, and source program sections have `not_executed` status.

The safe evaluator takes declarative JSON expression trees, including exact arithmetic, factorials, binomial coefficients, bounded sums, linear recurrences, Bell/Fubini/Motzkin/partition recurrences, and basic arithmetic functions. It never passes OEIS data to Python `eval` or `exec`. There are argument bounds, but this is a research tool, not a hardened public execution service.

## Development roadmap

Next steps are to normalize more `%F` conventions into candidate structured ASTs **without assuming their correctness**, add independent proof receipts for the highest-value formulas, index cross-sequence transforms, and publish a read-only website browser backed by exported subsets or sharded JSON. Efficient formula ranking should benchmark real exact evaluators and preserve the distinction between term formulas, generating functions, recurrences, and approximation schemes.


## Expanded stage: 22 November 2026

The extension adds `seeds-extended.json` with **24 additional source-linked OEIS sequences** and **29 exact expression variants**. Across both seed files there are now **56 distinct OEIS IDs**, **61 finitely checked evaluator variants**, and **1,098 exact reference-term comparisons** (18 values per evaluator). There are no automatic claims of proof or historical novelty.

The `oeis_formula_discovery.py` module conservatively recognizes a subset of `a(n)=...` arithmetic expressions in `%N` and `%F` fields. Only integer arithmetic, the index variable `n`, integer powers, exact division, binomial coefficients, and factorials are translated into safe declarative expressions. Unsupported/ambiguous source text is left untouched. A candidate needs at least 12 matching reference values to receive `finite_checked`; its proof status remains **unassessed**. Negative mathematical offsets are preserved in the database, but automatic normalization skips them until index support is extended.

The `oeis_formula_polyphase.py` module constructs exactly indexed multisections `P_(m,r)[a](n)=a(o + m*n + r)` for integer `m>=1`, `0<=r<m`, and OEIS offset `o`. Subsequence lifts are conditional substitutions of the base evaluator, not new or distinct OEIS sequence registrations. Each sample is compared with the stored reference terms, and the source proof status is retained.

On changed OEIS `.seq` source content, the importer now invalidates stale finite-verification statuses, deletes obsolete normalized candidates, and rechecks existing curated evaluators against the updated source terms and mathematical offset.

### Incremental usage

```bash
python tools/oeis_formula_database.py --db oeis-formulas.sqlite3 ingest-seeds --path research/oeis-formulas/seeds.json
python tools/oeis_formula_database.py --db oeis-formulas.sqlite3 ingest-seeds --path research/oeis-formulas/seeds-extended.json
python tools/oeis_formula_discovery.py --db oeis-formulas.sqlite3
python tools/oeis_formula_polyphase.py --db oeis-formulas.sqlite3 calculate --id A000040 --m 2 --r 0 --n 3
python tools/oeis_formula_polyphase.py --db oeis-formulas.sqlite3 export --output polyphase.jsonl
python tools/export_formula_browser.py --db oeis-formulas.sqlite3 --output formula-browser.html
python -m unittest discover -s tools -p 'test_oeis_formula_*.py' -v
```

Ingesting the retained OEIS `stripped.gz` / `names.gz` alone does not provide the complete `%F` formula fields. Those require the full official `.seq` export. The Komorebi 2,333-record research library remains a separate source and must be imported explicitly through `ingest-komorebi`; no claim is made that its records are included in the new 56-sequence seed database.
