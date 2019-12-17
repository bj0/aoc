import time
from collections import defaultdict, deque
import numpy as np

with open('d22.txt', 'rt') as f:
    input = f.read().strip()

inp = """
..#
#..
...
""".strip()


def part1(input, n, pad_sz=3):
    mem = np.array([list(x) for x in input.split('\n')])

    def pad(v, w, ia, kw):
        v[:w[0]] = "."
        v[-w[1]:] = "."
        return v

    # pad so we don't need to do bounds checking
    mem = np.pad(mem, pad_sz, pad)

    left = np.array([[0, -1], [1, 0]])
    right = np.array([[0, 1], [-1, 0]])
    r, c = np.array(mem.shape) // 2
    infections = 0
    dir = (-1, 0)
    for _ in range(n):
        node = mem[r, c]
        if node == '.':  # clean
            dir = left.dot(dir)
            mem[r, c] = '#'
            infections += 1
        elif node == '#':  # infected
            dir = right.dot(dir)
            mem[r, c] = '.'

        # move
        r, c = (r, c) + dir

    # print('\n'.join(' '.join(x for x in row) for row in mem))
    print(infections)


def part2(input, n, pad_sz=3):
    # mem = np.array([list(x) for x in input.split('\n')])
    mem = defaultdict(lambda: '.')
    lines = input.splitlines()
    for r in range(len(lines)):
        for c in range(len(lines[r])):
            mem[(r, c)] = lines[r][c]

    r = c = len(lines)//2
    infections = 0
    d = 0
    for _ in range(n):
        node = mem[(r, c)]
        if node == '.':  # clean
            d = (d - 1) % 4
            mem[(r, c)] = 'W'
        elif node == '#':  # infected
            d = (d + 1) % 4
            mem[(r, c)] = 'F'
        elif node == 'W':
            mem[(r, c)] = '#'
            infections += 1
        elif node == 'F':
            d = (d + 2) % 4
            del mem[(r, c)]
            # mem[(r, c)] = '.'

        # move
        # doing it this way instead of dot products cuts it by an order of magnitude
        if d == 0:
            r -= 1
        elif d == 1:
            c += 1
        elif d == 2:
            r += 1
        else:
            c -= 1
        # r, c = (r, c) + dir

    # print('\n'.join(' '.join(x for x in row) for row in mem))
    print(infections)


# part1(inp, 70)

# part1(inp, 10000, 200)

# part1(input, 10000, 200)

part2(inp, 100)

t = time.perf_counter()

# 2511978 in 200s
part2(input, int(1e7), 250)

print(f'{time.perf_counter()-t}s')
