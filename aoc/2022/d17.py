from collections import Counter, deque
from functools import cache, lru_cache
from itertools import combinations, cycle, repeat
from time import sleep

import numpy as np

from aocd import data

from aoc.util import perf

import networkx as nx
import re

# data = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
puz = [-1 if c == "<" else 1 for c in data]

shapes = (
    {0, 1, 2, 3},
    {1, 1j, 1 + 1j, 2 + 1j, 1 + 2j},
    {0, 1, 2, 2 + 1j, 2 + 2j},
    {0, 1j, 2j, 3j},
    {0, 1, 1j, 1 + 1j},
)

floor = {i + 0j for i in range(9)}


def hit(shape, pile):
    return (shape & pile) or any(x.real == 0 or x.real == 8 for x in shape)


@perf
def part1(N):
    cache = {}
    pile = floor
    wind = cycle(enumerate(puz))
    height = 0
    for i, shape in enumerate(cycle(shapes)):
        j, dir = next(wind)
        x, y = 3, height+4
        shape = {c + (x + y * 1j) for c in shape}
        while True:
            if not hit(moved := {c + dir for c in shape}, pile):
                shape = moved
            if hit(moved:= {c  - 1j for c in shape}, pile):
                pile = {x for x in (pile | shape) if (height - x.imag) < 65}
                break
            shape = moved
            j, dir = next(wind)

        # save state to look for repeats
        height = int(max(c.imag for c in pile))
        heights = [height - int(max(c.imag for c in pile if c.real == x)) for x in range(1,8)]
        i += 1
        # state
        curr = (i, height, heights)
        if (idx:=(i%5, j)) not in cache:
            # save states
            cache[idx] = curr
        else:
            # cache hit
            if (p:= cache[idx])[2] != heights:
                # early heights are perturbed by the floor
                cache[idx] = curr
            else:
                # found cycle
                last_i, last_height, last = p
                di = i - last_i
                # wait for it to divide into N (lazy way)
                # todo, why not just set N and height on first cycle and let the rest of N (quotient) run out, faster than looking for a new cycle
                if (N-i) % di == 0:
                    return (height-last_height) * ((N-i)//di) + height
        if i == N:
            return height

print(f"part1: {part1(2022)}")


# @perf
# def part2():

# found that j = 38 repeated every 1715 cycles (of all shapes), so shifted to make 1e12 divide by i = 5160 then (1e12-5160) / 1715 * dy + h; dy was 2574, h at 5160 was 7763
# todo: make this automatic
print(f"part2: {part1(1_000_000_000_000)}")

