from aocd import data


def step(idx, mem):
    op = mem[idx]
    if op == 99:
        return None

    a, b, c = mem[idx + 1:idx + 4]
    if op == 1:
        r = mem[a] + mem[b]
        return mem[:c] + (r,) + mem[c + 1:]
    elif op == 2:
        r = mem[a] * mem[b]
        return mem[:c] + (r,) + mem[c + 1:]
    else:
        raise Exception("invalid op")


def run(memory, a, b):
    program = memory[:1] + (a, b) + memory[3:]

    idx = 0
    while next := step(idx, program):
        program = next
        idx += 4

    return program[0]


memory = tuple(int(x) for x in (data.strip().split(',')))

ret = run(memory, 12, 2)

print(f'part 1: {ret}')
# 4484226

for a in range(100):
    for b in range(100):
        ret = run(memory, a, b)
        if ret == 19690720:
            print(f'part 2: {a, b}, {100 * a + b}')
# 5696
