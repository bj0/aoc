import os
import sys

if __name__ == '__main__' and __package__ is None:
    __package__ = 'aoc.2019'
    right_import_root = os.path.abspath(__file__)
    for i in range(__package__.count('.') + 2):
        right_import_root = os.path.dirname(right_import_root)
    sys.path.insert(0, right_import_root)

from . import intcode
import trio
from aocd import data


async def run(memory, input):
    async with trio.open_nursery() as nursery:
        # set up channels
        in_send, in_recv = trio.open_memory_channel(10)
        out_send, out_recv = trio.open_memory_channel(0)
        # start program
        nursery.start_soon(intcode.process, memory, in_recv, out_send)

        async with in_send, out_recv:
            async for status in out_recv:
                if status == intcode.Command.INPUT:
                    await in_send.send(input)
                # else:
                # print(f'out: {status}')
            return status


def main(*_):
    async def main():
        memory = intcode.init(data.strip().split(','))

        part_a = await run(memory, 1)
        print(f'part 1: {part_a}')
        # part1 7265618

        part_b = await run(memory, 5)
        print(f'part 2: {part_b}')
        # part2 7731427

        return part_a, part_b

    return trio.run(main)


# print(Puzzle(2019, 5).answers)
if __name__ == '__main__':
    main()
