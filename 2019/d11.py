import intcode
import trio
from aocd import data


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


async def main():
    memory = intcode.init(data.strip().split(','))
    paint = await run(memory, 0)
    print(f'part 1: {len(paint)}')

    paint = await run(memory, 1)
    print('part 2:')
    for r in range(-1, 7):
        print(''.join('.' if paint.get((c + r * 1j), 0) else '#' for c in range(0, 41)))


trio.run(main)
