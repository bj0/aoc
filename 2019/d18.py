from collections import deque
from time import perf_counter

from aocd import data

import networkx as nx

# data = """
# ########################
# #@..............ac.GI.b#
# ###d#e#f################
# ###A#B#C################
# ###g#h#i################
# ########################
# """
# data = """
# #################
# #i.G..c...e..H.p#
# ########.########
# #j.A..b...f..D.o#
# ########@########
# #k.E..a...g..B.n#
# ########.########
# #l.F..d...h..C.m#
# #################
# """

KEYS = 'abcdefghijklmnopqrstuvwxyz'
DOORS = KEYS.upper()
_dir = (-1, -1j, 1, 1j)

t = perf_counter()

map = {x + y * 1j: c for y, row in enumerate(data.strip().split('\n')) for x, c in enumerate(row)}

start = next(k for k in map if map[k] == '@')
map_keys = set(k for k in KEYS if k in map.values())
num_keys = len(map_keys)
kpos = {map[p]: p for p in map if map[p] in KEYS}


# dpos = {map[p]: p for p in map if map[p] in DOORS}


print(start, num_keys)

def build_graph(start, map):
    g = nx.Graph()
    q = deque([start])
    visited = set()
    while q:
        pos = q.popleft()
        if pos in visited:
            continue
        visited.add(pos)
        for d in _dir:
            p = pos + d
            if p in visited:
                continue
            if map[p] != '#':
                g.add_edge(pos, p)
                q.append(p)
                # print(f'{pos}->{p}')
    return g


def build_paths(g, map_keys, kpos):
    paths = {}
    kpos['@'] = start
    for s in map_keys | {'@'}:
        sp = kpos[s]
        for k in map_keys - {s}:
            kp = kpos[k]
            paths[(sp, kp)] = nx.shortest_path(g, sp, kp)
            paths[(kp, sp)] = paths[(sp, kp)][::-1]
    return paths


# g = build_graph(start, map)
# paths = build_paths(g, map_keys, kpos)
g, paths = None, None


def find_keys(pos, map, keys, map_keys=map_keys, kpos=kpos, paths=paths):
    doors = set(k.upper() for k in keys)
    test = doors | set('.@' + KEYS)
    for k in map_keys - set(keys):
        path = paths[(pos, kpos[k])]
        if any(map[p] not in test for p in path):
            continue
        yield k, kpos[k], len(path) - 1


def search(start, map):
    q = deque([(start, 0, ())])
    win = None
    cache = {}
    while q:
        pos, n, keys = q.popleft()
        if win and n >= win:
            continue
        if len(keys) == num_keys:
            print('win!')
            win = n
            yield n, keys
        key = (pos, ''.join(sorted(keys)))
        if key in cache:
            l, res = cache[key]
            if l <= n:
                continue
        else:
            res = tuple(sorted(find_keys(pos, map, keys), key=lambda r: r[2]))
        cache[key] = n, res
        for k, p, m in res:
            q.append((p, n + m, keys + (k,)))


# part 1
# for path in search(start, map):
#     print(path)
# (5450, ('l', 'g', 'a', 'z', 'p', 'h', 'o', 'm', 'd', 'v', 'y', 'q', 'x', 'i', 'c', 's', 't', 'r', 'w', 'k', 'e', 'b', 'n', 'u', 'f', 'j'))
# 430s (pypy)
# now 34s (100s with pypy)

print(f'time: {perf_counter() - t:.2f}s')
t = perf_counter()


def multi_search(rbots, map):
    starts = tuple(r[0] for r in rbots)
    q = deque([(starts, 0, ())])
    win = None
    cache = {}
    while q:
        poss, n, keys = q.popleft()
        if win and n >= win:
            continue
        if len(keys) == num_keys:
            print('win!')
            win = n
            yield n, keys
        key = (poss, ''.join(sorted(keys)))
        if key in cache:
            # print('hit')
            l, res = cache[key]
            if l <= n:
                continue
        else:
            res = []
            for i, pos in enumerate(poss):
                _, _, rkpos, rmap_keys, rpaths = rbots[i]
                # print(pos, keys, rmap_keys)
                rres = tuple(sorted(find_keys(pos, map, keys, rmap_keys, rkpos, rpaths), key=lambda r: r[2]))
                for stuff in rres:
                    res.append((i, *stuff))
                    # print('ap',res, len(res))
        cache[key] = n, res
        # print('r',res, len(res))
        for i, k, p, m in res:
            nposs = poss[:i] + (p,) + poss[i + 1:]
            # print(n,m,keys)
            q.append((nposs, n + m, keys + (k,)))


# data = """
# #############
# #g#f.D#..h#l#
# #F###e#E###.#
# #dCba@#@BcIJ#
# #############
# #nK.L@#@G...#
# #M###N#H###.#
# #o#m..#i#jk.#
# #############
# """
# map = {x + y * 1j: c for y, row in enumerate(data.strip().split('\n')) for x, c in enumerate(row)}
# replace center
map = {**map, start: '#'}
for d in _dir:
    map[start + d] = '#'
for x in [-1, 1]:
    for y in [-1, 1]:
        map[start + x + y * 1j] = '@'

starts = tuple(k for k in map if map[k] == '@')
map_keys = set(k for k in KEYS if k in map.values())
num_keys = len(map_keys)
kpos = {map[p]: p for p in map if map[p] in KEYS}
# dpos = {map[p]: p for p in map if map[p] in DOORS}

print(starts)

rbots = []
for start in starts:
    g = build_graph(start, map)
    rkpos = {k: p for k in kpos if (p := kpos[k]) in g.nodes}
    # rdpos = {k: dpos[k] for k in dpos if k in g}
    rmap_keys = {k for k in map_keys if kpos[k] in g.nodes}
    rpaths = build_paths(g, rmap_keys, rkpos)
    rbots.append([start, g, rkpos, rmap_keys, rpaths])

    # print(rmap_keys)

for res in multi_search(rbots, map):
    print(res)

# part 2
#(2020, ('h', 'o', 'z', 'l', 'g', 'a', 't', 'p', 'm', 'd', 'v', 'y', 'r', 'q', 'w', 'k', 's', 'x', 'i', 'c', 'e', 'b', 'n', 'u', 'f', 'j'))
# 70s

print(f'time: {perf_counter() - t:.2f}s')
t = perf_counter()
