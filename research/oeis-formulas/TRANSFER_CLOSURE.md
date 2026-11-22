# Komorebi Sequence Transfer Compiler — v0.7

**Author: Komorebi P.**  
**Source data:** The Online Encyclopedia of Integer Sequences (OEIS Foundation Inc.), CC BY-SA 4.0.  
**Scope:** Exact all-index transfer theorems for the supplied curated recurrence definitions. Identity of those definitions with OEIS sequence records is supported by exact finite term comparisons, not independently proved for all indices.

## 1. Transfer operators

Write \(S a_n=a_{n+1}\) and suppose \(P(S)a=0\), where
\[
P(X)=X^d-c_1X^{d-1}-\cdots-c_d,
\qquad a_0,\ldots,a_{d-1}\in\mathbb Z.
\]

### Binomial and inverse binomial

For \(\mathcal B_\epsilon a(n)=\sum_{k=0}^n\binom nk\epsilon^{n-k}a_k\), with \(\epsilon=1\) or \(-1\), the exponential generating functions satisfy
\[
\widehat{\mathcal B_\epsilon a}(z)=e^{\epsilon z}\widehat a(z).
\]
Consequently,
\[
P(S-\epsilon)\mathcal B_\epsilon a=0.
\]
The code constructs \(P(X-\epsilon)\) by exact integer polynomial translation and computes its first \(d\) values by a finite exact binomial sum. These uniquely determine the transformed sequence, for all indices. The resulting recurrence is evaluated with the quotient-ring binary-exponentiation packet.

Exact illustrative identities, for the stated classical recurrence definitions:
\[
\mathcal B[F]_n=F_{2n},\qquad
\mathcal B[L]_n=L_{2n},\qquad
\mathcal B[2^n]=3^n,
\qquad \mathcal B[3^n]=4^n.
\]

### Cauchy convolution

For rational OGFs \(A(z)=N_A(z)/D_A(z)\), \(B(z)=N_B(z)/D_B(z)\),
\[
\sum_{n\ge0}\left(\sum_{k=0}^n a_kb_{n-k}\right)z^n
=\frac{N_A(z)N_B(z)}{D_A(z)D_B(z)}.
\]
An exact polynomial gcd cancels common factors, after which the reduced rational OGF supplies the recurrence. If a numerator polynomial remains (finite-support sequences), the recurrence includes sufficient zero roots to cover its degree.

For the Fibonacci self-convolution \(c_n=\sum_{k=0}^n F_kF_{n-k}\):
\[
C(z)=\frac{z^2}{(1-z-z^2)^2},\qquad
c_n=2c_{n-1}+c_{n-2}-2c_{n-3}-c_{n-4}\quad(n\ge4).
\]

### Hadamard (termwise) product

Represent two C-finite sequences as \(a_n=u^T T_a^n v\), \(b_n=s^T T_b^n w\). Then
\[
a_nb_n=(u\otimes s)^T(T_a\otimes T_b)^n(v\otimes w).
\]
The code computes a scalar minimal recurrence of order at most \(d_a d_b\) and verifies its residual for a complete \(d_a d_b\)-dimensional observability window. The tensor state's Cayley–Hamilton equation proves the residual vanishes for all subsequent indices.

For Fibonacci squares \(s_n=F_n^2\):
\[
s_0,s_1,s_2=0,1,1,\qquad s_n=2s_{n-1}+2s_{n-2}-s_{n-3}\quad(n\ge3).
\]

## 2. General sparse-power/multinomial transfer

Let \(R=\mathbb Z[X]/(P(X))\) and \(X^m\equiv\sum_{j=0}^{d-1}q_jX^j\pmod{P(X)}\). For every solution \(a\) of \(P(S)a=0\), and all \(n,r\ge0\),
\[
a_{mn+r}=
\sum_{k_0+\cdots+k_{d-1}=n}
\frac{n!}{\prod_jk_j!}\left(\prod_{j=0}^{d-1}q_j^{k_j}\right)
 a_{r+\sum_j jk_j}.
\]
Proof: apply \(S^r (\sum_jq_jS^j)^n=S^{mn+r}\) to the sequence, then use the multinomial theorem. This is not a numerical induction and does not depend on the initial values.

| Family (defining recurrence) | Shift polynomial | Exact sample transfer |
|---|---|---|
| Fibonacci and Lucas: \(P=X^2-X-1\) | \(X^2\equiv X+1\) | \(a_{2n}=\sum_k\binom nk a_k\) |
| Pell: \(P=X^2-2X-1\) | \(X^2\equiv 2X+1\) | \(a_{2n}=\sum_k\binom nk2^ka_k\) |
| Jacobsthal: \(P=X^2-X-2\) | \(X^2\equiv X+2\) | \(a_{2n}=\sum_k\binom nk2^{n-k}a_k\) |
| Padovan: \(P=X^3-X-1\) | \(X^3\equiv X+1\) | \(a_{3n}=\sum_k\binom nk a_k\) |
| Tribonacci: \(P=X^3-X^2-X-1\) | \(X^3\equiv X^2+X+1\) | \(a_{3n}=\sum_{i+j+k=n}\frac{n!}{i!j!k!}a_{j+2k}\) |

Sparse polynomial powers (support at most 3, coefficient magnitude at most 20, moduli 2–12) currently yield **138 exact sequence-family instances**, **107** with support at most two. They are representations of universal quotient-ring identities, not 138 independent discoveries. Their OEIS correspondence remains finitely verified.

## 3. Mining and verification policy

Each mined link has separate fields for (i) the source evaluator and hash, (ii) the all-index operator certificate, (iii) the target recurrence and initial-state certificate, (iv) the finite OEIS comparison, and (v) computational cost if benchmarked. A match with a finite OEIS prefix alone is **never** promoted to an all-index identity.

The closure table records 406 operator certificates on the current 33 exact recurrence definitions: 33 binomial, 33 inverse binomial, 170 Cauchy products and 170 pointwise products. Pairwise coverage is deliberately bounded; 33-squared pairwise closure has not been completed. A raw count of phase matches can be misleading because periodic and zero sequences generate duplicate correspondences; use the individual certificates and nontrivial examples instead.

The exact Fibonacci binomial benchmark at \(n=5{,}000\) gave 0.0382 seconds for a single-pass exact direct sum and 0.000122 seconds for the compiled recurrence (five-run medians, approximately 314-fold in one environment). This is **not** a universal speedup claim and does not include all compilation, setup, or disk I/O costs.

## 4. Raw OEIS ingestion, licensing and limitations

The official [oeis/oeisdata](https://github.com/oeis/oeisdata) source organizes each entry as `seq/A123/A123456.seq`. The importer stages `%N` names, `%O` mathematical offsets, `%S/%T/%U` term excerpts, all `%F` formula lines, `%p/%t/%o` program references, and unverified `%Y` cross-references. Raw external text is **never executed**. A restricted arithmetic parser makes candidates only from fully parsed expressions, then finite-compares them against the same source's recorded terms.

The tree importer traverses shard directories deterministically and commits transactional record batches. The staged GitHub Actions source workflow can be triggered by a feature-branch `push` to test the first 25 OEIS shards without requiring a merge. A manual run with `max_records=0` requires the workflow file to be present on the repository's default branch.

At the v0.7 local build, the **full OEIS source corpus has not been imported**, and only 56 curated OEIS records are present. Do not advertise corpus coverage or global OEIS verification until the external import workflow produces a completed provenance receipt.

## 5. Reproduce

Run from the project root:

```sh
python -B -m unittest discover -s tools -p 'test_*.py' -q
python -B tools/sequence_transfer_closure.py --db oeis-formulas.sqlite3 --export research/oeis-formulas/closure-operators.jsonl --max-pairs 170
python -B tools/sequence_sparse_lifts.py --db oeis-formulas.sqlite3 --export research/oeis-formulas/sparse-lifts.jsonl
python -B tools/benchmark_sequence_transfer_closure.py --n 5000 --repeat 5 --output research/oeis-formulas/BINOMIAL_TRANSFORM_BENCHMARK.json
python -B tools/oeis_bulk_import.py --db DATA.sqlite3 --tree-root /path/to/oeisdata/seq --limit 25000
python -B tools/oeis_formula_discovery.py --db DATA.sqlite3
python -B tools/sequence_formula_retrieval.py --db DATA.sqlite3 index
python -B tools/sequence_transfer_index.py --db DATA.sqlite3 index
```

The official OEIS source and extracts are licensed CC BY-SA 4.0. The research code retains the host repository's own code licensing. Author: Komorebi P.
