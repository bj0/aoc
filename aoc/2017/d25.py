import re
from collections import defaultdict

with open('d25.txt', 'rt') as f:
    input = f.read()

inp = """
Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.
"""


def stater(value, new_value, direction, new_state, value2, new_value2, direction2, new_state2):
    current = yield
    while True:
        if current == value:
            current = yield new_state, new_value, -1 if direction == 'left' else 1
        elif current == value2:
            current = yield new_state2, new_value2, -1 if direction2 == 'left' else 1
        else:
            raise Exception(f"invalid value: '{current}' (not '{value}' or '{value2}')")


def parse(input):
    start = re.search(r"Begin in state (\w)", input, re.DOTALL).group(1)
    checksum = re.search(r"checksum after (\d+) steps", input, re.DOTALL).group(1)

    states = {}

    matches = re.findall(
        r"In state (\w):.*?current value is (\d).*?the value (\d).*?to the (right|left).*?with state (\w).*?current value is (\d).*?the value (\d).*?to the (right|left).*?with state (\w)",
        input,
        re.DOTALL)

    for groups in matches:
        state, args = groups[0], groups[1:]
        gen = stater(*args)
        next(gen)
        states[state] = gen

    return states, start, checksum


def part1(input):
    states, state, N = parse(input)
    tape = defaultdict(lambda: '0')
    cursor = 0
    for n in range(int(N)):
        state, new_value, dc = states[state].send(tape[cursor])
        tape[cursor] = new_value
        cursor += dc

    print(list(tape[i] for i in sorted(tape.keys())))
    print(sum(int(i) for i in tape.values()))


part1(inp)

part1(input)
