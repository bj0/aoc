with open('d19.txt', 'rt') as f:
    input = f.read().strip('\n')

inp = """
     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 
""".strip('\n')

import numpy as np


def part1(input):
    lines = input.split('\n')
    n = max(len(row) for row in lines)
    diagram = np.array([list(row.ljust(n)) for row in lines])

    def pad(v, w, ia, kw):
        v[:w[0]] = " "
        v[-w[1]:] = " "
        return v

    # pad so we don't need to do bounds checking
    diagram = np.pad(diagram, 1, pad)

    print(diagram.shape)
    c = np.where(diagram[1, :] == '|')[0][0]
    r = 1
    move = (1, 0)
    seen = ''
    steps = 1
    while True:
        steps += 1
        dr, dc = move
        r, c = r + dr, c + dc
        op = diagram[r, c]
        if op == '|' or op == '-':  # just continue
            continue
        elif op == '+':  # turn
            if dc == 0:  # left or right
                for delta in (-1, 1):
                    if diagram[r, c + delta] not in ['|', ' ']:
                        move = (0, delta)
                        continue
            else:  # up or down
                for delta in (-1, 1):
                    if diagram[r + delta, c] not in ['-', ' ']:
                        move = (delta, 0)
                        continue
        elif op == ' ':  # ran past the end!
            steps -= 1
            break
        else:  # some letter
            seen += op

    return seen, steps


print(part1(inp))

print(part1(input))