# without caching takes forever

from dataclasses import dataclass, replace
from functools import lru_cache, wraps

from aoc.util import perf

_cost = dict(A=1, B=10, C=100, D=1000)
_doors = dict(A=2, B=4, C=6, D=8)


@dataclass
class Amp:
    type: str


def parse_input(data):
    map = {(i, 0): '.' for i in range(11)}
    chars = (c for c in data if c in 'ABCD')
    for i, c in zip((2, 4, 6, 8), chars):
        map[(i, 1)] = c
    for i, c in zip((2, 4, 6, 8), chars):
        map[(i, 2)] = c

    return map


def open(map, c):
    x = _doors[c]
    return all(i in ['.', c] for i in (map[(x, j)] for j in (1, 2)))


def full(map, c):
    x = _doors[c]
    return all(i == c for i in (map[(x, j)] for j in (1, 2)))


def is_stuck(map, pos):
    return pos[1] == 2 and map[(pos[0], 1)] != '.'


def can_reach_home(map, pos):
    c = map[pos]
    x = _doors[c]
    dir = 1 if x > pos[0] else -1
    return all(i == '.' for i in (map[(j, 0)] for j in range(pos[0] + dir, x, dir)))


def is_home(map, pos):
    c = map[pos]
    x = _doors[c]
    return pos[0] == x and map[(x, 2)] == c


def moves(map, pos):
    if is_home(map, pos) or is_stuck(map, pos):
        return
    c = map[pos]
    if pos[1] == 0:  # isle
        if open(map, c) and can_reach_home(map, pos):
            x = _doors[c]
            yield x, 2 if map[(x, 2)] == '.' else 1
    else:  # move to isle
        p = pos[0] - 1, 0
        while p[0] >= 0 and map[p] == '.':
            if p[0] not in _doors.values():
                yield p
            p = (p[0] - 1, 0)

        p = pos[0] + 1, 0
        while p[0] < 11 and map[p] == '.':
            if p[0] not in _doors.values():
                yield p
            p = (p[0] + 1, 0)


def solve(map, total=0, limit=1e9, seen=None):
    if all(full(map, c) for c in 'ABCD'):  # done
        return total

    seen = seen if seen is not None else set()

    for p, c in map.items():
        if c in 'ABCD':
            for move in moves(map, p):
                cost = abs(move[0] - p[0]) + p[1] + move[1]
                cost *= _cost[c]
                if total + cost >= limit:
                    continue
                new_map = {**map, p: '.', move: c}
                sig = total, hash(frozenset(new_map.items()))
                if sig in seen: continue
                seen.add(sig)
                limit = solve(
                    new_map,
                    total + cost, limit, seen)

    return limit


@perf
def part1(map):
    return solve(map)


def main(data):
    map = parse_input(data)

    print(f'part 1: {part1(map)}')


if __name__ == '__main__':
    # from aocd import data

    # main(data)

    main("""#############
#...........#
###C#A#B#D###
  #D#C#A#B#
  #########
""")

#     main("""#############
# #...........#
# ###B#C#B#D###
#   #A#D#C#A#
#   #########""")
