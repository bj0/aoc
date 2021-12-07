def parse_input(data):
    return [[tuple(int(x) for x in pt.split(',')) for pt in line.split(' -> ')] for line in data.split('\n')]


def map_lines(lines):
    map = {}
    for frm, to in lines:
        dx = 0 if frm[0] == to[0] else -1 if frm[0] > to[0] else 1
        dy = 0 if frm[1] == to[1] else - 1 if frm[1] > to[1] else 1
        pos = frm
        while pos != to:
            map[pos] = map.setdefault(pos, 0) + 1
            pos = (pos[0] + dx, pos[1] + dy)
        map[pos] = map.setdefault(pos, 0) + 1
    return map


def main():
    from aocd import data
#     data = """0,9 -> 5,9
    # 8,0 -> 0,8
    # 9,4 -> 3,4
    # 2,2 -> 2,1
    # 7,0 -> 7,4
    # 6,4 -> 2,0
    # 0,9 -> 2,9
    # 3,4 -> 1,4
    # 0,0 -> 8,8
    # 5,5 -> 8,2"""
    all_lines = parse_input(data)
    lines = [(p0, p1) for (p0, p1) in all_lines if p0[0] == p1[0] or p0[1] == p1[1]]
    map = map_lines(lines)

    print(f'part 1: {sum(1 for v in map.values() if v >= 2)}')

    map = map_lines(all_lines)

    print(f'part 2: {sum(1 for v in map.values() if v >= 2)}')


if __name__ == '__main__':
    main()
