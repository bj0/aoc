import numpy as np

with open('d21.txt', 'rt') as f:
    input = f.read().strip()

inp = """
../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#
""".strip()

initial = """
.#.
..#
###
""".strip()


def parse(input):
    lines = input.split('\n')
    rules = {}
    for line in lines:
        pat, out = line.split(' => ')
        out = out.split('/')
        rules[pat] = out
        spat = pat.split('/')
        # each pat can be rotated or flipped
        rot90 = '/'.join(''.join(x) for x in zip(*reversed(spat)))
        rot270 = '/'.join(''.join(x) for x in reversed(tuple(zip(*spat))))
        rot180 = '/'.join(''.join(x) for x in reversed(tuple(reversed(t) for t in spat)))
        flipx = '/'.join(''.join(x) for x in (reversed(t) for t in spat))
        flipy = '/'.join(''.join(x) for x in reversed(spat))
        rotflipx = '/'.join(''.join(x) for x in (reversed(t) for t in rot90.split('/')))
        rotflipy = '/'.join(''.join(x) for x in reversed(rot90.split('/')))
        # print(pat)
        for mod_pat in {rot90, rot270, rot180, flipx, flipy, rotflipx, rotflipy}:
            # print(mod_pat)
            # print(out)
            rules[mod_pat] = out
        # print()

    return rules


import operator
import functools


def step(img, rules):
    def chunk(n, it):
        return zip(*[iter(it)] * n)

    def flat(it):
        return functools.reduce(operator.concat, it)

    N = len(img)
    if N % 2 == 0:
        img = np.array([tuple(x) for x in img])
        # print(img)
        img = flat(np.split(half, N // 2, 1) for half in np.split(img, N // 2, 0))
        # print(img)

        new = []
        for sub in img:
            pat = '/'.join(''.join(c for c in row) for row in sub)
            # print('sub',sub)
            new.append(rules[pat])

        new = [flat(a) for a in flat(list(zip(*c)) for c in chunk(N // 2, new))]
    else:
        if N > 3:
            img = np.array([tuple(x) for x in img])
            img = flat(np.split(half, N // 3, 1) for half in np.split(img, N // 3, 0))
        else:
            img = [img]

        new = []
        for sub in img:
            pat = '/'.join(''.join(c for c in row) for row in sub)
            new.append(rules[pat])

        if len(new) == 1:
            new = new[0]
        else:
            new = [flat(a) for a in flat(list(zip(*c)) for c in chunk(N // 3, new))]

    # print('new', new)
    # print('\n'.join(new))
    # print()
    return new


def part1(input, n=2):
    rules = parse(input)
    img = initial.split('\n')
    for _ in range(n):
        img = step(img, rules)
    img = '\n'.join(img)

    return img, sum(1 for c in img if c == '#')


img, c = part1(inp)
print(img)
print(c)  # 12

img, c = part1(input, 18)
print(img)
print(c)  # 197
