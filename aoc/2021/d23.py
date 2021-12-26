# without caching takes forever
# got it down from 20+ minutes to 4s!

from itertools import cycle

from aoc.util import perf

_cost = dict(A=1, B=10, C=100, D=1000)
_doors = dict(A=2, B=4, C=6, D=8)


def parse_input(data):
    map = {'h': '.' * 11}
    chars = (c for c in data if c in 'ABCD')
    for h, c in zip(cycle('ABCD'), chars):
        map[h] = map.get(h, '') + c

    return map


def is_open(home, c):
    return len(home) == 0 or all(i == c for i in home)


def is_full(map, c):
    return c not in map['h'] and all(i == c for i in map[c])


def can_reach_home(hall, pos):
    c = hall[pos]
    x = _doors[c]
    dir = 1 if x > pos else -1
    return all(i == '.' for i in hall[pos + dir:x:dir])


def moves(hall, pos):
    p = pos - 1
    # print(p,hall)
    while p >= 0 and hall[p] == '.':
        if p not in _doors.values():
            yield p
        p -= 1

    p = pos + 1
    while p < 11 and hall[p] == '.':
        if p not in _doors.values():
            yield p
        p += 1


def _hash(map):
    return ';'.join(''.join(x) for x in (map[i] for i in 'hABCD'))


def solve(map, total=0, limit=1e9, seen=None, D=2):
    if all(is_full(map, c) for c in 'ABCD'):  # done
        # print('dun', total, limit)
        # print(map)
        return total

    seen = seen if seen is not None else {}
    hall = map['h']
    for i, c in enumerate(hall):
        if c != '.' and is_open(home := map[c], c) and can_reach_home(hall, i):
            cost = abs(_doors[c] - i) + D - len(home)
            cost *= _cost[c]
            if total + cost > limit:
                continue
            new_map = {**map, 'h': hall[:i] + '.' + hall[i + 1:], c: [c] + home}
            sig = _hash(new_map)
            if sig in seen and seen[sig] <= total:
                continue
            seen[sig] = total
            limit = solve(
                new_map,
                total + cost, limit, seen, D=D)

    for x, home in ((i, map[i]) for i in 'ABCD'):
        if not is_open(home, x):
            for move in moves(hall, _doors[x]):
                c, *rest = home
                cost = abs(move - _doors[x]) + D - len(rest)
                cost *= _cost[c]
                if total + cost > limit:
                    continue
                new_map = {**map, 'h': hall[:move] + c + hall[move + 1:], x: rest}
                sig = _hash(new_map)
                if sig in seen and seen[sig] <= total:
                    continue
                seen[sig] = total
                limit = solve(
                    new_map,
                    total + cost, limit, seen, D=D)
    return limit


@perf
def part1(map):
    return solve(map)

@perf
def part2(map):
    return solve(map, D=4)


def main():
    # part 1
    map = parse_input("""#############
    #...........#
    ###C#A#B#D###
      #D#C#A#B#
      #########
    """)

    print(f'part 1: {part1(map)}')

    # part 2
    map = parse_input("""#############
#...........#
###C#A#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #D#C#A#B#
  #########
""")
#     map = parse_input("""#############
# #...........#
# ###B#C#B#D###
#   #D#C#B#A#
#   #D#B#A#C#
#   #A#D#C#A#
#   #########
# """)

    print(f'part 2: {part2(map)}')


if __name__ == '__main__':
    main()
