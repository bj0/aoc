from aocd.models import Puzzle


def mod_fuel(m):
    return m // 3 - 2


def total_fuel(m):
    f = 0
    while (m := mod_fuel(m)) > 0:
        f += m
    return f


def main(puzzle):
    masses = [int(m) for m in puzzle.input_data.strip().split()]

    fuels = [mod_fuel(m) for m in masses]
    part_a = sum(fuels)
    print(f'part 1: {part_a} (actual: {puzzle.answer_a})')
    # 3406342

    ffs = [total_fuel(m) for m in masses]

    part_b = sum(ffs)
    print(f'part 2: {part_b} (actual: {puzzle.answer_b})')
    # 5106629

    return part_a, part_b
    # part2 = sum(map(lambda m: sum(takewhile(lambda x: x > 0, ((m := m // 3 - 2) for _ in repeat(1)))), masses))
    # masses = [int(m) for m in fileinput.input('d1.txt')]
    # part1 = sum(m // 3 - 2 for m in masses)
    # part2 = sum(map(lambda m: sum(takewhile(lambda x: x > 0, accumulate(repeat(m // 3 - 2), lambda x, _: x // 3 - 2))), masses))
    # print(part1, part2)


if __name__ == '__main__':
    main(Puzzle(2019, 1))
