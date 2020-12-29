import re
from itertools import product

from aocd import data

pre, messages = re.split(r'\n\n', data)

rules = {}
for line in pre.splitlines():
    n, rule = line.split(':')
    if '"' in rule:
        rules[n] = rule.strip('" ')
    else:
        rules[n] = [[x for x in part.split()] for part in rule.split('|')]


def parse(rule):
    if isinstance(rule, str):
        return [rule]
    return {''.join(p) for part in rule for p in product(*[[y for y in parse(rules[x])] for x in part])}


rule0 = parse(rules['0'])

print(f'part1: {sum(1 for msg in messages.splitlines() if msg in rule0)}')

rule42 = parse(rules['42'])
rule31 = parse(rules['31'])

# print(rule42)
# print(rule31)
# 0: 8 11
# 8: 42 | 42 8
# 11: 42 31 | 42 11 31

r42 = f'({"|".join(rule42)})'
r31 = f'({"|".join(rule31)})'
pat = re.compile(f'({r42}+)({r31}+)')
valid = set()
for msg in messages.splitlines():
    if m := re.fullmatch(pat, msg):
        l, _, r, _ = m.groups()
        if len(l) > len(r):
            valid.add(msg)
        # else:
        #     print(msg, m.groups())

# not 311
print(f'part2: {len(valid)}')


# alt

def z(msg, rule):
    if isinstance(_rule := rules[rule], str):
        if msg and msg[0] == _rule:
            return [msg[1:]]
    else:
        a = []
        for part in rules[rule]:
            zm = [msg]
            for _rule in part:
                zm = [_left
                      for _msg in zm
                      for _left in z(_msg, _rule)]
                if not zm:
                    break
            else:
                a += zm
        return a
    return []


print(sum('' in z(msg, '0') for msg in messages.splitlines()))
rules['8'] = [['42'], ['42', '8']]
rules['11'] = [['42', '31'], ['42', '11', '31']]
print(sum('' in z(msg, '0') for msg in messages.splitlines()))