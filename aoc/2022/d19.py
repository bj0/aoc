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
    {
        "ore": {"ore": int(a)},
        "clay": {"ore": int(b)},
        "obs": {"ore": int(c), "clay": int(d)},
        "geo": {"ore": int(e), "obs": int(f)},
    }
    for bp in bps
    for (a, b, c, d, e, f) in [bp[1:]]
]

_keys = ["ore", "clay", "obs", "geo"]


def best(bp, T):
    q = deque([(0, {"ore": 1}, {})])
    seen = {}

    # max useful bots
    maxb = {k: max(r.get(k, 0) for r in bp.values()) for k in _keys if not k == "geo"}
    maxb["geo"] = 1000
    while q:
        t, bots, res = q.pop()
        if t >= T:
            yield res["geo"]
            continue
        state = tuple(bots.get(x, 0) for x in _keys)
        if seen.get(state, 100) < t:
            continue
        seen[state] = t

        for r in bp:
            if bots.get(r, 0) == maxb[r]:
                # enough bots!
                continue

            cost = bp[r]
            # can we even build this bot
            if cost.keys() <= bots.keys():
                # time till bot is complete
                dt = (
                    max(
                        (
                            ceil((cost[x] - res.get(x, 0)) / bots[x])
                            for x in cost
                            if cost[x] > res.get(x, 0)
                        ),
                        default=0,
                    )
                    + 1
                )
                if t + dt >= T:
                    # takes too long
                    yield res.get("geo", 0) + bots.get("geo", 0) * (T - t)
                else:
                    newr = {
                        x: res.get(x, 0) + bots.get(x, 0) * dt - cost.get(x, 0)
                        for x in bp
                    }
                    newq = (t + dt, {**bots, r: (bots.get(r, 0) + 1)}, newr)
                    if r == "geo":
                        q.appendleft(newq)
                    else:
                        q.append(newq)


@perf
def part1():
    return sum(max(best(bp, 24)) * (i + 1) for i, bp in enumerate(bps))
    # f = best(bp)
    # print(max(f))


# 1081
print(f"part1: {part1()}")


@perf
def part2():
    return sum(max(best(bp, 32)) * (i + 1) for i, bp in enumerate(bps[:3]))


# 
print(f"part2: {part2()}")
