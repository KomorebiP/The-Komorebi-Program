# Komorebi OEIS automation and identification proof gate

**Author: Komorebi P.**
**Published: 23 November 2026.**
**Scope:** Exact source-conditional proof automation and replay. No unconditional OEIS identification, full-corpus coverage, or automatic promotion to the public transfer graph is claimed.

The proof automation system combines source acquisition, C-finite recurrence transfers, formal generating-function and named-definition checks, hypergeometric gauges, affine-lane intertwiners, algebraic generating functions and joint recurrence transfers. Each certificate retains its source premises and admissible domain. The system does not modify the curated `manifests/sequence-transfer-network.json` or promote conditional identities into unconditional OEIS proofs.

## Contents

- `tools/oeis_gap_automation.py`: source-text ingestion and prioritization.
- `tools/oeis_cfinite_bridge.py`: exact recurrence and shifted-source bridge engine.
- `tools/oeis_identification_proofs.py`: safe OEIS `.seq` parser, exact OGF/recurrence/name-definition checks, certificate replay and conditional overlay output.
- `tools/oeis_hypergeometric_gate.py`: Pochhammer and first-order P-recursive ratio proof gates.
- `tools/oeis_precursive_gate.py`: conditional order 2–4 rational Ore-gauge implication gate.
- `tools/oeis_shift_operator_gate.py`: bounded affine-lane intertwiners, rational inverses, original-denominator guards, queue-driven planning, and pointwise local Smith precision receipts. See [Affine-lane recurrence transfers](OEIS_AFFINE_LANE_TRANSFER_GATE.md).
- `tools/oeis_algebraic_gate.py` and `tools/oeis_joint_transfer_gate.py`: formal algebraic branches, exact compositions and joint recurrence transfers. See [Algebraic and joint transfers](OEIS_ALGEBRAIC_AND_JOINT_TRANSFER_GATE.md).
- Six standard-library proof-gate test modules: 74 positive and rejection tests. The algebraic and joint-transfer suite adds 21 tests with a pinned symbolic algebra runtime.
- `fixtures/oeis_identification/`: four abbreviated genuine examples and separate intentionally synthetic adversarial `.seq` fixtures.
- `fixtures/existing_sequence_network_v15.json`: synthetic network fixture for the earlier gap-engine tests, not a substitute for the public 916-node index.
- `.github/workflows/oeis-*.yml`: optional workflows, including one to fetch real OEIS `.seq` source and retain proof receipts.
- `docs/OEIS_AUTOMATION_ROADMAP.md`, `docs/OEIS_IDENTIFICATION_PROOF_GATE.md`, `docs/OEIS_HYPERGEOMETRIC_AND_P_RECURSIVE_PROOF_GATE.md`: mathematical scope and audit protocol.
- `reports/oeis-identification-demo/`: local example reports; not an official OEIS replay.

## Verified results

The source-bound identification audit rechecked four full OEIS records and four conditional transfer directions ([CI receipt](https://github.com/KomorebiP/The-Komorebi-Program/actions/runs/45289459477/job/138094189919)). The integrated recurrence and affine-lane workflow on `main` passed 74 tests, replayed selected full official source records and reproduced 24 conditional affine-lane transfer directions, of which 18 have stride greater than one ([CI receipt](https://github.com/KomorebiP/The-Komorebi-Program/actions/runs/45325359220/job/138213522864)). The integrated algebraic and joint-transfer workflow passed 21 further tests and replayed six complete pinned records, obtaining one joint certificate, two composition certificates and three family and finite-sum normal forms ([CI receipt](https://github.com/KomorebiP/The-Komorebi-Program/actions/runs/45325359130/job/138213522547)). These are bounded audits, not whole-corpus or novelty counts. Records and transfer directions can overlap across audits; the counts must not be added to infer independent discoveries.

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

## Archival source distributions

The proof-gate sources are incorporated in the repository. No historical patch needs to be applied to a current checkout. For reproduction of the original source distribution only, `KOMOREBI_OEIS_AUTOMATION_PROOF_STAGE3_FULL.patch` (provided alongside the archival ZIP) can be applied to its documented baseline checkout:

```sh
git apply --check KOMOREBI_OEIS_AUTOMATION_PROOF_STAGE3_FULL.patch
git apply KOMOREBI_OEIS_AUTOMATION_PROOF_STAGE3_FULL.patch
PYTHONPATH=tools python -B -m unittest test_oeis_gap_automation test_oeis_cfinite_bridge test_oeis_identification_proofs test_oeis_hypergeometric_gate test_oeis_precursive_gate test_oeis_shift_operator_gate -v
```

Use the documented historical baseline and check for collisions before applying an archived patch. The current integrated source is the normal entry point for verification.

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

<a id="stage-4-extension"></a>

## Affine-lane and algebraic transfer methods

Read the [affine-lane gate](OEIS_AFFINE_LANE_TRANSFER_GATE.md) for exact recurrence intertwiners, nonsingular domains and local precision. The [algebraic and joint-transfer gate](OEIS_ALGEBRAIC_AND_JOINT_TRANSFER_GATE.md) develops formal branch elimination and multiple-input recurrence certificates. Both retain source premises and exact replay receipts. Historical delta patches belong to their recorded baselines. Full-corpus acquisition remains opt-in, and no automatic network publication is enabled.
