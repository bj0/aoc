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
print(w,h)


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
            if r <= 50: # from ride side face to back face (y -> 150-y, x -> -x)
                return ((150-r+1)*1j + 100), -1
            elif r <= 100: # from bottom face to right side face (x -> -y, y -> x)
                return (50*1j + (r + 50)), -1j
            elif r <= 150: # from back face to to right side face (x -> -x, y -> -y)
                return ((150-r+1)*1j + 150), -1
            else: # from top face to back face (y -> x, x -> -y)
                return (150*1j + (r - 100)), -1j

        case -1:
            if r <= 50: # front face to left side (x -> -x, y -> -y) 
                return (1 + (150-r+1)*1j), 1
            elif r <= 100: # bottom to left (x -> -y, y -> x)
                return (101*1j + (r-50)), 1j
            elif r <= 150: # left to front (x -> -xx, y -> -y)
                return (51 + (150-r+1)*1j), 1
            else: # top to front (x -> -y, y -> x)
                return (1j + (r-100)), 1j
            
        case 1j:
            if c <= 50: # top to right (y -> y, x -> x)
                return (1j + (100+c)), 1j
            elif c <= 100: # back to top (y -> -x, x -> y)
                return (50 + (c + 100)*1j), -1
            else: # right to bottom (y -> -x, x -> y)
                return (100 + (c-50)*1j), -1

        case -1j:
            if c <= 50: # left to bottom (y -> -x, x -> y)
                return (51 + (c+50)*1j), 1
            elif c <= 100: # front to top (y -> -x, x -> y)
                return (1 + (c+100)*1j), 1
            else: # right to top (y -> -x, x -> y)
                return (200j + (c-100)), -1j

def walk(p0, dir, n):
    p = p0
    dir1 = dir
    for i in range(n):
        p1 = p + dir
        # print(p,dir,p1,dir1)
        if p1 not in g:
            p1, dir1 = wrap(p, dir)
        # print(p,dir,p1,dir1)
        if g[p1] == "#":
            return p
        p, dir = p1, dir1
    return p


@perf
def part2(dirs):
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

    print(p, dir)
    return {1: 0, 1j: 1, -1: 2, -1j: 3}[dir] + 1000 * p.imag + 4 * p.real


# 171088.0 low
print(f"part2: {part2(dirs)}")
