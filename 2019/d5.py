from aocd import data


def step(idx, mem, input):
    op = mem[idx]
    if op == 99:
        print('halt')
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
    elif op == 3:  # input 1
        print('input')
        a = mem[idx + 1]
        return idx + 2, mem[:a] + (input,) + mem[a + 1:]
    elif op == 4:
        a = mem[idx + 1]
        print(f'out:{mem[a]}')
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


def run(memory, input):
    # program = memory[:1] + (a, b) + memory[3:]
    program = memory

    idx = 0
    while next := step(idx, program, input):
        idx, program = next


memory = tuple(int(m) for m in data.strip().split(','))

run(memory, 1)
# part1 7265618

run(memory, 5)
# part2 7731427
