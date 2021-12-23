from dataclasses import dataclass, replace
from functools import lru_cache

from aoc.util import perf

home = {
    'A': {3 + i * 1j for i in (2, 3)},
    'B': {5 + i * 1j for i in (2, 3)},
    'C': {7 + i * 1j for i in (2, 3)},
    'D': {9 + i * 1j for i in (2, 3)}
}

_cost = dict(A=1, B=10, C=100, D=1000)

doors = {i + 1j for i in (3, 5, 7, 9)}


@dataclass(frozen=True)
class Amp:
    type: str
    pos: complex

    def cost(self):
        return _cost[self.type]

    def is_home(self):
        return self.pos in home[self.type]

    def is_bottom(self):
        return self.pos.imag == 3


def parse_input(data):
    map = {}
    amps = set()
    for j, line in enumerate(data.splitlines()):
        for i, c in enumerate(line):
            if not c == '':
                map[i + j * 1j] = '#' if c == '#' else '.'
                if c in 'ABCD':
                    amps.add(Amp(c, i + j * 1j))
    return map, amps


# def flatten(amps):
#     return (amp for k in amps for amp in amps[k])


def dof(map, amps, amp, path):
    pos = path[-1] if len(path) > 0 else amp.pos
    # landed home
    if pos in home[amp.type] and (pos.imag == 3 or (pos + 1j) in (x.pos for x in amps if x.type == amp.type)):
        return {path}  # done
    # invalid spot
    if map[pos] != '.':
        return set()
    # already occupied
    if pos in (x.pos for x in amps if x != amp):
        return set()

    paths = set()
    # cannot stop in front of a door or in old spot
    if pos not in doors and pos != amp.pos:
        if amp.pos.imag > 1:  # only moves to hallway if not in hallway
            if pos.imag == 1:  # move to hallway
                paths.add(path)

    for n in (pos + d for d in (1, -1, 1j, -1j)):
        if n not in path and n != amp.pos:
            paths |= dof(map, amps, amp, path + (n,))

    return paths


def cwalk(map, _amps):
    # i = 0
    @lru_cache(None)
    def walk(amps):
        # print(amps)
        from pprint import pprint
        # pprint.pprint([(amp,amp.is_home(),amp.is_bottom()) for amp in amps])
        done = {amp for amp in amps if
                amp.is_home() and (amp.is_bottom() or all(x.is_home() for x in amps if x.type == amp.type))}
        amps = amps - done
        # print('wtf',amps)
        # print('wtf',done)
        # print()
        # global i
        # i += 1
        # if i == 30:
        #     exit()
        if len(amps) == 0:
            yield 0  # done
        moves = sorted(((amp, dof(map, amps, amp, ())) for amp in amps), key=lambda x: len(x[1]))
        for amp, paths in moves:
            # print(amp,len(paths))
            # if len(paths) > 9:
            #     print('wtf len', len(paths))
            #     pprint(amp)
            #     pprint(sorted(paths, key=lambda p: p[-1].real))
            #     # print([p[-1] for p in paths])
            #     pprint(amps)
            #     exit()
            for path in paths:
                # print(amp, f'move to {path[-1]}')
                amp2 = replace(amp, pos=path[-1])
                for cost in walk(frozenset((amps - {amp}) | {amp2})):
                    yield len(path) * amp.cost() + cost

    yield from walk(_amps)


@perf
def part1(map, amps):
    return min(cost for cost in cwalk(map, frozenset(amps)))


def main(data):
    map, amps = parse_input(data)

    print(f'part 1: {part1(map, amps)}')


if __name__ == '__main__':
    # from aocd import data
    #
    # main(data)

    main("""#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########""")
