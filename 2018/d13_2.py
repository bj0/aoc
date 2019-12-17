from itertools import cycle


def parse(input):
    m = {}
    carts = {}
    dir = {'<': -1, '^': -1j, '>': 1, 'v': 1j}
    for r, line in enumerate(input.splitlines()):
        for c, t in enumerate(line):
            loc = c + r * 1j
            if t in r'/\+':
                m[loc] = t
            elif t in dir:
                carts[loc] = dir[t], cycle([-1j, 1, 1j])

    return m, carts


def part1(input):
    m, carts = parse(input)
    while len(carts) > 1:
        for loc in sorted(carts, key=lambda k: (k.imag, k.real)):
            if loc not in carts:
                continue
            dir, turn = carts.pop(loc)
            loc += dir
            if loc in carts:
                print(f'collision! {loc.real:.0f},{loc.imag:.0f}')
                del carts[loc]
                continue
            if loc in m:
                if m[loc] == '+':
                    dir *= next(turn)
                else:
                    dir *= (2 * ((m[loc] == '/') ^ (dir.imag == 0)) - 1) * (1j)
            carts[loc] = dir, turn

    if len(carts) > 0:
        loc = list(carts)[0]
        print(f'last cart: {loc.real:.0f},{loc.imag:.0f}')


inp = r"""
/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   
""".strip('\n')

with open('d13.txt', 'rt') as f:
    input = f.read().strip('\n')

part1(inp)
print()
part1(input)
