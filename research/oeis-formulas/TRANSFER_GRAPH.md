# Komorebi Sequence Transfer Graph: first research checkpoint

**Author: Komorebi P.**

## Objective and stage

The destination is a wide-coverage, *representation-first* graph of OEIS and Komorebi sequences. Collect every source formula, generating function, recurrence, program reference, normalization, and source-level cross-reference before prioritizing expensive mathematical audits. Do not discard formula text just because it is not yet executable or proved. Each object retains its origin, mathematical offset, and verification status.

A sequence is a node. A formula is a separate node. A transformation or reusable operator schema is another node. Each explicit edge records: expression, direction, operation, provenance, strength of evidence, exact comparison count where applicable, and actual or unmeasured cost. No finite-prefix agreement is promoted to infinite equality. An OEIS `%Y` line becomes a `reference_only` edge until classified and justified.

Current working specimen: **56 sequence nodes, 61 formula nodes, 10 operator-scheme nodes, 70 links, of which 9 are algebraic transformation examples and 61 are formula-to-sequence representation links.** This is not the full OEIS nor an exhaustive graph of the 56 sequences.

## A universal Fibonacci transfer

Define Fibonacci numbers by F(0)=0, F(1)=1, F(k+2)=F(k+1)+F(k). The classical generating function identity is

    sum_{k>=0} F(k+1) z^k = 1/(1-z-z^2).

For formal power series D(x), N(x) in Q[[x]] with D(0)=1, set

    phi_D(x) = (sqrt(5-4*D(x))-1)/2

where the square root is the unique formal series with constant term 1. It follows directly that

    1-phi_D(x)-phi_D(x)^2 = D(x),

and hence

    N(x)/D(x) = N(x)*sum_{k>=0}F(k+1)*phi_D(x)^k.

Since phi_D(0)=0, coefficient [x^n] depends only on finitely many k <= n. This is an **exact formal identity**, not a numeric approximation, and is not claimed to be historically novel or inherently computationally cheaper.

For the Euler zigzag numbers (OEIS A000111), E(x)=sec(x)+tan(x)=(1+sin(x))/cos(x). Substitute D(x)=cos(x), N(x)=1+sin(x). Because phi_D(x) starts with x^2/2, the coefficient is

    E_n = n![x^n](1+sin(x))*sum_{k=0}^{floor(n/2)}
             F(k+1)*((sqrt(5-4*cos(x))-1)/2)^k.

This uses Fibonacci numbers and elementary formal power series but no Euler-number inputs. The repository exact-arithmetic test matches A000111 through n=17 and independently verifies the general relation against the conventional quotient recurrence for several nontrivial numerator and denominator series. The algebraic derivation establishes the identity for all n over Q.

## Stored example transformations

- `A000045 -> A000032`: Lucas(n)=2*Fibonacci(n+1)-Fibonacci(n).
- `A000984 -> A000108`: Catalan(n)=central_binomial(n)/(n+1).
- `A000079 -> A000302`: 4^n = (2^k) evaluated at k=2n.
- `A000079 -> A000225`: Mersenne(n)=2^n-1.
- `A000217 -> A000124`: central polygonal numbers = triangular numbers+1.
- `A000290 -> A000330`: square pyramidal numbers = prefix sums of squares.
- `A000111 -> A000364`: secant numbers are the even Euler zigzag indices.
- `A000040 -> A001223`: prime gaps are differences of neighboring primes.
- `A000045 -> A000111`: Fibonacci resolvent composition through cos and sin.

A Bell-to-sets-of-lists EGF composition schema is defined when both OEIS records are available, but it is deliberately **not** counted as a materialized graph edge in the current 56-sequence snapshot.

## Operator libraries, expansion policy, and accounting

Store infinite operator families once, with parameters, rather than materializing every instance. The initial ten include ordinary/EGF products, EGF composition, binomial transforms, finite differences, polyphase, parity splits, roots-of-unity residue projectors, quotient solvers, and the Fibonacci universal resolvent.

In the next collection phase:

1. Import all official `.seq` records into the existing SQLite tables. Preserve `%F` formulas and `%p/%t/%o` program fields without executing them; preserve names, terms, offsets and record hashes.
2. Ingest all OEIS `%Y` cross-references as candidate edges with source citation, not verified identities. Reimporting one record replaces that record's previously staged `%Y` edges. The graph rebuild reconstructs them.
3. Ingest the complete Komorebi `assets/sequence-library-data.json` export through the existing `ingest-komorebi` command, connecting independently checked local terms and cited source claims without treating finite matches as identity proofs.
4. Normalize syntax, classify operators and automatically detect candidate transfer families. Delay expensive theorem proving and performance benchmarking until these source and candidate layers are broad.
5. Search shortest *structural* routes, simplify composition into a canonical operator expression, remove cycles and equivalent representations, then benchmark and certify paths. Structural shortest-path length is **not** a measured computation-cost minimum.

The initial graph's counts are intentionally small. Its value is the explicit source/evidence model and an expandable operator schema, not a claim of comprehensive coverage.

## Reproduce

From the repository root, after seeding the existing database:

```sh
python tools/sequence_transfer_graph.py --db oeis.sqlite3 build --export transfer-graph.jsonl
python tools/sequence_transfer_graph.py --db oeis.sqlite3 path --from-id A000045 --to-id A000364
python tools/sequence_transfer_graph.py --db oeis.sqlite3 xrefs --seq-root /path/to/oeisdata/seq
python -m unittest discover -s tools -p 'test_sequence_transfer_graph.py' -v
```

For the full OEIS upstream source, see https://github.com/oeis/oeisdata. OEIS data: The Online Encyclopedia of Integer Sequences, OEIS Foundation Inc., CC BY-SA 4.0 (https://oeis.org/LICENSE). Komorebi source code follows this repository's code license.
