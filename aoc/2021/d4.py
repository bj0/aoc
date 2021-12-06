import re

from aocd import data

nums, *boards = data.strip().split('\n\n')
nums = nums.split(',')


def check_boards(boards, num):
    boards = [re.sub(rf'\b{num}\b', '.', b) for b in boards]

    # check rows
    for b in boards:
        if re.search(r'(\. *){5}', b):
            # print('row')
            return boards, b

    # check columns
    for b in boards:
        items = b.split()
        for i in range(5):
            if all(items[i + 5 * j] == '.' for j in range(5)):
                # print('col')
                return boards, b

    return boards, False


def part1(nums, boards):
    for num in nums:
        boards, win = check_boards(boards, num)
        if win:
            print(win)
            if isinstance(win, str):
                win = win.split()
            return sum(int(x) for x in win if x != '.') * int(num)
    return -1


def part2(nums, boards):
    for num in nums:
        print(f'doing {num}')
        boards, win = check_boards(boards, num)
        if win:
            while win:
                boards.remove(win)
                last = win
                boards, win = check_boards(boards, num)
                print(f'win {len(boards)}')
            if len(boards) == 0:
                if isinstance(last, str):
                    win = last.split()
                return sum(int(x) for x in win if x != '.') * int(num)
    return -1


print(f'part1: {part1(nums, boards)}')

print(f'part2: {part2(nums, boards)}')
