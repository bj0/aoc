from collections import deque

from aocd import data

from aoc.util import perf

puz = data


@perf
def find(puz, n=4):
    mark = deque(puz[:n], maxlen=n)
    if len(set(mark)) == n: return n
    for i, c in enumerate(puz[n:]):
        mark.append(c)
        if len(set(mark)) == n:
            return i + n + 1


# 1779
print(f'part1: {find(puz)}')

# 2635
print(f'part2: {find(puz, 14)}')
