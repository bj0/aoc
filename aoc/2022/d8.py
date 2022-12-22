from itertools import takewhile, count

from aocd import data
from functools import reduce
from operator import mul

from aoc.util import perf

# data = """30373
# 25512
# 65332
# 33549
# 35390"""

puz = {(i + j * 1j): int(c)
       for j, line in enumerate(data.split('\n'))
       for i, c in enumerate(line)}


def is_visible(map, pos):
    sz = map[pos]
    for d in (-1, 1, -1j, 1j):
        p = pos
        while map[(p := p + d)] < sz:
            if (p + d) not in map:
                return True
    return False


@perf
def part1(puz):
    h = int(max(x.real for x in puz.keys()) + 1)
    w = int(max(x.imag for x in puz.keys()) + 1)
    return w * 2 + (h - 2) * 2 + sum(is_visible(puz, i + j * 1j)
                                     for j in range(1, h - 1)
                                     for i in range(1, w - 1))


# 1796
print(f'part1: {part1(puz)}')


@perf
def part2(puz):
    def dist(map, pos, d):
        sz = 0
        for t in (map.get(pos + dd * d, 10) for dd in count(1)):
            match t:
                case 10:
                    return sz
                case _ if t < map[pos]:
                    sz += 1
                case _:
                    return sz + 1

    h = int(max(x.real for x in puz.keys()) + 1)
    w = int(max(x.imag for x in puz.keys()) + 1)

    return max(reduce(mul, (dist(puz, i + j * 1j, d)
                            for d in (-1, 1, -1j, 1j)))
               for j in range(h)
               for i in range(w))


# 288120
print(f'part2 {part2(puz)}')
