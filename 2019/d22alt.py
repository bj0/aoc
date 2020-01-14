from aocd import data

# https://github.com/zedrdave/advent_of_code/blob/master/2019/22/__main__.py
# https://www.reddit.com/r/adventofcode/comments/ee0rqi/2019_day_22_solutions/fbtugcu/

shuffles = {'deal with increment ': lambda x, m, a, b: (a * x % m, b * x % m),
            'deal into new stack': lambda _, m, a, b: (-a % m, (m - 1 - b) % m),
            'cut ': lambda x, m, a, b: (a, (b - x) % m)}


# data = """
# deal into new stack
# cut -2
# deal with increment 7
# cut 8
# cut -4
# deal with increment 7
# cut 3
# deal with increment 9
# deal with increment 3
# cut -1
# """

# data = """
# deal with increment 7
# deal with increment 9
# cut -2
# """

def shuffle(m):
    a, b = 1, 0
    for s in data.strip().split('\n'):
        for name, f in shuffles.items():
            if s.startswith(name):
                arg = int(s[len(name):]) if name[-1] == ' ' else 0
                a, b = f(arg, m, a, b)
                break
    return a, b


m = 10007
a, b = shuffle(m)
print(f'part 1: {(2019 * a + b) % m}')
# 1867

m = 119315717514047
n = 101741582076661
a, b = shuffle(m)
pos = 2020
r = (b * pow(1 - a, m - 2, m)) % m
p = ((pos - r) * pow(a, n * (m - 2), m) + r) % m
print(f'part 2: {p}')
