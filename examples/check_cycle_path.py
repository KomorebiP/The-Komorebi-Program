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


def recurrence_poly(d, initial, shift=0):
    """Ascending coefficients for p_(j+1)=(x-shift)*p_j-p_(j-1)."""
    a, b = [initial], [-shift, 1]
    for _ in range(d):
        a, b = b, [
            (b[i - 1] if i else 0)
            - (shift * b[i] if i < len(b) else 0)
            - (a[i] if i < len(a) else 0)
            for i in range(len(b) + 1)
        ]
    return a


def apply(poly, seq, k):
    return sum(c * seq[k + j] for j, c in enumerate(poly))


def odd_remainder(m):
    """Remainder of x^m*(x^2-4) modulo the odd cycle minimal polynomial."""
    r = (m - 1) // 2
    u = recurrence_poly(r, 1)
    v = recurrence_poly(r - 1, 1)
    w = [c + (v[i] if i < len(v) else 0) for i, c in enumerate(u)]
    modulus = [(w[i-1] if i else 0) - (2*w[i] if i < len(w) else 0)
               for i in range(len(w) + 1)]
    assert modulus[-1] == 1
    p = [0]*m + [-4, 0, 1]
    while len(p) >= len(modulus):
        offset, lead = len(p) - len(modulus), p[-1]
        for i, c in enumerate(modulus):
            p[offset+i] -= lead*c
        p.pop()
    return p


# Published coefficients, ascending powers and padded to degree (m-1)/2.
POLYNOMIALS = {
    3: [2, -1], 5: [2, -5, 2], 7: [-8, -14, 9, 0],
    9: [16, -24, -64, -6, 21],
    11: [80, 242, -229, -308, 66, 55],
    13: [-242, 715, 1471, -858, -1183, 143, 221],
}

# Short OEIS prefixes, with the path's n=0 term supplied where necessary.
# Cycle fixtures are full moments for odd m and even moments for even m.
FIXTURES = {
    3: ([1, 0, 2, 2, 6, 10], [1, 1, 1, 1, 1]),
    4: ([1, 2, 8, 32, 128], [1, 2, 4, 8, 16]),
    5: ([1, 0, 2, 0, 6, 2, 20, 14], [1, 3, 8, 21, 55]),
    6: ([1, 2, 6, 22, 86, 342], [1, 4, 13, 40, 121]),
    7: ([1, 0, 2, 0, 6, 0, 20, 2], [1, 5, 19, 66, 221]),
    8: ([1, 2, 6, 20, 72, 272], [1, 6, 26, 100, 364]),
    9: ([1, 0, 2, 0, 6, 0, 20, 0, 70, 2], [1, 7, 34, 143, 560]),
}


def main():
    if not __debug__:
        raise RuntimeError('Run without -O so assertions remain enabled.')
    counts = dict(doubling=0, endpoints=0, entries=0, trace=0,
                  inverse=0, polynomial=0, coefficients=0, obstruction=0,
                  fixtures=0)
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
        b = [path[0][2*n+m-2][-1] for n in range((m+50)//2)]
        for n in range(21):
            L = 2*n + m - 2
            assert 2*b[n] == a[L+2] - 4*a[L] - c[L+2] + 4*c[L], (m, n)
            counts['endpoints'] += 1
        cheb = [recurrence_poly(d, 2) for d in range(2*m-1)]
        for i in range(1, m):
            for j in range(1, m):
                p, q = cheb[abs(i-j)], cheb[i+j]
                for k in range(21):
                    assert 2*path[i-1][k][j-1] == apply(p, reconstructed, k) - apply(q, reconstructed, k), (m, i, j, k)
                    counts['entries'] += 1
        from_trace = []
        for k in range(41):
            trace = sum(path[i][k][i] for i in range(m-1))
            value, rem = divmod(2**k + (-2)**k + 2*trace, 2*m)
            assert rem == 0 and value == c[k], (m, k)
            from_trace.append(value)
            counts['trace'] += 1
        for n in range(21):
            assert a[n] == sum(comb(n, h)*(-2)**(n-h)*from_trace[2*h] for h in range(n+1)), (m, n)
            counts['inverse'] += 1
        if m % 2:
            q = odd_remainder(m)
            if m in POLYNOMIALS:
                assert q == POLYNOMIALS[m], (m, q)
                counts['coefficients'] += 1
            for n in range(21):
                assert 2*b[n+1] == apply(q, a, 2*n), (m, n, q)
                counts['polynomial'] += 1
        else:
            # 2*T_(m/2)((x-2)/2)-2 kills every squared cycle eigenvalue.
            p = recurrence_poly(m//2, 2, shift=2)
            p[0] -= 2
            # Every source shift passes the annihilator, including odd shifts.
            for shift in range(2):
                source = a[shift::2]
                for n in range(21):
                    assert apply(p, source, n) == 0, (m, shift, n)
                    counts['obstruction'] += 1
            # The target fails: this is an exact rejection control.
            assert any(apply(p, b, n) != 0 for n in range(m//2)), m
            counts['obstruction'] += 1
        if m in FIXTURES:
            ca, pb = FIXTURES[m]
            assert (a if m % 2 else a[::2])[:len(ca)] == ca, m
            assert b[:len(pb)] == pb, m
            counts['fixtures'] += 2
    print(counts)
    print('PASS:', sum(counts.values()), 'exact assertions')


if __name__ == '__main__':
    main()
