from functools import cmp_to_key

from aocd import data

from aoc.util import perf

# data = """[1,1,3,1,1]
# [1,1,5,1,1]
#
# [[1],[2,3,4]]
# [[1],4]
#
# [9]
# [[8,7,6]]
#
# [[4,4],4,4]
# [[4,4],4,4,4]
#
# [7,7,7,7]
# [7,7,7]
#
# []
# [3]
#
# [[[]]]
# [[]]
#
# [1,[2,[3,[4,[5,6,7]]]],8,9]
# [1,[2,[3,[4,[5,6,0]]]],8,9]"""

puz = [tuple(eval(packet) for packet in line.split('\n'))
       for line in data.split('\n\n')]


def check(left, right):
    match (left, right):
        case (int(a), int(b)):
            return (a < b) - (b < a)
        case (list(a), int(b)):
            return check(a, [b])
        case (int(a), list(b)):
            return check([a], b)
        case (list(a), list(b)):
            for x, y in zip(a, b):
                if (ret := check(x, y)) != 0:
                    return ret
            return (len(a) < len(b)) - (len(b) < len(a))


@perf
def part1(puz):
    return sum(i + 1
               for i, (left, right) in enumerate(puz) if check(left, right) != -1)


# 6070
print(f'part1: {part1(puz)}')


@perf
def part2(puz):
    msg = sorted((l for pair in (puz + [[[[2]]], [[[6]]]]) for l in pair), key=cmp_to_key(check), reverse=True)
    return (msg.index([[2]]) + 1) * (msg.index([[6]]) + 1)


# 20758
print(f'part2: {part2(puz)}')
