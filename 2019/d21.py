from time import perf_counter

import intcode
import trio
from aocd import data


async def run(memory, input):
    async with trio.open_nursery() as nursery:
        # set up channels
        in_send, in_recv = trio.open_memory_channel(0)
        out_send, out_recv = trio.open_memory_channel(0)
        # start program
        nursery.start_soon(intcode.process, memory, in_recv, out_send)

        line = ''
        out = iter(ord(c) for c in input)
        async with in_send, out_recv:
            async for status in out_recv:
                if status == intcode.Command.INPUT:
                    await in_send.send(next(out))
                else:
                    if status > 255:
                        print(f"damage: {status}")
                        return status
                    elif status == 10:
                        print(line)
                        line = ''
                    else:
                        line += chr(status)


async def main():
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

trio.run(main)
