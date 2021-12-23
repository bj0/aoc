import re

from aoc.util import perf


def parse_input(data):
    ops, blocks = zip(*(line.split(' ') for line in data.splitlines()))
    blocks = [tuple((int(a), int(b))
                    for a, b in (span.split('..')
                                 for span in re.findall(r'(-?\d+..-?\d+)', block)))
              for block in blocks]
    return ops, blocks


@perf
def part1(ops, blocks):
    core = {}
    for op, block in zip(ops, blocks):
        p = 1 if op == 'on' else 0
        x, y, z = block
        for i in range(max(-50, x[0]), min(51, x[1] + 1)):
            for j in range(max(-50, y[0]), min(51, y[1] + 1)):
                for k in range(max(-50, z[0]), min(51, z[1] + 1)):
                    core[(i, j, k)] = p

    return core


def intersection(a, b):
    return [(max(l), min(r)) for l, r in (zip(ca, cb) for ca, cb in zip(a, b))]


@perf
def part2(ops, blocks):
    core = set()
    for op, block in zip(ops, blocks):
        p = 1 if op == 'on' else 0
        x, y, z = block
        for i in range(x[0], x[1] + 1):
            for j in range(y[0], y[1] + 1):
                for k in range(z[0], z[1] + 1):
                    if p:
                        core.add((i, j, k))
                    else:
                        core.discard((i, j, k))

    return core


def main(data):
    ops, blocks = parse_input(data)

    core = part1(ops, blocks)
    print(f'part 1: {sum(1 for p in core if core[p])}')

    core = part2(ops, blocks)
    print(f'part 2: {sum(1 for p in core if core[p])}')


if __name__ == '__main__':
    from aocd import data

    main(data)
