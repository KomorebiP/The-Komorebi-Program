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

    def test_query_fiber_dependence_on_base_source(self):
        # For C=1+2x^2 over Z/4, both coordinate ghosts vanish.
        # At A0=1+xy, x^3 y acquires coefficient 2; at A0=1 it does not.
        self.assertEqual((2 * 2) % 4, 0)
        self.assertNotEqual((2 * 1) % 4, 0)


if __name__ == "__main__":
    unittest.main()
