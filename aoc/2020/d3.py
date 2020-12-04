from itertools import count
from math import prod

from aocd import data

grid = data.splitlines()
m = len(grid[0])
n = len(grid)


def trees(dx, dy):
    return sum(1 for (y, x) in (zip(range(0, n, dy), count(0, dx))) if grid[y][x % m] == '#')
    # x, y = 0, 0
    # count = 0
    # while y < n:
    #     if grid[y][x % m] == '#':
    #         count += 1
    #     x += dx
    #     y += dy
    # return count


# 242
print(f'part1={trees(3, 1)}')

tot = prod(trees(dx, dy) for (dx, dy) in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)))

# 2265549792
print(f'part2={tot}')
