input = 'hfdlxzhv'

from collections import deque

from d10 import part2 as hash


def scan_region(map, i, j):
    region = [(i, j)]
    check = deque([(i, j)])
    while check:
        i, j = check.pop()
        for coord in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 > coord[0] or coord[0] > 127 or 0 > coord[1] or coord[1] > 127:
                continue
            if map[coord] != 0 and coord not in region:
                check.appendleft(coord)
                region.append(coord)

    return region


def part1(input):
    rows = []
    count = 0
    for i in range(128):
        h = hash(f'{input}-{i}')
        row = f'{int(h, 16):0128b}'
        # print(row)
        rows.append(row)
        count += len([c for c in row if c == '1'])

    return count, rows


import numpy as np


def part2(input):
    _, rows = part1(input)
    map = np.array([[int(n) for n in row] for row in rows])
    v = map.view().reshape(-1)

    # regions = []
    count = 0
    for i in range(v.size):
        if v[i] == 1:
            # new region
            count += 1
            x, y = i // 128, i % 128
            region = scan_region(map, x, y)
            to = -1 if count == 1 else count
            for coord in region:
                map[coord] = to
            # regions.append(region)

    return count, map  # , regions


# print(part1('flqrgnkx'))

# print(part1(input))

c, m = part2('flqrgnkx')
print(m[:8, :9])
print(c)

c, m = part2('hfdlxzhv')
print(m[:8, :9])
print(c)
