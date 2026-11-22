# Start here

**Realization Calculus and Komorebi Space · Komorebi P.**

The Komorebi Program investigates what survives a change of mathematical representation. Breaking an object into components, changing coordinates, or replacing it with a summary may simplify a calculation. But which operations remain valid after that change? Can the original object be recovered? If not, what information is missing?

**Realization Calculus** studies decomposition, transfer, refinement, and reconstruction using packets, seeds, coordinates, and explicit residuals. **Komorebi Space** provides a framework for comparing representations (or *realizations*), checking when they are compatible, and identifying obstructions when they are not.

The collection investigates these questions in algebra, analysis, arithmetic, signal processing, computation, and models of interacting systems. Use the [project map](PROJECT_MAP.md) to see connections between subjects, or [browse by work](BROWSE.md) to find manuscripts and source files.

## A quick way in

**New to the project?** Begin with the [Euler-number case study](demonstrations/EULER_PACKETS.md). It follows one calculation through several representations and shows where reconstruction and residual correction enter.

**Interested in the mathematical framework?** Read [Realization Calculus](works/realization-calculus-book.md) alongside [Komorebi Space](works/komorebi-space.md), using the [notation index](NOTATION_INDEX.md) as needed.

**Looking for proofs or code?** Go directly to the [status catalogue](STATUS_CATALOG.md), [written proofs](browse/PROOFS.md), [Lean material](browse/LEAN.md), or [code index](browse/CODE.md). These are different kinds of evidence and should not be treated as interchangeable.

You do not need to read the collection in order. The routes below give several independent starting points.

## What the project is trying to contribute

The aim is a reusable language for decomposing objects, transporting operations between descriptions, and determining when reconstruction succeeds. When a transfer fails, the framework seeks to state the obstruction or residual explicitly rather than hide it in an approximation.

Each work must be judged by its stated definitions, hypotheses, constructions, and proofs. A similar pattern in two subjects is a motivation for investigation, not by itself a theorem connecting them. A valid transfer needs an argument that preserves the required structure and assumptions.

The [sources and contributions](SOURCES_AND_CONTRIBUTIONS.md) page distinguishes classical inputs from the constructions and explanations used in the introductory Euler, wavelet, and seed-generation examples.

## Start with an extended case study

An extended case study makes the abstract terminology concrete. Start with one subject and track the representations, valid operations, information retained, and information lost. The following three studies illustrate different settings; they are alternatives, not prerequisites for one another.

### Arithmetic and coordinates

Start with [Euler numbers](demonstrations/EULER_PACKETS.md), then continue to [factorial lanes](demonstrations/FACTORIAL_LANES.md). Follow reciprocal series, changes of basis, prime-adic bounds, refinement, and residual repair.

### Signals and operations

Read [wavelets and polyphase transfer](demonstrations/WAVELET_POLYPHASE.md). Follow four Haar levels, filter transport, finite stability, and the exact error caused by omitted interactions.

### Quantum information

Read [quantum phase and measurement](demonstrations/QUANTUM_PHASE_MEASUREMENT.md). Examine which measurements are recoverable, what coherence is discarded, and when a reversible record permits finite recovery.

The [extended case-study index](DEMONSTRATIONS.md#extended-case-studies) links to additional counting and polynomial examples. Consult each study for its stated calculations, controls, and verification scope. The [Special Functions guide](SPECIAL_FUNCTIONS.md) offers a separate entry into function constructions and analytic questions.

## Choose a reading route

Choose according to what you want to understand or verify. You can move from a worked example to the general theory, or begin with a manuscript and inspect its supporting material.

For works with a complete online manuscript and visual guide, use the [guided reading paths](https://KomorebiP.github.io/The-Komorebi-Program/read/start.html). You can begin with the visual introduction, read the manuscript, or inspect supporting evidence.

### Foundations and mathematical developments

- **Common framework:** [Realization Calculus](works/realization-calculus-book.md) and [Komorebi Space](works/komorebi-space.md).
- **Individual papers:** [Papers I–XII](../papers/README.md).
- **Limits of representation:** [Realization Boundaries](works/realization-boundaries.md).

### Examples and applications

- **Complete calculations:** [Extended case studies](DEMONSTRATIONS.md#extended-case-studies), starting with [Euler numbers](demonstrations/EULER_PACKETS.md).
- **Companion subjects:** [Monographs and companion volumes](../monographs/README.md).
- **Open questions:** [Research programs and their scope](../research/README.md).

### Verification and research method

- **Executable mathematics:** [Software guide](LIBRARIES.md) and [experimental laboratories](../experiments/README.md).
- **Discovery and review:** [Proof Path Theory](works/proof-path-theory.md) and [Komorebi Methodology](works/komorebi-methodology.md).

## Where the work stands

The collection includes mathematical manuscripts, formal developments, conditional results, software, and experiments. Their completion and verification status varies. The [completion and confidence guide](COMPLETION_STATUS.md) explains the status labels. The [status catalogue](STATUS_CATALOG.md) and [dated records](RECORDS.md) give the assessments for individual works and revisions.

The [finalization queue](FINALIZATION_QUEUE.md) records outstanding work, while the [project map](PROJECT_MAP.md#documented-connections) documents selected connections between sources. A complete theorem-dependency audit remains open. A polished reading edition is not necessarily a fully proved or independently reviewed result.

## Four questions to carry through the collection

1. **What is the object?** State the space, coefficient system, and admissible inputs.
2. **How is it resolved?** Identify the packets, coordinates, or other components used to represent it.
3. **How does the operation transfer?** Determine the blocks or compatibility laws relating representations.
4. **What is reconstructed?** State the recovered object and any residual or obstruction.

The [operator guide](OPERATOR_AUDIT.md) applies these questions to matrix operations, packet blocks, and coordinate changes. It examines omitted interactions and what a summary can recover, with worked chapters on polynomial and difference operators. The [operator catalogue](operators/catalog/README.md) lists formulas, assumptions, and source links. Interactive experiments and a worksheet support further investigation.

<a id="start-with-a-complete-demonstration"></a>

## Worked calculations

For a shorter introduction than the extended case studies, the [worked demonstrations](DEMONSTRATIONS.md) pair elementary calculations with small programs. Choose a question below and follow it from input to result.

- **Can smaller operations reconstruct the whole?** [Reconstruct an operator from packet blocks](demonstrations/PACKETS.md). Background: small matrix products.
- **What survives refinement, and what is lost by deletion?** [Refine a signal and account for a missing packet](demonstrations/REFINEMENT.md). Background: list indexing and sums.
- **Can a summary answer the original question?** [Test recovery from a summary](demonstrations/RECOVERY.md). Background: addition and functions.

These examples can be read without installing software. The accompanying [Python programs](DEMONSTRATIONS.md#run-without-installing-a-library) use the standard library, and their output is a check of the stated examples rather than a substitute for a general proof.

<a id="a-concrete-arithmetic-example"></a>

<a id="run-the-arithmetic-preview"></a>

## Run the Euler-number example

The [Euler-number case study](demonstrations/EULER_PACKETS.md), introduced above, traces reciprocal series, polynomial coordinates, exact transfer matrices, and residual correction. You can read the derivation alone or reproduce its finite checks.

Read the derivation [on the website](https://komorebip.github.io/The-Komorebi-Program/collection/demonstrations/EULER_PACKETS.html), or run the exact checker from the collection root:

```text
python -B examples/euler_packets.py
```

Python 3.10 or later is sufficient; the checker uses only the standard library. A successful run ends with `PASS: Euler packets, polynomials and residuals`. You can also download the [standalone checker](https://komorebip.github.io/The-Komorebi-Program/downloads/euler-packets/euler_packets.py) or the [complete source and results bundle](https://komorebip.github.io/The-Komorebi-Program/downloads/euler-packets/source-and-checks.zip).

The example records its sources and tested ranges. The [workflow guide](WORKFLOWS.md) explains the collection's verification commands.

## Interpret the evidence

Evidence should be interpreted according to what it establishes:

- **Written theorem:** Check the precise conclusion, assumptions, and argument.
- **Lean declaration:** Check the statement, imports, axioms, environment, and compilation record.
- **Exact finite calculation:** Check the inputs, arithmetic model, tested property, and any separate argument extending it beyond those inputs.
- **Numerical experiment:** Check precision, range, reference result, error criteria, and retained outcomes.
- **Software test:** Check the exercised behavior, platform, dependencies, and source revision.
- **File-integrity record:** Check which exact bytes and source snapshot it identifies.

**Important distinction:** a proof of “if A, then B” does not establish B until A is verified. Likewise, successful finite computations do not alone prove a universal statement. Open obligations, including those identified for Paper XI, Physics, and machine models, must be assessed against the current [status catalogue](STATUS_CATALOG.md), rather than inferred from the existence of a manuscript or test.

All software is **beta and work in progress**. For reproducibility, record the source revision, hypotheses, runtime, and test scope. Follow the [citation guidance](../CITATION.md) for the specific work and revision you use.

The [public project and authorship statement](PROJECT_STATEMENT.md) explains the pseudonym, AI assistance, and publication circumstances. For installation and check commands, use the [verification guide](VERIFICATION.md).

[Notation index](NOTATION_INDEX.md) · [Papers](browse/PAPERS.md) · [Written proofs](browse/PROOFS.md) · [Lean](browse/LEAN.md) · [Code](browse/CODE.md) · [Complete component index](COMPONENT_INDEX.md) · [Collection](../README.md)
