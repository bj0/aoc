from functools import partial

with open('d16.txt', 'rt') as f:
    input = f.read()


def _s(x, line):
    # np.roll(line, x)
    # tmp = line[:-x]
    # line[:x] = line[-x:]
    # line[x:] = tmp
    return ''.join((line[-x:], line[:-x]))


def _x(a, b, line: str):
    if b < a:
        a, b = b, a
    return ''.join((line[:a], line[b], line[a + 1:b], line[a], line[b + 1:]))


def _p(a, b, line):
    a, b = line.index(a), line.index(b)
    # a = np.where(line==a)[0]
    # b = np.where(line==b)[0]
    return _x(a, b, line)


def part1(input, n=16, N=1):
    line = ''.join(chr(ord('a') + i) for i in range(n))
    input = input.strip().split(',')

    # build ops
    ops = []
    for step in input:
        op = step[0]
        if op == 's':
            arg = int(step[1:])
            ops.append(partial(_s, arg))
        elif op == 'x':
            a, b = [int(x) for x in step[1:].split('/')]
            ops.append(partial(_x, a, b))
        else:
            a, b = step[1:].split('/')
            ops.append(partial(_p, a, b))

    # without caching this would take hours, but there is a repeating cycle so this just turns into
    # a billion hash lookups
    cache = {}
    for _ in range(N):
        if line not in cache:
            old_line = line
            for op in ops:
                line = op(line)
            cache[old_line] = line
        else:
            line = cache[line]
    return line


print(part1('s1,x3/4,pe/b', 5))

print(part1(input))

import time

t = time.perf_counter()

# part 2 included in part 1
print(part1('s1,x3/4,pe/b', 5, 2))

print(part1(input, N=int(1e9)))

print(f'{time.perf_counter()-t}s')

# import profile

# profile.run("part1(input, N=int(1e2))")
