import numpy as np

input = 8141


def part1(input, sz=3):
    g = np.zeros((302, 302))
    for x in range(301):
        for y in range(301):
            rid = x + 10
            pw = (rid * y + input) * rid
            pw = (pw // 100) % 10
            g[x, y] = pw - 5

    def key(coord):
        i, j = coord
        np_sum = np.sum(g[i:i + sz, j:j + sz])
        # print(np_sum)
        return np_sum

    mx = max(((i, j) for i in range(1, 300 - sz) for j in range(1, 300 - sz)), key=key)

    # x, y = mx

    # print(g[x - 2:x + 3, y - 2:y + 3])

    # print(mx, key(mx))
    return mx, key(mx)


def part2(input, sz0=2, sz1=300):
    mx = 0
    mcoord = None
    msz = 0
    for sz in range(sz0, sz1 + 1):
        coord, max = part1(input, sz)
        if max > mx:
            mx = max
            mcoord = coord
            msz = sz
            print(mcoord, msz, mx)

    print(mcoord, msz, mx)


# not 235, 16
# part1(input)
import time
t = time.perf_counter()
part2(input, 2, 298)

print(f'{time.perf_counter() - t}s')
