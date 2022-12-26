from functools import cmp_to_key

from aocd import data

from aoc.util import perf, mdist


import re

# data = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
# Sensor at x=9, y=16: closest beacon is at x=10, y=16
# Sensor at x=13, y=2: closest beacon is at x=15, y=3
# Sensor at x=12, y=14: closest beacon is at x=10, y=16
# Sensor at x=10, y=20: closest beacon is at x=10, y=16
# Sensor at x=14, y=17: closest beacon is at x=10, y=16
# Sensor at x=8, y=7: closest beacon is at x=2, y=10
# Sensor at x=2, y=0: closest beacon is at x=2, y=10
# Sensor at x=0, y=11: closest beacon is at x=2, y=10
# Sensor at x=20, y=14: closest beacon is at x=25, y=17
# Sensor at x=17, y=20: closest beacon is at x=21, y=22
# Sensor at x=16, y=7: closest beacon is at x=15, y=3
# Sensor at x=14, y=3: closest beacon is at x=15, y=3
# Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

pat = re.compile(r"[^x]*x=([^,]+), y=([^:]+):[^x]*x=([^,]+), y=([^\s]+)")

puz = {
    (int(x), int(y)): (int(mx), int(my))
    for (x, y, mx, my) in (pat.match(line).groups() for line in data.split("\n"))
}

dists = {p: mdist(p, b) for p, b in puz.items()}


@perf
def part1(puz, dists):
    Y = 2000000
    # Y = 10
    ins = set()
    hits = [p for p in dists if abs(p[1] - Y) <= dists[p]]
    for p in hits:
        dx = dists[p] - abs(Y - p[1])
        for j in range(-dx, dx + 1):
            ins.add(p[0] + j)

    return len(ins - set(x for x, y in puz.values() if y == Y))


# 5403290
print(f"part1: {part1(puz, dists)}")


def coords(x0, y0, d):
    def x():
        yield from range(x0 - d - 1, x0 + d + 2)
        yield from range(x0 + d, x0 - d, -1)

    def y():
        yield from range(y0, y0 + d + 2)
        yield from range(y0 + d, y0 - d - 2, -1)
        yield from range(y0 - d, y0)

    yield from zip(x(), y())


def any_hit(x, y, dists):
    return any(mdist((x, y), p) <= d for p, d in dists.items())

def possible(x, y, dists, puz):
    # this seems 3x as fast as above for some reason
    for s, d in dists.items():
        sx, sy = s
        if abs(x-sx) + abs(y-sy) <= d and (x, y) not in puz.values():
            return False
    return True

@perf
def part2(puz, dists):
    # this one takes ~193s
    checked = set()
    for s, d in dists.items():
        for x, y in coords(*s, d):
            if not 0 <= x <= 4e6 or not 0 <= y <= 4e6 or (x, y) in checked:
                continue
            if not any_hit(x, y, dists):
                return int(x * 4e6 + y)
            checked.add((x, y))


@perf
def part2a(puz, dists):
    # this one takes ~ 55s
    for s, d in dists.items():
        sx, sy = s
        for dx in range(d+2):
            dy = (d+1)-dx
            for mx, my in [(-1,1), (1,-1),(-1,-1),(1,1)]:
                x, y = sx + (dx*mx), sy + (dy*my)
                if not(0 <= x <= 4_000_000 and 0 <= y <= 4_000_000):
                    continue
                if possible(x, y, dists, puz):
                # if not any_hit(x, y, dists):
                    return int(x * 4e6 + y)


# 10291582906626 (193s)
# print(f"part2: {part2(puz, dists)}")
# todo: prob faster to just check intersections instead of full circles
print(f"part2: {part2a(puz, dists)}")
