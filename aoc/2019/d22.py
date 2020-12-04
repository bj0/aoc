import re

from aocd import data


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception("failed")
    else:
        return x % m


def deal(s):
    yield from reversed(s)


def cut(n, s):
    yield from (i + n for i in s)


def inc(n, s, M):
    inv = modinv(n, M)
    yield from (inv * i for i in s)


data = """
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1
"""


def shuffle(M, N=1):
    s = range(M)
    for i in range(N):
        for line in data.strip().split('\n'):
            if 'stack' in line:
                s = deal(s)
            elif 'increment' in line:
                n = int(re.search(r'-?\d+', line).group())
                s = inc(n, s, M)
            elif 'cut' in line:
                n = int(re.search(r'-?\d+', line).group())
                s = cut(n, s)
    return (i % M for i in s)


M = 10
for i in shuffle(M):
    print(i)

# s = shuffle(tuple(range(10007)))
# p = s.index(2019)
print(f'part 1: {p}')
# 1867

shuffle(tuple(range(119315717514047)), 101741582076661)
