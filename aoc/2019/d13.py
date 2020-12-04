from collections import Counter

import intcode
import trio
from aocd import data
from aocd.models import Puzzle


def find_target(db, c, map):
    map = dict(map)
    dir = db
    pos = c
    # print(pos, dir, pos + dir)
    while (next := pos + dir).imag < 20:
        # print(pos, next, dir)
        x = complex(pos.real, next.imag)
        v = map.get(x, 0)
        if v == 1:
            dir = complex(dir.real, -dir.imag)
            continue
        elif v == 2:
            dir = complex(dir.real, -dir.imag)
            map[x] = 0
            continue
        x = complex(next.real, pos.imag)
        h = map.get(x, 0)
        if h == 1:
            dir = complex(-dir.real, dir.imag)
            continue
        elif h == 2:
            dir = complex(-dir.real, dir.imag)
            map[x] = 0
            continue
        n = map.get(next, 0)
        if n == 1:
            dir = -dir
            continue
        elif n == 2:
            dir = -dir
            map[next] = 0
            continue

        pos = next
    pos = complex(pos.real, next.imag)
    # print(f'target: {pos}')
    return pos


async def run(memory):
    async with trio.open_nursery() as nursery:
        # set up channels
        in_send, in_recv = trio.open_memory_channel(0)
        out_send, out_recv = trio.open_memory_channel(0)
        # start program
        nursery.start_soon(intcode.process, memory, in_recv, out_send)

        joy = 0

        async def push_joy():
            nonlocal joy
            try:
                while True:
                    await in_send.send(joy)
                    # print(f'pushd {joy}')
            except trio.BrokenResourceError:
                pass

        nursery.start_soon(push_joy)

        map = {}
        last_ball = 0
        pad = 0
        target = None
        score = 0
        try:
            while True:
                x = await out_recv.receive()
                y = await out_recv.receive()
                id = await out_recv.receive()
                c = x + y * 1j

                if x == -1 and y == 0:
                    # print(f'score {id}')
                    score = id
                    # print_map(map)
                    continue
                else:
                    map[c] = id

                if id == 3:
                    pad = c
                    # print(f'pad: {c}')
                if id == 4:
                    if last_ball:
                        db = c - last_ball
                        if not target or (c.imag == 19):
                            # print_map(map)
                            if not target:
                                target = find_target(db, c, map)
                            else:
                                target = find_target(complex(db.real, -1), c, map)
                        if target.real > pad.real + joy:
                            joy = 1
                        elif target.real < pad.real + joy:
                            joy = -1
                        else:
                            joy = 0
                        # print(f'ball: {c}, db:{db.real}, t:{target},pad:{pad.real}, joy:{joy}')
                    last_ball = c
        except (trio.BrokenResourceError, trio.EndOfChannel):
            pass  # channel closed

        return map, score


_char = {0: '.', 1: '#', 2: 'b', 3: '-', 4: 'O'}


def print_map(map):
    for r in range(22):
        for c in range(40):
            id = map.get(c + r * 1j, 0)
            print(_char[id], end='')
        print()


async def amain():
    memory = intcode.init(data.strip().split(','))
    result, score = await run(memory)
    result = Counter(result.values())
    part_a = result[2]
    print(f'part 1: {part_a}')

    # quarter
    memory = {**memory, 0: 2}
    result, score = await run(memory)
    print(f'part 2: {score}')
    return part_a, score


def main(*_):
    return trio.run(amain)


if __name__ == '__main__':
    main()
    print(Puzzle(2019, 13).answers)
