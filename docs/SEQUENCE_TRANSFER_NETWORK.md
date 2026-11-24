# Sequence Library transfer-network integration

**Author: Komorebi P.**  
**Public entry:** `sequence-library.html` → `sequence-network.html` (also linked from the existing Transfer page).

## Purpose and navigation

The Sequence Library remains the single search entry point for local KSEQ, KFOR, and KOM records, mathematical formulas, OEIS terms, comparisons, and exact calculators. The **Network** tab provides a source-bound read-only collection of transfer relations, without replacing the existing finite-convolution **Transfer** workbench.

Search results have a “Formula network” link. Local IDs hand off to at most eight finite OEIS comparison matches, **explicitly identified as finite matching leads**. An OEIS ID, such as `A000108`, opens the incident directed identities, hypergeometric gauges, Riordan transforms, and quadratic channels. Exact OEIS ID searches include only records where the identifier is a target or input. The sequence profile reports the distinct direct total and role counts under the selected relation class. A sequence name containing another identifier does not establish graph incidence; use `text:A000108` to include broader textual references. Search by name and simple formula text is supported. Both sequence-name matches and matching archived formula expressions are included when the same query matches each category; neither result class suppresses the other.

The browser loads the compact data only on `sequence-network.html`, not when visitors first open the Sequence Library search. It neither runs the offline Python optimizer nor executes external OEIS code. The Sequence Library also provides calculators, comparison, exact local formula text, and official OEIS reference lookup.

## Reading a transfer result

The target OEIS identifier appears **to the left of the arrow**. Select any participant ID in the result heading to explore its own direct transfer connections without leaving the Network. Official OEIS links remain available in each record's source disclosure. Identifiers to the right are the archived source formulas or sequence inputs. The network presents mathematical **formula relationships**, not independently checked identifications of every named OEIS sequence.

Gauge records now show their ratio equation separately from the scale \(K\), base \(c\), starting index \(t_0\), and defining factor \(L\). The archived gauge strings sometimes use \(t\) for the input of \(L\) while writing \(n\) inside its product. For display only, the reader uses the neutral variable \(u\) in the definition \(L(u)\). This is a change of **dummy variable**, not a change to the stored formula. The complete original text, offsets, proof reference, and source receipt remain available under each record's disclosure.

Formula and quadratic-channel records use mathematical typesetting where the archive grammar is supported. Riordan records display their stored parameters without inventing a full OGF equation that the index does not contain. Unsupported notation remains readable as original text. Nothing on this page executes source expressions.

On narrow or zoomed screens, the search controls stack vertically. Results appear in batches of 12 so readers do not have to navigate a single very long list. Every matching record in the pinned index remains accessible, even when a search matches more than 60 relations. The **Show next connections** button moves keyboard focus to the first newly revealed record and keeps the result count explicit. The separately loaded source-formula list appends groups of 25 without remounting earlier lines, and its **Show more formulas** control likewise focuses the first newly revealed line. The site-wide **Math display** preference switches between typeset notation and plain source text. Wide equations have their own horizontal scroll area. Keyboard access and source-text fallbacks are retained.

## Retained mathematical material

The network presents a compact, pinned projection of the **Komorebi OEIS Sparse Transfer Compiler**:

| Relationship | Records | Mathematical status |
| --- | ---: | --- |
| Hyperedges | 539 | All-index equality between supplied extracted formula expressions |
| Hypergeometric gauges | 975 | All-index formula equality on a specified nonsingular tail |
| Riordan | 41 | Exact rational generating-function identity, conditional on both recorded OGF premises |
| Quadratic-channel directions | 4 | Exact algebra of two quadratic channels, two directed views each |

**Total: 1,559 archived transfer views touching 916 OEIS IDs.** The two directions for each quadratic channel do not count as four independent theorems.

The archived formulas and identities originated in the retained 99,999-entry OEIS source snapshot. The pinned SQLite SHA-256 is `a121d7a6a5b6aa78a5a333fe748b604f170511bf8250ca16533f58cbcfa9e9f5`. Manifest `sources` hashes bind the three archived ledgers. Source OEIS names and formula text are attributed to **The Online Encyclopedia of Integer Sequences, OEIS Foundation Inc.**, under **CC BY-SA 4.0**. This page provides an independent Komorebi search presentation.

The site build checks the structural integrity of the projected transfer index and local-to-OEIS comparisons, but it does **not** rerun all 539 source-formula proof checks or revalidate the entire 99,999-entry database. The archived proof receipt and proof scope stay visible. Neither finite OEIS matches nor formula-level proofs automatically establish an all-index OEIS sequence identification. Those distinctions are essential for the index and its interface labels.

## Files and reproducibility

The site generation entry point is `tools/sequence_library.py`. It calls `tools/sequence_network_site.py`, which validates `manifests/sequence-transfer-network.json`, copies `website/assets/sequence-network-ui.mjs` and `.css` to output, writes an OEIS finite-comparison handoff index, and builds the Network page. The retained `manifests/sequence-transfer-network.json` is committed as a versioned, text-based source index, not generated from a moving web endpoint during the site build.

To regenerate the index, use the pinned SQLite snapshot and the corresponding archived compiler ledgers:

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

## Further work: precision-aware transfers

The [directional ghost and Frobenius quotient research note](DIRECTIONAL_GHOSTS.md) develops exact prime-power ambiguity formulas, a multivariate optimality theorem, query-relative Smith image calculations, and a lossless contracting quotient. Its [source and finite regression entry](../research/directional-ghosts/README.md) is separate from the curated OEIS formula index. It does not add unverified OEIS identities or change the source-validation status of any indexed edge.

The [public reading page](https://KomorebiP.github.io/The-Komorebi-Program/collection/DIRECTIONAL_GHOSTS.html) is linked from the Sequence Network. The current network remains read-only; precision-aware route optimization has not been deployed as a browser service.

## Lazy-loaded OEIS source formulas

A separately versioned source-text index contains **8,853 original OEIS `%F` lines**
for **845 of the 916** OEIS IDs in the curated transfer graph. The other 71
IDs have no `%F` field in the retained first-99,999-entry snapshot. The snapshot
file SHA-256 is the same `a121d7a6…` value used to pin the graph evidence.
The source text is **unreviewed**, not a mathematical proof or an executable
formula. Source-program blocks are excluded. Every source entry links to OEIS
and retains OEIS Foundation attribution under CC BY-SA 4.0.

The browser fetches `assets/sequence-network-formulas.json` only when the
reader requests source formulas for one exact OEIS A-number. It uses
`textContent` for all formula text and displays at most 25 records at a time,
with a further-results control. The generator
`tools/export_sequence_network_formulas.py` checks the pinned SQLite database
hash before producing the retained file. The source-text index does not add any all-index OEIS identity claims.

## Archived formula presentation

The Network provides exact participant navigation and transfer-specific
formatting. Archived source fields support a bounded display-only arithmetic
grammar and filtering by recorded formula class. Unsupported or
ambiguous syntax is left unchanged, and every original source field remains
available with a copy action. The source parser does not execute OEIS text,
derive a new identity, change the pinned snapshot, or promote any evidence
status. Pagination continues to append existing rows without recreating them;
switching the formula class intentionally resets the displayed subset.
