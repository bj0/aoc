import os
import sys

import trio
from aocd import data
from aocd.models import Puzzle

if __name__ == '__main__' and __package__ is None:
    __package__ = 'aoc.2019'
    right_import_root = os.path.abspath(__file__)
    for i in range(__package__.count('.') + 2):
        right_import_root = os.path.dirname(right_import_root)
    sys.path.insert(0, right_import_root)

from . import intcode
from .util import perf


async def run(memory, a, b):
    program = {**memory, 1: a, 2: b}

    program = await intcode.process(program)

    return program[0]


async def amain():
    memory = intcode.init(data.strip().split(','))

    perf()

    part_a = await run(memory, 12, 2)
    print(f'part 1: {part_a}')
    # 4484226

    perf()

    for a, b in ((x, y) for x in range(100) for y in range(100)):
        ret = await run(memory, a, b)
        if ret == 19690720:
            part_b = (100 * a + b)
            print(f'part 2: {a, b}, {part_b}')
            break

    # 5696

    perf()

    return part_a, part_b


def main(*_):
    return trio.run(amain)


if __name__ == '__main__':
    main()
