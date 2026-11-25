# Parity factorization of forbidden-pattern arrays

**Author: Komorebi P.**  
**Status:** written all-index proof and independently reconstructed exact computational certificates. No Lean verification or literature-priority claim.

The principal result is a reduction from constraints on triples of binary cells to independent sets on four smaller graphs. It applies to every rectangular size, not just to a finite sequence prefix. This also gives short closed forms for the two previously studied high-order sequence models, A202485 and A202487, and all the neighboring widths A202486–A202491.

## 1. General theorem

Let \(T(H,W)\) count binary \(H\times W\) arrays in which the patterns 000 and 010 are forbidden along each row, column and northwest-to-southeast diagonal. All rectangles have open boundaries. Let \(I(h,w)\) count independent sets on the rectangular grid with edges in the horizontal, vertical and northwest-to-southeast directions. Define \(I(0,w)=I(h,0)=1\).

Put

\[
h=\lfloor H/2\rfloor,\quad h'=\lceil H/2\rceil,
\qquad
w=\lfloor W/2\rfloor,\quad w'=\lceil W/2\rceil.
\]

Then

\[
T(H,W)=I(h,w)I(h,w')I(h',w)I(h',w').
\]

**Proof.** A triple is forbidden exactly when both endpoints are zero, regardless of the middle bit. Associate a graph vertex to each cell and connect cells differing by twice a permitted unit direction. A valid array is equivalent to an independent set of zero cells in this graph. Every edge preserves both coordinate parities. The four coordinate parity classes are disjoint induced subgraphs, and dividing their coordinate differences by two yields the four stated rectangular grid graphs. Independent sets on a disjoint union are independently chosen, so their counts multiply. This proof includes empty parity classes and all boundary cases.

In particular,

\[
T(H,2k+1)^2=T(H,2k)T(H,2k+2)
\]

for \(k\ge 0\), and

\[
T(2h,2w)=I(h,w)^4.
\]

The corresponding identities hold with the two dimensions interchanged. More generally, for any finite set of lattice directions, a binary pattern restriction equivalent to excluding two zero endpoints at distance \(q\) along each direction decomposes into residue classes modulo \(q\) in each coordinate. The same disjoint-union proof applies, including nonrectangular domains with induced edges. This does not apply to arbitrary forbidden triples whose middle bit matters.

## 2. Reduced transfer matrices and generating functions

Let \(I_w(m)=I(m,w)\). A row state is a \(w\)-bit mask \(a\) of selected vertices with no consecutive ones. For two consecutive rows \(a,b\), compatibility means \(a\mathbin{\&}b=0\) and \((a\ll1)\mathbin{\&}b=0\). Let \(M_w(a,b)\) be 1 when compatible and 0 otherwise. For \(m\ge1\),

\[
I_w(m)=\mathbf1^{T}M_w^{m-1}\mathbf1.
\]

Thus the ordinary generating function is \(1+x\mathbf1^{T}(I-xM_w)^{-1}\mathbf1\). The number of row states is \(F_{w+2}\), rather than the original unreduced two-row history dimension. For widths 1, 2 and 3, order the masks as \((0,1)\), \((0,1,2)\), \((0,1,2,4,5)\), respectively. The matrices are

\[
M_1=\begin{pmatrix}1&1\\1&0\end{pmatrix},\quad
M_2=\begin{pmatrix}1&1&1\\1&0&0\\1&1&0\end{pmatrix}.
\]

\[
M_3=\begin{pmatrix}
1&1&1&1&1\\
1&0&0&1&0\\
1&1&0&0&0\\
1&1&1&0&0\\
1&0&0&0&0
\end{pmatrix}.
\]

Write \(f_m=I_1(m)\), \(p_m=I_2(m)\), \(q_m=I_3(m)\). Direct evaluation of the resolvents gives

\[
F(x)=\frac{1+x}{1-x-x^2},\qquad f_m=F_{m+2},
\]

\[
P(x)=\frac{(1+x)^2}{1-x-2x^2-x^3},
\]

\[
Q(x)=\frac{1+4x+3x^2-x^4}{1-x-5x^2-4x^3+x^5}.
\]

The Fibonacci convention is \(F_0=0,F_1=1\); the use of \(F(x)\) for the first generating function is independent of the subscripted Fibonacci numbers.

## 3. Exact OEIS transfers

For \(n\ge1\) put

\[
h=1+\lfloor n/2\rfloor,\quad k=1+\lceil n/2\rceil.
\]

Then

\[
a_{202485}(n)=f_hf_kp_hp_k,
\]

\[
a_{202487}(n)=p_hp_kq_hq_k.
\]

The table of widths extends without new fitting: for width \(W\) the formula is \(T(n+2,W)\) from section 1. The seven consecutive IDs A202485–A202491 correspond to widths 3–9. In particular, the exact cross-sequence transfer

\[
a_{202487}(n)^2=a_{202486}(n)a_{202488}(n)
\]

holds at every \(n\ge1\), as does the analogous width-seven identity involving A202488, A202489 and A202490.

The reduced recurrences have orders 2, 3 and 5. They replace the much larger scalar recurrences by smaller composable state spaces. The original minimal scalar recurrence orders remain 30 for A202485 and 165 for A202487; this is a different statement from reducing the minimal scalar order itself.

## 4. Direct integer formula

The algebraic roots can be avoided entirely. Set \(B=2^{8n+24}\). For \(m=h,k\), define

\[
f_m=\left\lfloor\frac{B^{m+1}(B+1)}{B^2-B-1}\right\rfloor\bmod B,
\]

\[
p_m=\left\lfloor\frac{B^{m+1}(B+1)^2}
{B^3-B^2-2B-1}\right\rfloor\bmod B,
\]

\[
q_m=\left\lfloor\frac{B^{m+1}(B^4+4B^3+3B^2-1)}
{B^5-B^4-5B^3-4B^2+1}\right\rfloor\bmod B.
\]

Multiply the four appropriate factors in section 3. The remainder always means the least nonnegative remainder. Both factors are retained when \(h=k\).

**Proof of digit extraction.** Each coefficient \(u_i=I_w(i)\) is between 0 and \(2^{wi}\). For \(w\le3\), \(m\le n+2\), and the stated \(B\), all coefficients through index \(m\) are less than \(B\), while the remaining tail in \(B^m\sum_{i\ge0}u_i B^{-i}\) is bounded by \(8^{m+1}/(B(1-8/B))<1\). Taking the floor and reducing modulo \(B\) therefore gives exactly \(u_m\). Substitution of the three rational generating functions yields the displayed quotients. The final product is below \(B\) as well, since \(T(n+2,W)\le2^{5(n+2)}\) for \(W=3,5\). Thus reducing the product modulo \(B\) is also valid.

At \(n=8\) we have \(h=k=5\) and \((f_5,p_5,q_5)=(13,60,387)\). The respective values are \(608400\) and \(539168400\).

This is a closed floor-and-remainder form, using a standard coefficient-packing principle. It does not establish a new general coefficient-packing algorithm or a bit-complexity advantage. Reduced transfer matrix powering is another exact evaluation method.

## 5. Exact minimal orders and graph-size connection

A product of the two reduced strip states has dimension \(d=2\cdot3\) or \(d=3\cdot5\). Its tensor square and a two-phase clock give a linear realization of dimension at most \(D=2d^2\), namely 72 or 450. To see this, at odd \(n=2t+1\) the output is \(u_{t+1}u_{t+2}\), and at even \(n=2t+2\) it is \(u_{t+2}^2\), where \(u_m=f_mp_m\) or \(u_m=p_mq_m\). Both outputs are linear functionals on the tensor square of the state at \(m=t+1\); the state advances after each pair of outputs.

The reproduction program reconstructs the monic integer annihilators by modular Berlekamp–Massey and CRT. It tests \(D\) consecutive zero residuals with exact integers. The residual sequence itself has a realization of dimension at most \(D\), so Cayley–Hamilton proves that all later residuals vanish. The modular minimal degrees at the checked primes provide matching lower bounds: any rational recurrence can be cleared to a primitive integer polynomial, which has a nonzero reduction at every prime. Hence the two orders are exactly 30 and 165, not empirical fits.

There is an additional sharp graph realization result. For the monic minimal annihilator \(p(x)=x^r+\sum_{j=0}^{r-1}p_jx^j\), let \(M\) be its transpose companion (unit superdiagonal, last row \(-p_j\)). Define \(w_j=1+\max(0,p_{j-1})\), \(g_j=(w^TM)_j\), and

\[
\beta=1+\max(0,\max_j\lceil g_j/w_j\rceil),\qquad K=w_r+\beta.
\]

With \(Jx=(-w^Tx,x)\), define a nonnegative integer adjacency \(B\) on \(r+1\) vertices by its columns \(B_0=K e_0+Je_r\) and \(B_j=w_jB_0+JM e_j\), where the embedded and companion coordinate vectors have their respective dimensions. The first row is \((\beta,w_1\beta-g_1,\ldots,w_r\beta-g_r)\), the last row is \((1,w_1-p_0,\ldots,w_r-p_{r-1})\), and all intermediate rows are unit shifts. These entries are nonnegative by construction. The identities \(BJ=JM\) and \((B-KI)e_0=Je_r\) follow directly. For the raw marked walk \(c(n)=(B^n)_{1,0}\),

\[
U_p(n)=c(n+1)-Kc(n).
\]

Here \(U_p\) is the canonical impulse with initial vector \((0,\ldots,0,1)\). If the Laurent generating function of a zero-based target is \(N(x)/p(x)\), then the target is \(N(E)(E-K)c\), with \(E\) the forward shift. For the OEIS targets here the zero-based target is \(a(n+1)\). This construction is valid for any monic integer recurrence and uses no division of sequence values.

For these two array models, the trace of the square of any hypothetical \(r\)-vertex realization would be negative (Newton's identity \(q_1^2-2q_2\), where \(q_j\) are the ascending ordinary denominator coefficients). Nonnegative adjacency matrices have nonnegative traces of positive powers. A graph on fewer than \(r\) vertices cannot generate a minimal recurrence of order \(r\) using fixed polynomial shifts. The construction therefore attains the exact minima 31 and 166 in the class of single marked counts of nonnegative integer weighted directed graphs with fixed integral polynomial shifts. This is not a minimum-size result for simple undirected graphs, or for the original arrays themselves.

## 6. Reproduce and audit

From the repository root, using Node.js 18 or later with no dependencies:

```sh
node tools/check_parity_array_transfer.mjs
```


The script includes the pinned official OEIS prefixes, brute-force checks of small original arrays, reduced row-transfer enumeration, exact floor formulas, three-prime recurrence reconstruction, all-index residual certificates, and direct verification of the weighted-graph intertwining columns. It emits the full ordinary rational numerators and denominators, as well as the graph parameters and check counts. The attached audit JSON is the result of running the same functions before publication.

This note consolidates the array-related development from the retained v19 parser and v20 rational index through v29 sharp graph realization. It supersedes informal descriptions that did not specify the reduced grid edges or distinguish the offset \(n=1\) from a zero-based recurrence. The predecessor archives remain separate. Their SHA-256 values are:

- v19: `8dc644717bf2ef48966786183dbba18b65a85c89db76a4dcc7f4c4afdce405be`
- v20: `595160957b7d4b4e65b8f6f902e59bb32481410076a99e871478254ba471473d`
- v29: `b1d16a4b9e1c049e46602b81650a759cc6ede0e1b735cc9cf47cf06a1ed5cf12`

## 7. Attribution and scope

The original sequence definitions and reference values are credited to R. H. Hardin and The On-Line Encyclopedia of Integer Sequences, OEIS Foundation Inc. See [A202485](https://oeis.org/A202485), [A202487](https://oeis.org/A202487) and the adjacent entries. The reference data are retained under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). The source is the official [OEIS GitHub export](https://github.com/oeis/oeisdata), pinned to commit c5bd71de9eee0894df1301baa4f43f6431d8a08d. The live A202487 page returned HTTP 403, but its official source record was accessible and independently verified, including its mathematical offset. Independent Komorebi code follows the host repository's code license.

The parity bijection and graph construction are written mathematical proofs. Finite computational checks corroborate them and verify source identification. Literature novelty, peer review, Lean formalization, and a comprehensive global OEIS integration are outside this note's scope.

## Lattice and spectral generalization

[Read the lattice factorization, polyphase spectra and sharp graph realization continuation](LATTICE_POLYPHASE_GRAPH.md). It extends the exact recurrence orders through width ten, closes five weighted minima using integer spectral obstructions, and gives a direct cyclic graph construction and full-table independence-polynomial reconstruction theorem.
