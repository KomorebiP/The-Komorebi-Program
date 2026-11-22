# Sources and contributions

The worked examples use established mathematical results and develop them through the packet, transfer, and residual constructions of the Komorebi Program. This guide identifies the principal sources, gives precise locators, and explains how each source is used. It also distinguishes the original inputs from the work carried out in the examples.

This is a guide to three starting points, not an exhaustive bibliography or a general claim of mathematical priority.

[Euler numbers](#euler-numbers-and-quartic-reciprocals) · [Wavelets and polyphase filters](#haar-wavelets-lifting-and-polyphase-filters) · [Seed generation](#seed-generation-and-the-central-framework) · [Citation and corrections](#citation-and-corrections)

## Euler numbers and quartic reciprocals

[Read the Euler walkthrough](demonstrations/EULER_PACKETS.md) · [Source checks and conventions](../verification/euler-packets/SOURCES.md)

### Established sources

- **Euler numbers, Euler polynomials, and the secant series.** The NIST *Digital Library of Mathematical Functions* gives the signed Euler-number convention in [24.2.6](https://dlmf.nist.gov/24.2.E6), the Euler-polynomial generating function in [24.2.8](https://dlmf.nist.gov/24.2.E8), and the secant expansion in [4.19.5](https://dlmf.nist.gov/4.19.E5). These establish the signs, factorials, and indexing used in the calculation. The positive secant sequence is indexed by even degree, so its index is half the degree of the corresponding power.

- **Positive secant numbers.** [OEIS A000364](https://oeis.org/A000364), attributed in the entry to N. J. A. Sloane, supplies the comparison sequence. Its [table](https://oeis.org/A000364/b000364.txt), at indices 0 through 15, is checked against values reconstructed independently by the exact recurrence.

- **Quartic sequence.** [OEIS A211212](https://oeis.org/A211212), authored by Peter Luschny, records the 4-alternating permutation sequence used in the quartic calculation. The displayed recurrence is credited there to Ilya Gutkovskiy (27 January 2020), and the equivalent cosine/cosh generating function to Michael Wallner (17 November 2020). Both are treated as prior results.

- **Generalized alternating permutations.** Peter Luschny's [OEIS A181985](https://oeis.org/A181985), particularly its *Comments* section, provides the general pattern. An ascent occurs precisely when its position is divisible by the chosen block length.

### What the walkthrough does

The example carries the same Euler data through reciprocal packets, polynomial coordinates, local arithmetic, and explicit failure and repair calculations. The point is to connect the representations in one derivation and make each transition inspectable. Extensions using Papers IV and IX are identified together with their hypotheses in the [source notes](../verification/euler-packets/SOURCES.md).

The classical sequences, their credited formulas, and their combinatorial interpretations remain established inputs. Whether an additional general result is new requires a comparison of that specific statement with the literature.

## Haar wavelets, lifting, and polyphase filters

[Read the sixteen-sample walkthrough](demonstrations/WAVELET_POLYPHASE.md)

### Established sources

- **Discrete Haar analysis.** Martin Vetterli and Jelena Kovačević, *Wavelets and Subband Coding* (1995), corrected online manuscript, [§3.1.2, equations 3.1.10–3.1.14, printed p. 104](https://waveletsandsubbandcoding.org/Repository/VetterliKovacevic95_Manuscript.pdf#page=121). The example uses half-sums and half-differences, with the corresponding synthesis weights, rather than the book's orthonormal normalization.

- **Polyphase matrices.** Vetterli and Kovačević, [§3.2.1, equations 3.2.22–3.2.26, printed pp. 120–122](https://waveletsandsubbandcoding.org/Repository/VetterliKovacevic95_Manuscript.pdf#page=137). The example specializes the polyphase representation to a finite circular signal and derives the shift matrix and boundary correction explicitly.

- **Lifting and its inverse.** Wim Sweldens, *The Lifting Scheme: A New Philosophy in Biorthogonal Wavelet Constructions* (1995), [Figure 1 and the inverse algorithm, PDF p. 5](https://cm-bell-labs.github.io/who/wim/papers/spie95.pdf#page=5). The pair factorization is a lifting specialization with the example's stated signs and scaling.

### What the walkthrough does

The example follows one rational sixteen-sample signal through four Haar levels and a three-tap filter. It writes out the transferred operation, the full matrix, and the residuals caused by omitted interactions, changed operation order, and boundary terms. The derivations and reproducible tables allow the finite calculation to be checked from its inputs.

Haar analysis, lifting, polyphase representation, and operator conjugation are established methods. The stated formulas describe the example's finite circular model. They should not be read as claims about arbitrary boundary conditions or all filters.

## Seed generation and the central framework

[Read the two-dimensional seed example](examples/02_SEEDS.md) · [Paper I](works/paper-i.md)

### Established source

A linear operator on a finite-dimensional vector space defines a module over a polynomial ring. Cyclic generation and primary decomposition are standard results of that structure. See Paul Garrett, *Abstract Algebra* (June 2007), [Theorem 10.1.1 and Corollary 10.4.1, printed pp. 126 and 130](https://www-users.cse.umn.edu/~garrett/m/algebra/Whole#page=136).

### How the project uses it

The two-dimensional tutorial illustrates how repeated application of one operator to a seed can generate a space. Paper I's one-operator seed count follows from the classical module structure. The tutorial is an introduction to the project's terminology, not a new theorem about cyclic modules.

Realization Calculus develops packet, transfer, refinement, and residual constructions in its individual papers. [Komorebi Space](works/komorebi-space.md) develops a related realization and compatibility framework with a recorded sixteen-group correspondence. Those larger works must be assessed through their actual definitions, hypotheses, statements, and evidence rather than through the elementary seed example alone.

## Citation and corrections

When using an established formula or sequence, cite the original source and the particular equation, entry, comment, or credited contributor. When citing a result from this collection, identify the specific work, statement, and revision, following the [citation guide](../CITATION.md).

The wider citation record is still being reconstructed. The [project statement](PROJECT_STATEMENT.md#citations-and-acknowledgment-of-prior-work) explains that work and its limitations. Missing attribution should be corrected, not interpreted as an originality claim. To report an omission or inaccurate credit, [open a source or documentation issue](https://github.com/KomorebiP/The-Komorebi-Program/issues/new/choose) and include the relevant passage and reference.

[Start here](START_HERE.md) · [Worked examples](DEMONSTRATIONS.md) · [Project map](PROJECT_MAP.md)
