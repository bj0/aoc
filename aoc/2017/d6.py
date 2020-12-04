import numpy as np

input = "0	5	10	0	11	14	13	4	11	8	8	7	1	4	12	11"

def redist(banks):
    i = np.argmax(banks)
    m = banks[i]
    N = len(banks)
    banks[i] = 0
    i = (i + 1) % N
    for _ in range(m):
        banks[i] += 1
        i = (i + 1) % N


def part1(input):
    banks = [int(x) for x in input.split()]
    seen = set()
    x = tuple(banks)
    count = 0
    while x not in seen:
        seen.add(x)
        redist(banks)
        count += 1
        x = tuple(banks)

    return count


def part2(input):
    banks = [int(x) for x in input.split()]
    seen = set()
    x = tuple(banks)
    while x not in seen:
        seen.add(x)
        redist(banks)
        x = tuple(banks)

    # x is our loop
    redist(banks)
    count = 1
    while x != tuple(banks):
        redist(banks)
        count += 1

    return count


print(part1("0 2 7 0"))

print(part1(input))

print(part2("0 2 7 0"))

print(part2(input))