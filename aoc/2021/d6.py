# using a queue to keep track of totals instead of trying to keep track of each fish makes this
# "exponential" problem linear
from collections import deque, Counter


def parse_input(data):
    c = Counter(data.strip().split(','))
    return deque(c.get(s, 0) for s in '012345678')


def age(ages: deque):
    n = ages.popleft()
    ages.append(n)
    ages[6] += n
    return ages


def check(ages, days):
    for d in range(days):
        ages = age(ages)

    return sum(ages)


def main():
    from aocd import data

    # data = """3,4,3,1,2"""

    print(f'part 1: {check(parse_input(data), 80)}')
    print(f'part 2: {check(parse_input(data), 256)}')


if __name__ == '__main__':
    main()
