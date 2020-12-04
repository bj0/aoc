with open('d2.txt', 'rt') as f:
    input = f.read().strip()


def part1(input):
    input = input.split('\n')

    twos = 0
    threes = 0
    for line in input:
        box = {}
        for c in line:
            n = box.get(c, 0)
            box[c] = n + 1
        if any(box[k] == 2 for k in box):
            twos += 1
        if any(box[k] == 3 for k in box):
            threes += 1

    return twos, threes, twos * threes


def part2(input):
    input = input.split('\n')

    for (j, line) in enumerate(input):
        for line2 in input[j + 1:]:
            diff = 0
            cdiff = 0
            for i in range(len(line)):
                if line[i] != line2[i]:
                    diff += 1
                    cdiff = i
                    if diff > 1:
                        break
            else:
                return line, line2, cdiff, line[cdiff]


print(part1("""
abcdef
bababc
"""))

print(part1(input))

print(part2("""
fghij
fguij
""".strip()))

print(part2(input))
