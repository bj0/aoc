from itertools import product

from aocd import data

active = {(i, j, 0)
          for j, row in enumerate(data.splitlines())
          for i, c in enumerate(row)
          if c == '#'}

D = set(product([-1, 0, 1], repeat=3)) - {(0, 0, 0)}


def check(pos, active):
    i, j, k = pos
    m = sum(1 for di, dj, dk in D if (i + di, j + dj, k + dk) in active)
    return (pos in active and m in (2, 3)) or (pos not in active and m == 3)


for t in range(6):
    neighbors = {loc
                 for (i, j, k) in active
                 for di, dj, dk in D
                 if check(loc := (i + di, j + dj, k + dk), active)}
    active = {pos for pos in active if check(pos, active)} | neighbors

print(f'part1: {len(active)}')

active = {(i, j, 0, 0)
          for j, row in enumerate(data.splitlines())
          for i, c in enumerate(row)
          if c == '#'}

D = set(product([-1, 0, 1], repeat=4)) - {(0, 0, 0, 0)}


def check(pos, active):
    i, j, k, w = pos
    m = sum(1 for di, dj, dk, dw in D if (i + di, j + dj, k + dk, w + dw) in active)
    return (pos in active and m in (2, 3)) or (pos not in active and m == 3)


for t in range(6):
    neighbors = {loc
                 for (i, j, k, w) in active
                 for di, dj, dk, dw in D
                 if check(loc := (i + di, j + dj, k + dk, w + dw), active)}
    active = {pos for pos in active if check(pos, active)} | neighbors

print(f'part2: {len(active)}')
