from aocd import data

from aoc.util import mdist

TURN = {
    90: 1j,
    180: -1,
    270: -1j
}
DIR = {
    'N': 1,
    'E': 1j,
    'S': -1,
    'W': -1j
}


def p1(data):
    pos = 0 + 0j
    dir = 1j
    for line in data.splitlines():
        op, n = line[0], int(line[1:])
        if op in 'NESW':
            pos += n * DIR[op]
        elif op == 'R':
            dir *= TURN[n]
        elif op == 'L':
            dir *= TURN[360 - n]
        elif op == 'F':
            pos += n * dir
    return pos


def p2(data):
    pos = 0 + 0j
    wp = 1 + 10j
    for line in data.splitlines():
        op, n = line[0], int(line[1:])
        if op in 'NESW':
            wp += n * DIR[op]
        elif op == 'R':
            wp *= TURN[n]
        elif op == 'L':
            wp *= TURN[360 - n]
        elif op == 'F':
            pos += n * wp
    return pos


pos = p1(data)
# 636
print(f'part1: {mdist(0, pos)}')

pos = p2(data)
print(f'part2: {mdist(0, pos )}')