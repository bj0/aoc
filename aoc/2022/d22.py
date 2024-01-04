from collections import defaultdict
import enum
import re
from functools import cache
from math import ceil
from multiprocessing import Pool
from operator import add, floordiv, mul, sub, truediv
from typing import Any, Callable

from aocd import data

from aoc.util import perf

# data = """        ...#
#         .#..
#         #...
#         ....
# ...#.......#
# ........#...
# ..#....#....
# ..........#.
#         ...#....
#         .....#..
#         .#......
#         ......#.

# 10R5L5R10L4R5L5"""

board, dirs = data.split("\n\n")
board = board.split("\n")
bounds = defaultdict(lambda: [1e3, -1])
g = {}
h = len(board)
w = 0
for j, line in enumerate(board):
    j += 1
    l, r = len(line.split(".")[0].split("#")[0]), len(line)
    bounds[j * 1j] = [l + 1, r]
    w = max(w, len(line))
    # print(j,line[:15])
    # if j == 163:
    # print('wtf',j,line, len(line))
    for i, c in enumerate(line):
        i += 1
        # if i == 51 and j == 163:
        # print('wtf',i,j,c)
        # exit(1)
        if c in ".#":
            bounds[i] = [min(bounds[i][0], j), max(bounds[i][1], j)]
            g[i + j * 1j] = c


_DIR = {"R": 1j, "L": -1j}
print(w, h)
N = max(w, h) // 4


def walk(p0, dir, n):
    p = p0
    for i in range(n):
        p1 = p + dir
        if p1 not in g:
            # wrap
            match dir:
                case 1:
                    p1 = bounds[p.imag * 1j][0] + p.imag * 1j
                case -1:
                    p1 = bounds[p.imag * 1j][1] + p.imag * 1j
                case 1j:
                    p1 = bounds[p.real][0] * 1j + p.real
                case -1j:
                    p1 = bounds[p.real][1] * 1j + p.real
        if g[p1] == "#":
            return p
        p = p1
    return p


@perf
def part1(dirs):
    dir = 1
    p = bounds[1j][0] + 1j
    while dirs:
        if dirs[0] in "RL":
            d, *dirs = dirs
            dir = dir * _DIR[d]
        else:
            n = re.match(r"\d+", "".join(dirs)).group()
            p = walk(p, dir, int(n))
            dirs = dirs[len(n) :]

    return {1: 0, 1j: 1, -1: 2, -1j: 3}[dir] + 1000 * p.imag + 4 * p.real


# 56372
print(f"part1: {part1(dirs)}")


def wrap(p, dir):
    c, r = p.real, p.imag
    match dir:
        case 1:
            if r <= N:  # from ride side face to back face (y -> 150-y, x -> -x)
                return ((3 * N - r + 1) * 1j + 2 * N), -1
            elif r <= 2 * N:  # from bottom face to right side face (x -> -y, y -> x)
                return (N * 1j + (r + N)), -1j
            elif r <= 3 * N:  # from back face to to right side face (x -> -x, y -> -y)
                return ((3 * N - r + 1) * 1j + 3 * N), -1
            else:  # from top face to back face (y -> x, x -> -y)
                return (3 * N * 1j + (r - 2 * N)), -1j

        case -1:
            if r <= N:  # front face to left side (x -> -x, y -> -y)
                return (1 + (3 * N - r + 1) * 1j), 1
            elif r <= 2 * N:  # bottom to left (x -> -y, y -> x)
                return ((2 * N + 1) * 1j + (r - N)), 1j
            elif r <= 150:  # left to front (x -> -xx, y -> -y)
                return (N + 1 + (3 * N - r + 1) * 1j), 1
            else:  # top to front (x -> -y, y -> x)
                return (1j + (r - 2 * N)), 1j

        case 1j:
            if c <= N:  # top to right (y -> y, x -> x)
                return (1j + (2 * N + c)), 1j
            elif c <= 2 * N:  # back to top (y -> -x, x -> y)
                return (N + (c + 2 * N) * 1j), -1
            else:  # right to bottom (y -> -x, x -> y)
                return (2 * N + (c - N) * 1j), -1

        case -1j:
            if c <= N:  # left to bottom (y -> -x, x -> y)
                return (N + 1 + (c + N) * 1j), 1
            elif c <= 2 * N:  # front to top (y -> -x, x -> y)
                return (1 + (c + 2 * N) * 1j), 1
            else:  # right to top (y -> -x, x -> y)
                return (4 * N * 1j + (c - 2 * N)), -1j
# def wrap(p, dir): 
#    """special case for test"""
#     c, r = p.real, p.imag
#     match dir:
#         case 1:
#             if r <= N:  # from ride side face to back face (y -> 150-y, x -> -x)
#                 return ((3 * N - r + 1) * 1j + 4 * N), -1
#             elif r <= 2 * N:  # from bottom face to right side face (x -> -y, y -> x)
#                 return ((2*N+1) * 1j + (4*N-r+1 + N)), 1j
#             else:  # from back face to to right side face (x -> -x, y -> -y)
#                 return ((3*N-r+1) * 1j + (3*N)), -1

#         case -1:
#             if r <= N:  # front face to left side (x -> -x, y -> -y)
#                 return ((N+1)*1j + (r+N) ), 1j
#             elif r <= 2 * N:  # bottom to left (x -> -y, y -> x)
#                 return ((4*N) * 1j + (4*N-r+N+1)), -1j
#             else:  # left to front (x -> -xx, y -> -y)
#                 return ((2*N-r+2*N+1) + (2*N) * 1j), -1j

#         case 1j:
#             if c <= N:  # top to right (y -> y, x -> x)
#                 return (4*N*1j + (3*N-c+1)), -1j
#             elif c <= 2 * N:  # back to top (y -> -x, x -> y)
#                 return (2*N+1 + (2*N-c+1) * 1j), 1
#             elif c <= 3*N:
#                 return (2*N*1j + (3*N-c+1)),-1j
#             else:  # right to bottom (y -> -x, x -> y)
#                 return (1 + (4*n-c+1+N) * 1j), 1

#         case -1j:
#             if c <= N:  # left to bottom (y -> -x, x -> y)
#                 return (1j + (N-c+1+2*N) ), 1j
#             elif c <= 2 * N:  # front to top (y -> -x, x -> y)
#                 return (2*N+1 + (c-N) * 1j), 1
#             elif c <= 3*N:
#                 return ((N+1)*1j + (3*N-c+1)), 1j
#             else:  # right to top (y -> -x, x -> y)
#                 return (3*N + (c-3*N+N)*1j), -1


def walk(p0, dir, n):
    p = p0
    dir1 = dir
    for i in range(n):
        p1 = p + dir
        # print(p,dir,p1,dir1)
        if p1 not in g:
            p1, dir1 = wrap(p, dir)
            # print(f'   warp {p}->{p1}, {dir}->{dir1}')
        # print(p,dir,p1,dir1)
        if g[p1] == "#":
            return p, dir
        p, dir = p1, dir1
        # print(' step', p, dir)
    return p, dir


@perf
def part2(dirs):
    dir = 1
    p = bounds[1j][0] + 1j
    # print('start',p)
    while dirs:
        if dirs[0] in "RL":
            d, *dirs = dirs
            dir = dir * _DIR[d]
            # print('rot',d,dir)
        else:
            n = re.match(r"\d+", "".join(dirs)).group()
            # print('walk',p,dir,n)
            p, dir = walk(p, dir, int(n))
            # print('land',p)
            dirs = dirs[len(n) :]

    # print(p, dir)
    return {1: 0, 1j: 1, -1: 2, -1j: 3}[dir] + 1000 * p.imag + 4 * p.real


# 197047
print(f"part2: {part2(dirs)}")
