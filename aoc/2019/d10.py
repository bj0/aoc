from collections import defaultdict
from math import gcd, sqrt, pi, atan2

from aocd import data

# data = """
# .#..##.###...#######
# ##.############..##.
# .#.######.########.#
# .###.#######.####.#.
# #####.##.#.##.###.##
# ..#####..#.#########
# ####################
# #.####....###.#.#.##
# ##.#################
# #####.##.###..####..
# ..######..##.#######
# ####.##.####...##..#
# .#####..#.######.###
# ##...#.##########...
# #.##########.#######
# .####.#.###.###.#.##
# ....##.##.###..#####
# .#.#.###########.###
# #.#.#.#####.####.###
# ###.##.####.##.#..##
# """
from aocd.models import Puzzle


def can_see(target, frm, roids):
    """
    is there LOS from [frm] to [target]
    """
    dist = (target - frm)
    dx, dy = int(dist.real), int(dist.imag)
    f = gcd(dx, dy)
    step = dx / f + (dy / f) * 1j
    c = frm
    while (c := c + step) != target:
        if c in roids:
            return False
    return True


def shoot(frm, to, roids):
    """
    does shooting a laser from [frm] to [to] hit something?
    """
    dist = (to - frm)
    dx, dy = int(dist.real), int(dist.imag)
    f = gcd(dx, dy)
    step = dx / f + (dy / f) * 1j
    c = frm
    while (c := c + step) != to:
        if c in roids:
            return c
    return to if to in roids else None


def main(*_):
    # parse roids
    rows = data.strip().split()
    h = len(rows)
    w = len(rows[0])
    roids = set()
    for y in range(h):
        for x in range(w):
            if rows[y][x] == '#':
                roids.add(x + y * 1j)

    # map which roids can see which other roids
    map = {}
    for roid in roids:
        seen = map.setdefault(roid, set())
        for other in (roids - {roid}):
            if other in seen:
                continue
            if can_see(other, roid, roids):
                seen.add(other)
                map.setdefault(other, set()).add(roid)
    # print(len(roids),len(map))
    station = max(map, key=lambda k: len(map[k]))
    part_a = len(map[station])
    print(f'max roid: {station} can see {part_a}')

    # sort roids by polar angle
    polar = defaultdict(set)
    for roid in (roids - {station}):
        delta = roid - station
        r = sqrt(delta.real ** 2 + delta.imag ** 2)
        t = atan2(delta.real, -delta.imag)
        if t < 0:
            t += 2 * pi
        polar[t].add((r, roid))

    # can only hit one roid per angle, but [shoot] takes care of that
    hit = 0
    targets = [max(polar[k])[1] for k in sorted(polar.keys())]
    while targets and hit < 200:
        target = targets.pop(0)
        # target = polar[pop]
        # print(f'tgt: {target}')
        if (splash := shoot(station, target, roids)) is not None:
            hit += 1
            # print(f'hit {hit} was {splash}')

    part_b = splash.real * 100 + splash.imag
    print(f'part 2: {splash}, {part_b}')

    # print(Puzzle(2019, 10).answers)
    return part_a, part_b


if __name__ == '__main__':
    main()
