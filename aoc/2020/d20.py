import re
from math import prod
import numpy as np
from aocd import data


# def r(x):
#     return ''.join(reversed(x))


def ra(a):
    return '\n'.join(''.join(x for x in c) for c in zip(*a.split('\n')[::-1]))


def fa(a):
    return '\n'.join(''.join(reversed(row)) for row in a.split('\n'))

def match_right(a, b):
    return all(x == y for x,y in zip())

# @dataclass(frozen=True)
# class Tile:
#     id: int
#     tile: str = field(repr=False)
#     top: str = field(repr=False)
#     bottom: str = field(repr=False)
#     left: str = field(repr=False)
#     right: str = field(repr=False)
#     rot: int
#     flipped: bool
#
#     def get_tile(self):
#
#         if self.rot == 0:
#             if not self.flipped:
#                 return self.tile
#             else:
#                 return fa(self.tile)
#
#     @staticmethod
#     def _from(id, tile):
#         return Tile(id=id,
#                     tile='\n'.join(tile),
#                     top=tile[0],
#                     bottom=tile[-1],
#                     left=''.join(line[0] for line in tile),
#                     right=''.join(line[-1] for line in tile),
#                     rot=0,
#                     flipped=False)
#
#     def rotate(self, rot=1):
#         new = replace(self)
#         for i in range(rot):
#             new = replace(new,
#                           rot=(new.rot + 1) % 4,
#                           bottom=r(new.right),
#                           left=new.bottom,
#                           top=r(new.left),
#                           right=new.top)
#         return new
#
#     def flip(self):
#         return replace(self,
#                        flipped=not self.flipped,
#                        left=self.right,
#                        right=self.left,
#                        top=r(self.top),
#                        bottom=r(self.bottom))
#
#     def match_right(self, other):
#         return self.right == other.left
#
#     def match_down(self, other):
#         return self.bottom == other.top
#
#     def match_left(self, other):
#         return self.left == other.right
#
#     def match_up(self, other):
#         return self.top == other.bottom
#
#     def matches(self, other) -> bool:
#         return (self.match_right(other) or
#                 self.match_down(other) or
#                 self.match_left(other) or
#                 self.match_up(other))


tiles = {}
for tile in re.split(r'\n\n', data):
    lines = tile.split('\n')
    n = int(lines[0].split()[1][:-1])
    tiles[n] = Tile._from(n, lines[1:])


def mutate(tile):
    yield tile
    for i in range(3):
        yield (tile := tile.rotate())
    yield (tile := tile.rotate().flip())
    for i in range(3):
        yield (tile := tile.rotate())


matches = {}
for k0, t0 in tiles.items():
    for k1 in tiles.keys() - {k0}:
        t0d = matches.setdefault(k0, {})
        if len(t0d) == 4 or k1 in (t.id for t in t0d.values()):
            continue
        for y in mutate(tiles[k1]):
            if 'right' not in t0d and t0.match_right(y):
                t0d['right'] = y
                break
            if 'left' not in t0d and t0.match_left(y):
                t0d['left'] = y
                break
            if 'down' not in t0d and t0.match_down(y):
                t0d['down'] = y
                break
            if 'up' not in t0d and t0.match_up(y):
                t0d['up'] = y
                break
        # working
        # t1 = tiles[k1]
        # if any(t0.matches(y) for y in mutate(t1)):
        #     matches.setdefault(t0, set()).add(t1)
        #     matches.setdefault(t1, set()).add(t0)

# print(matches)
# print([k for k in matches if len(matches[k]) == 0])
# print([k for k in matches if len(matches[k]) == 1])
# print([k for k in matches if len(matches[k]) == 2])
# print([(k.id,matches[k]) for k in matches if len(matches[k]) == 2])
# print([matches[k] for k in (2347,1091,2297,1459)])

# 8581320593371
print(f'part1: {prod(k for k in matches if len(matches[k]) == 2)}')
