# started at 22
from collections import deque, defaultdict

with open('d8.txt', 'rt') as f:
    input = f.read().strip()

inp = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"


def part12(input):
    data = [int(x) for x in input.split()]

    kids = 1
    meta = 0
    idx = 0
    tot = 0
    stack = deque()
    stack.append((0, kids, meta))
    value = defaultdict(int)
    children = defaultdict(list)
    last_id = 0
    while stack:
        # print(stack)
        id, kids, meta = stack.pop()
        if kids > 0:
            stack.append((id, kids - 1, meta))
            kids, meta = data[idx:idx + 2]
            last_id += 1
            children[id].append(last_id)
            stack.append((last_id, kids, meta))
            idx += 2
        else:
            mdata = data[idx:idx + meta]

            tot += sum(mdata)
            idx += meta

            my_kids = children[id]
            if len(my_kids) == 0:
                value[id] = sum(mdata)
            else:
                value[id] = sum(value[my_kids[i - 1]] for i in mdata if 0 < i <= len(my_kids))

    print()
    print(tot)  # part 1
    print(value[1])  # part 2
    print(value)


part12(inp)

# p1 at 41
# p2 at 59
part12(input)
