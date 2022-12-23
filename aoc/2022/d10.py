from collections import deque

from aocd import data

from aoc.util import perf


#
# data = """addx 15
# addx -11
# addx 6
# addx -3
# addx 5
# addx -1
# addx -8
# addx 13
# addx 4
# noop
# addx -1
# addx 5
# addx -1
# addx 5
# addx -1
# addx 5
# addx -1
# addx 5
# addx -1
# addx -35
# addx 1
# addx 24
# addx -19
# addx 1
# addx 16
# addx -11
# noop
# noop
# addx 21
# addx -15
# noop
# noop
# addx -3
# addx 9
# addx 1
# addx -3
# addx 8
# addx 1
# addx 5
# noop
# noop
# noop
# noop
# noop
# addx -36
# noop
# addx 1
# addx 7
# noop
# noop
# noop
# addx 2
# addx 6
# noop
# noop
# noop
# noop
# noop
# addx 1
# noop
# noop
# addx 7
# addx 1
# noop
# addx -13
# addx 13
# addx 7
# noop
# addx 1
# addx -33
# noop
# noop
# noop
# addx 2
# noop
# noop
# noop
# addx 8
# noop
# addx -1
# addx 2
# addx 1
# noop
# addx 17
# addx -9
# addx 1
# addx 1
# addx -3
# addx 11
# noop
# noop
# addx 1
# noop
# addx 1
# noop
# noop
# addx -13
# addx -19
# addx 1
# addx 3
# addx 26
# addx -30
# addx 12
# addx -1
# addx 3
# addx 1
# noop
# noop
# noop
# addx -9
# addx 18
# addx 1
# addx 2
# noop
# noop
# addx 9
# noop
# noop
# noop
# addx -1
# addx 2
# addx -37
# addx 1
# addx 3
# noop
# addx 15
# addx -21
# addx 22
# addx -6
# addx 1
# noop
# addx 2
# addx 1
# noop
# addx -10
# noop
# noop
# addx 20
# addx 1
# addx 2
# addx 2
# addx -6
# addx -11
# noop
# noop
# noop"""


def run(code):
    """runs code and yields cycle and old/new x whenever register changes"""
    cycle = 0
    x = 1
    yield cycle, x, x
    for line in code.split('\n'):
        match line.split():
            case ['noop']:
                cycle += 1
            case ['addx', dx]:
                oldx = x
                x += int(dx)
                cycle += 2
                yield cycle, oldx, x
    yield cycle, x, x


@perf
def part1(puz):
    sig = 0
    samps = deque([20, 60, 100, 140, 180, 220])
    for c, xp, x in run(puz):
        if c >= samps[0]:
            sig += xp * samps.popleft()
        if not samps:
            break
    return sig


# 14620
print(f'part1: {part1(data)}')


@perf
def part2(puz):
    last = 0
    scr = ''
    for c, xp, x in run(puz):
        for i in range(last, c):
            scr += '#' if abs((i % 40) - xp) < 2 else '.'
            if i == 240:
                return '\n'.join(scr[j * 40:j * 40 + 40] for j in range(5))
        last = c

    return '\n'.join(scr[j * 40:j * 40 + 40] for j in range(6))


# BJFRHRFU
print(f'part2 \n{part2(data)}')
