# while this works and is very fast, some people noticed that there are a (very small) finite number of possible inputs
# and you don't need caching if you just figure them out and check them.  caching is the lazy way though.

from functools import reduce, lru_cache
from itertools import count, product

from aoc.util import perf


def parse_input(data):
    p1, p2 = data.splitlines()
    p1 = int(p1.split(': ')[-1])
    p2 = int(p2.split(': ')[-1])
    return p1, p2


def play(start, first_roll=1):
    score = 0
    pos = start
    for r in count(first_roll, step=6):
        pos = ((3 * r + 3 + pos - 1) % 10) + 1
        score += pos
        yield score


@perf
def part1(p1, p2):
    for j, (s1, s2) in enumerate(zip(play(p1), play(p2, first_roll=4))):
        if s1 >= 1000:
            s = s2
            r = (j + 1) * 3 * 2 - 3
            break
        elif s2 >= 1000:
            s = s1
            r = (j + 1) * 3 * 2
            break
    print(f'part 1: {r * s}')


@lru_cache(maxsize=None)
def qplay(p1, p2, s1=0, s2=0, turn=1):
    if s1 >= 21:
        return 1, 0
    elif s2 >= 21:
        return 0, 1
    else:
        def sum_wins(acc, x):
            return tuple(t + w for t, w in zip(acc, x))

        rolls = product((1, 2, 3), repeat=3)
        if turn == 1:
            pos = ((p1 + sum(r) - 1) % 10 + 1 for r in rolls)
            return reduce(sum_wins, (qplay(np1, p2, s1 + np1, s2, turn=2) for np1 in pos))
        else:
            pos = ((p2 + sum(r) - 1) % 10 + 1 for r in rolls)
            return reduce(sum_wins, (qplay(p1, np2, s1, s2 + np2, turn=1) for np2 in pos))


@perf
def part2(p1, p2):
    s1, s2 = qplay(p1, p2)

    print(s1, s2)
    print(f'part 2: {max(s1, s2)}')


def main(data):
    part1(*parse_input(data))

    part2(*parse_input(data))


if __name__ == '__main__':
    from aocd import data

    main(data)

    main("""Player 1 starting position: 4
Player 2 starting position: 8""")
