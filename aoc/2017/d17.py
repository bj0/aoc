def part1(input, N=2018):
    skip = int(input.strip())

    buffer = [0]
    pos = 0

    for step in range(1, N):
        pos = ((pos + skip) % step) + 1
        buffer.insert(pos, step)

    i = buffer.index(N - 1)
    return buffer[i - 2:i + 3]  # , buffer


def part2(input, N=2018):
    skip = int(input.strip())

    # buffer = [0]
    pos = 0
    insertions = [0]
    for step in range(1, N + 1):
        pos = ((pos + skip) % step) + 1
        # buffer.insert(pos, step)
        insertions.append(pos)

    for step in range(N, 0, -1):
        if insertions[step] == 1:
            return step

    raise Exception("no insertion at 1??")

    # i = buffer.index(N - 1)
    # return buffer[i - 2:i + 3], buffer


# print(part1('3'))

print(part1('355'))

import time

t = time.perf_counter()

print(part2('355', N=int(50e6)))

print(f'{time.perf_counter()-t}s')
