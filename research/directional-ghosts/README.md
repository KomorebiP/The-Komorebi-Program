# Directional ghosts and Frobenius transfer generalizations

**Author: Komorebi P.**  
**Checkpoint:** 2026-11-23  
**Status:** Written mathematical proofs and finite computational checks. No Lean formalization or historical novelty audit.

This article develops multivariate precision-fiber formulas for weighted Euler derivatives, a sharp first-order operator bound, Smith-lattice density estimates, query-specific Smith image calculations on affine fibers of nonlinear observations, and a lossless Frobenius/polyphase quotient.

## Source lineage

The preserved research inputs are `Komorebi_Ambient_Realization_All_Progress_2026-11-23.zip` and `Komorebi_Precision_Aware_Transfer_Bridge_v1_2_2026-11-23.zip`. These identifiers record the archival lineage; the public article is organized by mathematical subject rather than development version.

## Read

- [Full research note, proofs, assumptions, and limitations](../../docs/DIRECTIONAL_GHOSTS.md).
- [Public reading page](https://KomorebiP.github.io/The-Komorebi-Program/collection/DIRECTIONAL_GHOSTS.html).
- [Sequence transfer network context](../../docs/SEQUENCE_TRANSFER_NETWORK.md).
- [Exact regression subset](test_directional_ghosts.py).

The full 2026-11-23 development archive, maintained separately as `Komorebi_New_Generalizations_Directional_Ghosts_Frobenius_2026-11-23.zip`, contains additional exhaustive and randomized programs and machine-readable receipts. **This repository entry includes a smaller independent regression suite, not that entire archival ZIP.** Numerical statements are conditional on the precise finite-ring and observation assumptions in the note.

## Reproduce the public subset

Use Python 3.10 or later, standard library only:

```sh
python -m unittest -v research/directional-ghosts/test_directional_ghosts.py
```

The checks exercise the bivariate example (58/27/46 ambiguity digits), full-rank coordinate optimality at several primes and degrees, integral Frobenius quotient inversion, logarithmic-derivative intertwining, and the partition polyphase identity. These are finite tests, not replacements for mathematical proof.

## Claim boundary

- **Written proof:** algebraic statements in the note, with the stated hypotheses.
- **Computational evidence:** finite instances, not independent proof certification.
- **OEIS:** formal generating-function identities do not establish unverified OEIS sequence identifications.
- **Novelty:** *new in this continuation* does not imply historical priority.
- **Deployment:** the reader build renders the Markdown note and links it from the Sequence Network. There is no browser Python verifier or online optimization service.

Next steps: generalize query fibers beyond affine modules, attach independently available observation channels to costed routes, and benchmark rediscovery of withheld identities.
