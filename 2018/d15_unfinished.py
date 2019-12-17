from collections import ChainMap, deque


def rank(c):
    c = complex(c)
    return c.real, c.imag


def find_path(spots, units, start, *targets):
    # visiting = deque([(start, 0)])
    # meta = {start: (0, None)}
    # seen = set()
    # occupied = {*units, start}
    #
    # while visiting:
    #     pos, dist = visiting.popleft()
    #     for nb in (pos + dir for dir in (-1, -1j, 1j, 1)):
    #         if (nb not in spots) or (nb in occupied):
    #             continue
    #         if nb not in meta or meta[nb] > (dist + 1, rank(pos)):
    #             meta[nb] = (dist + 1, rank(pos))
    #         if nb in seen:
    #             continue
    #         if not any(nb == visit[0] for visit in visiting):
    #             visiting.append((nb, dist + 1))
    #     seen.add(pos)
    #
    # try:
    #     min_dist, closest = min((dist, rank(pos)) for pos, (dist, parent) in meta.items() if pos in targets)
    # except ValueError:
    #     return
    #
    # # path = []
    # d, r = min_dist, closest
    # pos = complex(r[0], r[1])
    # while d > 1:  # meta[closest][0] > 1:
    #     pos = complex(r[0], r[1])
    #     d, r = meta[pos]
    #     # path.append(pos)
    #
    # # path.reverse()
    # return pos  # path  # closest
    seen = set()
    steps = deque([(start, 0)])
    paths = {start: (0, None)}

    found = None
    while steps:
        pos, dist = steps.popleft()
        if (pos in seen) or (found and found[0] < dist):
            continue
        if pos in targets:
            # print(f'found {dist, pos}')
            if not found or found > (dist, rank(pos)):
                # if found:
                #     print(f'bettersol? {found, (dist, pos)}')
                found = (dist, rank(pos))
            continue
        for nb in (pos + dir for dir in (-1, -1j, 1j, 1)):
            if (nb not in spots) or (nb in units):
                continue
            if nb not in paths or paths[nb] > (dist + 1, rank(pos)):
                # if nb in paths:
                #     print(f'readjust? {paths[nb]}->{(dist + 1, rank(pos))}')
                paths[nb] = (dist + 1, rank(pos))
            if nb not in seen:
                steps.append((nb, dist + 1))
        seen.add(pos)

    if found:
        d, r = found
        # path = []
        pos = complex(r[0], r[1])
        while d > 1:
            pos = complex(r[0], r[1])
            # path.append(pos)
            d, r = paths[pos]

        # path.reverse()
        return pos  # path


def part1(input):
    spots = []
    gobs = {}
    elfs = {}
    for r, line in enumerate(input):
        for c, spot in enumerate(line.strip()):
            if spot in '.GE':
                coord = r + c * 1j
                spots.append(coord)
                if spot == 'G':
                    gobs[coord] = 200
                elif spot == 'E':
                    elfs[coord] = 200

    print('starting')
    turn = 0
    units = ChainMap({}, gobs, elfs)
    while gobs and elfs:
        if turn > 35:
            print(f'r:{turn}, g:{sum(g for g in gobs.values() if g > 0)}, e:{sum(e for e in elfs.values() if e > 0)}')
        for pos in sorted(units, key=lambda k: (k.real, k.imag)):
            # bug: this is breaking because if someone dies and another unit moves to his place, that unit
            # might get to take a second turn in place of the dead unit
            if not (gobs and elfs):
                # round ends early!
                break
            if pos in gobs:
                if turn == 38:
                    print(f'glin move: {pos}, {sum(gobs.values())} ')
                gob = gobs[pos]  # gobs.pop(pos)
                npos = do_turn(spots, units, elfs, pos)
                gobs.pop(pos)
                gobs[npos] = gob
            elif pos in elfs:
                if turn == 38:
                    print(f'e move: {pos}, {sum(elfs.values())} ')
                elf = elfs[pos]  # elfs.pop(pos)
                npos = do_turn(spots, units, gobs, pos)
                elfs.pop(pos)
                elfs[npos] = elf
        else:
            turn += 1
        # print_board(len(input[0].strip()), len(input), spots, gobs, elfs)
        # print(turn, gobs, elfs)
        # if turn > 22:
        #     return

    print_board(len(input[0].strip()), len(input), spots, gobs, elfs)
    print(turn)
    print(units)
    print('outcome', turn * sum(units.values()))


def print_board(w, h, spots, gobs, elfs):
    board = [list('#' * w) for _ in range(h)]
    for coord in spots:
        r, c = int(coord.real), int(coord.imag)
        board[r][c] = '.'
    for coord in gobs:
        r, c = int(coord.real), int(coord.imag)
        board[r][c] = 'G'
    for coord in elfs:
        r, c = int(coord.real), int(coord.imag)
        board[r][c] = 'E'

    print('\n'.join(''.join(c for c in row) for row in board))


def do_turn(spots, units, enemies, pos):
    # am i in range
    target = swing(enemies, pos)
    if target:
        # attack!
        # print(f'unit at {pos} attacks {target}!')
        # if target == (22 + 19j):
        #     print('wtf')
        #     print(f'{pos},{units[pos]} hitting {target},{enemies[target]}')

        if attack(enemies, target):
            print(f'unit died at {target}')
        return pos

    # not in range
    # find spots where enemies can be attacked
    targets = []
    for loc in enemies:
        for target in (loc + dir for dir in (-1, -1j, 1j, 1)):
            if (target in spots) and (target not in units):
                targets.append(target)

    move = find_path(spots, units, pos, *targets)
    if not move:
        # can't reach anyone!
        # print(f'no path from {pos}')
        return pos
    # move
    opos = pos
    pos = move
    # pos = path[1]
    target = swing(enemies, pos)
    if target:
        # in range, attack!
        # if target == (22 + 19j):
        #     print('wtf')
        #     print(f'{pos},{units[opos]} hitting {target},{enemies[target]}')

        if attack(enemies, target):
            print(f'unit died at {target}')
    return pos


def swing(enemies, pos):
    # am i in range
    targets = [target for target in (pos + dir for dir in (-1, -1j, 1j, 1)) if target in enemies]
    if targets:
        # if len(targets) > 0:
        #     hps = [enemies[t] for t in targets]
        #     m = min(hps)
        #     if len([h for h in hps if m == h]) > 1:
        #         print("duplicate mins hps!")
        #         print(targets)
        #         print(hps)
        #         print('choosing', min(targets, key=lambda t: enemies[t]))
        return min(targets, key=lambda t: enemies[t])


def attack(enemies, target):
    enemies[target] -= 3
    if enemies[target] <= 0:
        del enemies[target]
        return True
    return False


inp = ("""
#######   
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#   
#######""", """
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######""", """
#######   
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#   
#######""", """
#######   
#E.G#.#
#.#G..#
#G.#.G#   
#G..#.#
#...E.#
#######""", """
#######   
#.E...#   
#.#..G#
#.###.#   
#E#G#G#   
#...#G#
#######""", """
#########   
#G......#
#.E.#...#
#..##..G#
#...##..#   
#...#...#
#.G...G.#   
#.....G.#   
#########""")

# for x in inp:
#     part1(x.strip().splitlines())

# part1(inp[-1].strip().splitlines())

import time

with open('d15.txt', 'rt') as f:
    input = f.read().strip().splitlines()

t = time.perf_counter()

part1(input)

print(f'{time.perf_counter() - t}s')
# not 230126
# not 227955
# not 206800
# 206236?
