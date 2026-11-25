# Minimum supplementary reconstruction and reduced integral transfer lifts

Author: Komorebi P.

## Scope

This continuation certifies the arithmetic of the retained rank-272 transfer matrix and its integral row lattice. Its generating-function interpretation inherits the preceding written proofs. No new OEIS bindings, Lean proofs or optimal-runtime claims.

## 1. Minimum augmentation of the old basis

Let L be the integral span of the 537 series and L0 the lattice spanned by the specified original 272 rational-basis records. The finite group L/L0 has eight nonunit invariant factors. Its reductions at 2 and 3 each require eight generators. Every added original record contributes at most one generator; hence at least eight additional records are necessary when retaining the prescribed basis.

The following eight attain this lower bound: R08, ND62, R07, T36, T38, U07, B17, T37.

Only 55 active coordinates need computation; 217 other coordinates split off as identities. Let W denote the coefficient matrix of the old active basis relative to the integral basis. Let E denote the 63 x 55 coefficient matrix of the augmented active source set. The exact modular rank checks are:

- p=2: rank 47 before, rank 55 after.
- p=3: rank 47 before, rank 55 after.
- p=5: rank 50 before, rank 55 after.
- p=7: rank 54 before, rank 55 after.
- p=11: rank 54 before, rank 55 after.
- p=13: rank 54 before, rank 55 after.

The enlarged lattice contains L0, so its index in L divides [L:L0]. Any prime dividing a nonunit index belongs to the six checked primes. Full rank modulo each excludes such an index. Independently, HNF on the 63 selected rows regenerates the prior HNF and an integer left inverse V with V E=I_55. Thus 280 original records suffice and this augmentation is minimum subject to retaining the old 272.

A separate bounded determinant-decreasing catalogue-only basis search (one deterministic and twelve seeded trials) reduced the starting index 3841431346192362519895474176000000 to 10137600 but did not reach index one. This is not an impossibility certificate for a different 272-element subset.

## 2. Complete integer relation kernel

Let P=I_63-E V. Since V E=I_55, P E=0. Every row vector k with k E=0 satisfies k P=k. The rows of P therefore generate the entire integral relation kernel K. Projection to the eight supplementary coordinates is injective because the old 55 active records are independent. The projected lattice is the kernel of the surjection Z^8 -> L/L0 sending each coordinate to the corresponding supplementary record class. Its index in Z^8 is [L:L0].

Compute the 8 x 8 row HNF of the projected P rows together with the individual denominator-clearing relations. Recover the first 55 coefficients by exact division using the original rational transfer matrix. Check integrality, kernel equations and determinant. The full relation kernel in Z^63 is saturated, since its quotient is free; its projected lattice in Z^8 has finite index and is not saturated there.

## 3. Exact coefficient reduction

The restricted HNF and reduction by individual denominator relations reduce the maximum generator coefficient from 242 digits to 15 digits. LLL with delta=3/4 uses exact rational Gram-Schmidt arithmetic, then exact nearest-plane reduction and monotone local descent shorten the lifts by subtracting full-kernel relations. The code verifies all LLL size and Lovasz conditions and the determinant of the projected reduced kernel.

- Minimum supplementary record count: 8.
- Full source record count: 280.
- Active source/target dimensions: 63 and 320.
- Active integral recovery matrix: 55 x 63.
- Remaining identity coordinates: 217.
- Maximum final generator coefficient: 133185.
- Maximum final direct reconstruction coefficient: 219612.
- Exact checks in first stage: 21065.
- Exact checks in final stage: 24530.
- Both certificate JSON outputs replayed exactly.
- Deliberately corrupted direct reconstruction row rejected.

All new maps are integer matrices and commute with reduction modulo every positive integer. This preserves the original rank and eliminates extra-precision requirements when the supplementary records are given. LLL reduction certifies a substantial size improvement, not globally shortest or sparsest coefficients.

## 4. Reproduction and remaining boundaries

Run from repository root:

    node tools/compile_graph_atlas_optimized_integral.js rebuilt-optimized.json
    node tools/compile_graph_atlas_short_integral.js rebuilt-short.json

The second script uses the retained first-stage certificate. Compare each regenerated JSON against its committed version. The remaining 217 identity coordinates are precisely the original basis identifiers not present in activeBasis.

Remaining questions: a different catalogue-only integral basis of 272 records, minimal evaluation cost, joint optimization of sparsity and coefficient magnitude, universal parameterized rank, deferred scalar denominator expansions, independent review and Lean verification. The research branch is separate from the live publication.
