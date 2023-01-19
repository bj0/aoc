from functools import cache
from itertools import cycle
from math import ceil
from operator import add, floordiv, mul, sub, truediv

from aocd import data

from aoc.util import perf

# data = """....#..
# ..###.#
# #...#.#
# .#...##
# #.###..
# ##.#.##
# .#..#.."""

inp = {
    (i + j * 1j)
    for j, line in enumerate(data.split("\n"))
    for i, c in enumerate(line)
    if c == "#"
}


def can_move(elf, elfs, dir):
    return (not any((elf + dir + d * dir) in elfs for d in (-1j, 0, 1j))) and (
        not all(
            (elf + dir + d * dir) not in elfs
            for dir in (-1, 1, -1j, 1j)
            for d in (-1j, 0, 1j)
        )
    )


def printelfs(elfs, a=-4, b=10):
    for j in range(a, b):
        for i in range(a, b):
            print("#" if (i + j * 1j) in elfs else ".", end="")
        print()


@perf
def part1(elfs, N =10):
    # printelfs(elfs)
    dirs = (-1j, 1j, -1, 1)
    old = set()
    for r in range(N):
        # print(f"rd:{r},dir{dirs[r%4]}")
        prop = {}

        for elf in elfs:
            for d in range(4):
                dir = dirs[(r + d) % 4]
                if can_move(elf, elfs, dir):
                    if (p := elf + dir) in prop:
                        prop[p] = None
                    else:
                        prop[p] = elf
                    break

        elfs = {p for p in prop if prop[p] is not None} | (elfs - set(prop.values()))
        if elfs == old:
            # print(f'win! {r+1}')
            return r+1
        old = elfs
        # printelfs(elfs)
        # print()

    rect = (1, 1, 1, 1)
    for c in elfs:
        c, r = c.real, c.imag
        rect = (min(rect[0], c), min(rect[1], r), max(rect[2], c), max(rect[3], r))

    return (rect[2] - rect[0] + 1) * (rect[3] - rect[1] + 1) - len(elfs)


# 4091
print(f"part1: {part1(inp)}")

# 1036
print(f"part2: {part1(inp, 2000)}")
