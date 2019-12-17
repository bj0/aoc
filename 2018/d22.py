import heapq

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

def part2():
    # use heapq, a min sorted priority queue
    pq = [(0, Pt(0, 0), 1)]  # time, loc, tool
    seen = {}
    tgt = (target, 1)

    while pq:
        t, loc, tool = heapq.heappop(pq)
        k = (loc, tool)
        if k in seen and seen[k] <= t:
            continue
        seen[k] = t

        if k == tgt:
            print(f'found target: {t}')
            break

        # tool switches
        for i in range(3):
            if i != tool and i != region(loc):
                heapq.heappush(pq, (t + 7, loc, i))

        # move to neighbors
        for nb in (n for n in loc.nb4() if n.x >= 0 and n.y >= 0):
            if tool != region(nb):
                heapq.heappush(pq, (t + 1, nb, tool))


DEPTH, target = 5616, Pt(10, 785)
# DEPTH, target = 510, Pt(10, 10)

p1 = sum(region(Pt(x, y)) for x in range(target.x + 1) for y in range(target.y + 1))

print(f'part 1: {p1}')

import time
t = time.perf_counter()

# 1070 at ~50s
part2()

print(f'{time.perf_counter() - t}s')
