# Lattice factorization, polyphase spectra and sharp graph realization

**Author: Komorebi P.**  
**Status:** written all-index mathematical arguments and exact computational checks. No Lean verification or priority claim.

This continues [Parity array transfer](PARITY_ARRAY_TRANSFER.md), published at commit 9304424e11705bf296eaaf00d538973ef91e233b. The predecessor research archive is Komorebi_Lattice_Polyphase_Graph_Generalization.zip, SHA-256 a1aabf1e87ce65a38a4259f042cda1e32990223339e1312158fdc0b0ec26beb4. Its manifest and both verification reports were replayed successfully. This edition incorporates the stronger integral trace obstruction and direct graph construction developed in the continuation. All minimum sizes refer to nonnegative integer weighted directed adjacency matrices (loops allowed), a single marked walk count, and fixed integer polynomial forward shifts. Direct count constructions are separately identified.

## 1. General lattice decomposition

Let X be a finite subset of the integer lattice of dimension d and S a finite collection of edge displacement vectors. Put \(L=\operatorname{span}_{\mathbb Z}S\). Every allowed edge joins two vertices in the same coset of L. The induced pieces on the occupied cosets form a disjoint union, and hence the multivariate independence polynomial is

\[
P_G(\mathbf z)=\prod_c P_{G_c}(\mathbf z|_{G_c}).
\]

The pieces need not themselves be connected on a finite irregular domain. For full rank L, the index is the product of the Smith invariant factors, equivalently the gcd of the maximal minors. At lower rank the quotient also has a free part. For a full Cayley graph of a finite abelian group the cosets of the generated subgroup are precisely the connected components. This applies on a torus by taking displacement classes modulo the periods. A zero displacement interpreted as a loop excludes its vertex from an independent set.

In particular, q-step coordinate and northwest-to-southeast diagonal edges on a rectangle split into q squared residue grids. The original patterns 000 and 010 are precisely the q=2 endpoint restriction, since the two forbidden triples have zero endpoints and arbitrary middle bit. For irregular domains one must include only the constraints actually present.

## 2. Full-table reconstruction

Write \(T_q(H,W;z)\) for the independence polynomial of the q-step rectangle, with uniform vertex activity z, and \(I(h,w;z)=T_1(h,w;z)\). With \(H=qh+a,\ W=qw+b,\ 0\le a,b<q\),

\[
T_q(H,W;z)=I(h,w;z)^{(q-a)(q-b)}
 I(h+1,w;z)^{a(q-b)}
 I(h,w+1;z)^{(q-a)b}
 I(h+1,w+1;z)^{ab}.
\]

Empty rectangles have independence polynomial 1. Each exponent counts the number of row and column residue classes of the specified sizes. In particular \(T_q(qh,qw;z)=I(h,w;z)^{q^2}\).

Define \(C_{ij}=T_q(q(h+i),q(w+j);z)\) for i,j in {0,1}, and \(e_{00}=(q-a)(q-b),e_{10}=a(q-b),e_{01}=(q-a)b,e_{11}=ab\). Then

\[
T_q(H,W;z)^{q^2}=\prod_{i,j=0}^1 C_{ij}^{e_{ij}}.
\]

There is a unique formal power series root with constant term 1 over the rationals; the decomposition proves that this root is an integral polynomial. For unweighted counts use the unique positive integer root. Along any one coordinate, the corresponding identity is

\[
T_q(H,qw+b;z)^q=T_q(H,qw;z)^{q-b}T_q(H,q(w+1);z)^b.
\]

In dimension d, the same proof uses the 2^d adjacent corners of the q-spaced subtable. The exponent of a corner indexed by a binary vector is the product, over coordinates, of the selected residue multiplicities a_j or q-a_j. The root degree is q^d. Thus the subtable on dimensions divisible by q determines every rectangular count and the entire independence polynomial. The result concerns uniform weights or corresponding repeated weights on isomorphic pieces; arbitrary unrelated vertex activities retain the disjoint-union product, not necessarily the corner interpolation formula.

## 3. Polyphase spectral order

Suppose \(f_i(m)=\sum_j c_{ij}\lambda_{ij}^m\) for i=1,...,k, with d_i distinct nonzero spectral roots in factor i. Put \(u_m=\prod_i f_i(m)\) and \(a_{qm+r}=u_m^{q-r}u_{m+1}^r\) for \(0\le r<q\).

Choose a multiplicity tuple alpha_i of q roots in each factor, and write \(\Lambda_\alpha=\prod_{ij}\lambda_{ij}^{\alpha_{ij}}\). The phase coefficient of this product raised to m is

\[
C_{\alpha,r}=
\prod_i\left[
\frac{q!}{\prod_j\alpha_{ij}!}
\prod_j c_{ij}^{\alpha_{ij}}
\frac{e_r(\lambda_i[\alpha_i])}{\binom qr}
\right].
\]

Here e_r is the elementary symmetric polynomial of the indicated multiset. This follows by choosing which r of the q positions are shifted in each factor. Choose beta with beta^q=Lambda and a primitive q-th root of unity omega. The ordinary scalar modes beta omega^j have amplitudes

\[
\frac1q\sum_{r=0}^{q-1}C_{\alpha,r}\beta^{-r}\omega^{-jr}.
\]

A tuple pure in every factor contributes just one mode. All other tuples contribute at most q. Hence

\[
D\le q\prod_i\binom{d_i+q-1}{q}-(q-1)\prod_i d_i.
\]

Equality holds generically for algebraically independent roots and nonzero amplitudes. Distinct tuples then have distinct Lambda monomials. In a nonpure tuple select a root with multiplicity t strictly between 0 and q. The highest exponent of this root in a normalized phase-r coefficient is min(r,t)-rt/q, uniquely maximal at r=t. Its coefficient is nonzero, since the terms of that phase share the same amplitude product and root-of-unity factor and positive combinatorial multipliers. No other phase cancels it. Thus all q Fourier modes survive. Specialized roots can collide or yield zero amplitudes; their amplitudes must be combined before testing whether a mode remains. The formula is an upper bound in such cases, not an unconditional equality.

When the bound is saturated, the q-th spectral moment is

\[
s_q=q\prod_i h_q(\lambda_i)-(q-1)\prod_i\sum_j\lambda_{ij}^q
\]

where h_q is the complete homogeneous symmetric polynomial. Counting the q roots in each mixed packet and the single root in each pure packet proves this identity.

## 4. Exact orders for the original array family

The strip transfer matrix M_w has rows and columns indexed by w-bit masks with no adjacent ones. Entry (a,b) is 1 if both a&b and (a shifted left one)&b are zero. The dimension is \(d_w=F_{w+2}\). The strip count I_w(m) is the total of the distribution obtained after m row transitions from the empty mask.

For w=1,...,5, the exact characteristic polynomials are squarefree with nonzero constant term. For odd W the preceding q=2 bound applies to M_floor(W/2) and M_ceil(W/2). For even W=2w, use degree-four multisets of roots of M_w, so the tighter upper bound is \(2\binom{d_w+3}{4}-d_w\).

There is an explicit trace law: tr M_w=1 and \(t_w=\operatorname{tr}M_w^2=(2^{w+2}-(-1)^w)/3\). A pair of mutually compatible rows is equivalent to a nonconsecutive set of occupied columns, each with two row choices. Thus t_0=1,t_1=3,t_w=t_(w-1)+2t_(w-2). For saturated odd-width spectra the second moment is \((1+t_w+t_{w+1}-t_wt_{w+1})/2\), strictly negative for w>=1.

The following collision corrections are exact.

- Width 6: the roots of M_3 consist of -1 and the four roots of x^4-2x^3-3x^2-x+1, whose product is 1. The pure root +1 is duplicated in a mixed packet x^2-1. Remove one linear factor, so 135 becomes 134 and the moment of every positive power decreases by 1.
- Widths 9 and 10: M_5 contains x^4+2x^3-2x+1, the product of x^2+(1+i)x-1 and x^2+(1-i)x-1. Both quadratic root pairs have product -1. For width 9, the 36 degree-two multisets from M_4 each duplicate a mixed packet. Remove one quadratic factor per multiset, giving 6448-72=6376. For width 10, every degree-four multiset containing the first quadratic pair has a representative replacing that pair by the second. There are binom(14,2)=91 such deleted multisets, all mixed, giving 3627-182=3445. At an even moment 2j the correction in each case is -2 times (-1)^j times h_2 of M_floor(W/2)^j; odd moments have no correction. These deductions give exact upper bounds; modular lower bounds below certify that no further collisions or cancellations reduce the degree.

The included C++ verifier uses exact modular Berlekamp-Massey on prefixes long enough to give the matching lower bounds. The upper bounds above correspond to monic integer annihilators: actual modes are algebraic integers and their Galois-invariant set has a monic integer polynomial. Reduction of a monic integer annihilator remains monic at the tested prime. The finite-prefix modular lower bound therefore also bounds the characteristic-zero degree from below.

| Width | OEIS | Exact order r | s_1 | s_2 | Minimum weighted vertices |
|---:|---|---:|---:|---:|---|
| 3 | A202485 | 30 | 1 | -3 | 31 |
| 4 | A202486 | 27 | 5 | 5 | 27 or 28 |
| 5 | A202487 | 165 | 1 | -19 | 166 |
| 6 | A202488 | 134 | 10 | 10 | 134 or 135 |
| 7 | A202489 | 1040 | 1 | -99 | 1041 |
| 8 | A202490 | 652 | 21 | 13 | 653 |
| 9 | A202491 | 6376 | 1 | -397 | 6377 |
| 10 | Same table, width 10 | 3445 | 43 | 59 | 3445 or 3446 |

Widths 3–9 use height n+2 and offset n=1, as verified against the seven pinned OEIS definitions and 115 terms in the preceding audit. No separate OEIS ID is asserted for width 10.

## 5. Integral spectral obstruction

If an r-vertex integer nonnegative adjacency A realizes a sequence of minimal order r through polynomial shifts, its characteristic polynomial must be the minimal recurrence polynomial by Cayley-Hamilton. Thus \(s_n=\operatorname{tr}(A^n)\).

Treat an integer arc weight as that number of distinguishable parallel arcs. The trace counts rooted closed edge walks of length n. Every such walk is a repetition of a unique primitive cyclic word; an orbit of least period d has d rooted representatives. Consequently

\[
s_n=\sum_{d\mid n}d\,o_d,\qquad
o_n=\frac1n\sum_{d\mid n}\mu(d)s_{n/d}\in\mathbb Z_{\ge0}.
\]

This is a necessary integral condition, stronger than nonnegative spectral moments alone. In particular \(s_2\ge s_1\): directly, the trace of A squared contains the sum of squared diagonal entries and nonnegative reciprocal-arc contributions, and integral diagonal entries satisfy a^2>=a.

For width 8, \(o_2=(13-21)/2=-4\). Hence a 652-vertex realization is impossible even though the tested moments are positive. The universal upper bound r+1 yields 653 exactly. Widths 4 and 6 have s_2=s_1, so any minimum-size candidate would necessarily have diagonal entries 0 or 1 and no mutually opposite nonzero off-diagonal arcs. This does not prove feasibility. All eight families were tested through primitive orbit length 64, leaving widths 4, 6 and 10 without a detected obstruction; absence of an obstruction is not existence.

For completeness the universal upper bound is explicit. For monic p of degree r, let M be the transpose companion with superdiagonal 1 and last row -p_j. Put w_j=1+max(0,p_(j-1)), g=w^T M, beta=1+max(0,max_j ceil(g_j/w_j)), K=beta+w_r. Embed Jx=(-w^T x,x). On r+1 coordinates define B_0=K e_0+J e_r and B_j=w_j B_0+JM e_j. Its first row is (beta,w_1 beta-g_1,...,w_r beta-g_r), last row is (1,w_1-p_0,...,w_r-p_(r-1)), and intermediate rows are unit shifts. Every entry is nonnegative. Directly BJ=JM and (B-KI)e_0=Je_r. For the marked count c(n)=(B^n)_(1,0), the impulse with Laurent function 1/p is (E-K)c. An integral target with Laurent numerator N is N(E)(E-K)c. This gives r+1 without division, and proves all the sharp minima where an r-vertex obstruction is present.

## 6. An infinite class of sharp examples

Choose k>=2 distinct primes p_i congruent to 1 modulo 4 and D_i=(p_i-1)/4. Let M_i=[[1,D_i],[1,0]], f_i(m)=tr(M_i^m), u_m=product_i f_i(m), and a_(2m)=u_m^2, a_(2m+1)=u_m u_(m+1).

The two eigenvalues in each field have sum 1, product -D_i and different magnitudes. In the multiquadratic compositum, conjugations may independently flip each prime square root. The three degree-two choices from each factor give 3^k distinct joint products: flipping just a differing field in an alleged equality would force the ratio of its two distinct choices to be equal to its inverse, impossible by their different magnitudes. For a mixed tuple the squared ratio of the phase-one amplitude to beta times the phase-zero amplitude is the product over mixed factors of -1/(4D_i), with absolute value below one. Neither of the two Fourier modes cancels. Pure tuples contribute one each. Therefore

\[
r=2\cdot3^k-2^k,\qquad
s_2=2\prod_i(1+D_i)-\prod_i(1+2D_i)<0.
\]

The last inequality follows from (1+D_i)/(1+2D_i)<=2/3 and k>=2. The exact minimum is r+1 for every such family. There are arbitrarily many distinct primes 1 modulo 4: an odd prime divisor of (2 product p_i)^2+1 is new and congruent to 1 modulo 4. The modular verifier corroborates k=2 through 6 (minimum sizes 15,47,147,455,1395).

## 7. Direct graph counts, without spectral subtraction

The optimal spectral graph may contain large arc weights. There is a different, direct construction with small weights, a single source and terminal, and no signed taps. For width W=qw+b, one row-residue group contains q-b strips of width w and b strips of width w+1.

For each multiplicity k of identical strips, take the ordered tensor of k row-state automata and identify tuples differing by a permutation. This partition is equitable for outgoing weights: permuting the source permutes the ordered target transitions with identical weights. The quotient states are multisets, with adjacency weights equal to the sum over all ordered target assignments from one representative. Starting with all empty masks and summing the resulting distribution gives exactly the product of the k strip counts. Thus the row-group state count is

\[
D=\binom{d_w+q-b-1}{q-b}\binom{d_{w+1}+b-1}{b}.
\]

Use q copies of this row-group state space. The directed graph has tuple vertices (v_1,...,v_q); one step advances v_1 along its row-group transition and rotates it to the end, (v_2,...,v_q,v'_1). Start at the all-empty tuple. After H=qh+a steps, exactly a row groups have advanced h+1 times and the others h times. The sum over all terminal tuples is therefore precisely T_q(H,W;z). Add a single sink and one unit arc from every tuple to it. With c the single marked walk count from the all-empty tuple to that sink,

\[
c(H+1)=T_q(H,W;z).
\]

For z=1 the graph has D^q+1 vertices and nonnegative integral arcs. For positive integral z the row weight z^(number of selected bits) also realizes the weighted polynomial value. For q=2 and odd W no identical-strip quotient is needed; all arcs have weight one, with loops permitted. Even W uses at most weight two in this construction. The original OEIS offset gives a(n)=c(n+3). This is a direct enumeration upper bound, not a competing minimum proof.

| Width | Row-group states D | Direct graph vertices | Maximum arc weight |
|---:|---:|---:|---:|
| 3 | 6 | 37 | 1 |
| 4 | 6 | 37 | 2 |
| 5 | 15 | 226 | 1 |
| 6 | 15 | 226 | 2 |
| 7 | 40 | 1601 | 1 |
| 8 | 36 | 1297 | 2 |
| 9 | 104 | 10817 | 1 |
| 10 | 91 | 8282 | 2 |

## 8. Reproduction and boundaries

Run the following from the repository root:

```sh
c++ -O3 -std=c++17 tools/check_lattice_polyphase_orders.cpp -o /tmp/check_lattice_polyphase_orders
/tmp/check_lattice_polyphase_orders
python tools/check_lattice_polyphase_spectra.py  # requires SymPy
python tools/check_direct_lattice_graph.py     # standard library only
```


The retained predecessor replay matched both reports exactly. The new checks independently compare 416 direct walk counts, 441 interpolation identities, 324 exhaustive small weighted array counts, and 512 primitive orbit counts. The audit JSON gives exact traces, bounds, and direct graph parameters. The large graphs are specified by their constructive rules, not stored densely. A trial of equitable partition refinement on the q=2 even-width direct tuple graphs yielded no further quotient merging; this does not rule out other positive realizations.

The remaining weighted minima for widths 4, 6 and 10 are unresolved by one vertex. Original OEIS attribution: R. H. Hardin, The On-Line Encyclopedia of Integer Sequences, OEIS Foundation Inc., official export commit c5bd71de9eee0894df1301baa4f43f6431d8a08d. This continuation does not copy additional reference terms or claim new corpus coverage. Literature novelty, evaluation speedups and Lean formalization remain open. Code is governed by the host repository license.
