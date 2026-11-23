# Directional ghosts, Frobenius obstructions, query fibers, and contractive transfers

**Research status:** Written algebraic proofs supported by finite computational checks. No Lean formalization, independent peer review, or historical novelty assessment has been completed. Here, *new* means new within this research continuation.

[Sequence transfer network](SEQUENCE_TRANSFER_NETWORK.md) · [Sequence Library](https://KomorebiP.github.io/The-Komorebi-Program/sequence-network.html) · [Research sources and reproducibility](../research/directional-ghosts/README.md)

**Author: Komorebi P.**  
**Research checkpoint: 2026-11-23.**  
**Inputs:** `Komorebi_Ambient_Realization_All_Progress_2026-11-23.zip` and `Komorebi_Precision_Aware_Transfer_Bridge_v1_2_2026-11-23.zip`.

**Scope of this note.** The results below extend the earlier one-variable logarithmic-derivative and finite-module reconstruction work to multivariate directional observations, prime-power lattice counts, nonlinear-observation query fibers, and contracting transfer operators. The written proofs and finite tests support the statements under their stated assumptions; they do not establish historical priority, independent source verification, or Lean certification.

## Reader's guide

**In plain language.** A directional ghost records how a generating function changes along a weighted direction. Different generating functions can produce identical observations at finite precision. The results below count those indistinguishable inputs, identify the remaining arithmetic obstructions, and distinguish recovering an entire series from recovering only the answer to a specific query. A change of coordinates can make those obstructions easier to study, but cannot manufacture missing measurements.

The central question is how much information about a truncated generating function survives a family of observations. These results distinguish **full reconstruction** of its coefficients from **query reconstruction**, where only a chosen answer must be determined.

| Term | Meaning in this note |
| --- | --- |
| Source \(A\) | A truncated formal series with constant coefficient \(1\). |
| Directional ghost \(\Gamma_i(A)\) | The logarithmic derivative \(\delta_i A/A\) along a specified weighted direction. |
| Precision \(p^k\) | The modulus of the source coefficients being reconstructed; observations may use higher precision. |
| Fiber | Source reductions modulo \(p^k\) for which at least one full-precision lift matches the supplied signatures. |
| \(e_\alpha\) | The number of undetermined base-\(p\) digits at coefficient index \(\alpha\). |
| \(E\) and \(b\) | Total ambiguity exponent and number of blind coefficient indices, respectively. |
| Rescue channel | An independently available supplementary measurement. It cannot be synthesized from the same information already lost. |
| \(\Phi_q\) | A lossless change of series coordinates defined by \(A(\mathbf{x})/A(\mathbf{x}^q)\). |

**Reading route:** Sections 2–3 quantify the remaining source ambiguity. Section 4 asks what is needed for a particular query. Section 5 gives a lossless transformation that may offer more useful coordinates, without creating new information. Section 6 separates the established results from unresolved research objectives.

## 1. Setup

Fix a prime \(p\), integers \(k,D,d\geq1\), and the truncated formal-series ring

\[
R_D=\mathbb Z_p[x_1,\ldots,x_d]/(x_1,\ldots,x_d)^{D+1},\qquad I=(x_1,\ldots,x_d).
\]

Write \(A=1+\sum_{0<|\alpha|\le D}a_\alpha\mathbf{x}^\alpha\), where \(\alpha\in\mathbb Z_{\ge0}^d\), \(|\alpha|=\sum_j\alpha_j\), and \(\mathbf{x}^\alpha=\prod_j x_j^{\alpha_j}\). Here \(\mathbb Z_p\) denotes the \(p\)-adic integers. The series \(A\) belongs to the multiplicative group \(1+I\).

For integer weight vectors \(w_i=(w_{i1},\ldots,w_{id})\), define the commuting Euler derivations

\[
\delta_i=\sum_{j=1}^d w_{ij} x_j\partial_{x_j},\qquad
\Gamma_i(A)=\frac{\delta_i A}{A}.
\]

Suppose the \(i\)th signature is independently observed modulo \(p^{k+h_i}\), where \(h_i\ge0\). The goal is to recover source coefficients modulo \(p^k\). A source reduction is called **compatible** if it admits a lift to \(R_D\) whose signatures match all supplied measurements at their stated precisions. This matters because a signature modulo \(p^{k+h_i}\) need not be determined by source coefficients modulo \(p^k\) alone. Put \(v_p(0)=+\infty\) and \(\lambda_{i,\alpha}=w_i\cdot\alpha\).

The signature readings are **independently supplied observations** of the source, potentially at different precisions. They need not be statistically independent. Deterministic postprocessing of an existing signature does not count as a new measurement.

A scalar measurement \(f\) on source coefficient arrays is **1-Lipschitz in the congruence sense** when coordinatewise congruence \(u\equiv v\pmod{p^j}\) implies \(f(u)\equiv f(v)\pmod{p^j}\) for every \(0\le j\le k\). This includes coefficient projections and integral-polynomial measurements. The channel lower bounds below are **not** claims about arbitrary discontinuous or non-congruence-preserving encodings.


### A small reconstruction example

In one variable, take \(p=2\), \(k=2\), \(h=0\), \(D=4\), and observe \(\Gamma(A)=xA'(x)/A(x)\) modulo \(4\). The **Euler derivative** \(x\partial_x\) multiplies the coefficient of \(x^n\) by \(n\). Taking a quotient of two source series reduces equality of their nonlinear ghosts to these linear coefficient conditions. Theorem 2.1 gives:

| Degree \(n\) | \(v_2(n)\) | Remaining exponent \(e_n\) |
| ---: | ---: | ---: |
| 1 | 0 | 0 |
| 2 | 1 | 1 |
| 3 | 0 | 0 |
| 4 | 2 | 2 |

Thus there are \(2^{0+1+0+2}=8\) compatible source reductions modulo \(4\), with two blind indices (degrees \(2\) and \(4\)). For the zero ghost, they are exactly \(A=1+c_2x^2+c_4x^4\), where \(c_2\in\{0,2\}\) and \(c_4\in\{0,1,2,3\}\) modulo \(4\). If the **ghost** is independently supplied modulo \(8\), then \(h=1\), and each attainable set of measurements admits just \(2\) source reductions modulo \(4\). Extra observation precision is useful, but it does not replace an unavailable measurement.

## 2. Exact multichannel directional-ghost fiber theorem

### Theorem 2.1. Exact directional-ghost fiber size

Fix one admissible collection of signatures from an input \(A_0\). The set of input coefficient reductions modulo \(p^k\) compatible with those signatures has exactly

\[
\boxed{p^E},\quad E=\sum_{0<|\alpha|\le D} e_\alpha,
\]

where

\[
\boxed{e_\alpha=\min_i\,\min\bigl(k,\max(0,v_p(\lambda_{i,\alpha})-h_i)\bigr).}
\]

The convention is that \(\min(k,+\infty)=k\). Every attainable signature collection has the same number of compatible coefficient reductions.

**Proof.** For any two units \(A_0\) and \(B\), write \(B=A_0C\). The Leibniz rule gives \(\Gamma_i(A_0C)=\Gamma_i(A_0)+\Gamma_i(C)\). The signatures agree modulo \(p^{k+h_i}\) exactly when \(\delta_i(C)\equiv0\pmod{p^{k+h_i}}\), since \(C\) is invertible. Writing \(C=1+\sum_\alpha c_\alpha\mathbf{x}^\alpha\), the coefficient constraints are \(\lambda_{i,\alpha}c_\alpha\equiv0\pmod{p^{k+h_i}}\). The permissible reductions of \(c_\alpha\) modulo \(p^k\) form the ideal \(p^{k-e_\alpha}(\mathbb Z/p^k\mathbb Z)\), containing exactly \(p^{e_\alpha}\) elements. The monomial constraints are independent. Multiplication by \(A_0\) bijects the permissible \(C\) with permissible \(B\), so the total fiber size is \(p^{\sum_\alpha e_\alpha}\). \(\square\)

### Corollary 2.2. Minimum full-source rescue count

 Put

\[
\boxed{b=\#\{\alpha:0<|\alpha|\le D,\ e_\alpha>0\}.}
\]

Knowledge modulo \(p^k\) of the source coefficients \(a_\alpha\) at these \(b\) blind monomials, together with the signatures, determines every coefficient modulo \(p^k\). Moreover, no fewer than \(b\) arbitrary **scalar 1-Lipschitz** supplementary channels with values in \(\mathbb Z/p^k\mathbb Z\) can guarantee full reconstruction uniformly.

**Proof of sufficiency.** Compare two compatible sources \(A_0\) and \(B=A_0C\), and proceed in increasing total degree. At an index with \(e_\alpha=0\), the signature constraints force \(c_\alpha=0\). At a blind index, equality of the observed source coefficient \(a_\alpha\), combined with equality at all lower indices, forces \(c_\alpha=0\). Thus \(C=1\pmod{p^k}\) and \(B=A_0\pmod{p^k}\).

**Proof of lower bound.** At each of the \(b\) blind indices, choose \(c_\alpha=p^{k-1}t_\alpha\) with \(t_\alpha\in\{0,\ldots,p-1\}\), and set all other \(c_\alpha=0\). Because \(e_\alpha>0\), each \(\lambda_{i,\alpha}\) is divisible by \(p^{h_i+1}\). All \(p^b\) resulting sources share the same signatures and are mutually congruent modulo \(p^{k-1}\). A scalar 1-Lipschitz channel modulo \(p^k\) takes at most \(p\) values on such a set. Consequently \(m\) channels distinguish at most \(p^m\) of these sources, forcing \(m\ge b\). \(\square\)

**Important:** the lower bound concerns full-source rescue, not every possible query. Candidate channels must still be computable or independently available for practical use.

## 3. An exact prime-power lattice formula

Assume all \(h_i=h\), and assemble the weight rows into an \(m\times d\) matrix \(W\).

Define the discrete congruence count

\[
N_s(W,D)=\#\{\alpha\in\mathbb Z_{\ge0}^d:0<|\alpha|\le D,\ W\alpha\equiv0\pmod{p^s}\}.
\]

### Theorem 3.1. Layer counting



\[
\boxed{E(W;p,k,h,D)=\sum_{s=h+1}^{h+k} N_s(W,D)}.
\]

**Proof.** For a fixed \(\alpha\), the exponent \(e_\alpha\) counts precisely those levels \(s\in\{h+1,\ldots,h+k\}\) for which \(W\alpha\equiv0\pmod{p^s}\). Interchanging the two finite sums yields the identity. \(\square\)

### Theorem 3.2. Optimality among weighted Euler derivatives

For every integer matrix \(W\),

\[
\boxed{E(W;p,k,h,D)\ge
\sum_{s=h+1}^{h+k}\left[\binom{\lfloor D/p^s\rfloor+d}{d}-1\right].}
\]

If \(W\) has full column rank modulo \(p\), equivalently if some \(d\times d\) minor is a \(p\)-adic unit, equality holds for **every** \(D,k,h\). Thus \(d\) coordinate derivatives, or any \(p\)-adically left-invertible recombination of them, attain the minimum ambiguity among collections of weighted Euler derivatives.

**Proof.** Every \(\alpha\) divisible componentwise by \(p^s\) satisfies \(W\alpha\equiv0\pmod{p^s}\). The number of nonzero such monomials with total degree at most \(D\) is \(\binom{\lfloor D/p^s\rfloor+d}{d}-1\), by stars and bars. This yields the lower bound level by level. If \(W\) has full column rank modulo \(p\), it admits a left inverse over \(\mathbb Z_p\). Therefore \(W\alpha\equiv0\pmod{p^s}\) if and only if \(\alpha\equiv0\pmod{p^s}\), proving equality. \(\square\)

### Corollary 3.3. Optimal scalar-channel budget

 With a full-column-rank weight family, the exact minimum number of supplementary scalar 1-Lipschitz channels for full input reconstruction is

\[
\boxed{b_\mathrm{opt}=\binom{\lfloor D/p^{h+1}\rfloor+d}{d}-1.}
\]

For a full-column-rank family, the residual ambiguity consists precisely of exponent vectors divisible componentwise by \(p,p^2,\ldots\). This **Frobenius filtration** is unavoidable within the weighted first-derivative operator class: multiplying an exponent vector by \(p^s\) increases every derivative eigenvalue's \(p\)-adic valuation by at least \(s\). Other kinds of observation are not covered by this optimality statement.

**Worked comparison:** \(d=2\), \(D=10\), \(p=2\), \(k=3\), \(h=0\).

| Weight observations | Ambiguity exponent \(E\) | Blind indices \(b\) |
| --- | ---: | ---: |
| Total-degree derivative, \(w=(1,1)\) | 58 | 35 |
| Coordinate derivatives, \(W=I_2\) | 27 | 20 |
| Total-degree and difference, \(W=\left(\begin{smallmatrix}1&1\\1&-1\end{smallmatrix}\right)\) | 46 | 35 |

The last matrix has determinant \(-2\), which is not a unit modulo \(2\). Rational linear independence is insufficient for optimal reconstruction in the \(2\)-adic setting.

For \(W=I_2\), the layer counts give \(E=\bigl[\binom72-1\bigr]+\bigl[\binom42-1\bigr]+\bigl[\binom32-1\bigr]=20+5+2=27\).

### Theorem 3.4. Smith-lattice density

 Fix \(p,k,h,W,d\). Let \(\rho\) be the rank of \(W\), and let \(s_1,\ldots,s_\rho\) denote the valuations of its nonzero Smith invariant factors, **including factors with valuation zero**. Then, as \(D\to\infty\),

\[
\boxed{E(W;p,k,h,D)=\frac{D^d}{d!}\sum_{t=h+1}^{h+k}
 p^{-\sum_{j=1}^{\rho}\max(0,t-s_j)}+O_{p,k,h,W,d}(D^{d-1}).}
\]

**Proof.** Smith normal form shows that the homomorphism \(W:(\mathbb Z/p^t\mathbb Z)^d\to(\mathbb Z/p^t\mathbb Z)^m\) has image size \(p^{\sum_{j=1}^{\rho}\max(0,t-s_j)}\). Its kernel therefore occupies the reciprocal fraction of residue classes modulo \(p^t\). For each fixed residue class, the lattice points in the nonnegative simplex \(0<|\alpha|\le D\) contribute \(D^d/(d!\,p^{td})+O(D^{d-1})\). Hence \(N_t(W,D)=D^d/(d!\,|\operatorname{im} W_t|)+O(D^{d-1})\). Summation over the fixed finite range of \(t\) completes the proof. \(\square\)

This provides an exact leading-order prediction of the ambiguity *from Smith invariants of the derivative-direction matrix* before enumerating any monomials. It also exposes a precision-versus-observation tradeoff: adding directions that improve the rank modulo \(p\) can reduce ambiguity, but independent observations require additional computation or access to the source.

## 4. Query-specific reconstruction from nonlinear ghost observations

Version 1.2 has a Smith-fiber formula for linear main observations. The new ghost theorem shows a different case: a nonlinear main observation can have a **linear/affine coefficient fiber**, and thus admits a Smith calculation for a linear query.

Fix a representative \(A_0\) of the measured ghost fiber and work modulo \(p^k\). Let \(\mathcal S\) be the set of positive monomial indices, with \(e_\alpha\) as in Theorem 2.1, and put \(r_\alpha=k-e_\alpha\). The compatible sources are exactly

\[
\begin{aligned}
\mathcal F&=A_0(1+\mathcal L),\\
\mathcal L&=\bigoplus_{\alpha\in\mathcal S}
p^{r_\alpha}(\mathbb Z/p^k\mathbb Z)\mathbf x^\alpha.
\end{aligned}
\]

Let \(M_{A_0}\) be the integral unitriangular convolution matrix for multiplication of truncated series by \(A_0\), and let \(Q\) be an integral linear query on the input coefficient vector. Define

\[
H_Q=Q\,M_{A_0}\,\operatorname{diag}(p^{r_\alpha}).
\]

### Theorem 4.1. Nonlinear observations and linear-query Smith formula

If \(s_1,\ldots,s_u\) are the \(p\)-adic valuations of the Smith invariant factors of \(H_Q\), including \(s_j=+\infty\) for zero pivots, then the exact number of distinct outputs \(Q(A)\pmod{p^k}\) consistent with the measured ghost signatures is

\[
\boxed{|Q(\mathcal F)|=p^{\sum_{j=1}^u\max(0,k-s_j)}.}
\]

**Proof.** The map from the coefficient vector \(c\) of \(C-1\) to the source difference \(A_0C-A_0\) is \(c\mapsto M_{A_0}c\), even though the original observation map is nonlinear. The permitted \(c\) form the diagonal module \(\mathcal L\). The possible query differences are therefore the image of \(H_Q\) modulo \(p^k\). Integer Smith diagonalization gives the claimed cardinality, including for rectangular or non-injective matrices. \(\square\)

For a single coordinate query \(a_\beta\), the formula specializes to

\[
\boxed{|\{a_\beta\}|=p^{k-\rho_\beta}},\qquad
\rho_\beta=\min\left(k,\min_{0<\alpha\le\beta}
\big[r_\alpha+v_p((A_0)_{\beta-\alpha})\big]\right),
\]

Here \(\alpha\le\beta\) is componentwise, \(v_p(0)=+\infty\), and the minimum of an empty index set is \(+\infty\). Thus the ambiguity of a source coefficient cannot be inferred from its *own* derivative eigenvalue alone: lower unknown coefficients can propagate through convolution with the base series \(A_0\).

**Worked example.** Let \(p=2\), \(k=2\), \(D=4\), and use both coordinate derivatives. The query is the coefficient of \(x^3y\).

* In the ghost fiber containing \(A_0=1\), this coefficient is uniquely determined modulo \(4\).
* In the ghost fiber containing \(A_0=1+xy\), the coefficient has **two** possible values modulo \(4\). The ambiguous \(x^2\) coefficient of \(C\) contributes to \(x^3y\) after multiplication by \(xy\).

So two fibers for the same set of operators can have different *query* ambiguity, even though their *full source* fibers have the same cardinality.

### Theorem 4.2. Ideal linear query rescue

For a fixed affine source fiber \(A_0+K\) over \(\mathbb Z/p^k\mathbb Z\) and a linear query \(Q\), the minimum number of supplementary **linear scalar channels modulo \(p^k\)** required to determine the query, when arbitrary linear source measurements are permitted, is the minimal number of generators of \(Q(K)\). Equivalently, it is the number of nonzero Smith pivots modulo \(p^k\) of a matrix generating \(Q(K)\).

**Proof.** Suppose a linear measurement \(P\) with \(m\) scalar outputs resolves the query on the fiber. Then \(\ker(P|_K)\subseteq\ker(Q|_K)\), so \(Q(K)\) is a quotient of \(P(K)\). Every submodule of \((\mathbb Z/p^k\mathbb Z)^m\) has at most \(m\) generators, hence \(m\ge\mu(Q(K))\). Conversely, a unimodular change of coordinates in the query's target sends \(Q(K)\) into its first \(\mu(Q(K))\) coordinates. Measuring those coordinates of the transformed query suffices. \(\square\)

**Restrictions.** This minimum is local to one known fiber and permits measurements derived from \(Q\) itself. It does **not** guarantee that such measurements are cheap or independently available. No comparable minimum is asserted for unrestricted nonlinear or non-1-Lipschitz channels.

## 5. A lossless Frobenius/polyphase quotient

The preceding theorem proves that first-order weighted derivatives cannot remove their Frobenius-layer kernel, regardless of how many directions are used. This motivates considering a fundamentally different operator class rather than adding further first derivatives.

### Theorem 5.1. Contracting coboundary theorem

Let \(R\) be a complete, separated commutative ring with an ideal \(I\), and let \(S:R\to R\) be a unital, continuous ring endomorphism satisfying \(S(I^n)\subseteq I^{2n}\) for all \(n\ge1\). Then

\[
\boxed{\Phi_S(A)=A/S(A)}
\]

is an automorphism of the multiplicative group \(1+I\), with explicit inverse

\[
\boxed{\Phi_S^{-1}(B)=\prod_{j\ge0}S^j(B).}
\]

The product converges in the \(I\)-adic topology. The conclusion concerns the multiplicative group \(1+I\), not an automorphism of the underlying additive ring.

**Proof.** The map is multiplicative because \(S\) is a ring endomorphism. For \(B\in1+I\), the terms \(S^j(B)\) tend to \(1\) at arbitrarily high \(I\)-adic order, so \(\prod_{j\ge0}S^j(B)\) converges. Calling this product \(A\), the product \(S(A)\) omits its first factor, hence \(A/S(A)=B\). Conversely, \(A/S(A)=1\) implies \(A=S(A)=S^n(A)\) for every \(n\). Contraction forces \(S^n(A)\to1\), hence \(A=1\). \(\square\)

For an integer \(q\ge2\), take the substitution endomorphism \(S_q(A)(x_1,\ldots,x_d)=A(x_1^q,\ldots,x_d^q)\). Then

\[
\boxed{\Phi_q(A)(\mathbf x)=\frac{A(\mathbf x)}{A(\mathbf x^q)},\quad
A(\mathbf x)=\prod_{j\ge0}\Phi_q(A)(\mathbf x^{q^j}).}
\]

The substitution, multiplication, and inversion of unit formal series are defined by integral coefficient formulas. Consequently, this coordinate change remains bijective modulo **every** \(p^k\), with coefficientwise congruence preservation in both directions. It is a lossless change of representation, **not an independent observation**: it cannot reconstruct information lost in an earlier ghost measurement.

### Theorem 5.2. Intertwining with directional ghosts

 For each weighted Euler derivation,

\[
\boxed{\Gamma_i(\Phi_q A)(\mathbf x)=\Gamma_i(A)(\mathbf x)-q\,\Gamma_i(A)(\mathbf x^q).}
\]

**Proof.** The logarithmic derivative is additive for products and subtractive for quotients. The chain rule gives \(\delta_i(S_qA)=q\,S_q(\delta_iA)\), hence \(\Gamma_i(S_qA)=q\,S_q(\Gamma_iA)\). Applying this to \(A/S_q(A)\) gives the identity. \(\square\)

The intertwining relation means the derivative signature of the transformed series carries no information beyond the old derivative signature, though the transformed **series coefficients** can provide independent supplementary information when externally available.

### Theorem 5.3. Alternative minimal rescue coordinates

Let \(\mathcal B=\{\alpha:e_\alpha>0\}\) be the blind index set of Theorem 2.1. Instead of independently observing the source coefficients \(a_\alpha\) for \(\alpha\in\mathcal B\), one may independently observe the corresponding \(|\mathcal B|\) coefficients of \(\Phi_q(A)\) modulo \(p^k\), for **any integer \(q\ge2\)**. Together with the primitive directional signatures, these observations determine the full source modulo \(p^k\). The channel count remains minimal among uniformly valid scalar 1-Lipschitz schemes.

**Proof.** The coefficient of \(\mathbf{x}^\alpha\) in \(\Phi_q(A)=A/S_q(A)\) equals \(a_\alpha\) plus an integral polynomial in source coefficients of strictly smaller positive total degree, because \(S_q(A)-1\) starts in degree at least \(q\ge2\). Compare two sources with identical primitive ghosts and the specified \(\Phi_q\) coefficients, and induct on total degree. At \(\alpha\notin\mathcal B\), the ghost constraints force agreement. At \(\alpha\in\mathcal B\), the observed transformed coefficient and agreement at all lower degrees force agreement of \(a_\alpha\). All source coefficients therefore agree modulo \(p^k\). The lower bound is Corollary 2.2. \(\square\)

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

This is the classical identity between partitions with each part occurring at most \(q-1\) times and partitions whose parts are not divisible by \(q\). At \(q=2\), it becomes the distinct-part/odd-part identity. These are exact candidate edges for the transfer network, **not historically new partition identities**.

Since \(\Gamma(P)=\sum_{n\ge1}\sigma_1(n)x^n\), we also obtain

\[
\boxed{\Gamma(\Phi_q P)(x)
=\sum_{n\ge1}[\sigma_1(n)-q\,\mathbf 1_{q\mid n}\sigma_1(n/q)]x^n.}
\]

For the shifted-Fibonacci ordinary generating function \(F(x)=1/(1-x-x^2)\),

\[
\boxed{\Phi_q F(x)=\frac{1-x^q-x^{2q}}{1-x-x^2}},
\]

The corresponding Lucas ghost coefficients transform by \(L_n\mapsto L_n-q\mathbf 1_{q\mid n}L_{n/q}\), with the term involving \(n/q\) present only when \(q\mid n\).

### Notation for implementation

In Section 4, \(A_0\) is any chosen representative of the measured fiber. The full fiber size is independent of that representative, but the ambiguity of a specified linear coefficient query can depend on the observed fiber. A Smith certificate must record both the query and the representative used to construct \(M_{A_0}\).

In Section 5, the quotient \(\Phi_q(A)\) and its inverse are transformations of **available source data**. Their coefficients may serve as rescue measurements only when independently known or computable from information beyond the original ghost signatures.

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
3. For a requested query \(Q\), form \(H_Q=QM_{A_0}\operatorname{diag}(p^{k-e_\alpha})\), compute its Smith image modulo \(p^k\), and retain a certificate of the resulting query-specific ambiguity.
4. If missing information remains, request admissible independent channels; do not pretend a transformation of the same data provides them.
5. Test the resulting route against source-validated full-index identities and measured computational cost before upgrading any public proof label.

A useful first research benchmark is to supply bivariate series with several independently available decompositions, hide a subset of coefficients, and compare query reconstruction under one versus two directional signatures. A second is to add the \(\Phi_q\) family to the existing partition and rational-OGF transfer graph, retaining source definitions and exact series certificates.