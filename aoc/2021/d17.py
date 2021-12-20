import re
from math import sqrt


def parse_input(data):
    # m = re.search((r'x=-?\d+..-?\d+, y='))
    _, data = data.split('x=')
    x, y = data.split(', y=')
    x = [int(v) for v in x.split('..')]
    y = [int(v) for v in y.split('..')]
    return x, y


def part1(data):
    # x doesn't matter, answer is highest y-vel that doesn't pass y0 on the way down
    x, y = parse_input(data)
    max_vy = abs(y[0]) - 1

    v = max_vy
    Y = 0
    while v > 0:
        Y += v
        v -= 1
    return Y


def scan(vmax, y0, hit):
    for i in range(vmax[0] + 1):
        for j in range(-vmax[1] - 1, vmax[1] + 1):
            p = (0, 0)
            v = (i, j)
            while v[1] >= y0:
                p = [a + b for (a, b) in zip(p, v)]
                v = max(0, v[0] - 1), (v[1] - 1)
                if hit(p):
                    yield p
                    break


def main(data):
    print(f'part1: {part1(data)}')

    x, y = parse_input(data)
    vmax = x[1] + 1, abs(y[0])

    def hit(p):
        return x[0] <= p[0] <= x[1] and y[0] <= p[1] <= y[1]

    tot = len([p for p in scan(vmax, y[0], hit)])
    print(f'part2: {tot}')


if __name__ == '__main__':
    from aocd import data

    # test_data = """38006F45291200"""
    test_data = """target area: x=20..30, y=-10..-5"""

    # main(test_data)
    main(data)
