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
