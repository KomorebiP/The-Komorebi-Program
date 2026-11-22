# Komorebi sequence transfer compiler, v0.6

**Author: Komorebi P.**  
**Checkpoint:** 22 November 2026  
**OEIS attribution:** OEIS Foundation Inc., [OEIS](https://oeis.org), CC BY-SA 4.0. The full OEIS `.seq` source corpus has **not** been ingested in this release.

## 1. Purpose

This release extends the formula catalogue into an **exact symbolic transfer engine**. Its proof claims are **conditional on the declarative formula definitions**. Passing a finite OEIS term test does not establish that the formula describes the OEIS sequence for every integer.

The engine separates three independent records:

1. Original OEIS formula/program fields, indexed as attributed, **unexecuted source text**.
2. Curated evaluators, compared against exact finite OEIS excerpts with the mathematical offset preserved.
3. All-index algebraic relations **of the curated evaluator expressions**, established from symbolic identities or defining recurrences.

No finite prefix can, by itself, promote a candidate to level 3.

## 2. Universal recurrence packet theorem

Let

\[
 a_{n+d}=c_1a_{n+d-1}+\cdots+c_da_n,
 \qquad a_0,\ldots,a_{d-1}\in\mathbb Z,
\]

and define

\[
 \chi(X)=X^d-c_1X^{d-1}-\cdots-c_d.
\]

Let \(R_n(X)=X^n\bmod\chi(X)=\sum_{j=0}^{d-1}r_j(n)X^j\).
For the shift \(S(a_n)=a_{n+1}\), \(\chi(S)a=0\). Consequently

\[
 \boxed{a_n=\sum_{j=0}^{d-1}r_j(n)a_j}\qquad(n\ge0).
\]

The remainder \(R_n\) is calculated by binary modular polynomial exponentiation in \(O(d^2\log(n+1))\) ring operations; this is not a bit-complexity bound. **All sequences with the same \(\chi\) share the same remainder packet.**

## 3. Structural derivation without prefix fitting

The restricted evaluator normalizer recognizes

\[
 a(n)=\sum_{\lambda\in\Lambda}P_\lambda(n)\lambda^n,
 \qquad P_\lambda\in\mathbb Q[n],\ \lambda\in\mathbb Z\setminus\{0\}.
\]

Because \((S-\lambda)^{\deg(P)+1}(P(n)\lambda^n)=0\), an annihilator is

\[
 \boxed{\chi(S)=\prod_{\lambda\in\Lambda}(S-\lambda)^{\deg(P_\lambda)+1}.}
\]

The proof also accommodates exact affine binomial polynomials, residue-periodic terms, affine floor divisions and declared recurrences. All unsupported syntax is rejected rather than interpolated. Mathematical index offsets are applied explicitly to the local sequence \(b_n=a_{o+n}\).

For example \(a(n)=n^2\) is annihilated by \((S-1)^3\), so \(a_{n+3}=3a_{n+2}-3a_{n+1}+a_n\). For \(a(n)=\binom n6\), the seventh forward difference vanishes, yielding \((S-1)^7\).

## 4. Exact polyphase closure

For a positive integer \(m\) and \(0\le r<m\), let \(b_n=a_{mn+r}\). Let \(T\) be multiplication by \(X\) in \(\mathbb Q[X]/(\chi)\); then

\[
 b_n=L\,(T^m)^nT^re_0,
\]

where \(L=[a_0,\dots,a_{d-1}]\). By Cayley–Hamilton, \(\det(YI-T^m)\) annihilates every phase. A potential lower-degree recurrence is certified by verifying its residual for the first \(d\) phase indices: the residual is itself a solution of a recurrence of order at most \(d\), so these exact zeros prove all-index vanishing.

As a concrete example, for Fibonacci \(F_n\),

\[
 F_{2n+4}=3F_{2n+2}-F_{2n},\qquad
 \sum_{n\ge0}F_{2n}z^n=\frac{z}{1-3z+z^2}.
\]

Likewise the odd phase has OGF \((1-z)/(1-3z+z^2)\). Each asserted identity is a theorem of the source recurrence, and no OEIS identity is inferred solely from its first few terms.

## 5. Transfer graph and shared denominators

Every derived phase has a rational OGF. Reducing the numerator/denominator over \(\mathbb Q[z]\) permits exact denominator-grouping and on-demand quotient filters. For sources with OGFs \(A(z),B(z)\), the relation

\[
 B(z)=z^e\frac{N(z)}{D(z)}A(z)
\]

is checked by exact polynomial cross multiplication. These quotients are valid in the Laurent series field \(\mathbb Q((z))\). **Not every quotient is a causal or computationally useful algorithm**; the cost ranking is a preliminary *structural* heuristic, not a runtime measurement.

For this release's 33 recurrence-supported curated sequences, phases \(m=2,\ldots,8\) produce 1,155 exact polyphase recurrences and rational OGFs, grouped into 72 reduced denominator modules. There are 118 phase order reductions relative to the source supplied recurrence and 817 low-complexity module-hub quotients. These are not 1,155 distinct OEIS sequences, nor 817 newly proved OEIS identities.

## 6. Automatic exact cross-sequence cancellation

Canonicalizing admitted expressions into \(\sum_\lambda P_\lambda(n)\lambda^n\), with mathematical offset alignment, enables unconditional coefficient comparisons **inside the curated expression algebra**.

The miner recovers 58 all-index identities across 21 source expressions: 7 shifted differences, 5 pointwise products, and 46 small signed integer combinations. Examples:

\[
 n^2=2\binom{n+1}{2}-n,
\]

\[
 \sum_{j=0}^{n}j^2=2\binom{n+2}{3}-\binom{n+1}{2},
\]

\[
 (2^n)(2^n)=4^n.
\]

Those 21 source expressions span a **9-dimensional rational vector space** in the finite exponential-polynomial basis. The nine selected generator records and all 21 exact projections are in `EXACT_BASIS.json`. This basis optimizes symbolic reuse, not necessarily runtime.

Crucial adversarial control: the polynomial \(\prod_{j=0}^{9}(n-j)\) agrees with zero on ten indices but is rejected as a symbolic identity, because the canonical coefficient vectors differ.

## 7. Dyadic and odd-prime lifts

For \(m=p^\ell\), a base-\(p\) digit \(d_\ell\) refines the residue and the packet state by

\[
 (m,r,T^m,w)\longmapsto
 (mp,r+md_\ell,(T^m)^p,(T^m)^{d_\ell}w).
\]

The equality holds over integers first. Reduction modulo \(p^h\) is then an exact ring homomorphism. The included Fibonacci dyadic and Pell odd-adic files provide numerical witnesses, not claims of new valuation laws or resolved conjectures.

## 8. Measured benchmark

`PACKET_BENCHMARK.json` records a specific 33-sequence workload at local index \(n=12{,}000\), median of three runs, Python 3.13.5 on Linux:

- Independent iterative evaluation: **0.359256 s**.
- Shared quotient-ring packet evaluation: **0.003705 s**.
- Observed ratio: **96.96×**. All exact integer outputs agreed.

This comparison is against straightforward recurrence stepping, not against every known specialized fast-doubling or asymptotically optimized algorithm. It includes Python-specific overhead and says nothing about arbitrary sequences outside the admitted C-finite class.

## 9. Full-corpus preparation

`sequence_formula_retrieval.py` indexes every untrusted OEIS formula/program text using incremental SQLite FTS5, preserving a content fingerprint, OEIS source link and CC BY-SA attribution. This is the mass ingestion route once the official `.seq` archive is made available; no text is executed. Its synthetic 10,000-entry test checks import, retrieval, stale source removal and lexical cross-reference handling. **Synthetic tests are not counted as imported OEIS sequences.**

The optional `.github/workflows/oeis-full-corpus.yml` describes a manually initiated end-to-end OEIS checkout, raw formula import, FTS index and provenance report. It is not evidence that a 400,000-plus entry corpus has already been imported.

## Reproduction

From this package root:

```sh
python -B -m unittest discover -s tools -p 'test_*.py' -q
python -B tools/sequence_recurrence_packets.py --db oeis-formulas.sqlite3 compile --max-modulus 8
python -B tools/sequence_packet_atlas.py --db oeis-formulas.sqlite3 --formulas research/oeis-formulas/phase-formulas.jsonl --index research/oeis-formulas/packet-atlas-index.json
python -B tools/sequence_linear_identity_compiler.py --db oeis-formulas.sqlite3 --export research/oeis-formulas/exact-linear-identities.jsonl --basis-export research/oeis-formulas/EXACT_BASIS.json
python -B tools/sequence_formula_retrieval.py --db oeis-formulas.sqlite3 index
python -B tools/sequence_padic_lifts.py --db oeis-formulas.sqlite3 --id A000045 --prime 2 --digits 1,0,1,1 --precision 4
python -B tools/benchmark_sequence_packets.py --db oeis-formulas.sqlite3 --n 12000 --repeat 3
```
