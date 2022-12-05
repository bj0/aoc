from aocd import data

from aoc.util import perf

puz = [[tuple(map(int, r.split('-'))) for r in line.split(',')]
       for line in data.split('\n')]


@perf
def part1(puz):
    def contains(r0, r1):
        a, b = r0
        x, y = r1
        return (a <= x and y <= b) or (x <= a and b <= y)

    return sum(contains(a, b) for (a, b) in puz)


# 560
print(f'part1: {part1(puz)}')


@perf
def part2(puz):
    def excludes(r0, r1):
        a, b = r0
        x, y = r1
        return a > y or b < x

    return sum(not excludes(a, b) for (a, b) in puz)


# 2581
print(f'part2 {part2(puz)}')
