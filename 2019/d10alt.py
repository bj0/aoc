from cmath import pi, phase
from collections import defaultdict
from itertools import islice

from aocd import data


# data = """
# .#..##.###...#######
# ##.############..##.
# .#.######.########.#
# .###.#######.####.#.
# #####.##.#.##.###.##
# ..#####..#.#########
# ####################
# #.####....###.#.#.##
# ##.#################
# #####.##.###..####..
# ..######..##.#######
# ####.##.####...##..#
# .#####..#.######.###
# ##...#.##########...
# #.##########.#######
# .####.#.###.###.#.##
# ....##.##.###..#####
# .#.#.###########.###
# #.#.#.#####.####.###
# ###.##.####.##.#..##
# """


def angle(frm, to):
    dist = (to - frm)
    return (phase(dist) + pi / 2) % (2 * pi)


# parse roids
rows = data.strip().split()
roids = set((x + y * 1j) for y in range(len(rows)) for x in range(len(rows[0])) if rows[y][x] == '#')

vis = {a: set(angle(a, b) for b in (roids - {a})) for a in roids}
station = max(vis, key=lambda k: len(vis[k]))
print(f'part 1: max roid: {station} can see {len(vis[station])}')

# sort roids by angle
targets = defaultdict(set)
for roid in (roids - {station}):
    targets[angle(station, roid)].add(roid)

# use zip to interlace lists of roids at each angle
order = (roid for roids in zip(*(sorted(targets[t], key=lambda a: abs(a - station)) for t in sorted(targets)))
         for roid in roids)
splash = next(islice(order, 199, 200))
print(f'part 2: {splash}, {splash.real * 100 + splash.imag}')
