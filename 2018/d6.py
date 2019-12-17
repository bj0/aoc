from collections import defaultdict

with open('d6.txt', 'rt') as f:
    input = f.read().strip().splitlines()

inp = """
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
""".strip().splitlines()


def dist(frm, to):
    x0, y0 = frm
    x1, y1 = to
    return abs(x1 - x0) + abs(y1 - y0)


def part1(input):
    coords = tuple(tuple(int(x) for x in line.split(', ')) for line in input)
    szx = max(coords, key=lambda t: t[0])[0]
    szy = max(coords, key=lambda t: t[1])[1]
    sz = max(szx, szy)
    areas = defaultdict(int)
    for i in range(sz):
        for j in range(sz):
            closest = min(coords, key=lambda c: dist((i, j), c))
            areas[closest] += 1

    # remove infinities
    for i in range(-1, sz + 1):
        closest = min(coords, key=lambda c: dist((i, -1), c))
        areas[closest] = 0
        closest = min(coords, key=lambda c: dist((i, sz + 1), c))
        areas[closest] = 0

    for j in range(-1, sz + 1):
        closest = min(coords, key=lambda c: dist((-1, j), c))
        areas[closest] = 0
        closest = min(coords, key=lambda c: dist((sz + 1, j), c))
        areas[closest] = 0

    print(areas)
    mx = max(areas, key=lambda k: areas[k])
    print(mx, areas[mx])


def part2(input, tol=10000):
    coords = tuple(tuple(int(x) for x in line.split(', ')) for line in input)
    szx = max(coords, key=lambda t: t[0])[0]
    szy = max(coords, key=lambda t: t[1])[1]
    sz = max(szx, szy)
    areas = defaultdict(int)
    inside = 0
    outside = 0
    for i in range(sz):
        for j in range(sz):
            total = sum(dist((i, j), c) for c in coords)
            if total < tol:
                inside += 1
            else:
                outside += 1

    print(inside, outside)


# part1(inp)

# part1(input)

part2(inp, 32)

part2(input)
