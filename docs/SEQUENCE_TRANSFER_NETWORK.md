# Sequence Library transfer-network integration

**Author: Komorebi P.**  
**Public entry:** `sequence-library.html` → `sequence-network.html` (also linked from the existing Transfer page).

## Purpose and navigation

The Sequence Library remains the single search entry point for local KSEQ, KFOR, and KOM records, mathematical formulas, OEIS terms, comparisons, and exact calculators. The **Network** tab provides a source-bound read-only collection of transfer relations, without replacing the existing finite-convolution **Transfer** workbench.

Search results have a “Formula network” link. Local IDs hand off to at most eight finite OEIS comparison matches, **explicitly identified as finite matching leads**. An OEIS ID, such as `A000108`, opens the incident directed identities, hypergeometric gauges, Riordan transforms, and quadratic channels. Search by name and simple formula text is supported.

The browser loads the compact data only on `sequence-network.html`, not when visitors first open the Sequence Library search. It neither runs the v1.4 Python optimizer nor executes external OEIS code. The existing site still provides calculators, comparison, exact local formula text, and official OEIS reference lookup.

## Retained mathematical material

A compact, pinned projection of the **Komorebi OEIS Sparse Transfer Compiler v1.4** contributes:

| Relationship | Records | Mathematical status |
| --- | ---: | --- |
| Hyperedges | 539 | All-index equality between supplied extracted formula expressions |
| Hypergeometric gauges | 975 | All-index formula equality on a specified nonsingular tail |
| Riordan | 41 | Exact rational generating-function identity, conditional on both recorded OGF premises |
| Quadratic-channel directions | 4 | Exact algebra of two quadratic channels, two directed views each |

**Total: 1,559 archived transfer views touching 916 OEIS IDs.** The two directions for each quadratic channel do not count as four independent theorems.

The archived formulas and identities originated in the retained 99,999-entry OEIS source snapshot. The pinned SQLite SHA-256 is `a121d7a6a5b6aa78a5a333fe748b604f170511bf8250ca16533f58cbcfa9e9f5`. Manifest `sources` hashes bind the three archived ledgers. Source OEIS names and formula text are attributed to **The Online Encyclopedia of Integer Sequences, OEIS Foundation Inc.**, under **CC BY-SA 4.0**. This page provides an independent Komorebi search presentation.

The site build checks the structural integrity of the projected transfer index and local-to-OEIS comparisons, but it does **not** rerun 539 full source-formula proofs or revalidate the entire 99,999-entry database. The archived proof receipt and proof scope stay visible. Neither finite OEIS matches nor formula-level proofs automatically establish an all-index OEIS sequence identification. Those distinctions are essential for the index and its interface labels.

## Files and reproducibility

The site generation entry point is `tools/sequence_library.py`. It calls `tools/sequence_network_site.py`, which validates `manifests/sequence-transfer-network.json`, copies `website/assets/sequence-network-ui.mjs` and `.css` to output, writes an OEIS finite-comparison handoff index, and builds the Network page. The retained `manifests/sequence-transfer-network.json` is committed as a versioned, text-based source index, not generated from a moving web endpoint during the site build.

To regenerate after a reviewed update (requires the pinned SQLite snapshot and v1.4 ledger files):

```sh
python tools/create_site_transfer_snapshot.py \
  --db /path/to/pinned/oeis-full.sqlite3 \
  --hyperedges /path/to/v12-certified-hyperedges.jsonl \
  --gauges /path/to/structured-gauges.jsonl \
  --riordan /path/to/archive-v08-cross-version-replay-v14.json \
  --output manifests/sequence-transfer-network.json
```

Independent tests:

```sh
PYTHONPATH=tools python -m unittest discover -s tools -p test_sequence_network_site.py -v
node --test tools/test_sequence_network_site.mjs
```

The normal `sequence-library-checks.yml` workflow also builds the Sequence Library and checks browser functionality. Public pages are static. A full formula-execution/optimization service would require separate infrastructure and fresh authenticated source-bound certificates, not a claim that these indexed expressions can safely be evaluated in a GitHub Pages client.
