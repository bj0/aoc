from aocd import data

from aoc.util import perf

import re

inp = data.splitlines()

# inp = """two1nine
# eightwothree
# abcone2threexyz
# xtwone3four
# 4nineeightseven2
# zoneight234
# 7pqrstsixteen""".strip().splitlines()


@perf
def part1(puz):
    def g():
        for line in puz:
            match re.findall(r'\d', line):
                case [a]:
                    yield int(a + a)
                case [a, b]:
                    yield int(a + b)
                case [a, *_, b]:
                    yield int(a + b)

    return sum(g())


# 53080
print(f'part1: {part1(inp)}')

_num = {'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9'}


@perf
def part2(puz):
    def g():
        for line in puz:
            pat = r'(?=(\d|' + '|'.join(_num.keys()) + '))'
            x = re.findall(pat, line)
            # print(x, pat, line)
            match x:
                case [a]:
                    # print('a', a)
                    a = _num.get(a, a)
                    yield int(a + a)
                case [a, b]:
                    # print('b', a, b)
                    a = _num.get(a, a)
                    b = _num.get(b, b)
                    yield int(a + b)
                case [a, *_, b]:
                    # print('c', a, b)
                    a = _num.get(a, a)
                    b = _num.get(b, b)
                    yield int(a + b)

    return sum(g())


# 53268
print(f'part2 {part2(inp)}')
