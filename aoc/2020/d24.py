from aocd import data

data = data.replace('ne', 'a').replace('se', 'b').replace('sw', 'c').replace('nw', 'd')

DIRS = dict(
    a=1 - 1j,
    b=1j,
    c=-1 + 1j,
    d=-1j,
    e=1,
    w=-1
)

tiles = [sum(DIRS[c] for c in tile) for tile in data.splitlines()]
floor = {}
for tile in tiles:
    floor[tile] = not floor.get(tile, False)

black = {p for p, v in floor.items() if v}
# 244
print(f'part1 {len(black)}')


def step(pos, black):
    n = sum(1 for d in DIRS.values() if (pos + d) in black)
    return ((pos in black) and not (n == 0 or n > 2)) or n == 2


for day in range(100):
    neighbors = {p + d for p in black for d in DIRS.values()}
    black = {p for p in black | neighbors if step(p, black)}

# 3665
print(f'part2 {len(black)}')
