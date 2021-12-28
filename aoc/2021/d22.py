# tracking every point requires too much memory, need to simplify
import re
from math import prod

from aoc.util import perf


def parse_input(data, limit=False):
    ops, blocks = zip(*(line.split(' ') for line in data.splitlines()))
    blocks = [tuple((int(a), int(b) + 1)
                    for a, b in (span.split('..')
                                 for span in re.findall(r'(-?\d+..-?\d+)', block)))
              for block in blocks]

    if limit:
        blocks = (tuple((min(max(a, -50), 51), max(-50, min(b, 51))) for a, b in block) for block in blocks)
        blocks = [block for block in blocks if not is_empty(block)]

    return ops, blocks


def is_empty(a):
    return any(i == j for i, j in a)


def intersects1d(a, b, i):
    # print(a,b,i)
    (al, ar), (bl, br) = a[i], b[i]
    return ar > bl and br > al


def intersects(a, b):
    return all(intersects1d(a, b, i) for i in (0, 1, 2))


def intersection(a, b):
    if not intersects(a, b):
        raise ValueError("they don't intersect")

    return [(max(l), min(r)) for l, r in (zip(ca, cb) for ca, cb in zip(a, b))]


def subtract(a, b):
    if not intersects(a, b):
        return [a]

    i = intersection(a, b)
    ((ixl, ixr), (iyl, iyr), (izl, izr)) = i
    ((axl, axr), (ayl, ayr), (azl, azr)) = a

    cubes = [
        ((axl, axr), (ayl, ayr), (azl, izl)),
        ((axl, axr), (ayl, ayr), (izr, azr)),
        ((axl, axr), (ayl, iyl), (izl, izr)),
        ((ixr, axr), (iyl, ayr), (izl, izr)),
        ((axl, ixr), (iyr, ayr), (izl, izr)),
        ((axl, ixl), (iyl, iyr), (izl, izr))
    ]

    return [c for c in cubes if not is_empty(c)]


def volume(cubes):
    return sum(prod((b - a) for a, b in cube) for cube in cubes)


def difference(a, cubes):
    cs = [a]
    for b in cubes:
        cs = sum((subtract(a, b) for a in cs), start=[])
    return cs


def solve(ops, blocks):
    cubes = []
    total = 0
    for op, block in reversed(tuple(zip(ops, blocks))):
        if op == 'on':
            # print(cubes)
            total += volume(difference(block, cubes))

        cubes.append(block)
    return total


@perf
def part1(data):
    ops, blocks = parse_input(data, limit=True)
    return solve(ops, blocks)


# def intersection(a, b):
#     return [(max(l), min(r)) for l, r in (zip(ca, cb) for ca, cb in zip(a, b))]


@perf
def part2(data):
    ops, blocks = parse_input(data)
    return solve(ops, blocks)


def main(data):
    print(f'part 1: {part1(data)}')

    print(f'part 2: {part2(data)}')


if __name__ == '__main__':
    from aocd import data

    main(data)

    #     main("""on x=10..12,y=10..12,z=10..12
    # on x=11..13,y=11..13,z=11..13
    # off x=9..11,y=9..11,z=9..11
    # on x=10..10,y=10..10,z=10..10
    # """)

#     main("""on x=-20..26,y=-36..17,z=-47..7
# on x=-20..33,y=-21..23,z=-26..28
# on x=-22..28,y=-29..23,z=-38..16
# on x=-46..7,y=-6..46,z=-50..-1
# on x=-49..1,y=-3..46,z=-24..28
# on x=2..47,y=-22..22,z=-23..27
# on x=-27..23,y=-28..26,z=-21..29
# on x=-39..5,y=-6..47,z=-3..44
# on x=-30..21,y=-8..43,z=-13..34
# on x=-22..26,y=-27..20,z=-29..19
# off x=-48..-32,y=26..41,z=-47..-37
# on x=-12..35,y=6..50,z=-50..-2
# off x=-48..-32,y=-32..-16,z=-15..-5
# on x=-18..26,y=-33..15,z=-7..46
# off x=-40..-22,y=-38..-28,z=23..41
# on x=-16..35,y=-41..10,z=-47..6
# off x=-32..-23,y=11..30,z=-14..3
# on x=-49..-5,y=-3..45,z=-29..18
# off x=18..30,y=-20..-8,z=-3..13
# on x=-41..9,y=-7..43,z=-33..15
# on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
# on x=967..23432,y=45373..81175,z=27513..53682
# """)
