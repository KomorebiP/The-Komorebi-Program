# OEIS sequence identification proof gate

**Author: Komorebi P.**
**Checkpoint: 23 November 2026.**
**Status: locally implemented and tested; no site publication or full OEIS scan claimed.**

## The missing logical edge

The existing Komorebi OEIS source index stores textual formulas and exact identities **between formula expressions**. A proof that two expressions are equal does not by itself prove that they produce the named sequences Axxxxxx, even if the OEIS records display matching initial terms. The identification bridge is a separate theorem obligation.

The proof gate defines a deliberately strict admission pipeline:

```
oeis/oeisdata (pinned .seq text)
  -> parse %O / %S,%T,%U / %N / %F with no source execution
  -> reject missing or unsupported offset alignment
  -> parse restricted exact rational OGF, name definition, or polynomial
  -> validate reported prefix (necessary only, not sufficient)
  -> derive exact recurrence Q(x)A(x)=P(x)
  -> independently compute OGF implied by explicit %N definition
  -> compare entire rational functions in Q(x) (where supported)
  -> derive exact shift-orbit transfer via rational linear algebra
  -> replay the same claims and receipts against the exact input-file SHA
  -> conditional_transfer_overlay.json
```

The following **distinct statuses** prevent proof laundering:

- `finite_consistency_only`: Source-supplied recurrence fits reported terms. No all-index identification established.
- `source_premise_exactly_rederived`: Exact recurrence derived from a pinned source OGF, but independent OEIS name definition was not verified.
- `oeis_name_definition_equivalence_proved`: A parseable **explicit** OEIS `%N` definition and an OEIS `%F` OGF are proved mathematically equivalent. The source statements remain premises.
- `quarantined_inconsistent_source_premises` or `quarantined_name_definition_conflict`: Contradictory evidence. No edge admission.
- `unsupported_nonzero_or_missing_offset`: A missing offset, or a nonzero offset with ambiguous OGF convention. Explicit polynomials with nonzero offsets are supported and evaluated at the stated index.
- `unresolved`: No safe exact proof supported by the current grammar.

**The result is a conditional mathematical certificate. It is not an unconditional proof of all OEIS claims or of a new mathematical theorem.** The existing curated `manifests/sequence-transfer-network.json` is never mutated by this program. New edges remain separate under `conditional_transfer_overlay.json`, tagged `conditional_exact_recurrence_transfer` and `conditional_overlay_only`.

## Mathematical proof obligation

For an explicitly asserted ordinary generating function

\[
A(x)=\frac{P(x)}{Q(x)},\quad Q(0)\ne0,
\]

coefficient comparison in \(Q(x)A(x)=P(x)\) yields a constant-coefficient recurrence for every \(n>\deg P\). A recurrence of order \(d=\deg Q\) has a complete initial window at \(b=\max(d,\deg P+1)-d\), so the certificate carries **both** `base_index=b` and `recurrence_valid_from=b+d`. Eventual recurrences do not get promoted to all-index recurrences at index zero.

For two compatible, source-bound recurrences of order \(d\), the engine solves exactly over \(\mathbb{Q}\)

\[
\begin{bmatrix}S(b)&\cdots&S(b+d-1)\\\vdots&&\vdots\\S(b+d-1)&\cdots&S(b+2d-2)\end{bmatrix}c
=\begin{bmatrix}T(b)\\\vdots\\T(b+d-1)\end{bmatrix}.
\]

When consistent, equality at the \(d\) base indices plus a common recurrence proves the resulting transfer for **all \(n\ge b\)**. Compatible singular shift-orbit systems are supported; nonunique solutions are reported, not disguised as unique. The `basis_matrix`, source SHA-256s, exact rational coefficients, and proof scope are saved in the receipts.

An explicit polynomial formula \(a(n)=p(n)\), with degree at most seven, is handled using \((E-1)^{\deg p+1}p=0\). When both a polynomial `%N` definition and rational `%F` OGF are present, the engine constructs the exact rational OGF of \(p(n)\) and proves the two rational expressions equal.

## Running the program

Requires Python 3.12+ and the three local modules (stdlib only):

```
PYTHONPATH=tools python -B -m unittest test_oeis_gap_automation test_oeis_cfinite_bridge test_oeis_identification_proofs test_oeis_hypergeometric_gate test_oeis_precursive_gate -v
python -B tools/oeis_identification_proofs.py \
  --oeis-root fixtures/oeis_identification \
  --output verification/oeis-identification/demo
python -B tools/oeis_identification_proofs.py \
  --oeis-root fixtures/oeis_identification \
  --output verification/oeis-identification/demo --verify-report
```

For the genuine, pinned OEIS export:

```
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/oeis/oeisdata.git /path/to/oeisdata
git -C /path/to/oeisdata sparse-checkout set seq/A000
python -B tools/oeis_identification_proofs.py \
  --oeis-root /path/to/oeisdata \
  --ids A000032,A000045,A000217,A000290 \
  --output /path/to/proof-output
python -B tools/oeis_identification_proofs.py \
  --oeis-root /path/to/oeisdata \
  --output /path/to/proof-output --verify-report
```

`--verify-report` **re-reads the pinned `.seq` records**. Any change in their raw content hashes, the resulting profiles, a transfer coefficient, its basis matrix, an initial value, or the evidence labels causes failure.

The supplied workflow `.github/workflows/oeis-identification-proofs.yml` tests the fixtures and performs a bounded verification against a fresh source-pinned OEIS git clone, reporting its git SHA. It saves source-bound proof receipts only as CI artifacts; it does not automatically publish them as curated edges.

## Verified local results and boundaries

The 9-entry local demonstration fixture contains four positive source-name and OGF pairs, one algebraically valid eventual recurrence, two deliberately inconsistent claims, one recurrence-only example, and one offset-one example.

- 4 explicit source-name definition equivalences proved.
- 4 conditional directed transfers generated and rechecked.
- Contradictory source formulas and explicit name-definition conflicts are quarantined; ambiguous nonzero-offset OGFs are held out, while explicit polynomial indices are supported.
- 58/58 tests passed across the recovered gap engine and the first- and higher-order proof-gated stages.
- 0 unconditional OEIS identifications or mathematical novelty claims.

The two fixture lines for Fibonacci, Lucas, triangular and square source statements are illustrative, abbreviated OEIS excerpts rather than full official `.seq` files. Test files `A987...` are *invented adversarial fixtures*, **not verified OEIS entries**. The genuine four-record OEIS job is configured but has not been executed as part of this offline test.

## Next automation tiers

1. **Formal coverage expansion**: rational OGFs with ambiguous nonzero-offset conventions, index-shift maps, and additional delayed-recurrence grammars with explicit index-map certificates.
2. **P-recursive / D-finite:** polynomial-coefficient recurrences and D-finite generating functions using Ore operator reduction; record singular indices and proof domains.
3. **Hypergeometric and Pochhammer bridge families:** Ore-Sato/Zeilberger creative telescoping, exact factorial-lane and polyphase maps, singular boundary conditions.
4. **Combinatorial definitions:** executable small-case checks are insufficient; add a proof language for bijections, species and recurrence derivations.
5. **Proof backend:** optional Lean generated theorems with a verified kernel replay. Current exact Python proofs are not Lean-verified.
6. **Cost and precision compiler:** directed hypergraph routing with input reconstruction, 2-adic/odd-adic valuations, Hensel branching and measured cost models. Never infer invertibility from undirected connectivity.
7. **CI governance:** require positive/rejection controls and a checked source fingerprint before any overlay is reviewed for the public site.

## License and provenance

OEIS formula and name text originate from the Online Encyclopedia of Integer Sequences, OEIS Foundation, Inc., and are available under Creative Commons Attribution-ShareAlike 4.0. See <https://github.com/oeis/oeisdata> and <https://oeis.org/>. The public export revision must be recorded separately for each run. This package does not include or redistribute the complete OEIS corpus.

**Current companion documentation:** [Hypergeometric and P-recursive proof gate](OEIS_HYPERGEOMETRIC_AND_P_RECURSIVE_PROOF_GATE.md). When source generation used `--ids`, pass the same `--ids` on `--verify-report`; omitted IDs replay the entire source root.
