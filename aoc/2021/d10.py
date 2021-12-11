from collections import deque

_match = {']': '[', '}': '{', '>': '<', ')': '('}
_pts = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}


def parse_input(data):
    return data.split("\n")


def check(line):
    q = deque([])
    for c in line:
        if c in '(<{[':
            q.append(c)
        elif c in ')>}]':
            if _match[c] != q.pop():
                return c

    return q


def complete(q):
    _m = {v: k for (k, v) in _match.items()}
    _p = {')': 1, ']': 2, '}': 3, '>': 4}
    tot = 0
    for c in reversed(q):
        tot = tot * 5 + _p[_m[c]]
    return tot


def main():
    from aocd import data

    #     data = """[({(<(())[]>[[{[]{<()<>>
    # [(()[<>])]({[<{<<[]>>(
    # {([(<{}[<>[]}>{[]{[(<()>
    # (((({<>}<{<{<>}{[]{[]{}
    # [[<[([]))<([[{}[[()]]]
    # [{[{({}]{}}([{[{{{}}([]
    # {<[[]]>}<{[{[{[]{()[[[]
    # [<(<(<(<{}))><([]([]()
    # <{([([[(<>()){}]>(<<{{
    # <{([{{}}[<[[[<>{}]]]>[]]
    # """

    lines = parse_input(data)
    tot = sum(_pts.get(c, 0) for line in lines if isinstance(c := check(line), str))
    print(f'part 1: {tot}')

    pts = [complete(q) for line in lines if isinstance(q := check(line), deque) and len(q) > 0]
    n = len(pts)
    print(f'part 2: {sorted(pts)[(n - 1) // 2]}')


if __name__ == '__main__':
    main()
