from math import prod

from aocd import data

from aoc.util import perf

inp = data.splitlines()

# inp = """467..114..
# ...*......
# ..35..633.
# ......#...
# 617*......
# .....+.58.
# ..592.....
# ......755.
# ...$.*....
# .664.598..""".splitlines()

grid = {}
for r, line in enumerate(inp):
    for c, s in enumerate(line):
        if s != '.':
            grid[(c, r)] = s

NUM = '0123456789'


def find_num(grid, pos, used):
    x, y = pos
    more = set()
    while grid.get((x, y), '.') in NUM: x -= 1
    n = ''
    while grid.get((x + 1, y), '.') in NUM:
        x += 1
        n += grid.get((x, y))
        if (x, y) in used:
            return None, used
        more.add((x, y))
    return n, used | more


@perf
def part1(grid):
    used = set()
    nums = {}
    for pos, s in grid.items():
        if s in NUM:
            continue
        for p in ((pos[0] + x, pos[1] + y) for x in (-1, 0, 1) for y in (-1, 0, 1)):
            if p not in used and grid.get(p, '.') in NUM:
                n, used = find_num(grid, p, used)
                if n is not None:
                    nums.setdefault(pos, []).append(int(n))
    return sum(x for x in (i for l in nums.values() for i in l)), nums


# 512794
print(f'part1: {part1(grid)[0]}')


@perf
def part2(grid):
    n, nums = part1(grid)
    return sum(prod(vals) for (p, vals) in nums.items() if grid[p] == '*' and len(vals) == 2)


# 67779080
print(f'part2 {part2(grid)}')
