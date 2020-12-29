import re
from math import prod

import numpy as np
from aocd import data

# right, down, left, up
DIRS = (1, 1j, -1, -1j)


def match_dir(a, b, dir):
    if dir == 1:
        return all(a[:, -1] == b[:, 0])
    if dir == 1j:
        return all(a[-1, :] == b[0, :])
    if dir == -1:
        return all(a[:, 0] == b[:, -1])
    if dir == -1j:
        return all(a[0, :] == b[-1, :])


def ra(a):
    """rotate an array 90d"""
    return np.rot90(a)


def fa(a):
    """flip an array horizontally"""
    return np.fliplr(a)


def mutate(a):
    """yield the permutations of rotating/flipping array"""
    yield a
    for i in range(3):
        yield (a := ra(a))
    yield (a := fa(ra(a)))
    for i in range(3):
        yield (a := ra(a))


tiles = {}
for tile in re.split(r'\n\n', data):
    lines = tile.split('\n')
    n = int(lines[0].split()[1][:-1])
    tiles[n] = np.array([[x for x in row] for row in lines[1:]])


def build_map(pos, map):
    """recursively build map with edge searches"""
    k0, t0 = map[pos]
    for dir in DIRS:
        loc = pos + dir
        if loc in map:
            continue
        left = tiles.keys() - {x[0] for x in map.values()}
        for k, y in ((k1, x) for k1 in left for x in mutate(tiles[k1])):
            if match_dir(t0, y, dir):
                map[loc] = k, y
                build_map(loc, map)
                break


map = {0: (n, tiles[n])}
build_map(0, map)

# shift so that 0,0 is top left
c0 = 1j * min(c.imag for c in map) + min(c.real for c in map)
cN = 1j * max(c.imag for c in map) + max(c.real for c in map)
map = {c - c0: v for c, v in map.items()}
cN = cN - c0

# 8581320593371
print(f'part1: {prod(map[c][0] for c in (0, cN, 1j * cN.imag, cN.real))}')

# stack tiles
pic = np.vstack(tuple(
    np.hstack(tuple(map[c + r * 1j][1][1:-1, 1:-1] for c in range(int(cN.real) + 1)))
    for r in range(int(cN.imag) + 1)
))

monster = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
""".strip('\n')
monster = np.array([[x for x in row] for row in monster.split('\n')])
midx = np.where(monster == '#')

hits = 0
t = 1
while hits == 0:
    if t > 10:
        print('fail')
        break
    print(f'try {t}')
    body = set()
    for r in range(pic.shape[0] - monster.shape[0] + 1):
        for c in range(pic.shape[1] - monster.shape[1] + 1):
            idx = [ax + i for ax, i in zip(midx, (r, c))]
            if np.all(pic[idx] == '#'):
                hits += 1
                body |= {c for c in zip(*idx)}
    # if no matches, rotate/flip image
    if hits == 0:
        if t == 4:
            pic = fa(ra(pic))
        else:
            pic = ra(pic)
        t += 1

waves = np.where(pic == '#')
print(f'part2: {sum(1 for c in zip(*waves) if c not in body)}')
