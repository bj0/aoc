with open('d9.txt', 'rt') as f:
    input = f.read().strip()


def find_eog(chunk):
    i = 0
    n = len(chunk)
    gc = 0
    while i < n:
        c = chunk[i]
        if c == '>':  # end
            return i, gc
        elif c == '!':  # skip
            i += 2
            continue
        i += 1
        gc += 1
    raise Exception("endless garbage")


def handle_group(chunk, score):
    i = 0
    n = len(chunk)
    total = score
    tgc = 0
    while i < n:
        c = chunk[i]
        if c == '}':  # end
            return i, total, tgc
        elif c == '{':  # new group
            eog, res, gc = handle_group(chunk[i + 1:], score + 1)
            total += res
            i += 2 + eog
            tgc += gc
            continue
        elif c == '<':  # garbage
            j, gc = find_eog(chunk[i + 1:])
            i += 2 + j
            tgc += gc
            continue
        # nothing?
        # print(f'wtf:{c}')
        i += 1
    raise Exception("endless group")


def part1(input):
    if input[0] != '{':
        raise Exception("does not start with a group")
    eog, tot, tgc = handle_group(input[1:], 1)

    # print(tot, eog + 1, len(input))
    return tot, tgc


for inp in """
{}
{{{}}}
{{},{}}
{{{},{},{{}}}}
{<a>,<a>,<a>,<a>}
{{<ab>},{<ab>},{<ab>},{<ab>}}
{{<!!>},{<!!>},{<!!>},{<!!>}}
{{<a!>},{<a!>},{<a!>},{<ab>}}
""".strip().split('\n'):
    print(inp)
    print(part1(inp))

print(part1(input))

for inp in """
<>
<random characters>
<<<<>
<{!>}>
<!!>
<!!!>>
<{o"i!a,<{i<a>
""".strip().split('\n'):
    print(find_eog(inp[1:]))
