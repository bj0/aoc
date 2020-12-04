import fileinput
import re
from collections import defaultdict


def ints(text):
    return re.findall(r'-?\d+', text)


inp = """
pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1
""".strip()


def dist(x, y, z, x2, y2, z2):
    return abs(x - x2) + abs(y - y2) + abs(z - z2)


def part1(input):
    bots = {}
    for line in input:
        x, y, z, r = map(int, ints(line))
        bots[(x, y, z)] = r

    pos = max(bots, key=lambda k: bots[k])
    r = bots[pos]
    num = sum(1 for b in bots if dist(*b, *pos) <= r)

    return bots, pos, num


def nb6(x, y, z, r):
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            for dz in range(-1, 2):
                yield (x + r * dx, y + r * dy, z + r * dz)


def part2(bots):
    minx = min(x for (x, y, z) in bots)
    miny = min(y for (x, y, z) in bots)
    minz = min(z for (x, y, z) in bots)
    maxx = max(x for (x, y, z) in bots)
    maxy = max(y for (x, y, z) in bots)
    maxz = max(z for (x, y, z) in bots)
    R = max(maxx - minx, maxy - miny, maxz - minz)
    spos = (0, 0, 0)
    reg = {spos}

    while R > 0:
        R = R // 2 + (R % 2 if R > 2 else 0)

        g = defaultdict(int)
        for pos in reg:
            for nb in nb6(*pos, R):
                g[nb] = 0
                for b in bots:
                    if dist(*nb, *b) <= bots[b] + R:
                        g[nb] += 1

        d = max(g.values())
        reg = set(k for k in g if g[k] == d)
        sd = 0
        print(d, len(reg), R, sd)

    ds = {k: dist(*spos, *k) for k in reg}
    sd = min(ds.values())

    print(f'min d: {sd}')


# inp = inp.split('\n')
inp = fileinput.input('d23.txt');

bots, pos, num = part1(inp)
print(f'part 1: {num}')

import time

t = time.perf_counter()

part2(bots)

print(f'{time.perf_counter() - t}s')
