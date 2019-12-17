import fileinput
# from itertools import repeat, takewhile, starmap, accumulate
from aocd import data


def mod_fuel(m):
    return m // 3 - 2


def total_fuel(m):
    f = 0
    while (m := mod_fuel(m)) > 0:
        f += m
    return f


masses = [int(m) for m in data.strip().split()]

fuels = [mod_fuel(m) for m in masses]
print(f'part 1: {sum(fuels)}')
# 3406342

ffs = [total_fuel(m) for m in masses]

print(f'part 2: {sum(ffs)}')
# 5106629

# part2 = sum(map(lambda m: sum(takewhile(lambda x: x > 0, ((m := m // 3 - 2) for _ in repeat(1)))), masses))
# masses = [int(m) for m in fileinput.input('d1.txt')]
# part1 = sum(m // 3 - 2 for m in masses)
# part2 = sum(map(lambda m: sum(takewhile(lambda x: x > 0, accumulate(repeat(m // 3 - 2), lambda x, _: x // 3 - 2))), masses))
# print(part1, part2)
