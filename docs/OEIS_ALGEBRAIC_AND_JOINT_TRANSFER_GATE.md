# Algebraic generating functions and joint recurrence transfers

**Author: Komorebi P.**
**Published:** 23 November 2026.
**Scope:** bounded, exact, source-conditional proof automation. No claim of new classical identities, unconditional OEIS identifications, whole-corpus coverage, or measured speedups.

## Algebraic generating functions

Let `P(x,y)` be a polynomial over the rationals, let `P(0,a0)=0`, and require `P_y(0,a0) != 0`. There is exactly one formal series `A` with constant coefficient `a0` and `P(x,A)=0`. Indeed, for each k >= 1, the coefficient of x^k in P(x,A) is `P_y(0,a0) a_k` plus an expression determined by earlier coefficients. Recursively setting it to zero proves existence and uniqueness. Reported source terms are checked against this construction, not used as an infinite identity test.

For the differential derivation require additionally that P and P_y be coprime over Q(x)[y]. In the finite algebra `Q(x)[y]/(P)`, differentiation is induced by

\[
D=\partial_x - (P_x/P_y)\partial_y.
\]

The inverse of P_y is computed and checked modulo P. Each derivative of y reduces to a vector in a space of dimension deg_y(P). Exact linear dependence of the constant vector and derivative vectors supplies a polynomial-coefficient inhomogeneous differential equation `sum_j q_j(x) A^(j)(x) = H(x)`. The quotient remainder is checked to be identically zero. The constant vector improves the order of the derived operator, with no claim of minimality. Rational functions in x may have poles at zero during elimination: the identity is interpreted in Q((x)) and the final cleared operator is polynomial. The nonsingular branch remains a formal power series.

For a monomial term `q[j,k] x^k D^j`, coefficient extraction at t >= 0 gives `q[j,k] (t-k+j)_falling_j a_(t-k+j)`. Negative sequence indices are zero. When t<k but t-k+j>=0, the falling factorial contains zero, so the expression is valid even at these boundary indices. Let `lo` be the smallest shift j-k after aggregation, and write t=n-lo. With n>=max(0,lo), all remaining indices are nonnegative. The polynomial forcing vanishes at t>deg(H); the recurrence is normalized only after proving its leading coefficient is nonzero on the admitted integer tail. Guard failures retain the excluded prefix. Seeds for the recurrence are derived from the formal branch.

Examples (indices n>=0):

* A000108: `(n+2) C(n+1) = (4n+2) C(n)`.
* A001006: `(n+4) M(n+2) = (2n+5) M(n+1) + 3(n+1) M(n)`.
* A006318: `(n+3) S(n+2) = (6n+9) S(n+1) - n S(n)`.

All three are derived from the selected implicit ordinary generating functions, without importing their recurrences.

## Exact composition and canonical family normal form

For a rational substitution phi regular at zero with phi(0)=0, and regular rational g,h, consider `B(x)=g(x) A(phi(x))+h(x)`. The certificate requires the target equation evaluated at `g*y+h` to have zero remainder modulo `P(phi(x),y)` over Q(x)[y], and the target branch's constant coefficient to agree. Uniqueness of the target formal branch completes the proof. This is stronger than agreement of truncated power series. The template search is bounded and is not a complete rational substitution solver.

A general recognizable family needs no substitution guessing. Suppose

\[
A=1+u(x)A+v(x)A^d,\qquad u(0)=v(0)=0,\quad d\ge2.
\]

Define the Fuss-Catalan series `F_d(z)=1+z F_d(z)^d`, with `F_d(0)=1`. Set `B=(1-u)A`. Direct substitution gives

\[
A(x)=\frac{1}{1-u(x)}F_d\!\left(\frac{v(x)}{(1-u(x))^d}\right).
\]

This is an exact identity by simple-branch uniqueness. The compiler recognizes the polynomial family, computes the substitution and prefactor and checks the symbolic substitution residual. If `u=a*x` and `v=b*x^s`, Lagrange inversion of `W=z(1+W)^d` gives `[z^k] F_d = binom(dk,k)/((d-1)k+1)`, including k=0. Expansion of `(1-a*x)^(-dk-1)` gives the finite-sum normal form

\[
[x^n]A=\sum_{k=0}^{\lfloor n/s\rfloor}
\frac{\binom{dk}{k}}{(d-1)k+1}b^k a^{n-sk}\binom{n-sk+dk}{dk}.
\]

The theorem allows general rational or formal u,v regular at zero, while the implemented family recognizer accepts bounded polynomial u,v. The code also tests the cubic case and polynomial u,v without claiming an explicit monomial finite sum for the latter.

For d=2, this gives Motzkin and large Schroeder as Catalan transforms:

\[
M(x)=\frac{C(x^2/(1-x)^2)}{1-x},\qquad
S(x)=\frac{C(x/(1-x)^2)}{1-x}.
\]

The coefficient identities are `M(n)=sum_k binom(n,2k) C(k)` (0<=k<=floor(n/2)) and `S(n)=sum_k binom(n+k,2k) C(k)` (0<=k<=n).

## Multiple-input recurrence hyperedges

For specified affine lanes m_i*n+r_i, let source i's order-d_i state be V_i(n) with recurrence transition matrix B_i(n). Use the direct sum of all source states. A candidate output has the form

\[
T(n)=\sum_i g_i(n)V_i(n).
\]

Reduce all shifted outputs into each source state and substitute them into the target recurrence. The residual must vanish independently in every block, not merely on one numerical seed. Solve the resulting exact rational coefficient equations and the target initial-state equations simultaneously. Clear denominators symbolically before equating coefficients. For each block of unknown polynomial coefficients, require a nonzero block. If a canonical free-zero solution omits a block, search for an exact homogeneous-nullspace direction with a nonzero component there. Each already-active block forbids at most one scalar along that direction, so finitely many integer choices suffice to activate a block without cancelling previous blocks. This yields completeness for the prescribed polynomial ansatz, independent-state obligations, and search caps, not all possible sequence identities.

A nonzero block need not be an indispensable source. Redundancy and dependencies among input states can require further analysis; the checker deliberately assumes independent states for the recurrence residual proof. Initial-state agreement and nonsingular induction yield the all-index tail identity.

## Automatic source selection by spectral covers

For a constant-coefficient recurrence companion A with initial state v, find the first dependence among `v, Av, ..., A^d v`. Its monic polynomial p is the exact minimal annihilator of the cyclic state, not a guessed recurrence. Indeed, applying A repeatedly propagates the dependence. The first state coordinate observes the full consecutive state via d consecutive observations, so the sequence has the same minimal annihilator on the defined tail. A sum of shifted source sequences is annihilated by the least common multiple of the source minimal polynomials. A necessary condition for a constant-coefficient shift representation of the target is that its minimal polynomial divide this LCM. The algorithm computes gcds with the target and searches bounded inclusion-minimal covers of two to four inputs. Repeated factors are handled by multiplicities in the LCM, never by adding multiplicities. It is a prefilter, not an identity proof. The full residual-and-seed checker must accept every proposed edge. Search caps and original nonminimal recurrence profiles can exclude feasible edges.

For A001045 the exact target polynomial is `(z-2)(z+1)`. The algorithm chooses A000079, with `z-2`, and A033999, with `z+1`, then solves the initial state and certifies `J(n) = (2^n-(-1)^n)/3`. Neither individual source admits the tested polynomial shift ansatz into this target.

## Reproduction

Requires Python and SymPy 1.14.0 (mpmath 1.3.0). SymPy is supplied only validated, constructed rational polynomials. No raw OEIS expression is passed to eval, exec, or sympify. The recurrence gates remain dependency-free. The algebraic and joint-transfer test directory is separate so the standard-library workflows do not unintentionally run tests requiring symbolic algebra.

```sh
python -m pip install sympy==1.14.0 mpmath==1.3.0
PYTHONPATH=tools python -B -m unittest discover -s tools -p 'test_oeis*.py' -v
PYTHONPATH=tools python -B -m unittest discover -s research/sequence-proof-stage5/tests -v
python -B tools/oeis_algebraic_gate.py --oeis-root fixtures/oeis_stage5 --plan fixtures/oeis_stage5/plan.json --output stage5.json
python -B tools/oeis_algebraic_gate.py --oeis-root fixtures/oeis_stage5 --plan fixtures/oeis_stage5/plan.json --output stage5.json --verify-report
```

The six selected source excerpts preserve the original `%S`, `%F`, `%O` lines. The full-source plan requires the exact official Git blob and selected original formula line at the pinned revision. Source: The Online Encyclopedia of Integer Sequences, OEIS Foundation Inc., CC BY-SA 4.0. Excerpts are not whole records; the two modes intentionally have distinct source hashes. The integrated [algebraic and joint-transfer verification](https://github.com/KomorebiP/The-Komorebi-Program/actions/runs/45325359130/job/138213522547) passed all 21 tests and replayed the six full records at their pinned revision. The full-record audit reproduced one joint certificate, two composition certificates, three family normal forms and three finite-sum normal forms. It does not harvest the full corpus.

Current bounds: ordinary zero-offset algebraic generating functions, simple formal branches, squarefree polynomial quotient, bounded polynomial degree and recurrence order, at most four inputs and bounded recurrence state dimensions. Non-simple branches, arbitrary P-recursive operator factorization, D-finite closure, telescoping, general nonlinear multi-input identities, global cost minimization, complete corpus scheduling, and unconditional source identification remain outside this gate. All results stay in a separate conditional overlay. No change is made to the public Sequence Network.
