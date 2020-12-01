from itertools import product

from aocd import data

nums = [int(x) for x in data.strip().split()]


# nums = [int(x) for x in """1721
# 979
# 366
# 299
# 675
# 1456""".strip().split()]


def part1(nums):
    for i, a in enumerate(nums):
        for b in nums[i + 1:]:
            if a + b == 2020:
                return a, b
    return None, None


a, b = part1(nums)

print(f'part1 a={a},b={b}, {a + b}, {a * b}')


def part2(nums):
    for i, a in enumerate(nums):
        for j, b in enumerate(nums[i + 1:]):
            for c in nums[i + j + 1:]:
                if a + b + c == 2020:
                    return a, b, c
    return None, None, None


a, b, c = part2(nums)

print(f'part2 a={a}, b={b}, c={c}, {a + b + c}, {a * b * c}')

# shorter
p1 = next(a * b for (a, b) in product(nums, nums) if a + b == 2020)
p2 = next(a * b * c for (a, b, c) in product(nums, nums, nums) if a + b + c == 2020)
print(f'p1={p1}, p2={p2}')
