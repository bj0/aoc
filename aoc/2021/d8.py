# alternate solution could be to just use the counts segment uses in 1-10, eliminates
# the need for custom logic
# todo?
# the counts are:
# sums = {
#         42: "0",
#         17: "1",
#         34: "2",
#         39: "3",
#         30: "4",
#         37: "5",
#         41: "6",
#         25: "7",
#         49: "8",
#         45: "9",
#     }


from collections import Counter

_digits = {
    frozenset('abcefg'): '0',
    frozenset('cf'): '1',
    frozenset('acdeg'): '2',
    frozenset('acdfg'): '3',
    frozenset('bcdf'): '4',
    frozenset('abdfg'): '5',
    frozenset('abdefg'): '6',
    frozenset('acf'): '7',
    frozenset('abcdefg'): '8',
    frozenset('abcdfg'): '9'
}


def parse_input(data):
    return [[g.split() for g in line.split(' | ')] for line in data.split('\n')]


def solve(sigs):
    map = {}
    sigs = [set(s) for s in sigs]
    opts = {i: [s for s in sigs if len(s) == i] for i in range(1, 9)}
    # print(opts)
    # print([len(x) for x in opts.values()])

    # find a by diff of 1 & 7
    one, = opts[2]
    seven, = opts[3]
    four, = opts[4]
    eight, = opts[7]

    for s in opts[6]:
        if four < s:
            nine = s
        elif not one < s:
            six = s
        else:
            zero = s

    for s in opts[5]:
        if one < s:
            three = s
        elif len(six ^ s) == 1:
            five = s
        else:
            two = s

    map['a'], = seven - one
    map['b'], = four - three
    map['c'], = seven - five
    map['d'], = eight - zero
    map['e'], = two - nine
    map['f'], = three - two
    map['g'], = nine - four - seven

    # print(map)
    return {v: k for (k, v) in map.items()}


def main():
    from aocd import data
    #
    #     data = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
    # edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
    # fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
    # fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
    # aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
    # fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
    # dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
    # bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
    # egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
    # gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

    inp, out = zip(*parse_input(data))
    num = sum(1 for dig in out for d in dig if len(Counter(d)) in [2, 4, 3, 7])
    print(f'part 1: {num}')

    tot = 0
    for inp, out in parse_input(data):
        map = solve(inp)
        d = ''.join(_digits[frozenset(map[c] for c in dig)] for dig in out)
        tot += int(d)

    print(f'part 2: {tot}')


if __name__ == '__main__':
    main()

