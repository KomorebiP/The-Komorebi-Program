# Komorebi: Transfer Discovery and Rational-Ratio Extraction

**Author: Komorebi P.**  
Checkpoint: 2026-11-22. Corpus: 56 deliberately curated OEIS sequences, not the full OEIS.

## Research objective

Build a representation and transfer index in which a sequence can have many mathematical representations, and where an operator identity is stored once, with parameter schemas, rather than duplicated for every pair of OEIS numbers. Collect raw formulas and cross-reference candidates before expensive mathematical review. Distinguish (i) formula recorded, (ii) prefix agreement, (iii) symbolic identity proved, and (iv) quantified computational advantage. These are **different** claims.

## Current reproducible specimen

- 56 OEIS sequences, 61 independently exact-prefix-tested formula evaluators.
- 17 manually derived algebraic transfer examples in the graph, including the existing Fibonacci-resolvent Euler bridge and eight additional identities with elementary proofs below.
- 52 nontrivial exact-prefix transfer candidates, after factoring out the neutral laws of pointwise addition/multiplication and OGF/EGF convolution. The unfiltered exploratory pass found 240 links, of which 188 are structurally redundant neutral-element instances.
- 18 first-order rational-ratio candidate recurrences, of which 17 have rational linear-factor decompositions and hence a Pochhammer expression for the fitted pattern.
- Graph projection: 170 nodes and 190 edges. Of those 17 are marked algebraic, 61 are formula representations and 112 are finite candidate visualization edges. **112 is not the number of candidate relations:** 25 of the 52 relation records are multi-input hyperedges and use more than one display arrow. Ratio candidates have separate nodes and edges.
- 38 passing Python tests across the imported project, plus JavaScript syntax and interactive Chromium checks for the standalone atlas.

The algebraic identity count excludes the neutral laws themselves, which remain general transformation conventions. All stored integer coefficients use exact Python integer arithmetic, and rational computations use `fractions.Fraction`.

## How discovery works

For each stored sequence `A`, define its *local* coefficient list `A[o_A+j]`, where `o_A` is the official mathematical offset, not a position guessed from a bulk export.

Univariate candidate classes:

- Shifts: `B[o_B+j] = A[o_A+j+r]`.
- Polyphase: `B[o_B+j] = A[o_A+m*j+r]` for `m>=2`, `0<=r<m`.
- Termwise affine changes, adjacent differences and prefix sums.
- Forward/inverse binomial transforms.

Bivariate candidate classes (AND hyperedges):

- `C[o_C+j] = A[o_A+j]*B[o_B+j]`, or the corresponding sum.
- Ordinary convolution: `C[o_C+j] = sum_{k=0}^j A[o_A+k]*B[o_B+j-k]`.
- Exponential convolution: `C[o_C+j] = sum_{k=0}^j binom(j,k)*A[o_A+k]*B[o_B+j-k]`.

The miner indexes the first ten exact output values to avoid a cubic scan over output sequences. It then checks every *available* overlapping term. At least one holdout term beyond the discovery signature is required. It stores the lengths of both windows, a source-record digest, a readable indexed statement, and `finite_candidate` status. Changed term data invalidates the projected candidate edge. A finite agreement never establishes an infinite identity. Neutral operations such as `A*1=A`, `A+0=A`, and convolution with `delta_0` are not materialized for each OEIS sequence.

### Rigorous examples promoted to algebraic transfers

For the binomial operator `B[a](n)=sum_{k=0}^n binom(n,k)a(k)`, the binomial theorem proves

```
B[1](n)   = 2^n,
B[2^k](n) = 3^n,
B[3^k](n) = 4^n.
```

Thus the chain `A000012 -> A000079 -> A000244 -> A000302` is established for all nonnegative integers, not merely observed for a finite prefix. Its parameter version is `B[c^k](n)=(c+1)^n`. Inverse binomial transformation gives `B^-1[c^k](n)=(c-1)^n`.

The derangement transform `A000166 -> A000142` follows by counting permutations of `n` items with exactly `n-k` fixed points: choose the `k` moving points in `binom(n,k)` ways and derange them in `!k` ways. Summing over `k` yields `n!`.

For `T_n=n(n+1)/2`, differences give `T_{n+1}-T_n=n+1`. For `S_n=n^2`, differences give `S_{n+1}-S_n=2n+1`. For `M_n=2^n-1`, differences give `M_{n+1}-M_n=2^n`. These are exact operator equalities with documented index offsets.

For `B_n=binom(2n,n)`, the ordinary generating function `B(x)=(1-4x)^(-1/2)` gives

```
[B(x)]^2 = (1-4x)^(-1) = sum_{n>=0}4^n*x^n
```

and hence `sum_{k=0}^n B_k B_{n-k}=4^n`. This proves a self-convolution transfer, `A000984 -> A000302`, for every `n>=0`.

These are classical identities. No historical novelty is asserted. Their importance here is the distinct, reusable transfer representations.

## Automatically recovered Pochhammer candidates

Look for a rational consecutive-coefficient ratio after the first nonzero sample `s`:

```
a(s+t+1)/a(s+t) = P(t)/Q(t),      Q(0)=1.
```

For polynomial degrees `<=2`, fit by exact rational Gaussian elimination on an initial segment of ratios, reserve at least four ratios as a *holdout*, and verify the whole stored excerpt. A rationally factorable pair gives a candidate Pochhammer form

```
a(s+t) = a(s) * c^t * product_i(alpha_i)_t / product_j(beta_j)_t.
```

A finite fit is neither a universal recurrence proof nor a guarantee that a denominator avoids zero at all future indices. Explicit source-derived proofs are needed before promoting any fitted candidate to an algebraic identity.

For Catalan numbers `C_n = (1/(n+1))*binom(2n,n)`, the miner recovers

```
C(n+1)/C(n) = 4*(n+1/2)/(n+2),
C(n) = 4^n * (1/2)_n / (2)_n.
```

Here the latter formula **is** classically proven using the factorial definition of `C_n`; the *general extraction procedure* does not confer proof on any other candidate.

For central binomial coefficients `B_n`, the analogous exact formula is `B_n=4^n*(1/2)_n/(1)_n`. The automatic ratio miner also correctly declines to fit Fibonacci as a rational first-order hypergeometric-ratio sequence in the tested bounded family.

## Cost and mathematical reuse

A structural equality is not a guaranteed computational speedup. A naive binomial transform has `n+1` summands, while the proven exponential specialization reduces to exponentiation by squaring with logarithmically many large-integer multiplications. Both methods ultimately have to produce the exact integer output, whose bit length matters. The Fibonacci-resolvent Euler transfer is a valid re-expression, but no speed improvement has been established. The graph must keep *provability*, *computational cost* and *novelty* as independent fields.

## Scalability and full-corpus ingestion

The archive importer accepts a **local** `.zip`/`.tar.gz` snapshot of the official `oeisdata` repository, reads `.seq` entries without extracting files, validates record identifiers and indexing, and stores `%F`, `%p/%t/%o` as unexecuted text plus `%Y` as reference-only crosswalks. It reports per-entry failures transactionally, logs archive SHA-256 and supports incremental idempotent reimport. OEIS attribution and CC BY-SA 4.0 requirements remain attached to sourced data.

The import step is designed to be run over an archive of arbitrary size, but this checkpoint has **not downloaded or imported the full OEIS archive**. Bivariate mining is deliberately prohibited above 300 loaded sequences because the current pair enumerator is quadratic. The CLI enforces a maximum loaded sequence count until the single-source miner can be sharded. Full-scale matching will require persistent prefix indexes and/or partitions; claiming complete graph coverage now would be inaccurate.

## Reproduce locally

From the `The-Komorebi-Program` repository root after copying the files into their paths:

```sh
python tools/oeis_formula_database.py --db oeis.sqlite3 ingest-seeds --path research/oeis-formulas/seeds.json
python tools/oeis_formula_database.py --db oeis.sqlite3 ingest-seeds --path research/oeis-formulas/seeds-extended.json
python tools/oeis_bulk_import.py --db oeis.sqlite3 --archive /path/to/oeisdata-main.zip
python tools/sequence_transfer_miner.py --db oeis.sqlite3 mine --no-pairs --max-sequences 500000 --export candidate-transfers.jsonl
python tools/sequence_transfer_graph.py --db oeis.sqlite3 build --export transfer-graph.jsonl
python tools/render_sequence_transfer_atlas.py --db oeis.sqlite3 --output sequence-transfer-atlas.html
python -m unittest discover -s tools -p 'test_*.py' -v
```

**Warning:** running one-source mining on hundreds of thousands of rows can still use substantial RAM and time; the `--max-sequences` option is a guard override, not a performance optimization. On a local limited-memory workstation, use bounded OEIS subsets until sharded mining is implemented.

Source: <https://github.com/oeis/oeisdata>, <https://oeis.org/LICENSE>. Mathematical and OEIS indexing details can change in upstream snapshots. Reingest and rerun source-digest checks before treating a receipt as current.
