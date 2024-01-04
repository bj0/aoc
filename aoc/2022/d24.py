from collections import deque
import enum
from functools import cache
from itertools import cycle
from math import ceil
from operator import add, floordiv, mul, sub, truediv
from time import sleep
from typing import Counter

from aocd import data

from aoc.util import perf

# data = """#.######
# #>>.<^<#
# #.<..<<#
# #>v.><>#
# #<^v^^>#
# ######.#"""

grid = data.split("\n")
W, H = len(grid[0]), len(grid)

_dirs = {"<": -1, ">": 1, "^": -1j, "v": 1j}
storms = {
    (i + j * 1j): [_dirs[c]]
    for j, line in enumerate(grid)
    for i, c in enumerate(line)
    if c in "<>^v"
}
walls = (
    {0 + j * 1j for j in range(H)}
    | {i + 0 * 1j for i in range(W)}
    | {W - 1 + j * 1j for j in range(H)}
    | {i + (H - 1) * 1j for i in range(W)}
)

# starting & ending pos
END = W - 2 + (H - 1) * 1j
walls = (walls - {1, END}) | {1 - 1j} | {END + 1j}

# print(walls)


_cache = {}


def move_storms(storms, n):
    if n in _cache:
        return _cache[n]
    new_storms = {}
    for g in storms:
        for s in storms[g]:
            p = g + s
            if p in walls:
                # wrap
                # print('wrap',p,s)
                p = ((p.real + 2 * s.real) % W) + ((p.imag + 2 * s.imag) % H) * 1j
                # print('to',p)
            new_storms.setdefault(p, []).append(s)
    _cache[n] = new_storms
    return new_storms


def find_path(storms, start, end, N=0):
    q = deque([(start, N, storms)])
    seen = set()
    while q:
        p, n, storms = q.popleft()
        if (p, n) in seen:
            continue
        seen.add((p, n))
        storms = move_storms(storms, n)
        if n > 1800:
            print(n, storms)
        for d in (-1, -1j, 0, 1, 1j):
            if (p2 := p + d) not in storms.keys() | walls:
                if p2 == end:
                    return n + 1, storms
                q.append((p2, n + 1, storms))


@perf
def part1(storms):
    return find_path(storms, 1, END)[0]


@perf
def part2(storms):
    a, storms = find_path(storms, 1, END)
    print('trip',a)
    b, storms = find_path(storms, END, 1, a)
    print('trip',b-a)
    c, storms = find_path(storms, 1, END, b)
    print('trip',c-b)
    return c


# 
print(f"part1: {part1(a:=storms)}")


# 
print(f"part2: {part2(storms)}")
