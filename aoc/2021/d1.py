from aocd import data

from aoc.util import perf

puz = [int(x) for x in data.strip().split()]


@perf
def part1(nums):
    return sum(x > y for (x, y) in zip(nums[1:], nums[:-1]))


# 1602
print(f'part1: {part1(puz)}')


@perf
def part2(nums):
    return sum(sum(nums[i + 1:i + 4]) > sum(nums[i:i + 3])
               for i in range(len(nums) - 3))


print(f'part2 {part2(puz)}')
