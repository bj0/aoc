from time import perf_counter

import intcode
import trio
from aocd import data
from aocd.models import Puzzle


async def run(memory, input=None):
    async with trio.open_nursery() as nursery:
        # set up channels
        in_send, in_recv = trio.open_memory_channel(0)
        out_send, out_recv = trio.open_memory_channel(0)
        # start program
        nursery.start_soon(intcode.process, memory, in_recv, out_send)

        input = iter(input)
        async with in_send, out_recv:
            async for status in out_recv:
                if status == intcode.Command.INPUT:
                    await in_send.send(next(input))

        return status


async def check(y, memory):
    # bin search to find min x
    xm, xx = 0, y
    x = xm
    while True:
        if await run(memory, (x, y)):
            xx = x
        else:
            xm = x
        x = (xm + xx) // 2
        if x == xm:
            break
    x += 1

    # check if we have a 100x100 box
    if await run(memory, (x + 99, y - 99)):
        return x
    return None


async def amain():
    memory = intcode.init(data.strip().split(','))

    t = perf_counter()

    pts = {(x, y): '.' for y in range(50) for x in range(50)}
    print(len(pts))
    for x, y in pts:
        hit = await run(memory, (x, y))
        pts[(x, y)] = '.' if hit == 0 else '#'

    for y in range(50):
        print(''.join(pts[(x, y)] for x in range(50)))

    part_a = sum(1 for k in pts if pts[k] == '#')
    print(f'part 1: {part_a}')

    print(f'time: {perf_counter() - t:.2f}s')
    t = perf_counter()

    ym = 500
    yx = 5000
    y = ym
    while True:
        if x := await check(y, memory):
            yx = y
        else:
            ym = y
        y = (ym + yx) // 2
        if y == ym:
            break
    y += 1

    # corner is at y-99
    part_b = x * 10000 + (y - 99)
    print(f'part 2: {part_b}')
    # 8771057
    #
    # for r in range(y - 99, y + 1):
    #     for c in range(x, x + 100):
    #         h = await run(memory, (c, r))
    #         print('#' if h else '.', end='')
    #     print()

    print(f'time: {perf_counter() - t:.2f}s')

    return part_a, part_b


def main(*_):
    return trio.run(amain)


if __name__ == '__main__':
    main()
    print(Puzzle(2019, 19).answers)
