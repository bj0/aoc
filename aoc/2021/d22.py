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
        blocks = [tuple((max(a, -50), min(b, 51)) for a, b in block) for block in blocks]

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


def union(a, b):
    if not intersects(a, b):
        return [a, b]

    i = intersection(a, b)
    ((ixl, ixr), (iyl, iyr), (izl, izr)) = i
    ((axl, axr), (ayl, ayr), (azl, azr)) = a
    ((bxl, bxr), (byl, byr), (bzl, bzr)) = b

    cubes = [i,
             ((axl, axr), (ayl, ayr), (azl, izl)),
             ((axl, axr), (ayl, ayr), (izr, azr)),
             ((axl, axr), (ayl, iyl), (izl, izr)),
             ((ixr, axr), (iyl, ayr), (izl, izr)),
             ((axl, ixr), (iyr, ayr), (izl, izr)),
             ((axl, ixl), (iyl, iyr), (izl, izr)),

             ((bxl, bxr), (byl, byr), (bzl, izl)),
             ((bxl, bxr), (byl, byr), (izr, bzr)),
             ((bxl, bxr), (byl, iyl), (izl, izr)),
             ((ixr, bxr), (iyl, byr), (izl, izr)),
             ((bxl, ixr), (iyr, byr), (izl, izr)),
             ((axl, ixl), (iyl, iyr), (izl, izr))
             ]

    return [c for c in cubes if not is_empty(c)]


def volume(cubes):
    return sum(prod((b-a) for a, b in cube) for cube in cubes)


def solve(ops, blocks):
    cubes = []
    total = 0
    for op, block in reversed(tuple(zip(ops, blocks))):
        if op == 'on':
            # print(cubes)
            total += volume([block]) - volume(intersection(block, b) for b in cubes if intersects(block, b))

        cs = [block]
        print(len(cubes))
        for c in cubes:
            if not intersects(block, c): continue
            ics = [b for b in cs if intersects(c, b)]
            while ics:
                c, *_ = ics


            cs = [x for l in (union(a, c) for a in cs) for x in l]
        print('2',len(cs))
        cubes = cs
    return total


@perf
def part1(ops, blocks):
    return solve(ops, blocks)


# def intersection(a, b):
#     return [(max(l), min(r)) for l, r in (zip(ca, cb) for ca, cb in zip(a, b))]


@perf
def part2(ops, blocks):
    core = set()
    for op, block in zip(ops, blocks):
        p = 1 if op == 'on' else 0
        x, y, z = block
        for i in range(x[0], x[1] + 1):
            for j in range(y[0], y[1] + 1):
                for k in range(z[0], z[1] + 1):
                    if p:
                        core.add((i, j, k))
                    else:
                        core.discard((i, j, k))

    return core


def main(data):
    ops, blocks = parse_input(data, limit=True)

    tot = part1(ops, blocks)
    print(f'part 1: {tot}')
    # print(f'part 1: {sum(1 for p in core if core[p])}')

    # core = part2(ops, blocks)  # todo not finished
    # print(f'part 2: {sum(1 for p in core if core[p])}')


if __name__ == '__main__':
    # from aocd import data
    #
    # main(data)

    main("""on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10
""")
