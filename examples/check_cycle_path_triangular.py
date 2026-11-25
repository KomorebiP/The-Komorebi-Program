"""Exact triangular cycle/path transfer. Author: Komorebi P."""
from math import comb


def moments(size, steps, cycle):
    row = [1] + [0] * (size - 1)
    out = [row[0 if cycle else -1]]
    for _ in range(steps):
        row = [(row[(i - 1) % size] if cycle or i else 0)
               + (row[(i + 1) % size] if cycle or i + 1 < size else 0)
               for i in range(size)]
        out.append(row[0 if cycle else -1])
    return out


def forward(m, a):
    """Recover endpoint counts from a finite prefix of cycle return moments."""
    assert m >= 3 and a[0] == 1
    b = [1]
    g = [0]
    for n in range(1, len(a)):
        h = sum(comb(n, j) * 2**(n-j) * a[j] for j in range(n+1))
        g.append(m*h - 4**n)
        value, rem = divmod(sum(g[k]*b[n-k] for k in range(1,n+1)), 2*n)
        assert rem == 0, (m, n, rem)
        b.append(value)
    return b


def inverse(m, b):
    """Recover cycle moments from a finite prefix of endpoint counts."""
    assert m >= 3 and b[0] == 1
    g, h, a = [0], [1], [1]
    for n in range(1, len(b)):
        g.append(2*n*b[n] - sum(g[k]*b[n-k] for k in range(1,n)))
        value, rem = divmod(g[n]+4**n, m)
        assert rem == 0, (m, n, rem)
        h.append(value)
        a.append(sum(comb(n, j)*(-2)**(n-j)*h[j] for j in range(n+1)))
    return a


# Prefixes of A259475, square-array rows 1 through 9, columns 0 through 5.
OEIS = [[1,1,1,1,1,1], [1,2,4,8,16,32], [1,3,8,21,55,144],
        [1,4,13,40,121,364], [1,5,19,66,221,728],
        [1,6,26,100,364,1288], [1,7,34,143,560,2108],
        [1,8,43,196,820,3264], [1,9,53,260,1156,4845]]


def main():
    if not __debug__:
        raise RuntimeError('Run without -O.')
    counts = dict(forward=0, inverse=0, prefix=0, oeis=0)
    N = 60
    for m in range(3, 101):
        a = moments(m, N, True)
        b = moments(m-1, 2*N+m-2, False)[m-2::2]
        for actual, expected in zip(forward(m,a), b):
            assert actual == expected, (m, 'forward')
            counts['forward'] += 1
        for actual, expected in zip(inverse(m,b), a):
            assert actual == expected, (m, 'inverse')
            counts['inverse'] += 1
        for k in (0,1,2,5,10,20,40):
            assert forward(m,a[:k+1]) == b[:k+1], (m,k,'prefix forward')
            assert inverse(m,b[:k+1]) == a[:k+1], (m,k,'prefix inverse')
            counts['prefix'] += 2
        if m <= 11:
            for actual, expected in zip(b, OEIS[m-3]):
                assert actual == expected, (m, 'OEIS A259475')
                counts['oeis'] += 1
    print(counts)
    print('PASS:',sum(counts.values()),'explicit comparisons (plus internal exact-division checks)')


if __name__ == '__main__':
    main()
