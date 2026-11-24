# OEIS affine-lane recurrence transfer gate

**Author: Komorebi P.**
**Published: 23 November 2026.**
**Scope:** exact conditional algebra over rational functions. No automatic publication of sequence identities, full-corpus coverage, Lean proof, novelty or runtime improvement is claimed.

## General transfer obligation

Let a source state have dimension d and satisfy the monic forward recurrence

    S(i+d) = sum_{j=0}^{d-1} c_j(i) S(i+j).

Let the target have dimension e with coefficients b_k(n). Fix an affine source lane i=m*n+r, m>=1. Define the rational row vectors v_h(n) such that

    S(m*n+r+h) = v_h(n) X(n),
    X(n) = (S(m*n+r), ..., S(m*n+r+d-1))^T.

The first d rows are coordinate vectors. Recursively reduce all later rows using the source recurrence at the actual indexed argument. For a proposed transfer

    T(n)=sum_{j<d} g_j(n) S(m*n+r+j),

its k-th shifted output row is

    W_k(n)=sum_{j<d} g_j(n+k) v_{mk+j}(n).

A sufficient exact certificate is the vanishing rational row

    W_e(n) - sum_{k<e} b_k(n) W_k(n) = 0,

plus equality of the e target initial values on a common admissible tail. It is necessary for a universal intertwiner on arbitrary local source states in this formal recurrence module. It need not be necessary for an identity of one special sequence whose state lies in a proper subspace. Induction proves the identity at every integer in the certified tail, without finite-prefix guessing.

For fixed stride, offset, source order, target order and maximum polynomial degree, the discovery routine substitutes a full polynomial basis for every g_j, clears denominators of the symbolic residual coefficient equations and appends exact initial constraints. Rational row reduction solves the resulting affine linear system. The solver is complete within each supported bounded polynomial ansatz provided the arithmetic budgets do not interrupt it. Rational verification is broader than polynomial discovery. Invertible state maps can generate rational reverse operators automatically, independently replayed against the reversed recurrence equations. This is not a complete solver for arbitrary rational intertwiners.

## Singularities, offsets and source selection

The strict parser supports homogeneous linear equations of orders 1–4, backward or forward integer shifts, and explicit lower bounds. It retains denominators of the original written expression **before cancellation**, including denominators inside nested quotients, and the leading recurrence coefficient. A normalized equation does not justify passing through an original pole. For example, `(n-1)/(n-1)` and a leading factor `n-1` both exclude the index n=1. A safe integer tail is proved by a shifted coefficient sign or Cauchy's root bound with exact finite enumeration of integer roots; a large bound is rejected. Earlier nonsingular reported recurrence instances are checked too. No relation is claimed for an omitted prefix.

Rational ordinary generating functions at offset zero yield monic recurrences by coefficient extraction. A nonzero offset with an unspecified OGF convention is not guessed. The selected `%F` statements and initial values remain external mathematical premises, and other formulas in an entry are not all certified. Unselected records with multiple inequivalent normalized operators require a reviewed premise selector. The hypergeometric and higher-order recurrence parsers also reject original-denominator poles that would disappear under cancellation.

## Exact state recovery and local precision

For equal orders d=e, form the square matrix A(n) from W_0 through W_{d-1}. Its nonzero determinant on an admissible tail, together with an exact checked inverse, supplies rational recovery of the original source state. At stride one an inverse row can become a new directed transfer. At stride greater than one it recovers a state on the corresponding affine lane, not automatically a whole inverse sequence. A missing recovery receipt can mean singularity, incompatible dimensions or an uncompleted arithmetic guard; it does not by itself prove information loss.

At a fixed certified index n and prime p, `local_precision` evaluates A exactly. For a matrix with p-integral rational entries, exact minimum-valuation pivot elimination gives the local Smith exponents e_1,...,e_r. Row and column operations are invertible over Z_p because all clearing multipliers have nonnegative valuation. If the input dimension is d, each nonempty fiber modulo p^k contains exactly

    p^(sum_i min(e_i,k) + (d-r)k)

input states. When r=d, the least output precision guaranteeing recovery of an arbitrary input state modulo p^k is k+max_i(e_i). When r<d no full-state reconstruction is possible even from exact output over Q_p. These are local, arbitrary-input-state statements, not claims of a uniform precision bound for a specific OEIS sequence. Nonintegral matrices are excluded from this modular contract. Pointwise examples and negative controls are recorded in the package.

## Reproducibility and results

The two local plans use 12 synthetic controls and seven selected official excerpts. The latter preserve source attribution, the official revision and original Git blob IDs. `full_source_plan.json` requires the full original file hashes and original formula lines. It cannot be satisfied by the excerpts. Only selected source premises are used even on a full record.

```sh
python -B -m unittest discover -s tools -p 'test_oeis_*.py' -v
for corpus in oeis_shift_operator oeis_shift_official_excerpts; do
  python -B tools/oeis_shift_operator_gate.py --oeis-root fixtures/$corpus --plan fixtures/$corpus/plan.json --output reports/$corpus.json
  python -B tools/oeis_shift_operator_gate.py --oeis-root fixtures/$corpus --plan fixtures/$corpus/plan.json --output reports/$corpus.json --verify-report
done
```

The gap scanner's ranked `review_queues.json` can automatically generate bounded proof plans rather than testing every sequence pair:

```sh
python -B tools/oeis_shift_operator_gate.py --oeis-root /path/to/pinned/oeisdata --queue /path/to/review_queues.json --max-leads 40 --save-plan /tmp/shift-plan.json --output /tmp/shift-receipts.json
```

Missing source files are acquisition gaps, not failed identities. The generated plan and actual source hashes are retained. Cross-component leads receive priority; both directions are tested. Unsupported or ambiguous recurrences are not promoted. To replay, reuse the saved plan with `--plan` and `--verify-report`.

The local official-excerpt audit yields 24 directed conditional certificates (18 stride>1), from 252 lane/pair candidates, using 7 records. The synthetic audit yields 10 certificates, including 2 automatically derived rational inverse directions. These are transfer directions and may represent redundant formulations of known identities, not counts of new theorems. The integrated [recurrence certification workflow](https://github.com/KomorebiP/The-Komorebi-Program/actions/runs/45325359220/job/138213522864) passed all 74 tests and replayed the seven full pinned official source records, independently reproducing 24 conditional directions, including 18 with stride greater than one. These full-record receipts are distinct from the excerpt receipts.

Remaining frontier: algebraic generating functions with explicit formal branch selection, general D-finite closure and creative telescoping, joint/multi-source operator ansatz, uniform singularity and valuation analysis, higher-order and higher-stride budgets, cost/precision-aware path search, independent OEIS identification and formal Lean certificates. No production network or website changes are part of this gate.
