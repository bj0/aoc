def parse_input(data):
    pic, folds = data.split('\n\n')
    pic = {tuple(map(int, x)) for x in (line.split(',') for line in pic.split('\n'))}
    folds = [f[11:].split('=') for f in folds.split('\n')]
    return pic, folds


def fold(pic, dir, val):
    def flip(x, i):
        y = list(x)
        y[i] = val - abs(val - y[i])
        return tuple(y)

    idx = 0 if dir == 'x' else 1
    return ({x for x in pic if x[idx] < val} |
            {flip(x, idx) for x in pic if x[idx] > val})


def print_pic(pic):
    x, *_, X = sorted(a for (a, b) in pic)
    y, *_, Y = sorted(b for (a, b) in pic)
    for j in range(y, Y + 1):
        print()
        for i in range(x, X + 1):
            print('#' if (i, j) in pic else '.', end='')
    print()


def main(data, debug=False):
    pic, folds = parse_input(data)

    if debug:
        print_pic(pic)
        print()
    first = True
    for (d, v) in folds:
        pic = fold(pic, d, int(v))
        if first:
            if debug:
                print_pic(pic)
            first = False
            print(f'part 1: {len(pic)}')

    print('part 2:')
    print_pic(pic)


if __name__ == '__main__':
    from aocd import data

    test_data = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

    main(data)
    # main(test_data, True)
