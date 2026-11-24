# OEIS real-corpus transfer audit: first 24,999 source records

**Author: Komorebi P.** · **Date: 22 November 2026**

## Provenance and scope

Official OEIS source snapshot: `oeis/oeisdata` Git commit
`12ede576d2f5b5c96c54d315a558be3ac56ee474`.
Source: <https://github.com/oeis/oeisdata>.
OEIS Foundation Inc. data attribution and license: <https://oeis.org/LICENSE>, CC BY-SA 4.0.

The reproducible GitHub Actions run is
<https://github.com/KomorebiP/The-Komorebi-Program/actions/runs/45083211787>.
It completed successfully and produced a zipped SQLite database and provenance receipts.
The sequence selection covers up to 25,000 entries from the first 25 shards,
not the whole OEIS (24,999 entries were present in the imported range).

Records imported: 24,999. Raw formula lines: 53,490. Unexecuted program blocks:
39,936. Formula/program entries retained: 96,318. OEIS cross references in the
normalized table: 81,262. Sequence entries with indexable ten-term prefixes:
20,993. Exact finite-checked normalized formula entries: 2,145.

A further exact-integer transfer-mining pass scanned all 24,999 records and
recorded 5,349 non-self finite matching edges across 3,737 OEIS IDs. Of these,
3,627 had at least ten *additional* agreeing terms after the ten-term discovery
signature, and 2,524 had at least twenty. There are 970 undirected connected
components, the largest containing 954 IDs. **This is a candidate graph, not
an equivalence or proof graph.** Even agreement on all published terms is not
proof for all indices.

All offsets are recorded explicitly, and each candidate carries the exact
local-versus-mathematical index relation, source and target term hashes,
transformation parameters, and total compared terms. `shift` and `polyphase`
refer to local coefficient positions; statements display the mathematical
offsets. Numeric signatures with many repeated/zero entries are pruned.

## Five selected all-index mathematical proofs

These are classical identities recovered as finite matches by the miner, then
separately proved from the *mathematical definitions*. They are not claims of
new mathematical discoveries or newly verified OEIS submissions. The data
source's term excerpts only validate the OEIS-to-definition identification
over the available window, except where the source itself provides the
stated definition/recurrence.

### 1. Catalan to Riordan (A000108 → A005043), inverse binomial transform

Let \(C_n=\binom{2n}{n}/(n+1)\). Its ordinary generating function obeys
\[
 C(x)=\frac{1-\sqrt{1-4x}}{2x}=1+xC(x)^2.
\]
For a sequence \(a_n\) with ordinary generating function \(A(x)\), the inverse
binomial transform \(b_n=\sum_{k=0}^n(-1)^{n-k}\binom nk a_k\) has generating function
\[
 B(x)=\frac{1}{1+x}A\left(\frac{x}{1+x}\right),
\]
by exchanging the (finite, coefficientwise) sums, or by inverting the standard
binomial transform \(\frac1{1-x}A(\frac{x}{1-x})\).
Thus the Catalan inverse has
\[
 R(x)=\frac{1-\sqrt{(1-3x)/(1+x)}}{2x}.
\]
Set \(S(x)=1-2xR(x)\). We have
\(S(x)^2=(1-3x)/(1+x)\), so formal differentiation gives
\[
 (1-2x-3x^2)S'(x)+2S(x)=0.
\]
Substituting \(S=1-2xR\) gives
\[
 \boxed{x(1-2x-3x^2)R'(x)+(1-3x^2)R(x)=1.}
\]
Comparing coefficients, \(r_0=1\), \(r_1=0\), and for \(n\ge2\)
\[
 \boxed{(n+1)r_n=(n-1)(2r_{n-1}+3r_{n-2}).}
\]
This is precisely the Riordan recurrence recorded in OEIS A005043, with the
same initial values. The recurrence uniquely determines the formal power
series, proving the transfer for every \(n\ge0\).

### 2. Prime indicator to prime counting (A010051 → A000720)

Let \(q_n=1\) if \(n\) is prime and \(0\) otherwise, \(n\ge1\). By definition,
\[\boxed{\pi(n)=\sum_{k=1}^n q_k},\qquad n\ge1.\]
The first local output value (OEIS A000720 at mathematical index 1) is zero.
This is a proven prefix-sum link by the definitions of the two functions.

### 3. Triangular differences (A000217 → A000027)

For \(T_n=n(n+1)/2\), \(n\ge0\),
\[
 \boxed{T_{n+1}-T_n=n+1}.
\]
OEIS A000027 starts at mathematical index 1 and has term \(n+1\) in local
position \(n\), so the shift in the candidate is essential.

### 4. Square differences (A000290 → A005408)

For \(q_n=n^2\), \(n\ge0\),
\[
 \boxed{q_{n+1}-q_n=2n+1}.\]
Both source and target records start at index zero, with target odd integers.

### 5. Fibonacci even-index packet (A000045 → A001906)

Let \(F_0=0\), \(F_1=1\) and \(F_{n+2}=F_{n+1}+F_n\). For \(G_n=F_{2n}\), the
characteristic roots are the squares of the Fibonacci roots, which sum to
3 and multiply to 1. Therefore
\[
 \boxed{G_{n+2}=3G_{n+1}-G_n},\quad G_0=0,\ G_1=1.
\]
These are the defining recurrence and initial conditions for A001906.
Hence \(A001906(n)=F_{2n}\) for all \(n\ge0\).

## Proof-promotion policy

1. `finite_candidate`: exact equality over the recorded prefix and holdout,
   not a theorem. This includes all 5,349 mined edges before independent proof.
2. `proved_from_definitions`: an all-index mathematical derivation based on
   source/target defining formulas or recurrences, with exact index conventions.
   The five results above meet this standard.
3. `machine_formalized`: optional future Lean-checkable proof artifact; **none
   of the five results are claimed to be Lean-verified here**.
4. `performance_certified`: executable comparison with a specified arithmetic
   cost model or measured workload; exact transfer alone does not imply speedup.

A single sequence may have several different representations. Different OEIS
entries can also be shifts, aliases, and parameter specializations. Therefore
neither the edge count nor the connected-component count measures the number
of independent mathematical discoveries.

## Reproduce

Extract the GitHub Actions ZIP containing `oeis-full.sqlite3`, then run

```
python -B tools/sequence_transfer_index.py --db oeis-full.sqlite3 mine --no-rebuild
python -B tools/render_oeis_real_transfer_atlas.py --db oeis-full.sqlite3 \
  --output real-oeis-transfer-atlas.html --jsonl real-transfer-candidates.jsonl \
  --summary real-transfer-summary.json
python -B -m unittest discover -s tools -p 'test_real_oeis_transfer_atlas.py' -q
```

The official OEIS corpus is not committed to the Komorebi GitHub repository.
The compressed database and provenance are retained as a GitHub Actions
artifact and as separately linked downloadable files. This is a bounded
snapshot, not a self-updating all-OEIS mirror.
