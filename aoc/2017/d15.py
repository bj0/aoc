input = (883, 879)


def gen(seed, factor):
    prev = seed
    while True:
        current = (prev * factor) % 2147483647
        yield current
        prev = current


def gen2(seed, factor, div):
    prev = seed
    while True:
        current = (prev * factor) % 2147483647
        if current % div == 0:
            yield current
        prev = current


def part1(input):
    seeda, seedb = input
    ga = gen(seeda, 16807)
    gb = gen(seedb, 48271)

    count = 0
    for _ in range(int(40e6)):
        x, y = next(ga), next(gb)
        if (x & 0xffff) == (y & 0xffff):
            count += 1

    return count


def part2(input):
    seeda, seedb = input
    ga = gen2(seeda, 16807, 4)
    gb = gen2(seedb, 48271, 8)

    count = 0
    for _ in range(int(5e6)):
        x, y = next(ga), next(gb)
        if (x & 0xffff) == (y & 0xffff):
            count += 1

    return count

import time

t = time.perf_counter()

# print(part1((65, 8921)))

# print(part1(input))

# print(part2((65, 8921)))

print(part2(input))

print(f'{time.perf_counter()-t}s')
