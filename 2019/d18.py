from collections import deque
from time import perf_counter

import networkx as nx
from aocd import data

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
_dir = (-1, -1j, 1, 1j)  # left up right down

map = {x + y * 1j: c for y, row in enumerate(data.strip().split('\n')) for x, c in enumerate(row)}

start = next(k for k in map if map[k] == '@')
map_keys = set(k for k in KEYS if k in map.values())
num_keys = len(map_keys)
kpos = {map[p]: p for p in map if map[p] in KEYS + '@'}


# build an nx graph of all possible moves (including through doors)
def build_graph(map, kpos):
    g = nx.Graph()
    for start in (kpos[k] for k in kpos if k in '@1234'):
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
    return g


# build key to key shortest path mappings (include start)
# this only works if paths can't go around doors (then there would be multiple "shortest path"s depending on which keys
# you have.  but then what good is a door you can walk around?
def build_paths(g, map_keys, kpos):
    paths = {}
    for s in map_keys | set('@1234'):
        if sp := kpos.get(s, ''):
            for k in map_keys - {s}:
                if (s, k) not in paths:
                    kp = kpos[k]
                    if not nx.has_path(g, sp, kp):
                        continue
                    path = nx.shortest_path(g, sp, kp)[1:-1]
                    stuff = set(d for p in path if (d := map[p]) not in '@.#1234')
                    paths[(s, k)] = len(path) + 1, stuff
                    paths[(k, s)] = len(path) + 1, stuff
    return paths


# find accessible keys from this keys position
def find_keys(key, keys, map_keys, paths):
    for k in map_keys - keys:
        if (key, k) in paths:
            # print(key,k)
            m, stuff = paths[(key, k)]
            if all(d.lower() in keys for d in stuff):
                yield k, m


# slower (.33-.5s)
def search1():
    q = deque([('@', 0, set())])
    cache = {}
    while q:
        ck, n, keys = q.popleft()
        key = (ck, frozenset(keys))
        if cache.get(key, n + 1) <= n:
            continue
        cache[key] = n
        if len(keys) == num_keys:
            yield n
            continue
        for k, m in find_keys(ck, set(keys), map_keys, paths):
            q.append((k, n + m, keys | {k}))


# faster (.07s)
def search0():
    cache = {('@', frozenset()): 0}
    # map_keys = set(k for p in paths.keys() if (k := p[0]) in KEYS)
    for _ in range(len(map_keys)):
        ncache = {}
        for ck, keys in cache:
            n = cache[(ck, keys)]
            for k, m in find_keys(ck, keys, map_keys, paths):
                nkeys = frozenset(keys | {k})
                if (k, nkeys) not in ncache or ncache[(k, nkeys)] > (n + m):
                    ncache[(k, nkeys)] = n + m
        cache = ncache
    yield from cache.values()


t = perf_counter()
g = build_graph(map, kpos)
paths = build_paths(g, map_keys, kpos)

print(f'build time: {perf_counter() - t:.2f}s')
t = perf_counter()

# part 1
n = min(n for n in search0())
print(f'part 1: {n}')
# 5450
# 430s (pypy)
# now 34s (100s with pypy)
# now 0.06s

print(f'time: {perf_counter() - t:.2f}s')
t = perf_counter()


# real slow
def multi_search(rbots):
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
                rres = tuple(sorted(find_keys(pos, keys, rmap_keys, rkpos, rpaths), key=lambda r: r[2]))
                for stuff in rres:
                    res.append((i, *stuff))
                    # print('ap',res, len(res))
        cache[key] = n, res
        # print('r',res, len(res))
        for i, k, p, m in res:
            nposs = poss[:i] + (p,) + poss[i + 1:]
            # print(n,m,keys)
            q.append((nposs, n + m, keys + (k,)))


def multisearch0():
    cache = {('1234', frozenset()): 0}
    for _ in range(len(map_keys)):
        ncache = {}
        for cks, keys in cache:
            n = cache[(cks, keys)]
            for i, rk in enumerate(cks):
                for k, m in find_keys(rk, keys, map_keys, paths):
                    nkeys = frozenset(keys | {k})
                    nks = cks[:i] + k + cks[i + 1:]
                    if (nks, nkeys) not in ncache or ncache[(nks, nkeys)] > (n + m):
                        ncache[(nks, nkeys)] = n + m
        cache = ncache
    yield from cache.values()


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
i = 1
for x in [-1, 1]:
    for y in [-1, 1]:
        map[start + x + y * 1j] = str(i)
        i += 1

starts = tuple(k for k in map if map[k] in '1234')
map_keys = set(k for k in KEYS if k in map.values())
num_keys = len(map_keys)
kpos = {map[p]: p for p in map if map[p] in KEYS + '1234'}

g = build_graph(map, kpos)
paths = build_paths(g, map_keys, kpos)

print(f'build time: {perf_counter() - t:.2f}s')
t = perf_counter()

# part 2
n = min(n for n in multisearch0())
print(f'part 2: {n}')
# 2020
# 70s
# now .1s

print(f'time: {perf_counter() - t:.2f}s')
t = perf_counter()
