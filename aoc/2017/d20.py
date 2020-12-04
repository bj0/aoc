with open('d20.txt', 'rt') as f:
    input = f.read().strip()

inp = """
p=<3,0,0>, v=<2,0,0>, a=<-1,0,0>
p=<4,0,0>, v=<0,0,0>, a=<-2,0,0>
""".strip()

inp2 = """
p=<-6,0,0>, v=<3,0,0>, a=<0,0,0>
p=<-4,0,0>, v=<2,0,0>, a=<0,0,0>
p=<-2,0,0>, v=<1,0,0>, a=<0,0,0>
p=<3,0,0>, v=<-1,0,0>, a=<0,0,0>
""".strip()

import numpy as np
import itertools

def parse(input):
    import re
    parts = []
    pat = re.compile(r"p=<(?P<pos>[-\d,]+)>, v=<(?P<vel>[-\d,]+)>, a=<(?P<acc>[-\d,]+)>")
    for line in input.split('\n'):
        mo = re.fullmatch(pat, line)
        if not mo:
            print(f"{pat}, '{line}'")
        pos = np.fromiter((int(x) for x in mo.group('pos').split(',')), int)
        vel = np.fromiter((int(x) for x in mo.group('vel').split(',')), int)
        acc = np.fromiter((int(x) for x in mo.group('acc').split(',')), int)
        parts.append((pos, vel, acc))

    return parts


def step(parts):
    for (i, (pos, vel, acc)) in enumerate(parts):
        vel += acc
        pos += vel
        parts[i] = (pos, vel, acc)
    return parts


def part1(input):
    parts = parse(input)

    acc = [p[2].dot(p[2]) for p in parts]
    return np.argmin(acc)


def collisions(part):
    seen = {}
    pos = (p[0] for p in part)

    for i, p in enumerate(pos):
        seen.setdefault(tuple(p), []).append(i)

    remove = (x for x in seen.values() if len(x) > 1)

    for idx in reversed(sorted(itertools.chain.from_iterable(remove))):
        part.pop(idx)

    return part


def part2(input):
    parts = parse(input)

    for i in range(1000):
        step(parts)
        collisions(parts)

    return len(parts), parts


print(part1(inp))
print(part1(input))

print(part2(inp2))
print(part2(input))
