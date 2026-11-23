# Komorebi OEIS automation and identification proof gate

**Author: Komorebi P.**
**Checkpoint: 23 November 2026.**
**Status: Offline implementation and proof-replay controls. No unconditional OEIS identification or deployment claimed.**

This additive package combines the previously retained OEIS gap-discovery and
C-finite transfer tooling with a new **source-bound OEIS identification proof
gate**. It does not modify the curated `manifests/sequence-transfer-network.json`
and does not promote conditional identities into unconditional OEIS proofs.

## Contents

- `tools/oeis_gap_automation.py`: source-text ingestion and prioritization.
- `tools/oeis_cfinite_bridge.py`: exact recurrence and shifted-source bridge engine.
- `tools/oeis_identification_proofs.py`: safe OEIS `.seq` parser, exact OGF/recurrence/name-definition checks, certificate replay and conditional overlay output.
- `tools/oeis_hypergeometric_gate.py`: Pochhammer and first-order P-recursive ratio proof gates.
- `tools/oeis_precursive_gate.py`: conditional order 2–4 rational Ore-gauge implication gate.
- `tools/oeis_shift_operator_gate.py`: bounded affine-lane intertwiners, rational inverses, original-denominator guards, queue-driven planning, and pointwise local Smith precision receipts. See [Stage 4](OEIS_AFFINE_LANE_TRANSFER_GATE.md).
- The six named proof-gate test modules listed below: 74 positive and rejection unit tests at the Stage 4 checkpoint.
- `fixtures/oeis_identification/`: four abbreviated genuine examples and separate intentionally synthetic adversarial `.seq` fixtures.
- `fixtures/existing_sequence_network_v15.json`: synthetic network fixture for the earlier gap-engine tests, not a substitute for the public 916-node index.
- `.github/workflows/oeis-*.yml`: optional workflows, including one to fetch real OEIS `.seq` source and retain proof receipts.
- `docs/OEIS_AUTOMATION_ROADMAP.md`, `docs/OEIS_IDENTIFICATION_PROOF_GATE.md`, `docs/OEIS_HYPERGEOMETRIC_AND_P_RECURSIVE_PROOF_GATE.md`: mathematical scope and audit protocol.
- `reports/oeis-identification-demo/`: local example reports; not an official OEIS replay.

## Offline verification

From the project root:

```sh
PYTHONPATH=tools python -B -m unittest test_oeis_gap_automation test_oeis_cfinite_bridge test_oeis_identification_proofs test_oeis_hypergeometric_gate test_oeis_precursive_gate test_oeis_shift_operator_gate -v
python -B tools/oeis_identification_proofs.py \
  --oeis-root fixtures/oeis_identification \
  --output reports/oeis-identification-demo
python -B tools/oeis_identification_proofs.py \
  --oeis-root fixtures/oeis_identification \
  --output reports/oeis-identification-demo --verify-report
```

The additional exact backends have synthetic controls and faithful official excerpts in
`fixtures/oeis_hypergeom/` and `fixtures/oeis_precursive/`. See
`docs/OEIS_HYPERGEOMETRIC_AND_P_RECURSIVE_PROOF_GATE.md` for full scope, domain
obligations, proof mathematics, and source-provenance boundaries.

## Verify on official OEIS source

Clone `https://github.com/oeis/oeisdata` into a separate directory, then run the
commands in `docs/OEIS_IDENTIFICATION_PROOF_GATE.md`. The GitHub workflow performs this bounded source check on relevant pull requests, main-branch pushes, or manual dispatch. Scheduled source clones remain disabled until their resource costs have been reviewed.
Record both the source git commit and the SHA-256 of each `.seq` file.

The output separates source assertions, finite consistency, exact formal
power-series implications, explicit definition equivalences, and incompatible
premises. **A textual OEIS match, a prefix recurrence fit, or a proved formula
relationship is not by itself a proof of OEIS sequence identification.**

## Integration

`KOMOREBI_OEIS_AUTOMATION_PROOF_STAGE3_FULL.patch` (provided alongside the ZIP) contains
all source additions. Apply from the root of `KomorebiP/The-Komorebi-Program`:

```sh
git apply --check KOMOREBI_OEIS_AUTOMATION_PROOF_STAGE3_FULL.patch
git apply KOMOREBI_OEIS_AUTOMATION_PROOF_STAGE3_FULL.patch
PYTHONPATH=tools python -B -m unittest test_oeis_gap_automation test_oeis_cfinite_bridge test_oeis_identification_proofs test_oeis_hypergeometric_gate test_oeis_precursive_gate test_oeis_shift_operator_gate -v
```

Check for collisions with later repository changes before applying. The patch
adds files only, and never silently overwrites a production transfer index.

OEIS material is attributed to the OEIS Foundation, Inc. under CC BY-SA 4.0.
The package contains no complete OEIS corpus and claims no independent novelty
or Lean-formalized OEIS identification.

## Expanded source-bound local checks

```sh
python -B tools/oeis_hypergeometric_gate.py --oeis-root fixtures/oeis_hypergeom --output verification/oeis/hypergeom
python -B tools/oeis_hypergeometric_gate.py --oeis-root fixtures/oeis_hypergeom --output verification/oeis/hypergeom --verify-report
python -B tools/oeis_precursive_gate.py --oeis-root fixtures/oeis_precursive --output verification/oeis/precursive
python -B tools/oeis_precursive_gate.py --oeis-root fixtures/oeis_precursive --output verification/oeis/precursive --verify-report
```

Source selection must be passed independently on verification. If generation
uses `--ids`, repeat the same `--ids` during `--verify-report`. No automatic
merger into the published sequence network is performed.

## Stage 4 extension

The Stage 4 delta patch applies to its recorded Stage 3 baseline; the consolidated source patch is for a repository without the proof-gate files. On this review branch the workflow and README were reconciled with the newer Stage 3 CI restrictions. See [the affine-lane gate](OEIS_AFFINE_LANE_TRANSFER_GATE.md) for all-index conditional obligations, exact local receipts and bounded source replay. No new scheduled jobs or automatic network publication are enabled.
