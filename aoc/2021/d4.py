from aocd import data

from aoc.util import perf


def parse_input(data):
    """parse input into list of draw numbers and 3d array of boards"""
    nums, *boards = data.strip().split('\n\n')
    nums = nums.split(',')
    boards = [[row.split() for row in board.split("\n")] for board in boards]
    return nums, boards


def check_board(nums, board):
    """check board rows and columns for match"""
    def check(group):
        if len(set(group) - set(nums)) == 0:
            return True

    for row in board:
        if check(row):
            return True

    for col in zip(*board):
        if check(col):
            return True

    return False


def drawer(nums):
    for i in range(len(nums)):
        yield nums[:i + 1]


def matcher(nums, boards):
    """iterate through matches"""
    for draw_nums in drawer(nums):
        for board in boards:
            if check_board(draw_nums, board):
                boards.remove(board)
                yield board, draw_nums

        if len(boards) == 0:
            break


def find_first_match(nums, boards):
    return next(matcher(nums, boards))


def find_last_match(nums, boards):
    return [m for m in matcher(nums, boards)][-1]


@perf
def find(nums, boards, matcher):
    board, nums = matcher(nums, boards)

    return sum(int(x) for row in board for x in row if x not in nums) * int(nums[-1])


def main():
    nums, boards = parse_input(data)
    print(f'part1: {find(nums, boards, find_first_match)}')

    print(f'part2: {find(nums, boards, find_last_match)}')


if __name__ == "__main__":
    main()
