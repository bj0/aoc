from itertools import count

from aocd import data

card, door, = [int(x) for x in data.splitlines()]


def trans(subj, lz, v0=1):
    v = v0
    for i in range(lz):
        v = (v * subj) % 20201227

    return v


v = 1
for i in count(1):
    v = trans(7, 1, v)
    if v in [card, door]:
        break

subj = door if v == card else card

# 18608573
print(f'part1: {trans(subj, i)}')
