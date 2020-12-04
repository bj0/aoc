from collections import defaultdict, Counter
from itertools import count

with open('d18.txt', 'rt') as f:
    input = f.read()


def part1(input, n=10, field=None):
    if field is None:
        field = defaultdict(lambda: ' ')
        for r, row in enumerate(input.splitlines()):
            for c, acre in enumerate(row):
                coord = r + c * 1j
                field[coord] = acre

    cache = {}
    for t in range(n):
        new = field.copy()
        for coord, acre in list(field.items()):
            adj = [coord + d for d in (-1, +1, -1j, +1j, 1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j)]
            if acre == ' ':
                continue
            elif acre == '.':
                if sum(1 for c in adj if field[c] == '|') >= 3:
                    new[coord] = '|'
            elif acre == '|':
                if sum(1 for c in adj if field[c] == '#') >= 3:
                    new[coord] = '#'
            elif acre == '#':
                nb = [field[c] for c in adj]
                if '#' not in nb or '|' not in nb:
                    new[coord] = '.'

        field = new

        display = [list(' ' * 51) for _ in range(51)]
        for coord, acre in field.items():
            display[int(coord.real)][int(coord.imag)] = acre
        # print('\n'.join(''.join(a for a in row) for row in display))
        sfield = '\n'.join(''.join(a for a in row) for row in display)
        if sfield in cache:
            last = cache[sfield]
            cycle = t - last
            # add one because t hasn't inc'd yet
            left = (n - (t + 1)) % cycle
            print(f'cache hit! cycle={cycle}, left={left}, t={t},c={cache[sfield]}')
            return part1(None, left, field)
        cache[sfield] = t

    # wood = sum(1 for k in field if field[k] == '|')
    # ly = sum(1 for k in field if field[k] == '#')
    # print(wood, ly)
    counter = Counter(sfield)
    # return wood*ly
    return counter['|'] * counter['#']


inp = """
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
""".strip()

part1(inp)

# part1(input)


import time

t = time.perf_counter()

print(part1(input, int(1e9)))
# part1(input, 426+14)

print(f'{time.perf_counter() - t}s')
