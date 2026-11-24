# Komorebi OEIS Transfer Compiler v0.8 — all-index formula certificates and common basis

**Author: Komorebi P.**  
**Date:** 22 November 2026  
**OEIS attribution:** The Online Encyclopedia of Integer Sequences, OEIS Foundation Inc. Data and adaptations: CC BY-SA 4.0 (<https://oeis.org/LICENSE>).  
**Source dataset:** OEIS `oeisdata`, commit `12ede576d2f5b5c96c54d315a558be3ac56ee474`, first 24,999 records, initially imported by the Komorebi GitHub Actions trial. The 172 MB source-backed SQLite artifact is retained separately from the public code repository.

## Motivation

The system is intended to compile a *network of usable formulas and exact transfers*, not simply list OEIS IDs. It distinguishes (1) source text, (2) executable extracted expressions, (3) finite numerical corroboration, (4) exact identities between formula definitions, (5) an independent OEIS all-index identification, and (6) measured computational advantage. No automated finite match promotes directly to (4) or (5).

## Real-corpus results

| Category | Count | Mathematical status |
|---|---:|---|
| Official OEIS entries loaded | 24,999 | Original source snapshot, not full OEIS |
| Stored raw formula lines | 53,490 | Attribution preserved; not executed |
| Stored program blocks | 39,936 | Source code text; not executed |
| Finite-checked normalized formulas | 2,145 | Checked against stored exact coefficients |
| Structurally C-finite formulas | 1,827 | Exact recurrence consequences of restricted DSL |
| Distinct C-finite formula IDs | 1,753 | Formula algebra, not universal OEIS IDs |
| Earlier finite-match transfer candidates | 5,349 | Candidates only |
| **All-index formula transfer certificates** | **2,165** | Recurrence annihilator proof conditional on both formulas |
| Independent certificate replay passed | **2,165** | Hashes, operators, full recurrence witness, source checks |
| Symbolic exponential-polynomial formula sequences | 1,752 | Canonical exact basis in Q |
| **Exact symbolic transfer links** | **5,167** | Entire formal expressions match exactly |
| Of which absent from previous prefix miner | **3,002** | Discovered without prefix matching |
| Rational linear basis rank | **109** | All 1,752 formula-defined sequences expand exactly |
| Formula-to-basis reconstructions | 1,752 | Exact Q-coordinate equality and functional controls |
| Local regression tests | 105 | Includes 12 new adversarial/structural tests |

The 2,165 recurrence certificates are independently included among the 5,167 symbolic identities. **Do not add these counts as if they were disjoint identities.** The 109 basis rank describes the span of the 1,752 admitted formulas, not all 24,999 sequences or the full OEIS.

## Recurrence annihilator theorem

Write a sequence as a function of the local index \(n\ge0\), with its OEIS mathematical offset stored separately. Let \(S a(n)=a(n+1)\). Suppose the two formula expressions \(b_n\) and \(c_n\) admit monic annihilators

\[
P(S)b=0,\qquad Q(S)c=0,\qquad\deg P=p,\quad\deg Q=q.
\]

Because polynomial shift operators commute, \(P(S)Q(S)\) annihilates each sequence, hence the difference. If the first \(p+q\) values of \(b-c\) are zero, the monic recurrence of order \(p+q\) forces the difference to vanish at every subsequent index. Thus:

\[
\boxed{[\forall\,0\le n<p+q,\ b_n=c_n]\ \Longrightarrow\ [\forall\,n\ge0,\ b_n=c_n].}
\]

The compiler **does not fit \(P\) or \(Q\) from these values**. It obtains recurrences from an independently restricted expression grammar and from exact algebraic operator rules:

- Shift and difference: \(P(S)S^r a=0\), \(P(S)(S-1)a=0\).
- Constant addition or prefix sum: \((S-1)P(S)\) annihilates the result.
- Binomial transform: \(P(S-1)\); inverse: \(P(S+1)\), by exponential generating-function conjugation.
- Polyphase \(a_{mn+r}\): characteristic polynomial of the quotient-ring shift operator \(S^m\), by Cayley–Hamilton.

Every certificate records source/target formula IDs, SHA-256 receipts for source entries and expressions, OEIS offsets, recurrence coefficients, exact initial-state witness length, and additional executable checks. Rebuilding the ledger never alters finite-candidate statuses.

## Canonical symbolic theorem

The accepted grammar also maps to finite exponential polynomials:

\[
a_n=\sum_{\lambda\in\Lambda}P_\lambda(n)\lambda^n, \quad\lambda\in\mathbb Z\setminus\{0\},\ P_\lambda\in\mathbb Q[n].
\]

Polyphase extraction sends \(P(n)\lambda^n\) to \(\lambda^rP(mn+r)(\lambda^m)^n\). The binomial transform acts on falling factorial terms by

\[
\sum_{k=0}^{n}\binom nk k^{\underline{j}}\lambda^k
=n^{\underline{j}}\lambda^j(1+\lambda)^{n-j}.
\]

For \(\lambda\neq-1\), the right side is again an exponential polynomial. The inverse uses \(\lambda-1\), and singular cases are deliberately declined because the result may have finite support. Prefix sums are computed by exact discrete antidifferentiation, including the \(\lambda=1\) polynomial case. No numerical interpolation is used to discover an edge: a hash hit requires exact equality of *all* rational coefficients in the canonical forms.

Among 1,752 supported formula sequences, 112 formal basis coordinates \(n^j\lambda^n\) appear. Sparse rational Gaussian elimination finds **rank 109** for the exact span of the admitted sequence functions. Each sequence is represented by a rational linear combination of 109 selected source formulas; the coefficients and source hashes are exported in `exact-sequence-basis-projections.jsonl`.

## Examples recovered from the real OEIS text

- A000079 to A000244, ordinary binomial transform: \(\sum_{k=0}^n\binom nk2^k=3^n\).
- A000244 to A000302: \(\sum_{k=0}^n\binom nk3^k=4^n\).
- A000290 to A005408, adjacent difference: \((n+1)^2-n^2=2n+1\).
- A000290 to A000330, prefix sum: \(\sum_{k=0}^n k^2=n(n+1)(2n+1)/6\).
- A000079 to A001018, polyphase: \(2^{3n}=8^n\).
- A000051 to A007689, binomial transform: \(\sum_{k=0}^{n}\binom nk(2^k+1)=3^n+2^n\).

These formulas are classical. Their value here is the independently generated, machine-replayable transfer mechanism, not novelty of the individual identities.

## Costs are measured separately

`exact-transfer-benchmark-v08.json` contains Python 3.13.5 exact-integer medians over five repetitions at \(n=3000\). For A000051 → A007689, direct binomial summation took roughly 0.313 s and recurrence evaluation roughly 0.000198 s (observed ratio about 1,582×), with equal 4,755-bit outputs. For A000290 → A000330, direct Python summation and recurrence evaluation were about 0.0000966 s and 0.0000844 s (about 1.14×). The second result shows why an exact transfer does not imply a useful speedup. In some cases the target's original closed form is faster than either algorithm. All timings depend on hardware, implementation, and workload.

## Proof boundary and next work

This release proves formulas **conditionally on the mathematical definitions extracted from OEIS text**. Independently proving each extracted expression equals its actual OEIS sequence at all indexes is still outstanding except where the original sequence definition and its proof are supplied. None of the exported proofs claim Lean formalization, new mathematical identities, or global OEIS coverage.

The next expansion is source coverage (staged first 100,000 entries), efficient verified treatment of general hypergeometric/factorial ratios, algebraic and D-finite generating functions, and route optimization against an explicit arithmetic cost model. Euler zigzag, Bell, partitions, and broad prime-indexed families need other representations and operators beyond this C-finite component.

## Reproduction

From this package, with the supplied 24,999-source SQLite dataset:

```bash
python -B tools/sequence_oeis_proof_promotion.py --db oeis-real-24999.sqlite3 --export certified-real-transfer-formulas.jsonl --summary proof-promotion-summary.json
python -B tools/sequence_oeis_proof_promotion.py --db oeis-real-24999.sqlite3 --export certified-real-transfer-formulas.jsonl --replay-only
python -B tools/sequence_oeis_symbolic_network.py --db oeis-real-24999.sqlite3 --export symbolic-network.jsonl --summary symbolic-network-summary.json
python -B tools/sequence_oeis_basis.py --db oeis-real-24999.sqlite3 --output exact-sequence-basis-projections.jsonl --basis-output exact-sequence-basis.json
python -B -m unittest discover -s tools -p 'test_*.py' -q
```

All exact proof results require the same source record receipts. Do not reuse a certificate after source content, formula extraction, or index conventions have changed; rebuild and replay instead.
