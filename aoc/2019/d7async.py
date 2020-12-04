from itertools import permutations

import intcode
import trio
from aocd import data
from aocd.models import Puzzle
from util import merge, perf


async def run(memory, phases):
    async with trio.open_nursery() as nursery:
        # set up channels
        a_send, a_recv = trio.open_memory_channel(0)
        b_send, b_recv = trio.open_memory_channel(0)
        # need a relay channel so we can tell when a needs input
        r_send, r_recv = trio.open_memory_channel(0)
        nursery.start_soon(intcode.process, memory, a_recv, r_send)
        c_send, c_recv = trio.open_memory_channel(0)
        nursery.start_soon(intcode.process, memory, b_recv, c_send, False)
        d_send, d_recv = trio.open_memory_channel(0)
        nursery.start_soon(intcode.process, memory, c_recv, d_send, False)
        e_send, e_recv = trio.open_memory_channel(0)
        nursery.start_soon(intcode.process, memory, d_recv, e_send, False)
        f_send, f_recv = trio.open_memory_channel(0)
        nursery.start_soon(intcode.process, memory, e_recv, f_send, False)
        # input phases
        await a_send.send(phases[0])
        await b_send.send(phases[1])
        await c_send.send(phases[2])
        await d_send.send(phases[3])
        await e_send.send(phases[4])

        sig = 0
        async with a_send, f_recv:
            async for out, ch in merge(nursery, r_recv, f_recv):
                if ch == r_recv:
                    if out == intcode.Command.INPUT:
                        await a_send.send(sig)
                    else:
                        await b_send.send(out)
                else:
                    sig = out

            return sig


# data = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"


async def part2():
    memory = intcode.init(data.strip().split(','))

    perf()

    mx = 0
    for phases in permutations(range(5, 10), 5):
        sig = await run(memory, phases)
        mx = max(mx, sig)

    print(f'part 2: {mx}')
    # part 2: 2645740

    perf()


def main(*_):
    trio.run(part2)


# print(Puzzle(2019, 7).answers)

if __name__ == '__main__':
    main()
