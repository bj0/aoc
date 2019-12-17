with open('d1.txt', 'rt') as f:
    input = f.read()


def part1(input, sep=','):
    changes = [int(x.strip()) for x in input.strip().split(sep)]

    start = 0
    for d in changes:
        start += d

    return start


def part2(input, sep=','):
    changes = [int(x.strip()) for x in input.strip().split(sep)]

    cur = 0
    seen = set()
    while cur not in seen:
        for d in changes:
            seen.add(cur)
            cur += d
            if cur in seen:
                return cur

    return cur


for inp in [
    "+1, -2, +3, +1",
    "+1, +1, +1",
    "+1, +1, -2",
    "-1, -2, -3"
]:
    print(part1(inp))

print(part1(input, '\n'))

for inp in [
    "+1, -2, +3, +1",
    '1, -1',
    '3, 3, 4, -2, -4',
    '-6, 3, 8, 5, -6',
    '7, 7, -2, -7, -4'
]:
    print(part2(inp))

print(part2(input, '\n'))