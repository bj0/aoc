with open('d24.txt', 'rt') as f:
    input = tuple(sorted(f.read().strip().splitlines()))

inp = """
0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10""".strip().splitlines()


def build(port, parts):
    # print(f'chk:{port},{parts}')
    for i, part in enumerate(parts):
        ports = part.split('/')
        if port in ports:
            # match
            next_port = ports[0] if ports[0] != port else ports[1]
            for bridge, strength, length in build(next_port, parts[:i] + parts[i + 1:]):
                yield f'{port}/{next_port}-{bridge}', int(port) * 2 + strength, length + 1

    # no match
    yield '', int(port), 0


def part1(input):
    starts = [p for p in enumerate(input) if p[1][0] == '0']
    parts = [part for part in input if part[0] != '0']
    # print(starts)
    max = 0
    maxb = ''
    for i, start in starts:
        # parts = input[:i] + input[i + 1:]
        start_port, port = start.split('/')
        for bridge, strength, length in build(port, parts):
            print(f'{start_port}/{port}-{bridge} : str={strength}, len={length+1}')
            if strength > max:
                max = strength
                maxb = f'{start_port}/{port}-{bridge} : {strength}'

    print()
    print(f'max {max}: {maxb}')


def part2(input):
    starts = [p for p in enumerate(input) if p[1][0] == '0']
    parts = [part for part in input if part[0] != '0']
    # print(starts)
    max = 0
    maxb = ''
    maxstr = 0
    for i, start in starts:
        # parts = input[:i] + input[i + 1:]
        start_port, port = start.split('/')
        for bridge, strength, length in build(port, parts):
            # print(f'{start_port}/{port}-{bridge} : str={strength}, len={length+1}')
            if length >= max:
                max = length
                maxb = f'{start_port}/{port}-{bridge} : {strength}'
                if strength > maxstr:
                    maxstr = strength

    print()
    print(f'max {max} (str={maxstr}): {maxb}')


# part1(inp)

import time

t = time.perf_counter()

# part1(input)

# part2(inp)

part2(input)

print(f'{time.perf_counter()-t}s')
