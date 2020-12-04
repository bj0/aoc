from operator import xor
from functools import reduce


def swap(input, index, size):
    """swap with wrapping"""
    subinput = input[index:]
    while size > len(subinput):
        subinput += input

    out = tuple(reversed(subinput[:size]))
    if size + index > len(input):
        over = (size + index) - len(input)
        return out[size - over:] + input[over:index] + out[:-over]
    else:
        return input[:index] + out + input[size + index:]


assert swap((0, 1, 2, 3, 4), 0, 3) == (2, 1, 0, 3, 4)
assert swap((2, 1, 0, 3, 4), 3, 4) == (4, 3, 0, 1, 2)


def hash_round(input, N=256, start_idx=0, start_skip=0, hash=None):
    hash = hash or tuple(range(N))
    if isinstance(input, str):
        input = (int(i) for i in input.strip().split(', '))

    skip = start_skip
    idx = start_idx
    for d in input:
        # print(hash, idx, skip)
        hash = swap(hash, idx, d)
        idx = (idx + d + skip) % N
        skip += 1

    return hash[0] * hash[1], hash, idx, skip


def part1(input, N):
    return hash_round(input, N)[:2]


def part2(input):
    input = tuple(ord(c) for c in input) + (17, 31, 73, 47, 23)
    idx = skip = 0
    hash = None
    for _ in range(64):
        _, hash, idx, skip = hash_round(input, start_idx=idx, start_skip=skip, hash=hash)

    # densify
    dhash = tuple(reduce(xor, hash[i:i + 16]) for i in range(0, 256, 16))
    return ''.join(f'{i:02x}' for i in dhash)


if __name__ == '__main__':
    # print(part1('3, 4, 1, 5', 5))
    assert part1('3, 4, 1, 5', 5) == (12, (3, 4, 2, 1, 0))

    # 48705
    print(part1(
        '192,69,168,160,78,1,166,28,0,83,198,2,254,255,41,12'.replace(',', ', '),
        256
    ))

    for inp in ('', 'AoC 2017', '1,2,3', '1,2,4'):
        print(part2(inp))

    print()
    print(part2('192,69,168,160,78,1,166,28,0,83,198,2,254,255,41,12'))
