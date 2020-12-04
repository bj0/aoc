from collections import Counter

from aocd import data
from aocd.models import Puzzle


def main(*_):
    pixels = data.strip()
    w, h = 25, 6
    layers = [pixels[(x * w * h): (x + 1) * w * h] for x in range(len(pixels) // (h * w))]
    counters = [Counter(layer) for layer in layers]

    c = min(counters, key=lambda x: x['0'])
    part_a = c["1"] * c["2"]
    print(f'part 1: {part_a}')

    img = layers[0]
    for layer in layers[1:]:
        img = [layer[p] if img[p] == '2' else img[p] for p in range(w * h)]

    print('part 2:')
    for r in range(h):
        print(''.join(img[r * w:(r + 1) * w]).replace('0', ' ').replace('1', 'x').replace('2', '.'))

    # part 2 determined by eyeballs
    return part_a, 'BCPZB'


# print(Puzzle(2019, 8).answers)


if __name__ == '__main__':
    main()
