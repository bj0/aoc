from itertools import count
from math import prod
from time import perf_counter

from aocd import data

T, buses = data.splitlines()
T = int(T)
buses = [int(x) for x in buses.split(',') if x != 'x']

times = [(x, (T // x + 1) * x) for x in buses]

print(T, times)

id, t = min(times, key=lambda x: x[1])

# 370
print(f'part1: {id * (t - T)}')

# data = """x
# 1789,37,47,1889"""
buses = [(i, int(b)) for i, b in enumerate(data.splitlines()[1].split(',')) if b != 'x']
print(buses)
t = perf_counter()


def find(it, p, r):
    return next(x for x in it if x % p == -r % p)


def red(buses, start=0, step=1):
    if not buses:
        return 0
    r, p = buses[0]
    x = find(count(start=start, step=step), p, r) // step
    return step * x + red(buses[1:], start + x * step, step * p)


# 894954360381385
print(f'part2: {red(buses)}')

print(f'{perf_counter() - t:.3f}s')

# alt
f = buses[0][1]
t = 0
for r, p in buses[1:]:
    while (t + r) % p != 0:
        t += f
    f *= p

print(f'part2.1: {t}')

# Chinese Remainder Theorem: https://mathworld.wolfram.com/ChineseRemainderTheorem.html

M = prod(m for r, m in buses)


def b(m):
    return next(b for b in range(1, m) if (b * M / m) % m == 1)


print(f'part2.2: {sum(((-r) * b(m) * M // m) % M for r, m in buses) % M}')
