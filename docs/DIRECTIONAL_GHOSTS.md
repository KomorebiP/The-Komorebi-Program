# Directional ghosts, Frobenius obstructions, query fibers, and contractive transfers

**Research status:** Written algebraic proofs supported by finite computational checks. No Lean formalization, independent peer review, or historical novelty assessment has been completed. Here, *new* means new within this research continuation.

[Sequence transfer network](SEQUENCE_TRANSFER_NETWORK.md) · [Sequence Library](https://KomorebiP.github.io/The-Komorebi-Program/sequence-network.html) · [Research sources and reproducibility](../research/directional-ghosts/README.md)

**Author: Komorebi P.**  
**Research checkpoint: 2026-11-23.**  
**Inputs:** `Komorebi_Ambient_Realization_All_Progress_2026-11-23.zip` and `Komorebi_Precision_Aware_Transfer_Bridge_v1_2_2026-11-23.zip`.

**Scope of this note.** The results below extend the earlier one-variable logarithmic-derivative and finite-module reconstruction work to multivariate directional observations, prime-power lattice counts, nonlinear-observation query fibers, and contracting transfer operators. The written proofs and finite tests support the statements under their stated assumptions; they do not establish historical priority, independent source verification, or Lean certification.

## Reader's guide

The central question is how much information about a truncated generating function survives a family of observations. These results distinguish **full reconstruction** of its coefficients from **query reconstruction**, where only a chosen answer must be determined.

| Term | Meaning in this note |
| --- | --- |
| Source \(A\) | A truncated formal series with constant coefficient \(1\). |
| Directional ghost \(\Gamma_i(A)\) | The logarithmic derivative \(\delta_i A/A\) along a specified weighted direction. |
| Precision \(p^k\) | Coefficients are determined modulo the stated prime power. |
| Fiber | All coefficient arrays compatible with the observed signatures. |
| Rescue channel | An independently available supplementary measurement. It cannot be synthesized from the same information already lost. |
| \(\Phi_q\) | A lossless change of series coordinates defined by \(A(\mathbf{x})/A(\mathbf{x}^q)\). |

**Reading route:** Sections 2–3 quantify the remaining source ambiguity. Section 4 asks what is needed for a particular query. Section 5 gives a lossless transformation that may offer more useful coordinates, without creating new information. Section 6 separates the established results from unresolved research objectives.

## 1. Setup

Fix a prime \(p\), integers \(k,D,d\geq1\), and the truncated formal-series ring

\[
R_D=\mathbb Z_p[x_1,\ldots,x_d]/(x_1,\ldots,x_d)^{D+1},\qquad I=(x_1,\ldots,x_d).
\]

Write \(A=1+\sum_{0<|\alpha|\le D}a_\alpha\mathbf{x}^\alpha\), so \(A\) belongs to the multiplicative group \(1+I\).

For integer weight vectors `w_i=(w_{i1},...,w_{id})`, define the commuting Euler derivations

\[
\delta_i=\sum_{j=1}^d w_{ij} x_j\partial_{x_j},\qquad
\Gamma_i(A)=\frac{\delta_i A}{A}.
\]

Suppose the \(i\)th signature is observed modulo \(p^{k+h_i}\), where \(h_i\ge0\). The goal is to reconstruct the input modulo \(p^k\). Define \(v_p(0)=+\infty\) and \(\lambda_{i,\alpha}=w_i\cdot\alpha\).

The signature readings are **independent observations** of the source; no deterministic postprocessing of an existing signature is assumed to produce additional independent signatures.

## 2. Exact multichannel directional-ghost fiber theorem

**Theorem 2.1.** Fix one admissible collection of signatures from an input `A_0`. The set of input coefficient reductions modulo `p^k` compatible with those signatures has exactly

\[
\boxed{p^E},\quad E=\sum_{0<|\alpha|\le D} e_\alpha,
\]

where

\[
\boxed{e_\alpha=\min_i\,\min\bigl(k,\max(0,v_p(\lambda_{i,\alpha})-h_i)\bigr).}
\]

The convention is that `min(k,+infinity)=k`. Every attainable signature collection has the same number of compatible coefficient reductions.

**Proof.** For any two units `A_0` and `B`, write `B=A_0 C`. The Leibniz rule and commutativity give the group homomorphism law `Gamma_i(A_0 C)=Gamma_i(A_0)+Gamma_i(C)`. The signatures agree modulo `p^{k+h_i}` iff `delta_i(C)=0` modulo that modulus, since `C` is invertible. Writing `C=1+sum c_alpha x^alpha`, each coefficient constraint is `lambda_{i,alpha} c_alpha = 0 (mod p^{k+h_i})`. Its allowable reductions modulo `p^k` form exactly the ideal `p^{k-e_alpha}(Z/p^k)` with `p^{e_alpha}` elements. All monomial coefficients vary independently. Multiplication by `A_0` is a bijection of the unit group, so the total number of source reductions is the product of the independent counts. QED.

**Corollary 2.2 (minimum full-source rescue count).** Put

\[
\boxed{b=\#\{\alpha:0<|\alpha|\le D,\ e_\alpha>0\}.}
\]

Knowledge modulo `p^k` of the named source coefficients `a_alpha` at these `b` monomials, together with all the signatures, determines every source coefficient modulo `p^k`. Moreover, no fewer than `b` arbitrary *scalar 1-Lipschitz* supplementary channels to `Z/p^k` can guarantee full reconstruction uniformly.

**Proof of sufficiency.** Proceed in increasing total degree. At every index with `e_alpha=0`, `c_alpha=0` follows already from the ghost signatures. At each remaining index, equality of the source coefficient `a_alpha` and the inductively known lower `c_beta` in `A_0 C` implies `c_alpha=0`. Therefore `C=1` modulo `p^k`.

**Proof of lower bound.** For each of the `b` indices choose `c_alpha=p^{k-1}t_alpha`, `t_alpha in {0,...,p-1}`, all other `c_alpha=0`. Since `e_alpha>0`, every `lambda_{i,alpha}` is divisible by `p^{h_i+1}`, so all `p^b` resulting inputs share the same signatures. These inputs are mutually congruent modulo `p^{k-1}`. Any scalar 1-Lipschitz output modulo `p^k` takes at most `p` distinct values on this set. Thus `m` such outputs can distinguish at most `p^m` points, requiring `m>=b`. QED.

**Important:** the lower bound concerns full-source rescue, not every possible query. Candidate channels must still be computable or independently available for practical use.

## 3. An exact prime-power lattice formula

Assume all \(h_i=h\), and assemble the weight rows into an \(m\times d\) matrix \(W\).

Define the discrete congruence count

\[
N_s(W,D)=\#\{\alpha\in\mathbb Z_{\ge0}^d:0<|\alpha|\le D,\ W\alpha\equiv0\pmod{p^s}\}.
\]

**Theorem 3.1 (layer counting).**

\[
\boxed{E(W;p,k,h,D)=\sum_{s=h+1}^{h+k} N_s(W,D)}.
\]

**Proof.** For a fixed monomial `alpha`, the number `e_alpha` in Theorem 2.1 is exactly the number of integers `s` in `h+1,...,h+k` for which `W alpha` is zero modulo `p^s`. Interchange the finite sums. QED.

**Theorem 3.2 (optimality among weighted Euler derivatives).** For every integer `W`,

\[
\boxed{E(W;p,k,h,D)\ge
\sum_{s=h+1}^{h+k}\left[\binom{\lfloor D/p^s\rfloor+d}{d}-1\right].}
\]

If `W` has full column rank modulo `p` (equivalently, some `d x d` minor is a p-adic unit), equality holds for **every** `D,k,h`. Thus `d` coordinate derivatives, or any `p`-adically left-invertible recombination of them, attain the smallest possible ambiguity among all collections of weighted Euler derivatives.

**Proof.** Every `alpha` divisible componentwise by `p^s` necessarily satisfies `W alpha=0 (mod p^s)`. The number of nonzero such monomials with total degree `<=D` is `binom(floor(D/p^s)+d,d)-1`, by stars and bars. This gives the lower bound term by term. If `W` is full column rank mod `p`, it has a left inverse over `Z_p`; hence `W alpha=0 (mod p^s)` iff `alpha=0 (mod p^s)`. Equality follows. QED.

**Corollary 3.3 (optimal scalar-channel budget).** With a full-column-rank weight family, the exact minimum number of supplementary scalar 1-Lipschitz channels for full input reconstruction is

\[
\boxed{b_\mathrm{opt}=\binom{\lfloor D/p^{h+1}\rfloor+d}{d}-1.}
\]

The residual ambiguity consists precisely of the nested exponent classes divisible componentwise by `p`, `p^2`, etc. This is a *Frobenius filtration* of the exponent lattice. Within the weighted-first-derivative operator class these layers are unavoidable: multiplying exponents by `p^s` always increases every derivative eigenvalue's p-adic valuation by at least `s`.

**Numerical example:** `d=2`, `D=10`, `p=2`, `k=3`, `h=0`.

* Single total-degree derivative `w=(1,1)`: `E=58`, `b=35`.
* Two coordinate derivatives `W=I_2`: `E=27`, `b=20`.
* Total-degree and difference derivatives `W=[[1,1],[1,-1]]`: `E=46`, `b=35`. Their determinant is `-2`, so they are not invertible modulo `2`; the deficiency is arithmetic, not linear independence over the rationals.

For `W=I_2`, `E=(binom(7,2)-1)+(binom(4,2)-1)+(binom(3,2)-1)=20+5+2=27`.

**Theorem 3.4 (Smith-lattice density).** Fix \(p,k,h,W,d\). Let \(\rho\) be the rank of \(W\), and let \(s_1,\ldots,s_\rho\) denote the valuations of its nonzero Smith invariant factors, **including factors with valuation zero**. Then, as \(D\to\infty\),

\[
\boxed{E(W;p,k,h,D)=\frac{D^d}{d!}\sum_{t=h+1}^{h+k}
 p^{-\sum_{j=1}^{\rho}\max(0,t-s_j)}+O_{p,k,h,W,d}(D^{d-1}).}
\]

**Proof.** The homomorphism \(W:(\mathbb Z/p^t)^d\to(\mathbb Z/p^t)^m\) has image size \(p^{\sum_{j=1}^{\rho}\max(0,t-s_j)}\) by Smith normal form. Exactly the reciprocal fraction of residue classes modulo `p^t` lies in its kernel. The lattice points in a growing nonnegative simplex are asymptotically equidistributed among fixed residue classes, each class contributing `D^d/(d! p^{td}) + O(D^{d-1})`. Therefore `N_t(W,D)=(D^d/d!) / |im W_t|+O(D^{d-1})`. Sum over the finitely many `t`. QED.

This provides an exact leading-order prediction of the ambiguity *from Smith invariants of the derivative-direction matrix* before enumerating any monomials. It also exposes a precision-versus-observation tradeoff: adding directions that improve the rank modulo \(p\) can reduce ambiguity, but independent observations require additional computation or access to the source.

## 4. Query-specific reconstruction from nonlinear ghost observations

Version 1.2 has a Smith-fiber formula for linear main observations. The new ghost theorem shows a different case: a nonlinear main observation can have a **linear/affine coefficient fiber**, and thus admits a Smith calculation for a linear query.

Fix one input `A_0` in a measured ghost fiber and work modulo `p^k`. Let the positive monomial indices be `S`, with `e_alpha` given by Theorem 2.1, and `r_alpha=k-e_alpha`. The compatible sources are precisely

\[
\mathcal F=A_0(1+\mathcal L),\quad
\mathcal L=\bigoplus_{\alpha\in S}p^{r_\alpha}(\mathbb Z/p^k)\mathbf x^\alpha.
\]

Let `M_{A_0}` be the integral unitriangular convolution matrix representing multiplication of truncated series by `A_0`, and let `Q` be any integral linear query on the input coefficient vector. Define

\[
H_Q=Q\,M_{A_0}\,\operatorname{diag}(p^{r_\alpha}).
\]

**Theorem 4.1 (nonlinear-observation/linear-query Smith formula).** If `s_1,...,s_u` are the Smith valuations of `H_Q` (with `s_j=+infinity` for zero pivots), the exact number of distinct values of `Q(A) (mod p^k)` consistent with the measured nonlinear ghost signatures is

\[
\boxed{|Q(\mathcal F)|=p^{\sum_{j=1}^u\max(0,k-s_j)}.}
\]

**Proof.** The map from a coefficient vector `c` of `C-1` to the source difference `A_0 C-A_0` is the linear map `M_{A_0}c`, even though the signature map is nonlinear. Its permitted parameters form the diagonal module `L`. Thus the set of query differences is exactly the image modulo `p^k` of `H_Q`. Integer Smith diagonalization gives the claimed cardinality, including non-injective or rectangular matrices. QED.

For a single coordinate query `a_beta`, the formula specializes to

\[
\boxed{|\{a_\beta\}|=p^{k-\rho_\beta}},\qquad
\rho_\beta=\min\left(k,\min_{0<\alpha\le\beta}
\big[r_\alpha+v_p((A_0)_{\beta-\alpha})\big]\right),
\]

where `alpha<=beta` is componentwise and `v_p(0)=+infinity`. This shows why the ambiguity of a source coefficient cannot be inferred from its *own derivative eigenvalue alone*: lower unknown coefficients can propagate through convolution with the chosen base source `A_0`.

**Example.** Set `p=2,k=2,D=4`, use both coordinate derivatives, and ask for the coefficient at `x^3 y`.

* In the ghost fiber containing `A_0=1`, this coefficient is uniquely determined modulo `4`.
* In the ghost fiber containing `A_0=1+xy`, it has **two** possible values modulo `4`, because the ambiguous `x^2` coefficient of `C` contributes to `x^3y` after multiplication by `xy`.

So two fibers for the same set of operators can have different *query* ambiguity, even though their *full source* fibers have the same cardinality.

**Theorem 4.2 (ideal linear query rescue).** For a fixed affine source fiber `A_0+K` over `Z/p^k` and a linear query `Q`, the minimum number of supplementary **linear scalar channels modulo p^k** needed to determine `Q` on that fiber, if arbitrary linear source measurements are permitted, is the minimal number of generators of `Q(K)`. Equivalently it is the number of nonzero modulo-`p^k` Smith pivots of a matrix generating `Q(K)`.

**Proof.** If `P:source -> (Z/p^k)^m` resolves the query then `Q(K)` is a quotient of `P(K)`; a submodule of the free rank-`m` module over the principal ideal ring `Z/p^k` has at most `m` generators, as does every quotient. Thus `m>=mu(Q(K))`. Conversely, by Smith normal form for the inclusion `Q(K) subset (Z/p^k)^t`, a unimodular change of target coordinates `U` sends `Q(K)` into the first `mu` coordinates. The `mu` measurements consisting of the first `mu` coordinates of `UQ` have no unresolved query ambiguity. QED.

**Restrictions:** This minimum is local to one known fiber, assumes that supplementary measurements derived from `Q` itself are permitted, and is not an algorithm for cheaply obtaining them. For unrestricted nonlinear Lipschitz channels, it is not a claimed minimum; p-adic digit packing can behave differently.

## 5. A lossless Frobenius/polyphase quotient

The preceding theorem proves that first-order weighted derivatives cannot remove their Frobenius-layer kernel, regardless of how many directions are used. This motivates considering a fundamentally different operator class rather than adding further first derivatives.

**Theorem 5.1 (contracting coboundary theorem).** Let `R` be a complete separated commutative ring with ideal `I`, and let `S:R->R` be a unital continuous ring endomorphism such that `S(I^n) subset I^{2n}` for all `n>=1`. Then

\[
\boxed{\Phi_S(A)=A/S(A)}
\]

is a multiplicative-group automorphism of `1+I`, with explicit inverse

\[
\boxed{\Phi_S^{-1}(B)=\prod_{j\ge0}S^j(B).}
\]

The product converges in the `I`-adic topology.

**Proof.** The map is multiplicative. For `B in 1+I`, the factors `S^j(B)` approach `1` to arbitrarily high `I`-adic order, so the product exists. If `A` is this product then `S(A)` is the same product without its first factor; consequently `A/S(A)=B`. Conversely `A/S(A)=1` implies `A=S(A)=S^n(A)`, and `S^n(A)->1`, forcing `A=1`. QED.

Take `S_q(A)(x_1,...,x_d)=A(x_1^q,...,x_d^q)` for integer `q>=2`. Then

\[
\boxed{\Phi_q(A)(\mathbf x)=\frac{A(\mathbf x)}{A(\mathbf x^q)},\quad
A(\mathbf x)=\prod_{j\ge0}\Phi_q(A)(\mathbf x^{q^j}).}
\]

Every operation uses integral formal-series multiplication/inversion, so the transformation is bijective modulo *every* `p^k`. The forward and inverse operations are coefficientwise congruence-preserving; in particular no p-adic digits are lost. This is a normal form, **not an independent observation and not a way to create missing information from a logarithmic derivative alone**.

**Theorem 5.2 (intertwining with directional ghosts).** For each weighted Euler derivation,

\[
\boxed{\Gamma_i(\Phi_q A)(\mathbf x)=\Gamma_i(A)(\mathbf x)-q\,\Gamma_i(A)(\mathbf x^q).}
\]

**Proof.** The logarithmic derivative is additive across products and quotients. The chain rule gives `delta_i(S_q A)=q S_q(delta_i A)`, hence `Gamma_i(S_q A)=q S_q(Gamma_i A)`. Subtract. QED.

The intertwining relation means the derivative signature of the transformed series carries no information beyond the old derivative signature, though the transformed **series coefficients** can provide independent supplementary information when externally available.

**Theorem 5.3 (alternative minimal rescue coordinates).** Let `S` be the blind index set of Theorem 2.1: `S={alpha:e_alpha>0}`. In place of observing the original source coefficients `a_alpha` for `alpha in S`, one may observe the `|S|` coefficients of `Phi_q(A)` at precisely those indices, modulo `p^k`, for **any integer `q>=2`**. Together with the original directional signatures, these observations also determine the full source modulo `p^k`, and the number of channels is again minimal among scalar 1-Lipschitz schemes that must work uniformly.

**Proof.** The coefficient of `x^alpha` in `Phi_q(A)=A/S_q(A)` is `a_alpha` plus an integral polynomial in coefficients of `A` of strictly smaller positive total degree; this follows because `S_q(A)-1` starts in degree at least `q>=2`. The same is true for every triangular coordinate change with unit diagonal. Take any two source series in one ghost fiber with the same stated `Phi_q` coefficients. Induct on degree. At an index not in `S`, the ghost conditions already force the two source coefficients to agree once all earlier differences have vanished. At an index in `S`, equality of the observed `Phi_q` coefficients and previously established lower source coefficients forces equality of the original source coefficient. This completes the induction. The 1-Lipschitz lower bound `|S|` was proved in Corollary 2.2 and still applies to these observations. QED.

This gives a genuinely different, integral **choice of rescue coordinates**; it does not make them free or infer them from the primitive ghosts. For partition-like series, they may be accessible via independently known Euler-product or polyphase descriptions.

### Example: an exact sequence family from a single polyphase quotient

For the ordinary partition generating function

\[
P(x)=\prod_{n\ge1}(1-x^n)^{-1},
\]

we obtain for **every integer q>=2**:

\[
\boxed{
\frac{P(x)}{P(x^q)}
=\prod_{n\ge1}(1+x^n+\cdots+x^{(q-1)n})
=\prod_{\substack{n\ge1\\q\nmid n}}(1-x^n)^{-1}.
}
\]

This is the classical bounded-multiplicity versus q-indivisible-parts partition identity, including the `q=2` correspondence between distinct-part and odd-part partitions. It is a concrete, infinite family of exact edges for the sequence-transfer graph, not a claimed historically new theorem.

Since `Gamma(P)=sum_{n>=1} sigma_1(n)x^n`, we also obtain

\[
\boxed{\Gamma(\Phi_q P)(x)
=\sum_{n\ge1}[\sigma_1(n)-q\,\mathbf 1_{q\mid n}\sigma_1(n/q)]x^n.}
\]

For the shifted-Fibonacci generating function `F(x)=1/(1-x-x^2)`,

\[
\boxed{\Phi_q F(x)=\frac{1-x^q-x^{2q}}{1-x-x^2}},
\]

and the corresponding Lucas ghost coefficients transform by `L_n -> L_n - q 1_{q|n} L_{n/q}`.

## 6. What these generalizations do and do not establish

1. **Proved:** exact multivariate weighted-derivative ambiguity; precise minimum full-source supplementary channel count for congruence-preserving scalar channels; the optimality and lattice layer formula; query-fiber Smith calculation for nonlinear primitive signatures; the contracting-coboundary automorphism and its intertwining law.
2. **Established as an asymptotic theorem:** ambiguity density from p-adic Smith invariants of directional weight matrices, for fixed arithmetic parameters as truncation degree grows.
3. **Verified computationally:** complete finite-input ghost-fiber enumerations, exact candidate kernel enumerations, randomized lattice identities, randomized multi-query image counts, and lossless quotient/inversion identities. Details in the results JSON files.
4. **Not established:** historical novelty; faster asymptotic runtimes or benchmark speedups; an automated supplier of independent ghost channels; recovery from old primitive signatures without extra information; verification of all OEIS entries; Lean formalization; resolution of a major open conjecture.

## 7. Proposed compiler integration

For a sequence/transfer object, register the tuple

`(source series, operator family, W, p, k, h_i, monomial domain, algebraic contract, precise query Q, observable availability, cost)`.

1. Normalize operator compositions, including contracting quotients and integral shears, *before* evaluating information loss.
2. For directional ghost families, compute lattice layer counts and the exact exponent-by-exponent remaining freedom.
3. For a requested query, use `H_Q=Q*M_A*diag(p^(k-e_alpha))`, calculate the Smith image, and retain a certificate of its query-specific ambiguity.
4. If missing information remains, request admissible independent channels; do not pretend a transformation of the same data provides them.
5. Test the resulting route against source-validated full-index identities and measured computational cost before upgrading any public proof label.

A useful first research benchmark is to supply bivariate series with several independently available decompositions, hide a subset of coefficients, and compare query reconstruction under one versus two directional signatures. A second is to add the `Phi_q` family to the existing partition and rational-OGF transfer graph, with original source definitions and exact series certificates.