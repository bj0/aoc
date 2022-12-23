from aocd import data

from aoc.util import perf

# data = """R 4
# U 4
# L 3
# D 1
# R 4
# D 1
# L 5
# R 2"""
#
# data = """R 5
# U 8
# L 8
# D 3
# R 17
# D 10
# L 25
# U 20"""

puz = [(a, int(b)) for a, b in
       (line.split() for line in data.split('\n'))]

_dirs = {"U": -1j, "D": 1j, "L": -1, "R": 1}


def touching(pos0, pos1):
    return max(abs(pos0.real - pos1.real), abs(pos0.imag - pos1.imag)) < 2


def move(pos, tail):
    dx = min(max(pos.real - tail.real, -1), 1)
    dy = min(max(pos.imag - tail.imag, -1), 1)
    return tail + dx + dy * 1j


@perf
def part1(puz):
    pos = 0
    seen = {pos}
    tail = pos
    for (dir, n) in puz:
        for step in range(n):
            pos += _dirs[dir]
            if not touching(tail, pos):
                tail = move(pos, tail)
                seen.add(tail)

    return len(seen)


# 6090
print(f'part1: {part1(puz)}')


@perf
def part2(puz):
    pos = 0
    seen = {pos}
    train = [pos] * 10
    for (dir, n) in puz:
        for step in range(n):
            train[0] += _dirs[dir]
            for j in range(1, len(train)):
                if not touching(train[j - 1], train[j]):
                    train[j] = move(train[j - 1], train[j])
            seen.add(train[-1])

    return len(seen)


# 2581
print(f'part2 {part2(puz)}')
