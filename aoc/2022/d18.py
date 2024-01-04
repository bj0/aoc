from collections import deque
from functools import cache, lru_cache

import networkx as nx
import numpy as np
from aocd import data
import numpy as np
from aoc.util import perf


# data = """2,2,2
# 1,2,2
# 3,2,2
# 2,1,2
# 2,3,2
# 2,2,1
# 2,2,3
# 2,2,4
# 2,2,6
# 1,2,5
# 3,2,5
# 2,1,5
# 2,3,5"""

cubes = {tuple(int(x) for x in line.split(",")) for line in data.split("\n")}


def shift(cube, dir):
    return tuple(a + b for a, b in zip(cube, dir))


@perf
def part1(cubes):
    return sum(
        1
        for c in cubes
        for dir in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
        if shift(c, dir) not in cubes
    )


# 4536
print(f"part1: {part1(cubes)}")


minx = min(x for (x, _, _) in cubes)
miny = min(x for (_, x, _) in cubes)
minz = min(x for (_, _, x) in cubes)
maxx = max(x for (x, _, _) in cubes)
maxy = max(x for (_, x, _) in cubes)
maxz = max(x for (_, _, x) in cubes)

DIRS = [
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
]


def outside(c):
    x, y, z = c
    return x < minx or x > maxx or y < miny or y > maxy or z < minz or z > maxz


def external(c, voids, cubes):
    if c in voids:
        return False
    seen = set()
    check = deque([c])
    while check:
        p = check.popleft()
        for dir in DIRS:
            if (d := shift(p, dir)) not in cubes and d not in seen:
                check.append(d)
                if outside(d):
                    return True
                seen.add(d)

    voids |= seen
    return False


@perf
def part2(cubes):
    f = 0
    voids = set()
    for c in cubes:
        for dir in DIRS:
            d = c
            while (d := shift(d, dir)) not in cubes:
                if external(d, voids, cubes):
                    # print('free',c)
                    f += 1
                    break
    return f


# 2606
print(f"part2: {part2(cubes)}")
