import re

from aocd import data

pps = [
    dict(field.split(':') for field in pp.split())
    for pp in re.split('\n\n', data)
]

required = 'byr iyr eyr hgt hcl ecl pid'.split()

# 247
print(f'part1: {sum(1 for pp in pps if all(key in pp for key in required))}')

rules = dict(
    byr=re.compile(r'19[2-9]\d|200[12]'),
    iyr=re.compile(r'20(1\d|20)'),
    eyr=re.compile(r'20(2\d|30)'),
    hgt=re.compile(r'1([5-8]\d|9[0-3])cm|(59|6\d|7[0-6])in'),
    hcl=re.compile(r'#[0-9a-f]{6}'),
    ecl=re.compile(r'(amb|blu|brn|gry|grn|hzl|oth)'),
    pid=re.compile(r'\d{9}')
)


def valid(pp):
    return (all(key in pp for key in required) and
            all(rules[key].fullmatch(pp[key]) for key in rules))


# 145
print(f'part2: {sum(1 for pp in pps if valid(pp))}')
