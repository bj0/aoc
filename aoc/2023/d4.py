from functools import lru_cache
from math import floor

from aocd import data

from aoc.util import perf

inp = data.splitlines()

# inp = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
# Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
# Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
# Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
# Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
# Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""".splitlines()

game = {}
for i, line in enumerate(inp):
    wins, nums = line.split(':')[1].strip().split('|')
    wins = set(int(x) for x in wins.strip().split())
    nums = [int(x) for x in nums.strip().split()]
    game[i + 1] = (wins, nums)


# print(game)
@perf
def part1(game):
    return sum(floor(2 ** (sum(1 for x in nums if x in wins) - 1))
               for (wins, nums) in game.values())


# 27059
print(f'part1: {part1(game)}')


@lru_cache
def process(c):
    if c not in game:
        return 0
    wins, nums = game[c]
    m = len([x for x in nums if x in wins])
    return m + sum(process(x) for x in (c + i for i in range(1, m + 1)))


@perf
def part2():
    n = max(game.keys())
    return sum((1 + process(x)) for x in range(1, n + 1))


# 5744979
print(f'part2 {part2()}')
