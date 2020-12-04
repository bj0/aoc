import intcode
import trio
from aocd import data
from aocd.models import Puzzle


async def run(memory, start):
    async with trio.open_nursery() as nursery:
        # set up channels
        in_send, in_recv = trio.open_memory_channel(0)
        out_send, out_recv = trio.open_memory_channel(0)
        # start program
        nursery.start_soon(intcode.process, memory, in_recv, out_send)

        pos = complex(0, 0)
        dir = -1j  # up
        paint = {pos: start}
        turns = {0: -1j, 1: 1j}
        async for color in out_recv:
            if color == intcode.Command.INPUT:
                await in_send.send(paint.get(pos, 0))
                continue
            paint[pos] = color
            dir *= turns[await out_recv.receive()]
            pos += dir

        return paint


async def amain():
    memory = intcode.init(data.strip().split(','))
    paint = await run(memory, 0)
    part_a = len(paint)
    print(f'part 1: {part_a}')

    paint = await run(memory, 1)
    print('part 2:')
    for r in range(-1, 7):
        print(''.join('.' if paint.get((c + r * 1j), 0) else '#' for c in range(0, 41)))

    # part 2 eyeball
    return part_a, 'BLCZCJLZ'


def main(*_):
    return trio.run(amain)


# print(Puzzle(2019, 11).answers)

if __name__ == '__main__':
    main()
