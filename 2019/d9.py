import intcode
import trio
from aocd import data


async def run(memory, *input):
    async with trio.open_nursery() as nursery:
        # set up channels
        in_send, in_recv = trio.open_memory_channel(0)
        out_send, out_recv = trio.open_memory_channel(0)
        nursery.start_soon(intcode.process, memory, in_recv, out_send)
        # start input
        for i in input:
            await in_send.send(i)

        out = 0
        async for sig in out_recv:
            out = sig
        return out


# data = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
# data = "1102,34915192,34915192,7,4,7,99,0"

async def main():
    memory = data.strip().split(',')
    memory = {i: int(memory[i]) for i in range(len(memory))}
    memory['rb'] = 0
    print(f'part 1: {await run(memory, 1)}')
    # part 1: 1 -> 2316632620
    print(f'part 2: {await run(memory, 2)}')
    # part 2: 2 -> 78869


trio.run(main)
