def f(n):
    print(f'n{n}')
    if n < 10:
        n = yield from f(n + 1)
    return n


def g(out, n):
    x = yield from f(n)
    out.append(x)


out = []
for i in g(out, 2):
    print('it')
    print(i)
print(out)
