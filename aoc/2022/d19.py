import re
from collections import deque
from functools import cache, lru_cache
from math import ceil

from aocd import data

from aoc.util import perf

data = """Blueprint 1:Each ore robot costs 4 ore.Each clay robot costs 2 ore.Each obsidian robot costs 3 ore and 14 clay.Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2:Each ore robot costs 2 ore.Each clay robot costs 3 ore.Each obsidian robot costs 3 ore and 8 clay.Each geode robot costs 3 ore and 12 obsidian."""

bps = [re.findall(r"\d+", line) for line in data.split("\n")]

bps = [
    [[int(a), 0, 0], [int(b), 0, 0], [int(c), int(d), 0], [int(e), 0, int(f)]]
    for bp in bps
    for (a, b, c, d, e, f) in [bp[1:]]
]


def best(bp, T):
    start = (T, [1, 0, 0, 0], [0, 0, 0, 0])
    q = deque([start])
    seen = set()

    # max useful bots
    maxb = [max(r[i] for r in bp) for i in range(3)]

    while q:
        t, bots, res = q.pop()
        state = tuple([t, *bots, *res])
        if state in seen:
            continue
        seen.add(state)

        # no build
        yield res[3] + bots[3] * t

        for bot, cost in enumerate(bp):
            if bot != 3 and bots[bot] >= maxb[bot]:
                # enough bots!
                continue

            dt = 0
            for rt, ra in enumerate(cost):
                if ra == 0:
                    continue
                if bots[rt] == 0:
                    break
                dt = max(dt, ceil((ra - res[rt]) / bots[rt]))
            else:
                newt = t - dt - 1
                if newt < 0:
                    continue
                newb = bots[:]
                newb[bot] += 1
                newr = [x + y * (dt + 1) - c for x, y, c in zip(res, bots, cost + [0])]
                # opt
                for i in range(3):
                    newr[i] = min(newr[i], (maxb[i] - bots[i] + 1) * newt)

                next = (newt, newb, newr)
                # if bot == 3:
                    # q.appendleft(next)
                # else:
                q.append(next)


@perf
def part1():
    return sum(max(best(bp, 24)) * (i + 1) for i, bp in enumerate(bps))
    # f = best(bp)
    # print(max(f))


# 1081
print(f"part1: {part1()}")


@perf
def part2():
    return tuple(max(best(bp, 32)) for i, bp in enumerate(bps[:3]))


#
# print(f"part2: {part2()}")
