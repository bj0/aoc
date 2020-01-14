import re
from collections import deque
from itertools import combinations, chain
from time import perf_counter

import intcode
import trio
from aocd import data

_dirs = {
    '- north': 1j,
    '- east': 1,
    '- west': -1,
    '- south': -1j
}
_compass = {_dirs[k]: k.strip('- ') for k in _dirs}

cache = {}

inv = []
ignored = set()


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def parse_screen(screen):
    # print(f"'{screen}'", re.search(r'== ([\w\s]+) ==', screen, re.MULTILINE))
    name = re.search(r'== ([\w\s-]+) ==', screen, re.MULTILINE).groups()[0]
    if 'Items here' in screen:
        items = [x.strip('- ') for x in
                 re.search(r'here:\n((- ([^\n]+)\n?)+)', screen, re.MULTILINE).groups()[0].strip(' -').split('\n') if x]
    else:
        items = []
    if name in cache:
        dirs = cache[name]
    else:
        dirs = [_dirs[k] for k in _dirs if re.search(fr'{k}\b', screen)]
        cache[name] = dirs

    return name, items, dirs


_exclude = ['infinite loop', 'photons', 'escape pod', 'molten lava', 'giant electromagnet']

found = False
returning = False
door = None
trying = False
combo = None

_DISPLAY = False


def next_move(pos, items, dirs, visited, path):
    global ignored

    # pick up any items
    if pickup := [item for item in items if item not in _exclude]:
        item = pickup[0]
        print(f'> taking {item}')
        items.remove(item)
        inv.append(item)
        return f'take {item}', None

    if ig := [item for item in items if item in _exclude]:
        ignored |= set(ig)

    # figure out where to go next
    # look for unvisited rooms
    for dir in dirs:
        p = pos + dir
        if p not in visited:
            move = _compass[dir]
            print(f'> moving {move}')
            # print(pos, p)
            return move, p

    # no unvisited rooms, backtrack
    if len(path) > 1:
        # print(path)
        _ = path.pop()  # this pos
        last = path.pop()  # last pos
        dir = last - pos
        # print(last, pos, dir)
        move = _compass[dir]
        print(f'> returning {move}')
        return move, last
    else:
        # back at beginning, everything traversed
        return None, None


async def display(out_recv):
    screen = ''
    async for line in intcode.irecv_ascii(out_recv):
        if line == intcode.Command.INPUT:
            if _DISPLAY:
                print(screen)
            yield screen
            screen = ''
        else:
            if isinstance(line, int) and line > 255:
                raise Exception(f"non-line: {line}")
            else:
                screen += f'\n{line}'
    if screen != '':
        yield screen  # program halted after final display


async def find_checkpoint(out_recv, in_send):
    pos = 0
    visited = {pos}
    path = deque([pos])
    async for screen in display(out_recv):
        if '==' in screen:
            name, items, dirs = parse_screen(screen)
            if name == 'Security Checkpoint':
                return pos, visited, path  # found it!
        move, npos = next_move(pos, items, dirs, visited, path)
        if npos is not None:
            path.append(npos)
            visited.add(npos)
            pos = npos
        intcode.send_ascii(in_send, move)


async def rewind(out_recv, in_send, pos, visited, path):
    # program waiting for input already, just take a step back
    move, pos = next_move(pos, [], [], visited, path)
    path.append(pos)
    intcode.send_ascii(in_send, move)

    async for screen in display(out_recv):
        if '==' in screen:
            name, items, dirs = parse_screen(screen)

        move, npos = next_move(pos, items, dirs, visited, path)
        if move is None:
            return  # back at beginning
        if npos is not None:
            path.append(npos)
            visited.add(npos)
            pos = npos
        intcode.send_ascii(in_send, move)


async def replay(out_recv, in_send, pos, path):
    # program waiting for input already, take first step
    _ = path.popleft()  # drop start
    npos = path.popleft()
    dir = npos - pos
    move = _compass[dir]
    print(f'> retracing {move}')
    intcode.send_ascii(in_send, move)
    pos = npos

    async for _ in display(out_recv):
        if not path:
            # figure out direction or assume west?
            return  # done
        npos = path.popleft()
        dir = npos - pos
        move = _compass[dir]
        print(f'> retracing {move}')
        intcode.send_ascii(in_send, move)
        pos = npos


def next_trick():
    ps = reversed(sorted(powerset(inv)))
    current = set(inv)
    first = True
    chk = {'tambourine', 'mutex', 'astronaut ice cream', 'easter egg'}
    while True:
        if not first:
            while not (chk := next(ps)):
                pass
            chk = set(chk)
        first = False
        rem = current - chk
        add = chk - current
        for move in rem:
            print(f'> dropping {move}')
            yield f'drop {move}'
        for move in add:
            print(f'> taking {move}')
            yield f'take {move}'
        print('> trying checkpoint')
        # yield 'inv'
        yield 'west'
        current = chk
        # return


async def trial(out_recv, in_send):
    moves = next_trick()
    move = next(moves)
    intcode.send_ascii(in_send, move)
    async for screen in display(out_recv):
        # print(screen.strip())
        # check if passed
        if '==' in screen:
            name, items, dirs = parse_screen(screen)
            if name != 'Security Checkpoint':
                print(screen.strip())
                return
        move = next(moves)
        intcode.send_ascii(in_send, move)


async def run(memory):
    async with trio.open_nursery() as nursery:
        # set up channels
        in_send, in_recv = trio.open_memory_channel(30)
        out_send, out_recv = trio.open_memory_channel(0)
        # start program
        nursery.start_soon(intcode.process, memory, in_recv, out_send)

        async with in_send, out_recv:
            # find checkpoint
            pos, visited, path = await find_checkpoint(out_recv, in_send)
            door = deque(path)

            print('>> found checkpoint')

            # backtrack to make sure every room is visited
            await rewind(out_recv, in_send, pos, visited, path)

            print('>> back at start')

            # re-follow door to checkpoint
            await replay(out_recv, in_send, 0, door)

            print('>> back at checkpoint')

            # now we test combos
            print(inv)
            await trial(out_recv, in_send)

            print('the end')


async def main():
    memory = intcode.init(data.strip().split(','))

    t = perf_counter()

    print(await run(memory))

    print(f'time: {perf_counter() - t:.2f}s')


trio.run(main)
