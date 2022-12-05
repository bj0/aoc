from aocd import data

from aoc.util import perf

puz = [[int(x) for x in elf.strip().split()] for elf in data.strip().split('\n\n')]


@perf
def part1(puz):
    return max(sum(elf) for elf in puz)


# 69626
print(f'part1: {part1(puz)}')


@perf
def part2(puz):
    return sum(sorted((sum(elf) for elf in puz), reverse=True)[:3])


# 206780
print(f'part2 {part2(puz)}')
