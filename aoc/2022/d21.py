import re
from functools import cache
from math import ceil
from multiprocessing import Pool
from operator import add, floordiv, mul, sub, truediv
from typing import Any, Callable

from aocd import data

from aoc.util import perf


def getop(op):
    match op.split():
        case [x]:
            return int(x)
        case [a, op, b]:
            return (a, b, op)


inp = {m: getop(op) for line in data.split("\n") for (m, op) in [line.split(": ")]}

_ops = {"+": add, "*": mul, "/": floordiv, "-": sub}


@cache
def monkey_val(monkey):
    match inp[monkey]:
        case int(x):
            return x
        case [a, b, op]:
            a = monkey_val(a)
            b = monkey_val(b)
            return _ops[op](a, b)


@perf
def part1():
    return monkey_val("root")


#
print(f"part1: {part1()}")


_rops = {"+": sub, "*": floordiv, "-": add, "/": mul}


@cache
def monkey_val(monkey):
    # this is super messy, prob a better way, currently reversing all ops
    match inp[monkey]:
        case int(x):
            return x
        case ["humn", b, op]:
            b = monkey_val(b)
            return lambda x: _rops[op](x, b)
        case [a, "humn", "-"]:
            a = monkey_val(a)
            return lambda x: a - x
        case [a, "humn", "/"]:
            a = monkey_val(a)
            return lambda x: a // x
        case [a, "humn", "*"]:
            a = monkey_val(a)
            return lambda x: x // a
        case [a, "humn", "+"]:
            a = monkey_val(a)
            return lambda x: x - a
        case [a, b, op]:
            a = monkey_val(a)
            b = monkey_val(b)
            match [a, b]:
                case [int(x), int(y)]:
                    return _ops[op](x, y)
                case [f, int(y)]:
                    return lambda z: f(_rops[op](z, y))
                case [x, f]:
                    if op in ["+", "*"]:
                        return lambda z: f(_rops[op](z, x))
                    elif op == "/":
                        return lambda z: f(x // z)
                    elif op == "-":
                        return lambda z: f(x - z)


@perf
def part2():
    a, b, _ = inp["root"]
    a = monkey_val(a)
    b = monkey_val(b)
    return a(b) if isinstance(a, Callable) else b(a)


# 3219579395609
print(f"part2: {part2()}")
