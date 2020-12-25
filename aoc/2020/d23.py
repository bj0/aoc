from itertools import accumulate, islice
from math import prod

from aocd import data

from aoc.util import perf

cups = [int(d) for d in data]
N = max(cups)


def rot(n, N):
    return ((n - 1) % N) + 1


@perf
def run(cups, moves):
    N = len(cups)
    cur = cups[0]
    after = {c: cups[(i + 1) % N] for i, c in enumerate(cups)}
    for _ in range(moves):
        held = tuple(accumulate([after[cur], 0, 0], lambda r, _: after[r]))
        t = rot(cur - 1, N)
        while t in held:
            t = rot(t - 1, N)
        after[cur] = after[held[-1]]
        after[held[-1]] = after[t]
        after[t] = held[0]
        cur = after[cur]
    return accumulate([1] * N, lambda r, _: after[r])


# 65432978
print(f'part1: {"".join(str(x) for x in run(cups, 100))[1:]}')

M = 1_000_000
cups += list(range(N + 1, M + 1))
N = M

r = run(cups, N * 10)
# 287230227046
print(f'part2: {prod(islice(r, 1, 3))}')
