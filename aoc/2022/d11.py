from dataclasses import dataclass
from functools import reduce
from operator import mul, add
from typing import Callable

from aocd import data

from aoc.util import perf

# data = """Monkey 0:
#   Starting items: 79, 98
#   Operation: new = old * 19
#   Test: divisible by 23
#     If true: throw to monkey 2
#     If false: throw to monkey 3
#
# Monkey 1:
#   Starting items: 54, 65, 75, 74
#   Operation: new = old + 6
#   Test: divisible by 19
#     If true: throw to monkey 2
#     If false: throw to monkey 0
#
# Monkey 2:
#   Starting items: 79, 60, 97
#   Operation: new = old * old
#   Test: divisible by 13
#     If true: throw to monkey 1
#     If false: throw to monkey 3
#
# Monkey 3:
#   Starting items: 74
#   Operation: new = old + 3
#   Test: divisible by 17
#     If true: throw to monkey 0
#     If false: throw to monkey 1"""

_ops = {'*': mul, '+': add}


@dataclass
class Monkey:
    items: list
    op: Callable[[int], int]
    test: int
    true: int
    false: int


def parse_monkey(block):
    """parse the monkey definition"""
    list = []
    op = test = true = false = None
    for line in block.split('\n'):
        match line.strip().split():
            case ['Starting', 'items:', *lst]:
                list = [int(x.strip(',')) for x in lst]
            case [*_, 'old', o, n]:
                if n == 'old':
                    op = lambda x: _ops[o](x, x)
                else:
                    op = lambda x, n=n: _ops[o](x, int(n))
            case [*_, 'by', n]:
                test = int(n)
            case [_, 'true:', *_, n]:
                true = int(n)
            case [_, 'false:', *_, n]:
                false = int(n)

    return Monkey(list, op, test, true, false)


@perf
def part1(puz):
    monkeys = [parse_monkey(block) for block in puz.split('\n\n')]
    sums = [0] * len(monkeys)
    for _ in range(20):
        # print([m.items for m in monkeys])
        for j, monkey in enumerate(monkeys):
            sums[j] += len(monkey.items)
            for i in monkey.items:
                # print(f'wtf {i}')
                i = monkey.op(i) // 3
                # print(f'wtf2 {i}')
                if i % monkey.test == 0:
                    monkeys[monkey.true].items.append(i)
                else:
                    monkeys[monkey.false].items.append(i)
            monkey.items = []

    return mul(*list(sorted(sums))[-2:])


# 120756
print(f'part1: {part1(data)}')


@perf
def part2(puz):
    monkeys = [parse_monkey(block) for block in puz.split('\n\n')]
    sums = [0] * len(monkeys)
    p = reduce(mul, (m.test for m in monkeys))
    for _ in range(10000):
        # print([m.items for m in monkeys])
        for j, monkey in enumerate(monkeys):
            sums[j] += len(monkey.items)
            for i in monkey.items:
                # print(f'wtf {i}')
                i = monkey.op(i) % p
                # print(f'wtf2 {i}')
                if i % monkey.test == 0:
                    monkeys[monkey.true].items.append(i)
                else:
                    monkeys[monkey.false].items.append(i)
            monkey.items = []

    return mul(*list(sorted(sums))[-2:])


# 39109444654
print(f'part2: {part2(data)}')
