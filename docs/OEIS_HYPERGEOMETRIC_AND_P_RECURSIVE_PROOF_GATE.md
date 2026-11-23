# OEIS conditional P-recursive and Pochhammer certificate layer

**Author: Komorebi P.**
**Checkpoint: 23 November 2026.**
**Scope:** exact first-order hypergeometric/Pochhammer and orders 2–4 P-recursive transfer implications.
**Status:** tested locally on faithful *excerpts* and explicitly synthetic controls, not a full official OEIS source replay or an independent OEIS identification proof.

## What the added engines certify

### First-order polynomial-coefficient recurrences

The new `tools/oeis_hypergeometric_gate.py` parses a restricted OEIS `%F` statement of the form

\[
  a(n+1)=r(n)a(n),\qquad r(n)=\frac{P(n)}{Q(n)}\in\mathbb Q(n),\quad n\ge b.
\]

The code extracts rational-polynomial coefficients with a bounded abstract syntax tree and **does not execute** OEIS text. It preserves the OEIS `%O` offset and the stated recurrence lower bound. It records the first source term at index `b` as a **source premise**, never as a proof from finite data. If that term and the recurrence are true, they uniquely determine the entire tail. Finite source terms are checked to detect contradictions.

Every denominator `Q(n)` must have an exact nonvanishing certificate on the whole half-line `n>=b`. The current sufficient guard writes `Q(t+b)` in the monomial basis and requires strictly positive constant and nonnegative remaining coefficients, or the corresponding strictly negative condition. This deliberately rejects some valid nonvanishing polynomials. When a recurrence fails the source prefix check, its whole sequence record is quarantined.

If `P/Q` factors completely into bounded rational linear factors, the engine proves the normal form

\[
  a(b+k)=a(b)c^k\frac{\prod_i (\alpha_i)_k}{\prod_j(\beta_j)_k},\qquad k\ge0,
\]

by factoring the rational consecutive-term ratio and proving its exact reconstruction in `Q(n)`. The denominator guard ensures each rising factorial in the denominator stays nonzero on the tail. If a rational factorization is outside the supported budget, no normal form is claimed.

For a candidate transfer `B(n)=g(n)A(n)`, the engine first **guesses** a low-degree rational `g` by exact finite interpolation. It then **proves**

\[
  g(n+1)r_A(n)=r_B(n)g(n),\quad B(b)=g(b)A(b),
\]

in the rational function field, checks `g`'s denominator on `n>=b`, and emits a source-bound conditional certificate. Finite interpolation itself is never used as proof.

### Higher-order polynomial-coefficient recurrences

The new `tools/oeis_precursive_gate.py` handles strict forward recurrences of orders `2`, `3` and `4`:

\[
  A(n+d)=\sum_{j=0}^{d-1}c_j(n)A(n+j),\qquad c_j\in\mathbb Q(n),\quad n\ge b.
\]

A complete seed vector `A(b),...,A(b+d-1)` and uniform denominator guards are required. For two sequences with the same order, the program proves the rational-gauge transfer `B(n)=g(n)A(n)` when, for every `j`,

\[
   d_j(n)g(n+j)=g(n+d)c_j(n),
\]

and all `d` initial values agree. This is an elementary gauge-conjugacy (Ore-style) certificate proved by recurrence induction. It is **not** a general Ore-algebra elimination, creative telescoping, or D-finite decision procedure. No invertibility is inferred from an undirected transfer graph.

### Existing OGF and identification layer

The original `tools/oeis_identification_proofs.py` now establishes explicit `%N` polynomial and named-linear-recurrence definitions from their *full formal rational generating functions*, including a name recurrence with all required seeds. Conflicting parseable `%N` and `%F` definitions are quarantined rather than demoted to unverified. Explicit nonzero-offset polynomial formulas are evaluated at their actual OEIS indices; an OGF whose coefficient-index convention is ambiguous is not shifted silently.

## Verified local cases

The faithful OEIS excerpts contain these **actual source formula lines** (the abbreviated `.seq` files are *not* byte-for-byte copies of the complete OEIS entries):

- `A000142`: `a(n)=n*a(n-1), n>=1` from OEIS `oeisdata` Git blob `16352064f74498374f3f253ad0e617dd2561bd99`.
- `A000984`: `a(n)=a(n-1)*(4-2/n)` from blob `afe58b4a1cf2f8b14ac41a22cbd6b9178c65afdf`.
- `A000108`: `a(n)=2*(2*n-1)*a(n-1)/(n+1)` from blob `de23ba4b88d265e350f0ee0ec653d52e9d17109a`.

Their corresponding **conditional** Pochhammer certificates are

\[
  n!=(1)_n,\qquad\binom{2n}{n}=4^n\frac{(1/2)_n}{(1)_n},\qquad
  C_n=4^n\frac{(1/2)_n}{(2)_n}.
\]

The exact rational-gauge certificate gives `C_n = binomial(2n,n)/(n+1)`, under both source statements and the initial terms. `A987110...` and `A987200...` are **synthetic test identifiers**, not asserted OEIS entries. The order-two demonstration is a designed positive control rather than a previously unknown OEIS transfer.

The three audit collections generate five first-order Pochhammer normal forms, eight first-order directed gauge certificates, and six order-two directed gauge certificates from the source-excerpt/synthetic fixture pools. These counts are for **local fixtures only**, not official OEIS corpus coverage. All 58 local Python unit tests passed at the checkpoint, including source hash replay and adversarial controls.

## Exact reproduction

```bash
python -B -m unittest discover -s tools -p 'test_oeis_*.py' -v
python -B tools/oeis_identification_proofs.py \
  --oeis-root fixtures/oeis_identification --output verification/oeis/identification
python -B tools/oeis_hypergeometric_gate.py \
  --oeis-root fixtures/oeis_hypergeom --output verification/oeis/hypergeom
python -B tools/oeis_precursive_gate.py \
  --oeis-root fixtures/oeis_precursive --output verification/oeis/precursive
```

For each proof engine, the *same* command with `--verify-report` will replay all parsed records and certificates. If generation used `--ids`, supply the **same explicit `--ids`** when verifying. Do not infer the verification selection from the report itself, as a truncated report could otherwise verify itself. The official OEIS source revision must be pinned to a git commit separately from the content hashes recorded in each receipt.

To run a bounded official source check after cloning `oeis/oeisdata`:

```bash
python -B tools/oeis_hypergeometric_gate.py \
  --oeis-root /path/to/oeisdata --ids A000108,A000142,A000984 \
  --output verification/oeis/official-hypergeom
python -B tools/oeis_hypergeometric_gate.py \
  --oeis-root /path/to/oeisdata --ids A000108,A000142,A000984 \
  --output verification/oeis/official-hypergeom --verify-report
```

The optional CI workflow stores receipts as artifacts. **Nothing is promoted into the existing static transfer graph without explicit review.** The release does not assert that full official OEIS ingestion, browser deployment, Lean certification or performance optimization has been completed.

## Remaining automation boundaries

A full corpus run needs a scalable candidate pairing scheduler rather than enumerating all pairs (the current bounded matcher raises when `max-pairs` is exceeded). Additional work: general P-recursive recurrence index conversions, complete denominator root isolation, rational gauge degrees above two, first-order recurrences with implicit multiplication, multidimensional/p-adic operators, differential-operator extraction from D-finite OGFs, creative telescoping, Lean proof replay, and precision-aware directed cost routing. OEIS `%F` text is untrusted input, so unsupported syntaxes and source ambiguities are reported, never auto-executed.

**Attribution:** OEIS Foundation, Inc., *Online Encyclopedia of Integer Sequences*, CC BY-SA 4.0, <https://oeis.org/> and <https://github.com/oeis/oeisdata>. The original files remain the authoritative source; the small excerpts in this package are for tests only.
