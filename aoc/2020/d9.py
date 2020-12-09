from itertools import combinations

from aocd import data

nums = tuple(map(int, data.splitlines()))


def check(x, pre):
    return any(a + b == x for (a, b) in combinations(pre, 2))


for idx, x in enumerate(nums[25:]):
    if not check(x, nums[idx:idx + 25]):
        # 133015568
        print(f'part1: {x} (i={idx})')
        break
else:
    print('no hit')

for i in range(len(nums)):
    for j in range(i + 2, len(nums)):
        if s := sum(nums[i:j]) == x:
            # 16107959
            print(f'part2: {min(nums[i:j]) + max(nums[i:j])}')
        elif s > x:
            break
