"""Exact integer tests for Cycle–Path Walk Transfers. Author: Komorebi P."""
from math import comb


def walks(size, steps, start, cycle=False):
    """All destinations from start, for lengths 0 through steps."""
    row = [int(i == start) for i in range(size)]
    out = [row]
    for _ in range(steps):
        row = [
            (row[(i - 1) % size] if cycle or i > 0 else 0)
            + (row[(i + 1) % size] if cycle or i + 1 < size else 0)
            for i in range(size)
        ]
        out.append(row)
    return out


def chebyshev2(d):
    """Integer coefficients of 2*T_d(x/2), ascending powers."""
    a, b = [2], [0, 1]
    for _ in range(d):
        a, b = b, [
            (b[i - 1] if i else 0) - (a[i] if i < len(a) else 0)
            for i in range(len(b) + 1)
        ]
    return a


def apply(poly, seq, k):
    return sum(c * seq[k + j] for j, c in enumerate(poly))


def main():
    counts = dict(doubling=0, endpoints=0, entries=0, inverse=0, seed=0)
    for m in range(3, 31):
        a = [r[0] for r in walks(m, 2*m + 48, 0, True)]
        c = [r[0] for r in walks(2*m, 4*m + 48, 0, True)]
        reconstructed = [0] * len(c)
        for h in range((len(c) + 1)//2):
            reconstructed[2*h] = sum(comb(h, j)*2**(h-j)*a[j] for j in range(h+1))
        for x, y in zip(c, reconstructed):
            assert x == y, (m, x, y)
            counts['doubling'] += 1
        path = [walks(m-1, 2*m + 48, i) for i in range(m-1)]
        for n in range(21):
            L = 2*n + m - 2
            assert 2*path[0][L][-1] == a[L+2] - 4*a[L] - c[L+2] + 4*c[L]
            counts['endpoints'] += 1
            if m == 9:
                assert 2*path[0][L+2][-1] == apply([16,-24,-64,-6,21], a, 2*n)
                counts['seed'] += 1
        for i in range(1, m):
            for j in range(1, m):
                p, q = chebyshev2(abs(i-j)), chebyshev2(i+j)
                for k in range(21):
                    assert 2*path[i-1][k][j-1] == apply(p, reconstructed, k) - apply(q, reconstructed, k)
                    counts['entries'] += 1
        for k in range(21):
            trace = sum(path[i][k][i] for i in range(m-1))
            assert 2*m*c[k] == 2**k + (-2)**k + 2*trace
            counts['inverse'] += 1
    print(counts)
    print('PASS:', sum(counts.values()), 'exact assertions')


if __name__ == '__main__':
    main()
