from collections import deque
from time import perf_counter

from aocd import data

# data
# data = """
#          A
#          A
#   #######.#########
#   #######.........#
#   #######.#######.#
#   #######.#######.#
#   #######.#######.#
#   #####  B    ###.#
# BC...##  C    ###.#
#   ##.##       ###.#
#   ##...DE  F  ###.#
#   #####    G  ###.#
#   #########.#####.#
# DE..#######...###.#
#   #.#########.###.#
# FG..#########.....#
#   ###########.#####
#              Z
#              Z       """

# data = """
#                    A
#                    A
#   #################.#############
#   #.#...#...................#.#.#
#   #.#.#.###.###.###.#########.#.#
#   #.#.#.......#...#.....#.#.#...#
#   #.#########.###.#####.#.#.###.#
#   #.............#.#.....#.......#
#   ###.###########.###.#####.#.#.#
#   #.....#        A   C    #.#.#.#
#   #######        S   P    #####.#
#   #.#...#                 #......VT
#   #.#.#.#                 #.#####
#   #...#.#               YN....#.#
#   #.###.#                 #####.#
# DI....#.#                 #.....#
#   #####.#                 #.###.#
# ZZ......#               QG....#..AS
#   ###.###                 #######
# JO..#.#.#                 #.....#
#   #.#.#.#                 ###.#.#
#   #...#..DI             BU....#..LF
#   #####.#                 #.#####
# YN......#               VT..#....QG
#   #.###.#                 #.###.#
#   #.#...#                 #.....#
#   ###.###    J L     J    #.#.###
#   #.....#    O F     P    #.#...#
#   #.###.#####.#.#####.#####.###.#
#   #...#.#.#...#.....#.....#.#...#
#   #.#####.###.###.#.#.#########.#
#   #...#.#.....#...#.#.#.#.....#.#
#   #.###.#####.###.###.#.#.#######
#   #.#.........#...#.............#
#   #########.###.###.#############
#            B   J   C
#            U   P   P               """

# data = """
#              Z L X W       C
#              Z P Q B       K
#   ###########.#.#.#.#######.###############
#   #...#.......#.#.......#.#.......#.#.#...#
#   ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###
#   #.#...#.#.#...#.#.#...#...#...#.#.......#
#   #.###.#######.###.###.#.###.###.#.#######
#   #...#.......#.#...#...#.............#...#
#   #.#########.#######.#.#######.#######.###
#   #...#.#    F       R I       Z    #.#.#.#
#   #.###.#    D       E C       H    #.#.#.#
#   #.#...#                           #...#.#
#   #.###.#                           #.###.#
#   #.#....OA                       WB..#.#..ZH
#   #.###.#                           #.#.#.#
# CJ......#                           #.....#
#   #######                           #######
#   #.#....CK                         #......IC
#   #.###.#                           #.###.#
#   #.....#                           #...#.#
#   ###.###                           #.#.#.#
# XF....#.#                         RF..#.#.#
#   #####.#                           #######
#   #......CJ                       NM..#...#
#   ###.#.#                           #.###.#
# RE....#.#                           #......RF
#   ###.###        X   X       L      #.#.#.#
#   #.....#        F   Q       P      #.#.#.#
#   ###.###########.###.#######.#########.###
#   #.....#...#.....#.......#...#.....#.#...#
#   #####.#.###.#######.#######.###.###.#.#.#
#   #.......#.......#.#.#.#.#...#...#...#.#.#
#   #####.###.#####.#.#.#.#.###.###.#.###.###
#   #.......#.....#.#...#...............#...#
#   #############.#.#.###.###################
#                A O F   N
#                A A D   M                     """

map = {x + y * 1j: c for y, row in enumerate(data.strip('\n').split('\n')) for x, c in enumerate(row)}


def neighbors(p):
    return [p + dir for dir in [-1, 1, -1j, 1j]]


for p in map:
    if map.get(p) == 'A' and any(map.get(k) == 'A' for k in neighbors(p)) and any(
            map.get(k) == '.' for k in neighbors(p) if (s := k)):
        start = s
        break

A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# find portals

outers = set()


def get_port(p):
    # print(p, map.get(p), )
    a, d = next((a, d) for d in neighbors(p) if (a := map.get(d, '?')) in A)
    if p.real > d.real or p.imag > d.imag:
        port = a + map[p]
    else:
        port = map[p] + a

    for c in (p, d):
        if any(map.get(k) == '.' for k in neighbors(c) if (s := k)):
            entry = s
            break
    for c in (p, d):
        if any(map.get(k, '?') == '?' for k in neighbors(c)):
            outers.add(entry)
    return port, entry


portals = {}
for p in map:
    if map[p] in A:
        port, d = get_port(p)

        # print(port, map.get(p), map.get(d), a)
        if any(map.get(k) == '.' for k in neighbors(p)):
            loc = p
        else:
            loc = d
        portals.setdefault(port, set()).add(d)

paths = {}
for portal in portals:
    if len(portals[portal]) > 1:
        a, b = portals[portal]
        paths[a] = b
        paths[b] = a


def part1():
    # bfs search for zz
    q = deque([(start, 0)])
    visited = set()
    while q:
        p, d = q.popleft()
        visited.add(p)
        for np in neighbors(p):
            c = map[np]
            if c == 'Z' and any(map.get(k) == 'Z' for k in neighbors(np)):
                print(f'found exit!: {p, d, c}')
                return d
            if np not in visited:
                if map.get(np) == '.':
                    q.append((np, d + 1))
                elif map.get(np, '?') in A:
                    if p in paths and paths[p] not in visited:
                        q.append((paths[p], d + 1))


def part2():
    # bfs search for zz
    q = deque([(start, 0, 0)])
    visited = set()
    while q:
        p, d, l = q.popleft()
        visited.add((p, l))
        for np in neighbors(p):
            c = map[np]
            if c == 'Z' and l == 0 and any(map.get(k) == 'Z' for k in neighbors(np)):
                print(f'found exit!: {p, d, c}')
                return d
            if (np, l) not in visited:
                if map.get(np) == '.':
                    q.append((np, d + 1, l))
                elif map.get(np, '?') in A:
                    if p in paths:
                        nl = l + (-1 if p in outers else 1)
                        if nl >= 0 and (paths[p], nl) not in visited:
                            q.append((paths[p], d + 1, nl))


t = perf_counter()

n = part1()
print(f'part 1: {n}')

print(f'{perf_counter() - t:.2f}s')
t = perf_counter()

n = part2()
print(f'part 2: {n}')

print(f'{perf_counter() - t:.2f}s')
