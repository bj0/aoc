from aocd import data
from aocd.models import Puzzle


def mandist(s, t):
    return sum(abs(x - y) for x, y in zip(s, t))


_dx = dict(U=0, R=1, L=-1, D=0)
_dy = dict(U=1, R=0, L=0, D=-1)


def get_pts(wire):
    pts = {}
    l = 1
    x, y = 0, 0
    for op in wire.split(','):
        d, n = op[0], int(op[1:])
        for i in range(n):
            x, y = x + _dx[d], y + _dy[d]
            pts.setdefault((x, y), l + i)
        l += n
    return pts


# input = """
# R8,U5,L5,D3
# U7,R6,D4,L4
# """.strip().split()
# input = """
# R75,D30,R83,U83,L12,D49,R71,U7,L72
# U62,R66,U55,R34,D71,R55,D58,R83""".strip().split()

def main(*_):
    wire0, wire1 = data.strip().split()
    pts0 = get_pts(wire0)
    pts1 = get_pts(wire1)
    cross = pts0.keys() & pts1.keys()
    part_a = min(mandist((0, 0), c) for c in cross)
    print(f'part 1: {part_a}')

    part_b = min(pts0[c] + pts1[c] for c in cross)
    print(f'part 2: {part_b}')

    return part_a, part_b


if __name__ == '__main__':
    main()
