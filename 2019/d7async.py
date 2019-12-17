from itertools import permutations

import intcode
import trio
from aocd import data


async def run(memory, phases):
    async with trio.open_nursery() as nursery:
        # set up channels
        a_send, a_recv = trio.open_memory_channel(0)
        b_send, b_recv = trio.open_memory_channel(0)
        nursery.start_soon(intcode.process, memory, a_recv, b_send)
        c_send, c_recv = trio.open_memory_channel(0)
        nursery.start_soon(intcode.process, memory, b_recv, c_send)
        d_send, d_recv = trio.open_memory_channel(0)
        nursery.start_soon(intcode.process, memory, c_recv, d_send)
        e_send, e_recv = trio.open_memory_channel(0)
        nursery.start_soon(intcode.process, memory, d_recv, e_send)
        f_send, f_recv = trio.open_memory_channel(0)
        nursery.start_soon(intcode.process, memory, e_recv, f_send)
        # input phases
        await a_send.send(phases[0])
        await b_send.send(phases[1])
        await c_send.send(phases[2])
        await d_send.send(phases[3])
        await e_send.send(phases[4])
        # start inpu
        await a_send.send(0)

        try:
            async for sig in f_recv:
                await a_send.send(sig)
        except trio.BrokenResourceError:
            pass  # a send closed

    return sig


# data = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"


async def part2():
    memory = intcode.init(data.strip().split(','))
    mx = 0
    for phases in permutations(range(5, 10), 5):
        sig = await run(memory, phases)
        mx = max(mx, sig)

    print(f'part 2: {mx}')
    # part 2: 2645740


trio.run(part2)
