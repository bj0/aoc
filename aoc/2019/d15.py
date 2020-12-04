import intcode
import networkx as nx
import trio
from aocd import data
from aocd.models import Puzzle

_dir = {1: 1j, 2: -1j, 3: -1, 4: 1}
_rev = {1: 2, 2: 1, 3: 4, 4: 3}

g = nx.Graph()


async def run(memory):
    async with trio.open_nursery() as nursery:
        # set up channels
        in_send, in_recv = trio.open_memory_channel(0)
        out_send, out_recv = trio.open_memory_channel(0)
        # start program
        nursery.start_soon(intcode.process, memory, in_recv, out_send)

        pos = 0
        map = {pos: 1}
        step = 1
        path = []
        ox = 0
        try:
            async with in_send, out_recv:
                async for status in out_recv:
                    if status == intcode.Command.INPUT:
                        await in_send.send(step)
                    else:
                        npos = pos + _dir[step]
                        if status != 0:
                            g.add_edge(pos, npos)
                            pos = npos
                            if npos not in map:
                                path.append(step)
                        if status == 2:
                            print(f'win! {npos}')
                            ox = npos

                        map[npos] = status
                        available = [dir for dir in _dir if (pos + _dir[dir]) not in map]
                        if available:
                            step = available[0]
                        else:
                            step = _rev[path.pop()]

        except Exception as e:
            print(f"stop: {e}")
            pass
        # map[pos] = -3
        # map[0] = -2
        # print_map(map)
        return map, ox


_map = {0: '#', 1: '.', 2: 'O', -1: ' ', -2: 'S', -3: 'R'}


def print_map(map):
    rx = int(max(c.imag for c in map)) + 1
    rm = int(min(c.imag for c in map))
    cx = int(max(c.real for c in map)) + 1
    cm = int(min(c.real for c in map))
    for r in range(rm, rx):
        print(''.join(_map[map.get(c - r * 1j, -1)] for c in range(cm, cx)))


async def amain():
    memory = intcode.init(data.strip().split(','))

    map, o = await run(memory)
    print_map(map)

    part_a = nx.shortest_path_length(g, 0, o)
    print(f'part 1: {part_a}')
    # 226

    ox = {o}
    t = 0
    spread = [o]
    while True:
        spread = [p for o in spread for dir in _dir.values() if map[(p := o + dir)] == 1 and p not in ox]
        if spread:
            t += 1
            for p in spread:
                ox.add(p)
        else:
            break

    print(f'part 2: {t}')
    # 342
    return part_a, t


def main(*_):
    return trio.run(amain)


if __name__ == '__main__':
    main()

    print(Puzzle(2019, 15).answers)
