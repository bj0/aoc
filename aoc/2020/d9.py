from itertools import combinations

from aocd import data


def part1(nums):
    for idx, x in enumerate(nums[25:]):
        if not any(a + b == x for (a, b) in combinations(nums[idx:idx + 25], 2)):
            return x


def part2(x, nums):
    for i in range(len(nums)):
        for j in range(i + 2, len(nums)):
            if s := sum(pre := nums[i:j]) == x:
                return min(pre) + max(pre)
            elif s > x:
                break


nums = tuple(map(int, data.splitlines()))

# 133015568
print(f'part1: {(val := part1(nums))}')

# 16107959
print(f'part2: {part2(val, nums)}')
