from aocd import data

steps = [(d, int(x)) for (d, x) in (line.split() for line in data.strip().split('\n'))]
map = dict(forward=1, down=1j, up=-1j)


def part1(steps):
    return sum(map[d] * x for (d, x) in steps)


def part2(steps):
    a = 0
    pos = 0
    for (d, x) in steps:
        d = map[d]
        if d.real:
            pos += x + x * a * 1j
        else:
            a += x * d.imag
    return pos


pos = part1(steps)
print(f'part1: x={pos.real}, d={pos.imag}, pos={pos.real * pos.imag}')

pos = part2(steps)
print(f'part2: x={pos.real}, d={pos.imag}, pos={pos.real * pos.imag}')
