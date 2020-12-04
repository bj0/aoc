import intcode
import trio
from aocd import data

"""
Figuring out when the inputs are read instead of using a separate task fixes the input lag (pull awaits instead of push),
that makes it possible to just follow position of ball instead of anticipating it.
"""


async def run(memory):
    async with trio.open_nursery() as nursery:
        # set up channels
        in_send, in_recv = trio.open_memory_channel(0)
        out_send, out_recv = trio.open_memory_channel(0)
        # start program
        nursery.start_soon(intcode.process, memory, in_recv, out_send)

        joy = 0

        map = {}
        pad = 0
        score = None
        try:
            while True:
                x = await out_recv.receive()
                if x == intcode.Command.INPUT:
                    await in_send.send(joy)
                    continue
                y = await out_recv.receive()
                id = await out_recv.receive()
                c = x + y * 1j

                if x == -1 and y == 0:
                    score = id
                    continue
                else:
                    map[c] = id

                if id == 3:
                    pad = c
                if id == 4:
                    if pad.real < c.real:
                        joy = 1
                    elif pad.real > c.real:
                        joy = -1
                    else:
                        joy = 0

        except (trio.BrokenResourceError, trio.EndOfChannel):
            pass  # channel closed

        print(f'score: {score}')
        return map


_char = {0: '.', 1: '#', 2: 'b', 3: '-', 4: 'O'}


def print_map(map):
    for r in range(22):
        for c in range(40):
            id = map.get(c + r * 1j, 0)
            print(_char[id], end='')
        print()


async def main():
    memory = intcode.init(data.strip().split(','))
    # result = await run(memory)
    # result = Counter(result.values())
    # print(f'part 1: {result[2]}')

    # quarter
    memory = {**memory, 0: 2}
    result = await run(memory)
    print_map(result)

trio.run(main)
