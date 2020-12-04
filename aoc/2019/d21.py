from collections import deque
from time import perf_counter

import intcode
import trio
from aocd import data
from aocd.models import Puzzle


async def run(memory, input):
    async with trio.open_nursery() as nursery:
        # set up channels
        in_send, in_recv = trio.open_memory_channel(10)
        out_send, out_recv = trio.open_memory_channel(0)
        # start program
        nursery.start_soon(intcode.process, memory, in_recv, out_send)

        out = deque(input.strip().split('\n'))
        async with in_send, out_recv:
            async for status in intcode.irecv_ascii(out_recv):
                if status == intcode.Command.INPUT:
                    intcode.send_ascii(in_send, out.popleft())
                else:
                    if isinstance(status, int) and status > 255:
                        print(f"damage: {status}")
                        return status
                    else:
                        print(status)


async def amain():
    memory = intcode.init(data.strip().split(','))

    t = perf_counter()

    d = await run(memory, """NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
WALK
""")
    print(f'part 1: {d}')

    d = await run(memory, """NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
NOT E T
NOT T T
OR H T
AND T J
    RUN
    """)


def main(*_):
    trio.run(amain)


if __name__ == '__main__':
    main()
    print(Puzzle(2019, 21).answers)
