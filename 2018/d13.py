import time
from collections import defaultdict

import numpy as np

with open('d13.txt', 'rt') as f:
    input = f.read().strip('\n')

inp = r"""
/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   
""".strip('\n')


def printtracks(tracks):
    print('\n'.join(''.join(x for x in row) for row in tracks))


def part1(input: str):
    X = max(len(line) for line in input.splitlines())
    tracks = np.array([list(line.ljust(X)) for line in input.splitlines()])

    hist = defaultdict(int)
    moves = {0: (0, -1), 2: (0, 1), 3: (1, 0), 1: (-1, 0)}
    dirmap = {'<': 0, '>': 2, 'v': 3, '^': 1}
    dirs = {}

    carts = np.transpose(np.where(np.isin(tracks, ['<', '>', '^', 'v'])))
    carts = list(sorted((tuple(c) for c in carts)))
    print(f'{len(carts)} carts')
    for cart in carts:
        # print(cart,tracks[cart])
        dir = dirmap[tracks[cart]]
        tracks[cart] = '-' if dir % 2 == 0 else '|'
        dirs[cart] = dir

    while len(carts) > 1:
        newcarts = []
        # print(carts)
        while carts:
            cart = carts.pop(0)
            dir = dirs[cart]
            last = hist[cart]
            r, c = cart
            dr, dc = moves[dir]
            newcart = (r + dr, c + dc)
            next = tracks[newcart]
            if newcart in newcarts or newcart in carts:
                print(f'collision! {newcart[1]},{newcart[0]}')
                # tracks[newcart] = 'X'
                if newcart in newcarts: newcarts.remove(newcart)
                if newcart in carts: carts.remove(newcart)
                continue
            if next == '-' or next == '|':  # no change
                pass
            elif next == '\\':
                if dir % 2 == 0:  # if horizontal turn right
                    dir = (dir + 1) % 4
                else:  # if vertical turn left
                    dir = (dir - 1) % 4
            elif next == '/':
                if dir % 2 == 0:  # if horizontal turn left
                    dir = (dir - 1) % 4
                else:  # if vertical turn right
                    dir = (dir + 1) % 4
            elif next == '+':  # turn based on hist
                if last == 0:
                    dir = (dir - 1) % 4
                elif last == 2:
                    dir = (dir + 1) % 4
                last = (last + 1) % 3
            hist[newcart] = last
            dirs[newcart] = dir
            newcarts.append(newcart)
        # print('n', newcarts)
        carts = list(sorted(newcarts))

    print('left', carts)


part1(inp)

part1(input)

#43,91
#35,59