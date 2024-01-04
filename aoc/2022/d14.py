from functools import cmp_to_key

from aocd import data

from aoc.util import perf

# data = """498,4 -> 498,6 -> 496,6
# 503,4 -> 502,4 -> 502,9 -> 494,9"""

puz = [
    [tuple(int(x) for x in pt.split(",")) for pt in line.split(" -> ")]
    for line in data.split("\n")
]


def map_paths(paths):
    map = {}
    for path in puz:
        for l in range(len(path) - 1):
            (x0, y0) = path[l]
            (x1, y1) = path[l + 1]
            for i in range(min(x0, x1), max(x0, x1) + 1):
                for j in range(min(y0, y1), max(y0, y1) + 1):
                    map[i + j * 1j] = "#"

    return map


@perf
def part1(puz):
    map = map_paths(puz)

    start = 500 + 0 * 1j
    pos = start
    bottom = max(p.imag for p in map) + 1
    while pos.imag < bottom:
        if map.get(pos + 1j, ".") == ".":
            pos += 1j
        elif map.get(pos + (-1 + 1j), ".") == ".":
            pos += -1 + 1j
        elif map.get(pos + (1 + 1j), ".") == ".":
            pos += 1 + 1j
        else:
            map[pos] = "o"
            pos = start

    return sum(1 for v in map.values() if v == "o")


# 805
print(f"part1: {part1(puz)}")


@perf
def part2(puz):
    map = map_paths(puz)

    start = 500 + 0 * 1j
    pos = start
    floor = max(p.imag for p in map) + 2

    while map.get(start, ".") != "o":
        if pos.imag == floor - 1:
            map[pos] = "o"
            pos = start
        elif map.get(pos + 1j, ".") == ".":
            pos += 1j
        elif map.get(pos + (-1 + 1j), ".") == ".":
            pos += -1 + 1j
        elif map.get(pos + (1 + 1j), ".") == ".":
            pos += 1 + 1j
        else:
            map[pos] = "o"
            pos = start

    return sum(1 for v in map.values() if v == "o")


# 20758
print(f"part2: {part2(puz)}")
