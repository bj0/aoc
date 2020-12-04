import networkx

from util import Pt, memoize


def gindex(pt: Pt):
    if pt == Pt(0, 0) or pt == target:
        return 0
    elif pt.x == 0:
        return pt.y * 48271
    elif pt.y == 0:
        return pt.x * 16807
    return erosion(pt - (1, 0)) * erosion(pt - (0, 1))


@memoize()
def erosion(pt: Pt):
    return (gindex(pt) + DEPTH) % 20183


def region(pt: Pt):
    return erosion(pt) % 3


# 0 - rocky / no nothing
# 1 - wet / no torch
# 2 - narrow / no climbing

DEPTH, target = 5616, Pt(10, 785)

# create a graph and add edges for switching tools
G = networkx.DiGraph()
for y in range(target.y + 50):
    for x in range(target.x + 50):
        loc = Pt(x, y)
        for t1 in range(3):
            for t2 in range(3):
                if t1 != region(loc) and t2 != region(loc):
                    G.add_edge((loc, t1), (loc, t2), weight=7)

        for nb in loc.nb4():
            if nb.x < 0 or nb.y <= 0:
                continue
            for t in range(3):
                if t != region(loc) and t != region(nb):
                    G.add_edge((loc, t), (nb, t), weight=1)

p1 = sum(region(Pt(x, y)) for x in range(target.x + 1) for y in range(target.y + 1))
print(f'part 1: {p1}')

import time

t = time.perf_counter()

shortest_path_length = networkx.dijkstra_path_length(G, (Pt(0, 0), 1), (target, 1))
print(f"part 2: {shortest_path_length}")

print(f'{time.perf_counter() - t}s')
