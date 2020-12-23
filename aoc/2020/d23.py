from aocd import data

from aoc.util import perf

data = '389125467'

cups = [int(d) for d in data]
N = max(cups)


def rot(n):
    return ((n - 1) % N) + 1


for move in range(100):
    cur, *rest = cups
    held, rest = rest[:3], rest[3:]
    next = rot(cur - 1)
    while next in held:
        next = rot(next - 1)
    i = rest.index(next) + 1
    cups = rest[:i] + held + rest[i:] + [cur]

i = cups.index(1)

# 65432978
print(f'part1: {"".join(str(x) for x in (cups[i:] + cups[:i]))[1:]}')

cups = [int(d) for d in data]
N = max(cups)
M = 10
cups += list(range(N + 1, M + 1))
N = M


# cups = [999_998, 999_999, 1_000_000, 8, 9,
#         *[i for i in range(11, 999_998 + 1) if i % 4 != 2],
#         1, 3, 4, 6, 7, 2, 5,
#         *[i for i in range(10, 999_994 + 1, 4)]]

# idx = cups.index(14)

@perf
def part2(cups):
    print(0, cups[:12], cups[-25:])
    last = None
    for move in range(M * 10):
        cur, *rest = cups
        held, rest = rest[:3], rest[3:]
        next = rot(cur - 1)
        while next in held:
            next = rot(next - 1)
        i = rest.index(next) + 1
        cups = rest[:i] + held + rest[i:] + [cur]
        # if (move + 1) % 100 == 0:
        # print(move + 1, cups[:12], cups[-25:])
        # print('  ',cups[idx-18:idx+4])
        i = cups.index(1)
        # if cups[i:i + 3] == [1, 524,822]:
        if cups[i:i+3] != last:
            print('wtf',move, cups[i:i + 3])
            last = cups[i:i+3]

    i = cups.index(1)
    print(cups[i:i + 10])


part2(cups)
# print(cups)
