from aocd import data

from aoc.util import perf

puz = [(ord(a) - ord('A'), ord(b) - ord('X')) for (a, b) in
       (line.split() for line in data.strip().split('\n'))]


@perf
def part1(puz):
    def game(a, b):
        # score of game
        r = ((b - a + 1) % 3) * 3
        # plus choice
        return r + b + 1

    return sum(game(a, b) for (a, b) in puz)


# 13009
print(f'part1: {part1(puz)}')


@perf
def part2(puz):
    def game(a, b):
        b = b - 1
        # choice based on b
        r = (a + b) % 3 + 1
        # score
        return (b + 1) * 3 + r

    return sum(game(a, b) for (a, b) in puz)


# 10398
print(f'part2 {part2(puz)}')
