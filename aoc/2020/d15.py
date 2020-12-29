from aocd import data

from aoc.util import perf


@perf
def do(N):
    mem = {m: i for i, m in enumerate((int(n) for n in data.split(',')), 1)}
    m = tuple(mem.keys())[-1]
    for i in range(len(mem), N):
        mem[m], m = i, i - mem.get(m, i)
    return m


# 240
print(f'part1: {do(2020)}')

# 505
print(f'part2: {do(30_000_000)}')
