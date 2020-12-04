with open('d5.txt', 'rt') as f:
    input = f.read().strip()


def part1(input):
    out = list(input)
    idx = 0
    while idx < len(out) - 1:
        c = out[idx]
        nc = out[idx + 1]
        if c != nc and c.lower() == nc.lower():
            # print(c,nc,idx, out)
            out.pop(idx)
            out.pop(idx)
            # print(out)
            idx -= 1
        else:
            idx += 1

    chain = ''.join(out)
    return len(chain), chain


def part2(input):
    chars = 'abcdefghijklmnopqrstuvwxyz'

    min = 100000
    minc = ''
    for c in chars:
        test = [x for x in input if x.lower() != c]
        l, c = part1(test)
        if l < min:
            print(l,c)
            min = l
            minc = c

    print(minc)
    print(min)


# print(part1('dabAcCaCBAcCcaDA'))

# print(part1(input))

part2("dabAcCaCBAcCcaDA")

part2(input)
