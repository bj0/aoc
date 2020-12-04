import re
from collections import Counter

from aocd import data


def parse(line):
    rl, ru, c, p = re.match(r'(\d+)-(\d+) (\w): (\w+)', line).groups()
    return int(rl), int(ru), c, p


def part1(data):
    def valid(line):
        rl, ru, c, p = parse(line)
        return rl <= Counter(p)[c] <= ru

    return sum(1 for line in data.split('\n') if valid(line))


def part2(data):
    def valid(line):
        rl, ru, c, p = parse(line)
        return (p[rl - 1] == c) ^ (p[ru - 1] == c)

    return sum(1 for line in data.split('\n') if valid(line))


p1 = part1(data)
print(f'part 1: {p1}')
# submit(p1)

p2 = part2(data)
print(f'part 2: {p2}')
# submit(p2)
