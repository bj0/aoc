_neighbors = {j + i * 1j for i in range(-1, 2) for j in range(-1, 2) if not ((i == 0) and (j == 0))}


def parse_input(data):
    return {
        j + i * 1j: int(p)
        for i, line in enumerate(data.split('\n'))
        for j, p in enumerate(line)
    }


def step(map):
    map = {pos: pow + 1 for (pos, pow) in map.items()}
    pop = {pos for pos in map if map[pos] > 9}
    count = 0
    popped = set()
    while pop:
        pos = pop.pop()
        if pos in popped:
            continue
        popped.add(pos)
        count += 1
        map[pos] = 0
        for n in (pos + d for d in _neighbors if pos + d in map and pos + d not in popped):
            map[n] = map[n] + 1
            if map[n] > 9:
                pop.add(n)

    return map, count


def main():
    from aocd import data

    #     data = """5483143223
    # 2745854711
    # 5264556173
    # 6141336146
    # 6357385478
    # 4167524645
    # 2176841721
    # 6882881134
    # 4846848554
    # 5283751526"""

    map = parse_input(data)

    tot = 0
    for i in range(100):
        map, c = step(map)
        tot += c

    print(f'part 1: {tot}')

    map = parse_input(data)
    for i in range(1000):
        map, c = step(map)
        if len(set(map.values())) == 1:
            print(f'part 2: {i + 1}')
            break


if __name__ == '__main__':
    main()
