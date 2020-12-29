from aocd import data

from aoc.util import perf


@perf
def part1(data):
    def step(map):
        changed = False

        def get(pos):
            nonlocal changed
            occ = sum(1 for d in (1, -1, 1j, -1j, 1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j)
                      if map.get((pos + d), '') == '#')
            if occ == 0 and map[pos] == 'L':
                changed = True
                return '#'
            elif occ >= 4 and map[pos] == '#':
                changed = True
                return 'L'
            return map[pos]

        new = {pos: get(pos) for pos in map}
        return changed, new

    map = {(r + c * 1j): x for r, row in enumerate(data.splitlines())
           for c, x in enumerate(row)
           if x != '.'}

    while (res := step(map))[0]:
        map = res[1]
    return map


@perf
def part2(data):
    def step(map):
        changed = False

        def check(pos, dir):
            while map.get((pos := pos + dir), '') == '.':
                continue
            return map.get(pos, '')

        def get(pos):
            nonlocal changed
            if (x := map[pos]) == '.': return '.'
            occ = sum(1 for d in (1, -1, 1j, -1j, 1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j)
                      if check(pos, d) == '#')
            if occ == 0 and x == 'L':
                changed = True
                return '#'
            elif occ >= 5 and x == '#':
                changed = True
                return 'L'
            return x

        new = {pos: get(pos) for pos in map}
        return changed, new

    map = {(r + c * 1j): x for r, row in enumerate(data.splitlines()) for c, x in enumerate(row)}

    while (res := step(map))[0]:
        map = res[1]
    return map


# 2359
map = part1(data)
print(f'part1: {sum(1 for c in map.values() if c == "#")}')

# 2131
map = part2(data)
print(f'part2: {sum(1 for c in map.values() if c == "#")}')
