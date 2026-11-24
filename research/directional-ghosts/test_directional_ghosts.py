#!/usr/bin/env python3
"""Finite exact regressions for directional ghosts and Frobenius quotients.

Author: Komorebi P. Run: python -m unittest -v test_directional_ghosts.py
This is a small public regression subset, not a Lean proof or a novelty audit.
"""
import itertools
import math
import unittest


def monomials(d, D):
    for alpha in itertools.product(range(D + 1), repeat=d):
        if 0 < sum(alpha) <= D:
            yield alpha


def valuation(n, p):
    if n == 0:
        return math.inf
    n = abs(n)
    v = 0
    while n % p == 0:
        v += 1
        n //= p
    return v


def ambiguity(W, p, k, h, D):
    """Return log_p(fiber size), blind coefficient count and lattice layers."""
    d = len(W[0])
    layers = [0] * k
    blind = 0
    exponent = 0
    for a in monomials(d, D):
        eigen = [sum(w[j] * a[j] for j in range(d)) for w in W]
        e = min(k, max(0, min(valuation(v, p) for v in eigen) - h))
        exponent += e
        blind += e > 0
        for s in range(h + 1, h + k + 1):
            layers[s - h - 1] += all(v % (p ** s) == 0 for v in eigen)
    return exponent, blind, layers


def multiply(a, b, modulus):
    N = len(a) - 1
    return [sum(a[i] * b[n - i] for i in range(n + 1)) % modulus
            for n in range(N + 1)]


def quotient(a, b, modulus):
    """Formal quotient a/b through degree N with b(0)=1."""
    assert len(a) == len(b) and b[0] == 1
    N = len(a) - 1
    c = [0] * (N + 1)
    for n in range(N + 1):
        c[n] = (a[n] - sum(b[j] * c[n - j] for j in range(1, n + 1))) % modulus
    return c


def substitute(a, q):
    N = len(a) - 1
    return [a[n // q] if n % q == 0 else 0 for n in range(N + 1)]


def frobenius_quotient(a, q, modulus):
    return quotient(a, substitute(a, q), modulus)


def frobenius_inverse(b, q, modulus):
    N = len(b) - 1
    result = [1] + [0] * N
    power = 1
    while power <= N:
        result = multiply(result, substitute(b, power), modulus)
        power *= q
    return result


def ghost(a, modulus):
    numerator = [n * a[n] % modulus for n in range(len(a))]
    return quotient(numerator, a, modulus)


def partitions(N):
    counts = [1] + [0] * N
    for m in range(1, N + 1):
        for n in range(m, N + 1):
            counts[n] += counts[n - m]
    return counts


class ExactRegression(unittest.TestCase):
    def test_sharp_multivariate_example(self):
        p, k, h, D = 2, 3, 0, 10
        self.assertEqual(ambiguity([[1, 1]], p, k, h, D)[:2], (58, 35))
        self.assertEqual(ambiguity([[1, 0], [0, 1]], p, k, h, D),
                         (27, 20, [20, 5, 2]))
        self.assertEqual(ambiguity([[1, 1], [1, -1]], p, k, h, D)[:2],
                         (46, 35))

    def test_mixed_observation_precisions_and_source_lifts(self):
        # Source precision is 4; the x derivative is observed mod 4,
        # while the y derivative is independently observed mod 8.
        # Candidate source reductions must admit a compatible mod-8 lift.
        p, k, D = 2, 2, 2
        weights = ((1, 0), (0, 1))
        extra = (0, 1)
        indices = tuple(monomials(2, D))
        matching_reductions = set()
        lifts = 0
        for values in itertools.product(range(8), repeat=len(indices)):
            coefficients = dict(zip(indices, values))
            compatible = all(
                (sum(w[j] * a[j] for j in range(2)) * value)
                % (p ** (k + h)) == 0
                for w, h in zip(weights, extra)
                for a, value in coefficients.items()
            )
            if compatible:
                lifts += 1
                matching_reductions.add(tuple(x % (p ** k)
                                              for x in values))

        self.assertEqual(lifts, 16)
        self.assertEqual(len(matching_reductions), 2)
        self.assertEqual({
            tuple(x for x in reduction if x != 0)
            for reduction in matching_reductions}, {(), (2,)})
        # The only blind index is (2,0). Without the higher-precision
        # y measurement, (0,2) would also remain blind.
        def valuation_excess(alpha):
            return min(k, max(0, min(
                valuation(sum(w[j] * alpha[j] for j in range(2)), p) - h
                for w, h in zip(weights, extra)
            )))
        self.assertEqual({a: valuation_excess(a) for a in indices},
                         {a: (1 if a == (2, 0) else 0) for a in indices})

    def test_nonuniform_precision_nonlinear_ghost_fibers(self):
        # Compare ALL source reductions against their actual nonlinear
        # directional logarithmic derivatives, not just against kernel tests.
        # A = 1 + a01*y + a02*y^2 + a10*x + a11*x*y + a20*x^2.
        # The x-ghost is read modulo 4 and the y-ghost modulo 8.
        from collections import defaultdict
        fibers = defaultdict(set)
        for a01, a02, a10, a11, a20 in itertools.product(
                range(8), repeat=5):
            x_ghost = (a10 % 4,
                       (a11 - a10*a01) % 4,
                       (2*a20 - a10*a10) % 4)
            y_ghost = (a01 % 8,
                       (a11 - a01*a10) % 8,
                       (2*a02 - a01*a01) % 8)
            source_reduction = (a01 % 4, a02 % 4, a10 % 4,
                                a11 % 4, a20 % 4)
            fibers[(x_ghost, y_ghost)].add(source_reduction)
        self.assertEqual(len(fibers), 2048)
        self.assertEqual({len(fiber) for fiber in fibers.values()}, {2})

    def test_full_rank_optimal_bound(self):
        for p in (2, 3, 5):
            for D in range(1, 15):
                for k in (1, 2, 3):
                    predicted = [math.comb(D // (p ** s) + 2, 2) - 1
                                 for s in range(1, k + 1)]
                    self.assertEqual(
                        ambiguity([[1, 0], [0, 1]], p, k, 0, D)[2],
                        predicted)
                    self.assertGreaterEqual(
                        ambiguity([[1, 1]], p, k, 0, D)[0],
                        sum(predicted))

    def test_frobenius_quotient_inversion(self):
        for modulus in (2, 4, 9, 25):
            for N in (6, 12, 22):
                a = [1] + [(n * n + 3 * n + 1) % modulus
                           for n in range(1, N + 1)]
                for q in (2, 3, 5):
                    b = frobenius_quotient(a, q, modulus)
                    self.assertEqual(frobenius_inverse(b, q, modulus), a)
                    left = ghost(b, modulus)
                    g = ghost(a, modulus)
                    sq = substitute(g, q)
                    self.assertEqual(
                        left, [(g[n] - q * sq[n]) % modulus
                               for n in range(N + 1)])

    def test_partition_polyphase(self):
        N, modulus = 28, 10**25
        P = partitions(N)
        for q in (2, 3, 4, 5):
            left = frobenius_quotient(P, q, modulus)
            bounded = [1] + [0] * N
            for m in range(1, N + 1):
                factor = [0] * (N + 1)
                for j in range(q):
                    if j * m <= N:
                        factor[j * m] = 1
                bounded = multiply(bounded, factor, modulus)
            self.assertEqual(left, bounded)

    def test_exact_univariate_ghost_fibers_and_rescue_coordinates(self):
        # Exhaust every unit series of degree <=4 modulo 4, not just one example.
        from collections import defaultdict
        fibers = defaultdict(list)
        for coeffs in itertools.product(range(4), repeat=4):
            a = [1, *coeffs]
            fibers[tuple(ghost(a, 4))].append(a)
        self.assertEqual(len(fibers), 32)
        self.assertEqual({len(fiber) for fiber in fibers.values()}, {8})

        # Blind coefficients at degrees 2 and 4 in the invertible
        # Frobenius/polyphase quotient provide genuinely separating coordinates.
        for fiber in fibers.values():
            rescue_values = [
                tuple(frobenius_quotient(a, 2, 4)[n] for n in (2, 4))
                for a in fiber
            ]
            self.assertEqual(len(set(rescue_values)), len(fiber))

        # Observe the same ghost at higher precision and count projected
        # source reductions modulo 4, as in the worked example.
        raised_precision = defaultdict(set)
        for coeffs in itertools.product(range(8), repeat=4):
            a = [1, *coeffs]
            raised_precision[tuple(ghost(a, 8))].add(
                tuple(value % 4 for value in a))
        self.assertEqual({len(fiber) for fiber in
                          raised_precision.values()}, {2})

    def test_query_fiber_dependence_on_base_source(self):
        # Enumerate the entire kernel of both coordinate Euler derivatives
        # over Z/4 through total degree 4 (rather than one illustrative value).
        p, k, D = 2, 2, 4
        modulus = p ** k
        blind = []
        for alpha in monomials(2, D):
            e = min(k, max(0, min(valuation(n, p) for n in alpha)))
            if e > 0:
                blind.append((alpha, e))
        self.assertEqual(len(blind), 5)
        choices = [range(0, modulus, p ** (k - e)) for _, e in blind]
        queried_unit = set()
        queried_mixed = set()
        count = 0
        for values in itertools.product(*choices):
            C = {(0, 0): 1}
            C.update({alpha: value for (alpha, _), value
                      in zip(blind, values)})
            # Vanishing coordinate derivatives certify that these C
            # have the same two ghost observations.
            for alpha, value in C.items():
                self.assertEqual(alpha[0] * value % modulus, 0)
                self.assertEqual(alpha[1] * value % modulus, 0)
            queried_unit.add(C.get((3, 1), 0) % modulus)
            # Multiplication by A0=1+xy adds the shifted x^2 coefficient.
            queried_mixed.add((C.get((3, 1), 0)
                               + C.get((2, 0), 0)) % modulus)
            count += 1
        self.assertEqual(count, 128)
        self.assertEqual(queried_unit, {0})
        self.assertEqual(queried_mixed, {0, 2})


if __name__ == "__main__":
    unittest.main()
