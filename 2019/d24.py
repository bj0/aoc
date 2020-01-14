from time import perf_counter

from aocd import data

# data = """
# ....#
# #..#.
# #..##
# ..#..
# #...."""


def bugs(grid, pos):
    count = 0
    for dir in (-1, 1, -1j, 1j):
        count += grid.get(pos + dir, 0)
    return count


def update(grid):
    ngrid = {}
    for pos in grid:
        n = bugs(grid, pos)
        if grid[pos] and n != 1:
            ngrid[pos] = 0
        elif not grid[pos] and (n == 1 or n == 2):
            ngrid[pos] = 1

    return {**grid, **ngrid}


def print_grid(grid):
    return '\n'.join(''.join('#' if grid[x + y * 1j] else '.' for x in range(5)) for y in range(5))


t = perf_counter()

grid = {}
for y, row in enumerate(data.strip().split('\n')):
    for x, c in enumerate(row):
        grid[x + y * 1j] = 1 if c == '#' else 0

seen = set()
i = 0
while (k := print_grid(grid)) not in seen:
    seen.add(k)
    grid = update(grid)
    i += 1
print(k)
print(i)

br = sum(2 ** (x.imag * 5 + x.real) for x in grid if grid[x] == 1)

print(f'part 1: {int(br)}')

print(f'time: {perf_counter() - t:.2f}s')
t = perf_counter()


def bugs2(grid, l, pos, dir):
    npos = pos + dir
    if npos == 2 + 2j:  # inner grid
        if any((lvl := grid.get(l + 1, {})).values()):
            if dir == -1:
                return sum(lvl.get(4 + y * 1j, 0) for y in range(5))
            elif dir == 1:
                return sum(lvl.get(y * 1j, 0) for y in range(5))
            elif dir == 1j:
                return sum(lvl.get(x, 0) for x in range(5))
            elif dir == -1j:
                return sum(lvl.get(x + 4j, 0) for x in range(5))
        else:
            return 0
    elif npos.imag < 0:
        return grid.get(l - 1, {}).get(2 + 1j, 0)
    elif npos.imag > 4:
        return grid.get(l - 1, {}).get(2 + 3j, 0)
    elif npos.real < 0:
        return grid.get(l - 1, {}).get(1 + 2j, 0)
    elif npos.real > 4:
        return grid.get(l - 1, {}).get(3 + 2j, 0)
    else:
        return grid.get(l, {}).get(npos)


def update2(grid):
    ngrid = {}
    lm = min(grid.keys()) - 1
    lx = max(grid.keys()) + 1
    grid[lm] = {**empty}
    grid[lx] = {**empty}
    for l in range(lm, lx + 1):
        ngrid[l] = {}
        for pos in grid[l]:
            if pos == 2 + 2j:
                continue
            n = 0
            for dir in (-1, 1, -1j, 1j):
                n += bugs2(grid, l, pos, dir)
            if grid[l][pos] and n != 1:
                ngrid[l][pos] = 0
            elif not grid[l][pos] and (n == 1 or n == 2):
                ngrid[l][pos] = 1
            else:
                ngrid[l][pos] = grid[l][pos]

    if not any(ngrid[lm].values()):
        del ngrid[lm]
    if not any(ngrid[lx].values()):
        del ngrid[lx]
    return ngrid


grid = {}
grid[0] = {}
empty = {}
for y, row in enumerate(data.strip().split('\n')):
    for x, c in enumerate(row):
        grid[0][x + y * 1j] = 1 if c == '#' else 0
        empty[x + y * 1j] = 0

for i in range(200):
    grid = update2(grid)

# for l in sorted(grid.keys()):
#     print(l)
#     for y in range(5):
#         print(''.join('?' if (x+y*1j) not in grid[l] else ('#' if grid[l].get(x + y * 1j) else '.') for x in range(5)))
print()
n = sum(sum(grid[lvl].values()) for lvl in grid)
print(f'part 2: {n}')

print(f'time: {perf_counter() - t:.2f}s')
