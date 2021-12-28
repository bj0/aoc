def parse_input(data):
    return {(i, j): c
            for j, line in enumerate(data.splitlines())
            for i, c in enumerate(line)}


def _print(map):
    sx = max(i for i, j in map) + 1
    sy = max(j for i, j in map) + 1
    disp = '\n'.join(
        ''.join(map[(i, j)] for i in range(sx))
        for j in range(sy))
    print(disp)


def step(map):
    sx = max(i for i, j in map) + 1
    sy = max(j for i, j in map) + 1
    east = map.copy()
    moves = 0
    for i, j in map:
        if map[(i, j)] == '>':
            p = (i + 1) % sx, j
            if map[p] == '.':
                moves += 1
                east[p] = '>'
                east[(i, j)] = '.'
    map = east
    south = map.copy()
    for i, j in map:
        if map[(i, j)] == 'v':
            p = i, (j + 1) % sy
            if map[p] == '.':
                moves += 1
                south[p] = 'v'
                south[(i, j)] = '.'

    return south, moves


def main(data):
    map = parse_input(data)

    i = 0
    while True:
        map, moves = step(map)
        i += 1
        if moves == 0:
            break

    print(f'part 1: {i}')


if __name__ == '__main__':
    from aocd import data

    main(data)

    main("""v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
""")
