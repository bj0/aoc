# from aocd import data

from aoc.util import perf

import networkx as nx

with open("../../input/2023/day25.txt") as f:
    data = f.readlines()

# puz = [[int(x) for x in elf.strip().split()] for elf in data.strip().split('\n\n')]

data = [line.strip() for line in data]

g = nx.complete_graph(5)
nx.draw(g)


print(data)

# @perf
# def part1(puz):
#     return max(sum(elf) for elf in puz)
#
#
# # 69626
# print(f'part1: {part1(puz)}')
#
#
# @perf
# def part2(puz):
#     return sum(sorted((sum(elf) for elf in puz), reverse=True)[:3])
#
#
# # 206780
# print(f'part2 {part2(puz)}')
