from aocd import data
from collections import deque

from aocd.models import Puzzle


def main(*_):
    orbits = (s.strip().split(')') for s in data.strip().split())

    # orbits = """
    # COM)B
    # B)C
    # C)D
    # D)E
    # E)F
    # B)G
    # G)H
    # D)I
    # E)J
    # J)K
    # K)L""".strip().split()

    map = {r: l for (l, r) in orbits}

    paths = {}
    r = 1
    level = deque((x, r) for x in map if map[x] == 'COM')
    while level:
        o, r = level.popleft()
        paths[o] = r
        for n in map:
            if map[n] == o:
                level.append((n, r + 1))

    part_a = sum(paths.values())
    print(f'part 1: {part_a}')

    path0 = {}
    o = 'YOU'
    n = 0
    while (o := map[o]) != 'COM':
        path0[o] = n
        n += 1

    o = 'SAN'
    n = 0
    while (o := map[o]) != 'COM':
        if o in path0:
            part_b = path0[o] + n
            print(f'part 2: {part_b}')
            break
        n += 1
    else:
        raise Exception("failed")

    return part_a, part_b
    # print(Puzzle(2019, 6).answers)


if __name__ == '__main__':
    main()
