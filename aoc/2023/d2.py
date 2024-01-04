from math import prod

from aocd import data

from aoc.util import perf

inp = data.splitlines()

# inp = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
# Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
# Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
# Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
# Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""".splitlines()

game = {}
for line in inp:
    gid, rev = line.split(':')
    gid = int(gid.split(' ')[-1])
    cols = {}
    for group in rev.strip().split(';'):
        for group2 in group.strip().split(','):
            n, col = group2.strip().split(' ')
            cols[col] = cols.get(col, ()) + (int(n),)
    game[gid] = cols


# print(game)


@perf
def part1(puz):
    return sum(i for (i, cols) in puz.items()
               if max(cols['red']) <= 12 and max(cols['green']) <= 13 and max(cols['blue']) <= 14)


# 2061
print(f'part1: {part1(game)}')

C = ('red', 'green', 'blue')


@perf
def part2(puz):
    return sum(prod(max(cols[c]) for c in C)
               for (i, cols) in puz.items())


# 72596
print(f'part2 {part2(game)}')
