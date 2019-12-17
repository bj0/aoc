import re
from functools import reduce
from math import gcd
from time import perf_counter

from aocd import data


class Moon:
    def __init__(self, line):
        self.pos = tuple(int(c) for c in re.findall(r'-?\d+', line))
        self.v = (0, 0, 0)

    @property
    def energy(self):
        return sum(abs(x) for x in self.pos) * sum(abs(x) for x in self.v)

    def __repr__(self):
        return f"Moon<{self.pos[0]},{self.pos[1]},{self.pos[2]}>({self.v[0]},{self.v[1]},{self.v[2]})"

    @property
    def id(self):
        return self.pos + self.v


# data = """
# <x=-1, y=0, z=2>
# <x=2, y=-10, z=-7>
# <x=4, y=-8, z=8>
# <x=3, y=5, z=-1>
# """
# data = """
# <x=-8, y=-10, z=0>
# <x=5, y=5, z=10>
# <x=2, y=-7, z=3>
# <x=9, y=-8, z=-3>
# """

moons = set(Moon(line) for line in data.strip().split('\n'))

vel = {}


def grav(a, b):
    return tuple(-1 if a[i] > b[i] else (1 if a[i] < b[i] else 0) for i in range(3))


def step(moons):
    # update vel
    for m in moons:
        v = m.v
        for other in (moons - {m}):
            dv = grav(m.pos, other.pos)
            v = tuple(v[i] + dv[i] for i in range(3))
        m.v = v

    # update pos
    for m in moons:
        m.pos = tuple(m.pos[i] + m.v[i] for i in range(3))


def ids(moons):
    return tuple(m.id for m in moons)


def idx(moons, i):
    return tuple((m.pos[i], m.v[i]) for m in moons)


t = perf_counter()

state = [set(idx(moons, 0)), set(idx(moons, 1)), set(idx(moons, 2))]
rx = [None] * 3
for i in range(1000):
    step(moons)
    for j in range(3):
        if not rx[j]:
            if (id := idx(moons, j)) in state[j]:
                rx[j] = i
                # print(f'repeat {j} at {rx[j]}')
                # print(id)
            else:
                state[j].add(id)

print(f'part 1: {sum(m.energy for m in moons)}')

if not all(rx):
    for j in range(1000000):
        step(moons)
        for k in range(3):
            if not rx[k]:
                if (id := idx(moons, k)) in state[k]:
                    rx[k] = i + j + 1
                    # print(f'repeat {k} at {rx[k]}')
                else:
                    state[k].add(id)
        if all(rx):
            break

print(rx)
print(f'part 2: {reduce(lambda a, b: a * b // gcd(a, b), rx)}')

print(f'time: {perf_counter() - t:.2f}s')
