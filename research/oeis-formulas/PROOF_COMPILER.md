# Komorebi: Indexed Transfer Search and Symbolic Proof Compiler

**Author: Komorebi P.**  
**Checkpoint:** 2026-11-22  
**Research artifact version:** 0.5

## Objective

Retain as many source formulas as possible, build a searchable graph of
transfer operators, and later optimize exact computation by reusing kernels.
A stored formula, a finite prefix match, an algebraic identity of two supplied
formulas, and an independently verified OEIS identity are four different
claims. The v0.5 implementation does **not** collapse them.

## Source data and scope

The reproducible specimen has **56 OEIS entries**, **61 exact evaluator
specifications**, **52 nonneutral finite-transfer candidates**, and **18
finite rational-ratio fits**. The complete official OEIS `.seq` corpus is
**not** present in this package. An existing archive importer can ingest it
from a user-supplied local archive without extracting entries or executing
OEIS formulas or code listings. OEIS-derived content is attributed to the
OEIS Foundation under CC BY-SA 4.0. Definitions of the local Komorebi
constructs remain separately attributed.

### Indexed discovery

The `transfer_prefix_index` table uses SHA-256 hashes of the first ten
*mathematical-offset-aligned* stored integers, with a second hash of the full
stored term list. Each source term list is visited once. Its shifts,
multisections, affine modifications, differences, prefix sums and inverse
or forward binomial transforms are compared with the indexed targets. A hit
requires ten discovery coefficients plus at least one further coefficient,
then agreement over the full overlapping stored prefix. Source hashes are
retained with candidate certificates; stale indexes are rejected.

Memory usage for this **single-source** miner is proportional to the current
source and the current candidate target, plus SQLite cursor state. The
persistent index grows with the number of sequences. SQL lookups replace the
previous all-records-in-memory scan. In terms of corpus size S, typical
index creation is O(total stored terms), while probing depends on the number
of generated operators, index lookup and verification of collisions. There
is no claim of a universal worst-case linear running time. Pairwise AND
hyperedges remain in the original bounded quadratic miner.

For a large SQLite source:

```shell
python tools/sequence_transfer_index.py --db formulas.sqlite3 index
python tools/sequence_transfer_index.py --db formulas.sqlite3 mine --no-rebuild --from-id A000001 --through-id A099999
python tools/sequence_transfer_index.py --db formulas.sqlite3 mine --no-rebuild --from-id A100000 --through-id A199999
```

To refresh the entire unary candidate table while preserving pairwise
relations, run `mine --reset-unary` without range flags. Sharded repeated
runs are idempotent; a source update requires an index rebuild before the
new candidate relations can be trusted. No finite candidate is automatically
promoted into an infinite OEIS theorem.

## Algebraic rational-ratio certificates

The restricted declarative evaluator language admits a mathematical proof
engine that never executes source prose. Supported terms include:

- Nonzero affine factors `a*n+b` and positive integer powers thereof.
- Factorials of nonnegative affine arguments and affine binomial coefficients.
- Products, exact quotients and constant-base exponentials with affine exponents.
- Compositions with affine index maps, when explicit in the evaluator tree.

For these constructors, a consecutive-value ratio follows from identities
such as

\[
\frac{(an+b+a)!}{(an+b)!}=\prod_{j=1}^{a}(an+b+j),
\quad
\frac{\binom{u(n+1)}{v(n+1)}}{\binom{u(n)}{v(n)}}
=\frac{u(n+1)!/u(n)!}{[v(n+1)!/v(n)!][(u-v)(n+1)!/(u-v)(n)!]}.
\]

The resulting exact ratio is stored in affine factors, and gives a terminating
Pochhammer product by induction. Factor denominators are checked for a safe
nonzero half-line beginning at the explicitly stored starting index. The
certificate is a theorem about the *declared expression*, not an infinite
OEIS identification. For a rationalized `exact_div` expression, mathematical
integrality at every index is a separate obligation unless already proved.

There are **21 symbolic ratio certificates**, and **17 of the existing finite
ratio fits** are confirmed *algebraically* by these independently derived
rational functions. The remaining fit is not automatically certified.
The Catalan and central-binomial cases include

\[
\frac{C_{n+1}}{C_n}=\frac{2(2n+1)}{n+2},\qquad
C_n=\frac{4^n(1/2)_n}{(2)_n};
\quad
B_n=\frac{4^n(1/2)_n}{(1)_n}.
\]

The normalizer also factors common factorial kernels. If two admitted term
expressions have a common factorial skeleton, their ratio is a product of
rational affine factors and a constant-base exponential:

\[
\frac{b(n)}{a(n)}=c\,\rho^n\prod_j(u_jn+v_j)^{m_j}.
\]

The v0.5 graph stores **14 representative symbolic quotient links** between
curated evaluators, rather than all quadratic pairwise combinations. Many
links are elementary polynomial relations; no novelty or speedup is claimed.
One useful example is the *derived* Catalan relationship

\[
C_n=\frac{B_n}{n+1},\qquad B_n=\binom{2n}{n}.
\]

`formula_algebra` edges link **formula nodes**; they never count as
independently proved OEIS sequence-to-sequence paths.

## Exact rational OGF compiler

For an order-d constant-coefficient recurrence

\[
a_n=\sum_{j=1}^dc_j a_{n-j}\quad(n\geq d),
\]

write

\[
Q(x)=1-\sum_{j=1}^dc_jx^j,\qquad
P(x)=\sum_{n=0}^{d-1}\left(a_n-\sum_{j=1}^{n}c_ja_{n-j}\right)x^n.
\]

Then the rational formal power series identity

\[
A(x)=\frac{P(x)}{Q(x)}
\]

holds for **every** coefficient of the declared recurrence by coefficient
comparison. For two such definitions, the exact transfer is

\[
B(x)=\frac{P_B(x)Q_A(x)}{Q_B(x)P_A(x)}A(x).
\]

The normalizer cancels the rational polynomial gcd and records the valuation
as a Laurent shift `x^s`; this correctly handles recurrences whose generating
functions begin with zero terms. Transfer composition is exact algebra in
`Q((x))`. Materializing every pair would be wasteful, so the compiler stores
one rational OGF per recurrence and computes cross-filters on demand.

The eight verified recurrence *formula definitions* give **eight rational
OGFs** and **four directed finite shift projections** for the two same-kernel
pairs (Fibonacci/Lucas and Pell/Pell–Lucas). For example,

\[
\frac{x}{1-2x-x^2}
=\frac{1-x-x^2}{1-2x-x^2}\,\frac{x}{1-x-x^2}
\]

and

\[
L_n=2F_{n+1}-F_n,\qquad Q_n=P_{n+1}-P_n.
\]

The shift projections are proved by showing both sides satisfy the same
recurrence and agree on d initial conditions. These are classical relations.
No general novelty finding or computational advantage has been established.

### Reproduce

From the package root (Python 3.10+, standard library only):

```shell
python tools/sequence_transfer_index.py --db oeis-formulas.sqlite3 index
python tools/sequence_transfer_index.py --db oeis-formulas.sqlite3 mine --reset-unary --no-rebuild
python tools/sequence_ratio_certificates.py --db oeis-formulas.sqlite3 --export research/oeis-formulas/certified-ratios.jsonl
python tools/sequence_kernel_transfers.py --db oeis-formulas.sqlite3 --export research/oeis-formulas/exact-kernel-transfers.jsonl
python tools/sequence_recurrence_transfers.py --db oeis-formulas.sqlite3
python tools/sequence_recurrence_transfers.py --db oeis-formulas.sqlite3 --from-id A000045 --to-id A000129
python tools/sequence_transfer_graph.py --db oeis-formulas.sqlite3 build --export research/oeis-formulas/transfer-graph.jsonl
python tools/render_sequence_transfer_atlas.py --db oeis-formulas.sqlite3 --output sequence-transfer-atlas.html
python -m unittest discover -s tools -p 'test_*.py' -v
```

The atlas distinguishes `algebraic_identity`, `formula_algebra`,
`finite_candidate`, and `recorded_representation` visibly. Proof-path search
includes only established sequence-link entries, never finite or formula-only
links. Formula-only edges may be added to proof paths only after independent
OEIS identification and domain review.

## Limitations and next work

1. Import and preserve the full official formula corpus rather than 56 seed records.
2. Normalize more than the restricted multiplicative/factorial DSL, notably
   multivariate sums, recurrences, generating functions, trigonometric/Euler
   constructions, non-holonomic terms, modular and p-adic transforms.
3. Establish source-linked proof certificates for actual infinite OEIS
   identifications, not just algebraic properties of curated evaluator trees.
4. Build cost-aware multi-output DAG scheduling and benchmark exact arithmetic,
   tracking operand bit sizes and shared intermediates. A true formula
   identity can be slower than a dedicated recurrence.
5. Add source-sharded cross-corpus indexes for AND-hyperedge discovery and
   a durable database for parameterized operator schemas.

Sources: OEIS Foundation, <https://oeis.org/>, <https://oeis.org/LICENSE>.
The archived full source is not in this artifact. No finite match proves
historical novelty, global OEIS identity, or a formerly open conjecture.
