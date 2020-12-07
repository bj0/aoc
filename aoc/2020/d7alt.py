import re

import networkx as nx
from aocd import data

g = nx.DiGraph()
for rule in data.splitlines():
    bag, contents = re.match(r'(.+) bags contain (.+)', rule).groups()
    for inner in contents.strip('.').split(','):
        inner = inner.strip()
        if inner == 'no other bags':
            g.add_edge(bag, 'empty', weight=0)
            continue
        n, col = re.match(r'(\d+) (.+) bags?', inner).groups()
        g.add_edge(bag, col, weight=int(n))

# tot = sum(nx.has_path(g, bag, "shiny gold") for bag in g.nodes if bag != "shiny gold")
tot = len(nx.dfs_tree(g.reverse(), "shiny gold").nodes) - 1
# 115
print(f'part1: {tot}')
# or
tot = len(nx.single_target_shortest_path(g, "shiny gold")) - 1
print(f'part1.1: {tot}')


def get(bag):
    if g.out_degree(bag) == 0:
        return 1
    return sum(g[bag][col]['weight'] * (get(col) + 1) for col in g.neighbors(bag))


tot = get('shiny gold')
# 1250
print(f'part2: {tot}')
