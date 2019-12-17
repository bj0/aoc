import intcode
import trio
from aocd import data


async def run(memory, input=None):
    async with trio.open_nursery() as nursery:
        # set up channels
        in_send, in_recv = trio.open_memory_channel(0)
        out_send, out_recv = trio.open_memory_channel(0)
        # start program
        nursery.start_soon(intcode.process, memory, in_recv, out_send)

        if input:
            inp = iter(input)
            async for c in out_recv:
                if c == intcode.Command.INPUT:
                    await in_send.send(ord(next(inp)))
        else:
            out = ''
            y, x = 0, 0
            map = {}
            async for c in out_recv:
                out += chr(c)
                if c == 10:
                    y += 1
                    x = 0
                else:
                    map[x + y * 1j] = chr(c)
                    x += 1

    if input:
        return c
    return map, out


async def main():
    memory = intcode.init(data.strip().split(','))

    map, out = await run(memory)
    print(out)

    a = 0
    for p in map:
        c = map[p]
        if c == '#':
            if all(map.get(p + dir, '') == '#' for dir in (1, -1, 1j, -1j)):
                print(f'is at {p}')
                a += p.real * p.imag

    print(f'part 1: {a}')

    D = {'<': -1, '>': 1, 'v': 1j, '^': -1j}
    T = {1j: 'R', -1j: 'L'}
    p = next(p for p in map if map[p] in D)  # get robot location
    d = D[map[p]]  # and direction
    tgt = len(tuple(p for p in map if map[p] == '#'))  # number of unvisited spots
    visited = set()
    path = ''
    step = 0
    while True:
        np = p + d
        if map.get(np, '') == '#' and np not in visited:
            step += 1
            p = np
            visited.add(p)
        else:
            if len(visited) == tgt:
                print('win!')
                if step > 0:
                    path += f'{step},'
                break
            # look for an unvisited spot
            for turn in T:
                if (tp := p + d * turn) not in visited and map.get(tp, '') == '#':
                    if step > 0:
                        path += f'{step},'
                        step = 0
                    d *= turn
                    path += f'{T[turn]},'
                    break
            else:
                # if we got here, all available spots are visited, just keep going till we find one
                if map.get(np, '') == '#':
                    step += 1
                    p = np
                    visited.add(p)
                else:
                    for turn in T:
                        if map.get(p + d * turn, '') == '#':
                            if step > 0:
                                path += f'{step},'
                                step = 0
                            d *= turn
                            path += f'{T[turn]},'
                            break
                    else:
                        raise Exception("not sure")

    # let's try and find 3 repeating substrings at most 20 chars long
    # for each substring, assume it has to start at the beginning of the (remaining) string (one has to)
    # then start at max possible substring and shrink until there's a repeat.
    # when i get 3 substrings this way i verify there's no left overs and all sizes check out
    # if something fails, try a smaller first pattern, so that the other patterns are bigger.
    #   This worked for me, but if it hadn't I would have also varied the 2nd pattern's size until a solution was found,
    # and since this is AoC, i assumed a solution existed...
    orig_path = path.strip(',')
    for mx in range(20, 1, -1):
        p2 = orig_path
        n = len(p2)
        for i in range(n - mx, n):
            p = p2[:-i].strip(',')
            if p[-1] in 'LR':
                continue
            if p2.count(p) > 1:
                A = p
                break
        else:
            raise Exception("no A")
        p2 = p2.replace(A, '').strip(',')  # leave double commas in the middle so next pattern doesn't span previous
        n = len(p2)
        for i in range(n - 20, n):
            p = p2[:-i].strip(',')
            if p[-1] in 'LR':
                continue
            if p2.count(p) > 1:
                B = p
                break
        else:
            raise Exception("no B")
        p2 = p2.replace(B, '')
        n = len(p2)
        for i in range(n - 20, n):
            p = p2[:-i].strip(',')
            if p[-1] in 'LR':
                continue
            if p2.count(p) > 1:
                C = p
                break
        else:
            raise Exception("no C")
        path = orig_path.replace(A, 'A').replace(B, 'B').replace(C, 'C').strip(',')
        if 'L' not in path and 'R' not in path and len(A) < 20 and len(B) < 20 and len(C) < 20 and len(path) < 20:
            break
        else:
            print("that one didn't work...")
    else:
        raise Exception("no solution found")

    print(f'path: {path}')
    print(f'A={A}\nB={B}\nC={C}')

    input = f'{path}\n{A}\n{B}\n{C}\nn\n'

    memory = {**memory, 0: 2}

    dust = await run(memory, input)
    print(f'part 2: {dust}')
    # 807320


trio.run(main)
