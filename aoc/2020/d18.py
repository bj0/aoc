from collections import deque
from math import prod
from operator import mul, add

from aocd import data


def compute(line):
    op = None
    q = deque(line)
    ret = 0
    while q:
        c = q.popleft()
        if c == ' ':
            continue
        elif c == '*':
            op = mul
            continue
        elif c == '+':
            op = add
            continue
        elif c == '(':
            num, q = compute(q)
        elif c == ')':
            return ret, q
        else:
            num = int(c)

        if op is None:
            ret = num
        else:
            ret = op(ret, int(num))
    return ret


tot = sum(compute(line) for line in data.splitlines())
print(f'part1: {tot}')


# data = "2 * 3 + (4 * 5)"
def compute2(line):
    while (i := line.find('(')) != -1:
        ret, end = compute2(line[i + 1:])
        line = line[:i] + str(ret) + end

    if (i := line.find(')')) != -1:
        return compute2(line[:i]), line[i + 1:]

    return prod(sum(int(y) for y in mg.split('+'))
                for mg in line.split('*'))


tot = sum(compute2(line) for line in data.splitlines())
print(f'part2: {tot}')
