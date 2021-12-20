# the parsing and tree traversal (especially explode) in this one was really annoying
from itertools import product


def parse_line(line):
    a, *rest = line
    if a == '[':
        a, rest = parse_line(rest)
    else:
        a = int(a)

    if not rest:
        return a

    if rest[0] == ',':
        b, rest = parse_line(rest[1:])
        a = [a, b]
    elif rest[0] == ']':
        rest = rest[1:]

    return a, rest


def parse_input(data):
    return [parse_line(line) for line in data.split('\n')]


def ladd(tree, dl):
    if isinstance(tree, int):
        return tree + dl
    left, right = tree
    return [left, ladd(right, dl)]


def expload(tree, depth=0, carry=0, boom=False):
    if isinstance(tree, int):
        return tree + carry, 0, 0, boom

    left, right = tree
    if depth >= 4 and isinstance(left, int) and isinstance(right, int) and not boom:
        return 0, left, right, True
    else:
        new_left, dl, carry, boom = expload(left, depth + 1, carry, boom)
        new_right, dl2, carry, boom = expload(right, depth + 1, carry, boom)
        if dl2 > 0:
            new_left = ladd(new_left, dl2)
            dl2 = 0
        return [new_left, new_right], dl + dl2, carry, boom


def split(tree, boom=False):
    if boom:
        return tree, boom
    if isinstance(tree, int):
        if tree >= 10:
            return [tree // 2, tree - (tree // 2)], True
        return tree, boom
    a, b = tree
    a, boom = split(a, boom)
    b, boom = split(b, boom)
    return [a, b], boom


def reduce(tree):
    while True:
        new_tree, *_ = expload(tree)
        if new_tree != tree:
            tree = new_tree
            continue
        new_tree, *_ = split(tree)
        if new_tree != tree:
            tree = new_tree
            continue
        break
    return tree


def add(a, b):
    return reduce([a, b])


def mag(tree):
    if isinstance(tree, int):
        return tree
    left, right = tree
    return 3 * mag(left) + 2 * mag(right)


def main(data):
    from time import perf_counter

    nums = parse_input(data)

    t = perf_counter()

    a = nums[0]
    for b in nums[1:]:
        a = add(a, b)

    print(f'part 1: {mag(a)} ({perf_counter() - t:.2}s)')

    t = perf_counter()
    mx = max(mag(add(a, b)) for a, b in product(nums, repeat=2) if a != b)

    print(f'part 2: {mx} ({perf_counter() - t:.2}s)')


if __name__ == '__main__':
    assert expload(parse_line('[[[[[9,8],1],2],3],4]'))[0] == [[[[0, 9], 2], 3], 4]
    assert expload(parse_line('[7,[6,[5,[4,[3,2]]]]]'))[0] == [7, [6, [5, [7, 0]]]]
    assert expload(parse_line('[[6,[5,[4,[3,2]]]],1]'))[0] == [[6, [5, [7, 0]]], 3]
    assert expload(parse_line('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]'))[0] == [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]
    assert expload(parse_line('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]'))[0] == [[3, [2, [8, 0]]], [9, [5, [7, 0]]]]

    assert split([[[[0, 7], 4], [15, [0, 13]]], [1, 1]])[0] == [[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]]

    assert reduce([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]) == [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]

    assert add([[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]) == [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]

    assert add([[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]], [7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]]) == [
        [[[4, 0], [5, 4]], [[7, 7], [6, 0]]], [[8, [7, 7]], [[7, 9], [5, 0]]]]

    test_data = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""
    main(test_data)

    from aocd import data

    main(data)
