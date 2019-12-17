from util import memoize

# this is much faster than using the Pt class

depth = 5616
tx, ty = 10, 785


@memoize()
def erosion(x, y):
    if x == 0 and y == 0:
        geo = 0
    elif x == tx and y == ty:
        geo = 0
    elif y == 0:
        geo = x * 16807
    elif x == 0:
        geo = y * 48271
    else:
        geo = erosion(x - 1, y) * erosion(x, y - 1)
    return (geo + depth) % 20183


def risk(x, y):
    return erosion(x, y) % 3


print(sum(erosion(x, y) % 3 for x in range(tx + 1) for y in range(ty + 1)))

import time

t = time.perf_counter()

# torch = 1
import heapq

queue = [(0, 0, 0, 1)]  # (minutes, x, y, cannot)
best = dict()  # (x, y, cannot) : minutes

target = (tx, ty, 1)
while queue:
    minutes, x, y, cannot = heapq.heappop(queue)
    best_key = (x, y, cannot)
    if best_key in best and best[best_key] <= minutes:
        continue
    best[best_key] = minutes
    if best_key == target:
        print(minutes)
        break
    for i in range(3):
        if i != cannot and i != risk(x, y):
            heapq.heappush(queue, (minutes + 7, x, y, i))

    # try going up down left right
    # for dx, dy in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
    for dx, dy in [[0, -1], [-1, 0], [1, 0], [0, 1]]:
        newx = x + dx
        newy = y + dy
        if newx < 0:
            continue
        if newy < 0:
            continue
        if risk(newx, newy) == cannot:
            continue
        heapq.heappush(queue, (minutes + 1, newx, newy, cannot))

print(f'{time.perf_counter() - t}s')
