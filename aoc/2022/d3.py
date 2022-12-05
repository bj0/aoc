import string
from aocd import data

from aoc.util import perf

puz2 = data.strip().split('\n')
puz = [(line[:len(line) // 2], line[len(line) // 2:]) for line in puz2]

rank = string.ascii_lowercase + string.ascii_uppercase


@perf
def part1(puz):
    return sum(rank.index((set(a) & set(b)).pop()) + 1 for (a, b) in puz)


# 7850
print(f'part1: {part1(puz)}')


@perf
def part2(puz):
    return sum(rank.index((set(a) & set(b) & set(c)).pop()) + 1
               for (a, b, c) in (puz[i:i + 3] for i in range(0, len(puz), 3)))


# 2581
print(f'part2 {part2(puz2)}')
