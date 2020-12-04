from aocd import data


def rule1(num):
    i = num[0]
    for j in num[1:]:
        if i == j:
            return True
        i = j
    return False


def rule2(num):
    i = num[0]
    for j in num[1:]:
        if i > j:
            return False
        i = j
    return True


def rule1a(num):
    i = num[0]
    rep = 0
    for j in num[1:]:
        if i == j:
            rep += 1
        elif rep == 1:
            return True
        else:
            rep = 0
        i = j

    return rep == 1


def main(*_):
    start, stop = data.strip().split('-')
    # print(start, stop)

    count = 0
    for n in range(int(start), int(stop) + 1):
        n = str(n)
        if rule1(n) and rule2(n):
            count += 1

    print(f'part 1:{count}')
    part_a = count

    count = 0
    for n in range(int(start), int(stop) + 1):
        n = str(n)
        if rule1a(n) and rule2(n):
            count += 1

    print(f'part 2:{count}')
    part_b = count

    return part_a, part_b
    # print(Puzzle(2019, 4).answers)


if __name__ == '__main__':
    main()
