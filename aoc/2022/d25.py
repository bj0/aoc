from collections import deque
import enum
from functools import cache
from itertools import count, cycle
from math import ceil
from operator import add, floordiv, mul, sub, truediv
from time import sleep
from typing import Counter

from aocd import data

from aoc.util import perf

# data = """1=-0-2
# 12111
# 2=0=
# 21
# 2=01
# 111
# 20012
# 112
# 1=-1=
# 1-12
# 12
# 1=
# 122"""

inp = data.split("\n")

_num = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
_dig = {x:k for k,x in _num.items()}

def conf(n):
    if n == 0: return '0'
    num = ''
    while n:
        n, r = n // 5, n % 5
        if r > 2:
            r = r-5
            n += 1
        num = _dig[r] + num
    return num

@perf
def part1(inp):
    return sum(sum(_num[d] * (5**p) for d, p in zip(reversed(num), count())) for num in inp)


# @perf
# def part2(storms):


#
print(f"part1: {conf(part1(inp))}")


#
# print(f"part2: {part2(storms)}")
