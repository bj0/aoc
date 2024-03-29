import networkx as nx
from aocd import data

from aoc.util import perf

# data = """Sabqponm
# abcryxxl
# accszExk
# acctuvwj
# abdefghi"""

grid = [row[:] for row in data.split('\n')]
g = nx.DiGraph()
mgrid = {i + j * 1j: c
         for j, row in enumerate(grid)
         for i, c in enumerate(row)}

for pos in mgrid:
    c = ord(mgrid[pos].replace('S', 'a').replace('E', 'z'))
    # print(f'pos:{pos}, {chr(c)} {c}')
    for d in (-1, -1j):
        b = mgrid.get(pos1 := pos + d, '#')
        if b == '#': continue
        if b == 'S': b = 'a'
        if b == 'E': b = 'z'
        # print(f'chk: {b} {ord(b)}')
        if ord(b) >= c - 1:
            # print(f'{pos1}->{pos}')
            g.add_edge(pos1, pos)
        if ord(b) <= c + 1:
            # print(f'{pos}->{pos1}')
            g.add_edge(pos, pos1)

print(g)


@perf
def part1(mgrid, g):
    start = next(p for p in mgrid if mgrid[p] == 'S')
    end = next(p for p in mgrid if mgrid[p] == 'E')
    # print(start, end)
    return nx.shortest_path_length(g, start, end)


#
print(f'part1: {part1(mgrid, g)}')


def try_get_path(g, start, end):
    try:
        return nx.shortest_path_length(g, start, end)
    except:
        return 1000


@perf
def part2(mgrid, g):
    starts = [pos for pos in mgrid if mgrid[pos] in 'aS']
    end = next(p for p in mgrid if mgrid[p] == 'E')
    return min(try_get_path(g, start, end) for start in starts)


#
print(f'part2: {part2(mgrid, g)}')
