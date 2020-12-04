import re
from collections import deque


def print_map(clay, wet=None, filled=None):
    x = [int(c.real) for c in clay]
    y = [int(c.imag) for c in clay]
    minx, maxx = min(x) - 1, max(x) + 2
    miny, maxy = min(y) - 1, max(y) + 2
    display = [list('.' * (maxx - minx + 3)) for _ in range(maxy + 1)]
    for c in clay:
        display[int(c.imag)][int(c.real) - minx] = '#'

    display[0][500 - minx] = '+'

    if wet:
        for c in wet:
            display[int(c.imag)][int(c.real) - minx] = '|'
    if filled:
        for c in filled:
            display[int(c.imag)][int(c.real) - minx] = '~'

    print('\n'.join(''.join(c for c in row) for row in display))


def part1(input):
    clay = set()
    for line in input.splitlines():
        x, xv, y, yvl, yvr = re.findall(r'(x|y)=(\d+), (x|y)=(\d+)..(\d+)', line)[0]
        xv, yvl, yvr = [int(i) for i in (xv, yvl, yvr)]
        if x == 'x':
            for y in range(yvl, yvr + 1):
                clay.add(xv + 1j * y)
        elif x == 'y':
            for y in range(yvl, yvr + 1):
                clay.add(y + 1j * xv)

    maxy = max(c.imag for c in clay)
    miny = min(c.imag for c in clay)

    s = 500 + miny * 1j

    water = deque([(s, 0j)])
    filled = set()
    wet = set()
    i = 0

    def stream(pos, dir, fill=False):
        cur = pos
        while True:
            cur = cur + dir
            if cur in filled or cur in clay:
                return False
            wet.add(cur)
            if fill:
                filled.add(cur)
            # print_map(clay, wet, filled)
            if dir == 1j:
                cur = cur + dir
                while cur not in filled and cur not in clay:
                    wet.add(cur)
                    cur = cur + dir
                    if cur.imag > maxy:
                        return True

                cur -= dir
                # hit something, split
                left = stream(cur, -1)
                right = stream(cur, 1)
                if not left and not right :
                    # filled
                    stream(cur, -1, True)
                    stream(cur, 1, True)
                    filled.add(cur)
                    cur += -2*1j
                else:
                    return True
            else:
                down = cur + 1j
                if down not in clay and down not in filled:
                    stream(cur, 1j)
                    return True

    stream(s-1j, 1j)

    print(i)
    print_map(clay, wet, filled)
    print(len(wet))
    print(len(filled))


with open('d17.txt', 'rt') as f:
    input = f.read().strip()

inp = """
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
""".strip()

import time

t = time.perf_counter()

part1(inp)
part1(input)


print(f'{time.perf_counter()-t}s')
