ops = {
    'addr': lambda r, a, b: r[a] + r[b],
    'addi': lambda r, a, b: r[a] + b,
    'mulr': lambda r, a, b: r[a] * r[b],
    'muli': lambda r, a, b: r[a] * b,
    'banr': lambda r, a, b: r[a] & r[b],
    'bani': lambda r, a, b: r[a] & b,
    'borr': lambda r, a, b: r[a] | r[b],
    'bori': lambda r, a, b: r[a] | b,
    'seti': lambda r, a, b: a,
    'setr': lambda r, a, b: r[a],
    'gtir': lambda r, a, b: 1 if a > r[b] else 0,
    'gtri': lambda r, a, b: 1 if r[a] > b else 0,
    'gtrr': lambda r, a, b: 1 if r[a] > r[b] else 0,
    'eqir': lambda r, a, b: 1 if a == r[b] else 0,
    'eqri': lambda r, a, b: 1 if r[a] == b else 0,
    'eqrr': lambda r, a, b: 1 if r[a] == r[b] else 0
}


def part1(input, part2=False):
    ipr = int(input[0][4])
    instructions = []
    for line in input[1:]:
        op, *params = line.split()
        a, b, c = [int(x) for x in params]
        instructions.append((op, a, b, c))

    regs = [0] * 6
    if part2:
        regs[0] = 1
    ip = 0
    N = len(instructions)
    while 0 <= ip < N:
        regs[ipr] = ip
        op, a, b, c = instructions[ip]
        regs[c] = ops[op](regs, a, b)
        ip = regs[ipr] + 1
        if ip == 2:
            print(*regs)

    print(regs)
    # ret = ops[op](regs, a, b)


with open('d19.txt', 'rt') as f:
    input = f.read().splitlines()

inp = """
#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5
""".strip().splitlines()

part1(inp)

part1(input, True)

# it's calculating a number in r2 (10551377), then counting the factors of that number
# = 10996992