import time

import networkx as nx
from aocd import data

t = time.perf_counter()

g = nx.Graph(o.strip().split(')') for o in data.strip().split())
print(f"part 1: {sum(nx.shortest_path_length(g, 'COM', o) for o in g.nodes)}")
print(f"part 2: {nx.shortest_path_length(g, 'YOU', 'SAN') - 2}")
# for directed graph
# print(f"part 1: {nx.transitive_closure(g).size()}")
# print(f"part 2: {nx.shortest_path_length(g.to_undirected(), 'YOU', 'SAN') - 2}")

print(f'done in {time.perf_counter() - t:.2}s')
