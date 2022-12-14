from collections import deque

from aocd import data

from aoc.util import perf

layout, steps = data.split('\n\n')

layout = [row for row in layout.split('\n')]

stacks = [deque() for i in range(9)]
for row in reversed(layout[:-1]):
    for i, c in enumerate(row[1::4]):
        if c != ' ':
            stacks[i].append(c)


@perf
def part1(stacks, steps):
    for step in steps.split('\n'):
        step = step.split(' ')
        n, frm, to = (int(step[i]) for i in (1, 3, 5))
        for x in [stacks[frm - 1].pop() for i in range(n)]:
            stacks[to - 1].append(x)

    return ''.join(x[-1] for x in stacks)


# VCTFTJQCG
print(f'part1: {part1([deque(s) for s in stacks], steps)}')


@perf
def part2(stacks, steps):
    for step in steps.split('\n'):
        step = step.split(' ')
        n, frm, to = (int(step[i]) for i in (1, 3, 5))
        for x in reversed([stacks[frm - 1].pop() for i in range(n)]):
            stacks[to - 1].append(x)

    return ''.join(x[-1] for x in stacks)


# GCFGLDNJZ
print(f'part2 {part2(stacks, steps)}')
