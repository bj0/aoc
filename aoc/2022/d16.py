from collections import deque
from functools import cache, lru_cache

from aocd import data

from aoc.util import perf

import networkx as nx
import re


# data = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
# Valve BB has flow rate=13; tunnels lead to valves CC, AA
# Valve CC has flow rate=2; tunnels lead to valves DD, BB
# Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
# Valve EE has flow rate=3; tunnels lead to valves FF, DD
# Valve FF has flow rate=0; tunnels lead to valves EE, GG
# Valve GG has flow rate=0; tunnels lead to valves FF, HH
# Valve HH has flow rate=22; tunnel leads to valve GG
# Valve II has flow rate=0; tunnels lead to valves AA, JJ
# Valve JJ has flow rate=21; tunnel leads to valve II"""


g = nx.Graph()
for line in data.split("\n"):
    (node, rate, tunnels) = re.match(
        r"Valve (\w+) has flow rate=(\d+);.* valves? (.+)", line
    ).groups()
    g.add_node(node, rate=int(rate))
    for tun in tunnels.split(", "):
        g.add_edge(node, tun)


# all travel distances
dists = {frm: to for frm, to in nx.all_pairs_shortest_path_length(g)}


@cache
def walk_paths(node, t, shut, T=30):
    if t >= T:
        return 0
    sum = g.nodes[node]["rate"] * (T - t)
    return (
        (
            sum
            + max(
                walk_paths(next, t + 1 + dists[node][next], shut - {next})
                for next in shut
            )
        )
        if shut
        else sum
    )


@perf
def part1(g, dists):
    return walk_paths(
        "AA", 0, frozenset(n for n, d in g.nodes(data=True) if d["rate"] > 0)
    )


print(f"part1: {part1(g, dists)}")


@lru_cache(100_000)
# @cache
def walk_paths2(node0, node1, t0, t1, shut):
    def first(x):
        return x[0]

    t = min(t0, t1)
    suma = sumb = (0, ((90, "end"),))
    # if we run out of time
    if t >= 26:
        return suma
    # if we're done opening something
    if t == t0:
        sum = g.nodes[node0]["rate"] * (26 - t)
        # more valves to open
        if shut:
            mx = max(
                (
                    walk_paths2(
                        next, node1, t + 1 + dists[node0][next], t1, shut - {next}
                    )
                    for next in shut
                ),
                key=first,
            )
            suma = (mx[0] + sum, ((t, f"a:{node0}"),) + mx[1])
        # no more valves to open, elephant still opening one?
        elif t1 > t:
            if node1 == "end":
                return (sum, ((f"b:{node0}"),))
            mx = walk_paths2("end", node1, 50, t1, shut)
            return (mx[0] + sum, ((t, f"a:{node0}"),) + mx[1])
    # if elephant's done opening something
    if t == t1:
        sum = g.nodes[node1]["rate"] * (26 - t)
        # more valvues to open
        if shut:
            mx = max(
                (
                    walk_paths2(
                        node0, next, t0, t + 1 + dists[node1][next], shut - {next}
                    )
                    for next in shut
                ),
                key=first,
            )
            sumb = (mx[0] + sum, ((t, f"b:{node1}"),) + mx[1])
        # no more valves to open, we still opening one?
        elif t0 > t:
            if node0 == "end":
                return (sum, ((f"b:{node1}"),))
            mx = walk_paths2(node0, "end", t0, 50, shut)
            return (mx[0] + sum, ((t, f"b:{node1}"),) + mx[1])
    return max(suma, sumb, key=first)


@perf
def part2(g, dists):
    return walk_paths2(
        "AA", "AA", 0, 0, frozenset(n for n, d in g.nodes(data=True) if d["rate"] > 0)
    )


#
print(f"part2: {part2(g, dists)}")
