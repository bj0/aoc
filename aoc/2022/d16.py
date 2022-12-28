from collections import deque
from functools import cache, lru_cache
from itertools import combinations

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
                walk_paths(next, t + 1 + dists[node][next], shut - {next}, T)
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


@perf
def part2(g, dists):
    nodes = frozenset((n for n, d in g.nodes(data=True) if d["rate"] > 0))
    return max(
        walk_paths("AA", 0, frozenset(valves), T=26)
        + walk_paths("AA", 0, nodes - set(valves), T=26)
        for i in range(2, len(g.nodes) // 2)
        for valves in combinations(nodes, i)
    )


#
print(f"part2: {part2(g, dists)}")
