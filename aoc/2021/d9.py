from collections import deque
from math import prod

_neighbors = {-1, 1, -1j, 1j}


def parse_input(data):
    data = [[int(v) for v in row] for row in data.split()]
    return {(i + j * 1j): data[j][i]
            for j in range(len(data))
            for i in range(len(data[0]))
            }


def find_lows(grid):
    return [c for c in grid if min(grid.get(c + d, 10) for d in _neighbors) > grid[c]]


def find_basins(grid, lows):
    return [map_basin(grid, c) for c in lows]


def map_basin(grid, c):
    basin = {c}

    # todo does it always end at 9 or can it change direction
    def flows(p):
        return grid.get(p, 10) < 9

    q = deque([c + d for d in _neighbors if flows(c + d)])
    while q:
        p = q.popleft()
        basin.add(p)
        for n in (p + d for d in _neighbors if flows(p + d) and (p + d) not in basin):
            q.append(n)

    return basin


def main():
    from aocd import data
    # data = """2199943210
    # 3987894921
    # 9856789892
    # 8767896789
    # 9899965678
    # """

    grid = parse_input(data)
    lows = find_lows(grid)
    risk = sum(grid[c] + 1 for c in lows)
    print(f'part 1: {risk}')

    tot = prod(sorted(len(map_basin(grid, c)) for c in lows)[-3:])
    print(f'part 2: {tot}')


if __name__ == '__main__':
    main()
