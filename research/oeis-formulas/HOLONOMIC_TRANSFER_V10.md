# Komorebi OEIS Transfer Compiler: P-recursive and Hypergeometric Layer (v1.0)

**Author: Komorebi P.**  
**Research date:** 22 November 2026  
**Reference data:** The Online Encyclopedia of Integer Sequences (OEIS Foundation Inc.), https://oeis.org/, CC BY-SA 4.0.  
**Scope:** Exact identities about *admitted mathematical evaluator expressions*. Agreement of these expressions with an OEIS entry over its stored excerpt is **not** a proof that the identity characterizes that OEIS sequence for every index.

## 1. Source and proof tiers

Raw `%F` OEIS lines, offsets, and program listings are preserved as source data. Program listings and source-text equations are not executed. A restricted evaluator AST is assigned `finite_checked` only after exact comparison with source terms at correctly aligned indices. Independently of that finite comparison, the compiler can prove algebraic identities for AST expressions using rational-function polynomial arithmetic. Every stored certificate includes formula ID, AST digest, current OEIS source SHA-256, index start, operator coefficients, and the proof method. The one-file source corpus used here contains 99,999 official OEIS records; no claim is made for the unimported remainder of OEIS.

## 2. P-recursive closure of finite hypergeometric sums

Let `u_i(n+1) = r_i(n) u_i(n)` on a nonzero, nonsingular integer tail, with `r_i(n)` in Q(n). Let `a(n) = sum_(i=1)^k u_i(n)` for `k <= 5`. Define

```
R_(i,0)(n) = 1,
R_(i,j)(n) = product_(h=0)^(j-1) r_i(n+h),
M(n) = (R_(i,j)(n))_(1<=i<=k,0<=j<=k).
```

Over the field Q(n), the `k x (k+1)` matrix has a nontrivial exact rational-function nullvector `c(n)`, hence

```
sum_(j=0)^k c_j(n) R_(i,j)(n) = 0       (every i)
sum_(j=0)^k p_j(n) a(n+j) = 0,
```

where all `p_j` are primitive integer polynomials obtained by clearing denominators, removing a common polynomial factor and multiplying through by a common scalar. This is a symbolic identity on the recorded nonsingular tail, not a recurrence guessed from sequence values. The compiler additionally verifies every available stored OEIS recurrence position after the tail index, so a fabricated later excerpt cannot silently pass an initial-prefix test.

**Example.** For `a(n) = 4^n + binomial(2n,n)`:

```
(8+16n) a(n) - (10+8n) a(n+1) + (n+2) a(n+2) = 0.
```

The two component ratios are `4` and `(4n+2)/(n+1)`, respectively; direct substitution verifies the recurrence for all nonnegative `n`.

## 3. Formal OGF differential equation

For `g_n = a(n0+n)` satisfying `sum_(j=0)^d p_j(n) g_(n+j)=0`, write `G(x)=sum_(n>=0) g_n x^n` and `theta=x d/dx`. In the formal power-series ring Q[[x]]:

```
sum_(j=0)^d x^(d-j) p_j(theta-j)
       (G(x) - sum_(i=0)^(j-1) g_i x^i) = 0.
```

The prefix subtraction is essential to keep the initial conditions correct. No convergence assumption is needed. The OGF certificates are *formal* differential identities for formula-defined sequences.

## 4. Hypergeometric/polyphase factorization

For a hypergeometric term with exact ratio `r(n)` and nonzero tail base, each phase `b_k=a_(n0+mk+r)` obeys

```
b_(k+1)/b_k = product_(h=0)^(m-1) r(n0+mk+r+h).
```

Factor the right-hand side over affine factors to obtain

```
b_k=b_0 lambda^k product_(alpha in U) (alpha)_k
                       /product_(beta in L) (beta)_k.
```

Its OGF is formally a generalized hypergeometric series, with the additional numerator parameter `1` canceling the `k!` coefficient normalization. This is not always an analytically convergent function. The first-order phase ledger contains **15,620** expressions from source moduli 2, 3 and 5.

## 5. P-recursive polyphase lift through rational state matrices

This extension removes the first-order restriction. Let

```
sum_(j=0)^d p_j(n) a_(n+j) = 0,
```

and suppose the leading coefficient `p_d(n)` is proved nonzero for all `n>=T`. A sufficient check used by the implementation is that the coefficients of `p_d(n+T)` all have the same weak sign and its constant term is strictly of that sign. With `v_n=(a_n,...,a_(n+d-1))^T`, let `M(n)` be the rational companion matrix. Then

```
v_(n+1) = M(n) v_n,
T_(m,r)(k) = M(mk+r+m-1) ... M(mk+r),
v_(m(k+1)+r) = T_(m,r)(k) v_(mk+r).
```

Writing `e=(1,0,...,0)`, define `R_0(k)=e`, `R_j(k)=e T(k+j-1)...T(k)`. There are `d+1` rows in a `d`-dimensional vector space over Q(k), so the exact rational nullspace produces integer polynomials `q_j(k)` such that

```
sum_(j=0)^d q_j(k) a_(T+m(k+j)+r) = 0.
```

The source recurrence and all matrix row identities are rebuilt from the currently stored formula hashes. This layer currently supports source order 1--3 and phase moduli 2 and 3, with complexity caps. Unsupported cases remain explicitly unsupported.

**Worked example.** Put `b_n=16^n+binomial(4n,2n)`. The exact derived recurrence is

```
(1248+7424n+10752n²+4096n³)b_n
 -(558+1792n+1728n²+512n³)b_(n+1)
 +(30+83n+66n²+16n³)b_(n+2) = 0.
```

Independent symbolic substitution into each summand checks this *identically* in n. The phase test also checks many exact integer terms, but those are secondary checks.

## 6. Rational gauge transfer and composition

For source formula `a_t` and target formula `b_t`, let their structurally derived ratios be `r_a(t)` and `r_b(t)`. The solver looks for a low-complexity shift coboundary

```
r_b(t)/r_a(t) = c L(t+1)/L(t),
L(t) = product_i (alpha_i t + beta_i)^(e_i).
```

Checking the exact rational-function identity and one nonzero initial ratio at `T` gives the all-index transfer

```
b_t = a_t * (b_T/a_T) * c^(t-T) * L(t)/L(T)   (t>=T).
```

There are **975** independently reconstructed direct gauge transfers. The path compiler now composes pairs of edges, *independently regenerates both input certificates*, validates the shared intermediate formula and source digests, and proves the output gauge directly over Q(t). The current ledger contains **351** two-hop certificates, including the following explicit route:

```
A000108 (Catalan expression)
  -- multiply by (n+1) --> A000984 (central binomial expression)
  -- multiply by (n+1)(2n+1) --> A002544 (binomial-polynomial expression)
```

Therefore, for their admitted formulas,

```
A002544(n) = (n+1)^2 (2n+1) A000108(n).
```

This is a proof of the formula-expression relationship. The independently sourced OEIS identifications remain a separate issue. Gauge path length and factor support are *symbolic* cost proxies, not measured algorithmic runtimes.

## 7. Nonholonomic Euler/Fibonacci bridge

Let `F_(k+1)` denote Fibonacci numbers and `E(x)=sec(x)+tan(x)` the Euler zigzag EGF. Define the formal series

```
u(x) = (sqrt(5-4 cos x)-1)/2,    u(0)=0.
```

Then `1-u-u^2=cos x` and

```
E(x) = (1+sin x) * sum_(k>=0) F_(k+1) u(x)^k.
```

Because `u` has valuation 2 in x, each coefficient extraction requires finitely many k. The formal identity is exact, but this is **not a runtime improvement**: its tested 34-term implementation is slower than a native exact Euler recurrence. `sec(x)+tan(x)` is not D-finite, so the project must retain nonholonomic transfer modes.

## 8. Runtime evidence and limitations

The accompanying `outputs/benchmark-v10.json` records five-run median timings in one environment:

- `C_0..C_2500` from 2,501 independent binomial evaluations versus one iterative rational recurrence: about 168x faster for the recurrence.
- `C_n`, `binomial(2n,n)`, and the OEIS A002544 binomial-polynomial expression through one shared prefix and two gauge transfers: at n=2500, 2.030 s for three independent binomial-based prefixes versus 0.00525 s for shared computation, a 386x measured ratio with 7,503 exact integers checked. See `outputs/benchmark-shared-v10.json`.
- An isolated `C_2500` is cheaper by direct binomial evaluation than generating the entire prefix, while a cached binomial intermediary gives a still cheaper quotient (the cache construction cost is omitted).
- For 34 Euler numbers, the Fibonacci composition is slower than the native recurrence.

These measured costs are workload-specific. No universal speedup is claimed.

### Counts are not automatically additive

The 3,924 primary P-recursive certificates, 229 supplemental P-recursive certificates, 15,620 first-order polyphase formulas, 1,000 higher-order polyphase certificates, 975 direct gauge identities, and 351 composed paths overlap in source sequences and algebraic content. Counting them as different new OEIS sequences would be incorrect. Their value lies in the common reusable operators and source-linked proof receipts.

### Remaining mathematical gaps

1. Whole-OEIS coverage beyond the imported 99,999 source entries.
2. Broader parser support for OEIS sum/product, multivariate, special-function and formal-extraction formulas.
3. Ore-algebra closure for general D-finite generating functions, creative telescoping, and singular-index handling beyond the conservative leader test.
4. Exact analytic and formal-series transfer search for non-D-finite families.
5. Proven infinite identification of extracted expressions with the corresponding source-defined OEIS sequences, where not already mathematically established externally.
6. End-to-end cost-aware graph search with realistic caching, amortization, bit complexity, and path fusion, to avoid promoting mathematically valid but inefficient routes.

**Data provenance:** Original OEIS terms, names, formulas, and cross-references are copyrighted and licensed by the OEIS Foundation Inc. under CC BY-SA 4.0. The native source database is distributed separately from this source extension. Theoretical derivations and new code are attributed to Komorebi P.
