# interesting idea, using recursion and caching:

from functools import lru_cache

from aoc.util import perf


def parse_input(data):
    algo, img = data.split('\n\n')
    return img.splitlines(), algo


@perf
def solve(img, algo, steps):
    @lru_cache(None)
    def f(x, y, t):
        if t == 0: return 0 <= y < len(img) and 0 <= x < len(img) and img[x][y] == '#'
        return algo[1 * f(x + 1, y + 1, t - 1) + 2 * f(x + 1, y, t - 1) + 4 * f(x + 1, y - 1, t - 1) +
                    8 * f(x, y + 1, t - 1) + 16 * f(x, y, t - 1) + 32 * f(x, y - 1, t - 1) +
                    64 * f(x - 1, y + 1, t - 1) + 128 * f(x - 1, y, t - 1) + 256 * f(x - 1, y - 1, t - 1)] == '#'

    return sum(f(x, y, steps) for x in range(-steps, len(img) + steps)
               for y in range(-steps, len(img) + steps))


def main(data):
    img, algo = parse_input(data)

    tot = solve(img, algo, 2)
    print(f'part 1:{tot}')

    tot = solve(img, algo, 50)
    print(f'part 2:{tot}')


if __name__ == '__main__':
    from aocd import data

    main(data)
