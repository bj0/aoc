from itertools import permutations

from aocd import data
from collections import deque

from aocd.models import Puzzle


def step(idx, mem, input, output):
    op = mem[idx]
    if op == 99:
        # print('halt')
        return None

    im0 = op // 100 % 10 == 1
    im1 = op // 1000 % 10 == 1
    op = op % 100

    if op == 1:
        a, b, c = mem[idx + 1:idx + 4]
        r = (a if im0 else mem[a]) + (b if im1 else mem[b])
        return idx + 4, mem[:c] + (r,) + mem[c + 1:]
    elif op == 2:
        a, b, c = mem[idx + 1:idx + 4]
        r = (a if im0 else mem[a]) * (b if im1 else mem[b])
        return idx + 4, mem[:c] + (r,) + mem[c + 1:]
    elif op == 3:  # input
        a = mem[idx + 1]
        inp = input.popleft()
        # print('input', inp)
        return idx + 2, mem[:a] + (inp,) + mem[a + 1:]
    elif op == 4:
        a = mem[idx + 1]
        # print(f'out:{mem[a]}')
        output.append(mem[a])
        return idx + 2, mem
    elif op == 5:
        a, b = mem[idx + 1:idx + 3]
        a = a if im0 else mem[a]
        b = b if im1 else mem[b]
        return b if a != 0 else (idx + 3), mem
    elif op == 6:
        a, b = mem[idx + 1:idx + 3]
        a = a if im0 else mem[a]
        b = b if im1 else mem[b]
        return b if a == 0 else (idx + 3), mem
    elif op == 7:
        a, b, c = mem[idx + 1:idx + 4]
        a = a if im0 else mem[a]
        b = b if im1 else mem[b]
        return idx + 4, mem[:c] + (1 if a < b else 0,) + mem[c + 1:]
    elif op == 8:
        a, b, c = mem[idx + 1:idx + 4]
        a = a if im0 else mem[a]
        b = b if im1 else mem[b]
        return idx + 4, mem[:c] + (1 if a == b else 0,) + mem[c + 1:]
    else:
        raise Exception(f"invalid op: {op}")


def run(memory, phases):
    program = memory
    sig = 0
    input = deque()
    output = deque()
    for phase in phases:
        input.append(phase)
        input.append(sig)
        idx = 0
        while next := step(idx, program, input, output):
            idx, program = next

        sig = output.popleft()

    print(f'thruster signal: {sig}')
    return sig


# data = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
def main(*_):
    memory = tuple(int(m) for m in data.strip().split(','))
    mx = 0
    for phases in permutations([0, 1, 2, 3, 4], 5):
        sig = run(memory, phases)
        mx = max(mx, sig)

    print(f'part1 {mx}')


# print(Puzzle(2019, 7).answers)

if __name__ == '__main__':
    main()
