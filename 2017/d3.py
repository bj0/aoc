def f(n):
    if n == 1: return 1
    return 4 * (n - 1) + f(n - 2)


def part1(input):
    for i in range(1, 2000, 2):
        if input <= f(i):
            break
    else:
        raise Exception(f" {i} not high enough: {input} > {f(i)}")

    brcorner = f(i)
    width = i
    N = 4 * (width - 1)
    side = N // 4
    shell = (i + 1) // 2

    if brcorner == input:
        return shell - 1, shell - 1

    tlcorner = brcorner - N // 2
    p = brcorner - side // 2
    if abs(p - input) < side // 2:
        return abs(p - input), shell - 1
    elif abs((p - side) - input) < side // 2:
        return shell - 1, abs((p - side) - input)
    elif abs((p - 2 * side) - input) < side // 2:
        return abs((p - 2 * side) - input), shell - 1
    elif abs((p - 3 * side) - input) < side // 2:
        return shell - 1, abs((p - 3 * side) - input)

    raise Exception(f"can't get here:{input},{shell},{width},{side},{brcorner}")


def part2(input):
    # this one will just be easier to do with a 2d array instead of some fancy maths...
    # cheat by using numpy
    import numpy as np

    def sum(a, i, j):
        return np.sum(a[i - 1:i + 2, j - 1:j + 2])

    array = np.zeros((100, 100))
    n = 1
    x, y = 50, 50
    array[x, y] = n
    y += 1
    last = 0
    while n < input:
        last = n
        n = sum(array, x, y)
        array[x, y] = n
        if array[x, y-1] > 0 and array[x-1, y] == 0:
            x -= 1  # go up
        elif array[x + 1, y] > 0 and array[x, y - 1] == 0:
            y -= 1  # go left
        elif array[x, y + 1] > 0 and array[x + 1, y] == 0:
            x += 1  # go down
        else:
            y += 1  # go right

    return last, n


for input in (1, 12, 23, 1024, 289326):
    r = part1(input)
    print(r, sum(r))

print(part2(289326))