# first solution works but takes ~30s for p2.
# would prob be faster to create a map of 3x3 blocks -> output
from aoc.util import perf

block = [(i + j * 1j) for i, j in [
    (-1, -1), (0, -1), (1, -1),
    (-1, 0), (0, 0), (1, 0),
    (-1, 1), (0, 1), (1, 1)
]]

_map = {'#': '1', '.': '0'}


def parse_input(data):
    algo, img = data.split('\n\n')
    img = {(i + j * 1j): c
           for j, line in enumerate(img.splitlines())
           for i, c in enumerate(line)}
    return img, algo


def enhance_pixel(img, algo, pos):
    idx = int(''.join(_map[img.get(n, '.')]
                      for n in (pos + d for d in block)), 2)
    return algo[idx]


def enhance(img, algo, X, Y, off):
    return {i + j * 1j: enhance_pixel(img, algo, i - off + (j - off) * 1j)
            for i in range(*X)
            for j in range(*Y)}


@perf
def super_enhance(algo, img, N):
    mx = int(max(p.real for p in img))
    my = int(max(p.imag for p in img))
    X = -mx - 2 * N, mx + 2 * N
    Y = -my - 2 * N, my + 2 * N
    for i in range(N):
        img = enhance(img, algo, X, Y, 0)
    # trim boundaries
    return {p: v for (p, v) in img.items() if -1.5 * N < p.real < mx + 1.5 * N and -1.5 * N < p.imag < my + 1.5 * N}


def main(data):
    img, algo = parse_input(data)
    img = super_enhance(algo, img, 2)

    tot = sum(1 for c in img.values() if c == '#')
    print(f'part 1: {tot}')

    img, algo = parse_input(data)
    img = super_enhance(algo, img, 50)

    tot = sum(1 for c in img.values() if c == '#')
    print(f'part 2: {tot}')


if __name__ == '__main__':
    from aocd import data

    main(data)

    test_data = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
"""
    main(test_data)
