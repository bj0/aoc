with open('d3.txt', 'rt') as f:
    input = f.read().strip()

import numpy as np


def part1(input):
    input = input.strip().split('\n')

    fab = np.zeros((1000, 1000), dtype='object')
    for line in input:
        claim, _, xy, wh = line.split()
        x, y = [int(i) for i in xy[:-1].split(',')]
        w, h = [int(i) for i in wh.split('x')]
        block = fab[x:x + w, y:y + h]
        block[block != 0] = 'X'
        block[block == 0] = claim

    return len(fab[fab == 'X']), fab


def part2(input):
    _, fab = part1(input)
    input = input.strip().split('\n')

    for line in input:
        claim, _, xy, wh = line.split()
        x, y = [int(i) for i in xy[:-1].split(',')]
        w, h = [int(i) for i in wh.split('x')]
        block = fab[x:x + w, y:y + h]
        if not np.any(block == 'X'):
            return claim


print(part1("""
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
"""))

print(part1(input))

print(part2(input))
