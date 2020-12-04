import re
from dataclasses import dataclass, field, replace
from enum import Enum

inp = """
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (weak to fire, cold; immune to radiation) with an attack that does 12 slashing damage at initiative 4
""".strip()


class Type(Enum):
    Immune = "Immune"
    Infection = "Infection"


@dataclass(unsafe_hash=True)
class Squad:
    type: Type
    id: int
    size: int = field(hash=False)
    unit_hp: int
    immunities: frozenset = field(repr=False)
    weaknesses: frozenset = field(repr=False)
    power: int
    attack_type: str = field(repr=False)
    initiative: int

    @property
    def effective_power(self):
        return self.power * self.size

    def dmg_factor(self, dmg_type):
        return 0 if dmg_type in self.immunities else 2 if dmg_type in self.weaknesses else 1

    def dmg_to(self, squad):
        return self.effective_power * squad.dmg_factor(self.attack_type)


def parse_squad(line, group_type, id):
    n, hp, effects, ap, type, init = re.match(
        r'(\d+).*?(\d+)[^(]*(\(.*\))?.*? (\d+) (\w+) damage at initiative (\d+)',
        line).groups()
    if effects is not None:
        weak = re.search(r'weak to ([\w ,]+)', effects)
        im = re.search(r'immune to ([\w ,]+)', effects)
    else:
        weak = im = None
    weak = frozenset() if weak is None else frozenset(weak.group(1).split(', '))
    im = frozenset() if im is None else frozenset(im.group(1).split(', '))
    n, hp, ap, init = map(int, (n, hp, ap, init))
    return Squad(group_type, id, n, hp, im, weak, ap, type, init)


def parse(input):
    _, immune, infection = [x.strip() for x in re.split(r'Immune System:|Infection:', input)]

    good, bad = set(), set()
    for i, line in enumerate(immune.split('\n')):
        sq = parse_squad(line, Type.Immune, i + 1)
        good.add(sq)
    for i, line in enumerate(infection.split('\n')):
        sq = parse_squad(line, Type.Infection, i + 1)
        bad.add(sq)

    return good, bad


def targeting(attackers, targets):
    # target phase
    # by order of (epower, init), groups choose a target  (ignoring target hp)
    # target order is (do most dmg to, largest epower, init)
    targets = set(targets)
    fight = {}
    for attacker in sorted(attackers, key=lambda s: (s.effective_power, s.initiative), reverse=True):
        if len(targets) == 0:
            break
        target = max(targets, key=lambda t: (attacker.dmg_to(t), t.effective_power, t.initiative))
        if attacker.dmg_to(target) > 0:
            fight[attacker] = target
            targets.remove(target)

    return fight


def fighting(fight):
    combatants = set(fight.keys())

    any_killed = False
    for attacker in sorted(combatants, key=lambda s: s.initiative, reverse=True):
        if attacker.size == 0:
            continue
        target = fight[attacker]
        killed = attacker.dmg_to(target) // target.unit_hp
        if killed > 0:
            any_killed = True
        killed = min(killed, target.size)
        if DEBUG:
            print(
                f'{attacker.type} grp {attacker.id} attacks {target.type} grp {target.id} for ' +
                f'{attacker.dmg_to(target)} dmg, killing {killed} units')
        target.size -= killed

    return any_killed


DEBUG = False


def solve(good, bad, boost=0, p2=False):
    global DEBUG
    # make copies
    good = {replace(u, power=u.power + boost) for u in good}
    bad = {replace(u) for u in bad}

    i = 0
    while good and bad:
        fight = targeting(good, bad)
        fight.update(targeting(bad, good))
        if not fighting(fight):
            print(f'fighting produced no casualties!')
            print(f'boost {boost} causes stalemate')
            return 0
        i += 1
        good = {u for u in good if u.size > 0}
        bad = {u for u in bad if u.size > 0}

    if not p2:
        print(f'fighting ended after {i} rounds')
        print(f'{"infection" if bad else "immune"} won!')
        print(sum(u.size for u in good | bad))
    else:
        return sum(u.size for u in good)


with open('d24.txt', 'rt') as f:
    input = f.read().strip()

good, bad = parse(input)
# good, bad = parse(inp)
# solve(good, bad, 1570)
# exit(0)
import time

t = time.perf_counter()

print('part 1:')
solve(good, bad)

print()
print('part 2:')
solve(good, bad, 55)
# for boost in [55]:
#     left = solve(good, bad, boost, True)
#     if left > 0:
#         print(f'boost of {boost} left {left} units')
#         solve(good, bad, boost)
#         break

print(f'{time.perf_counter() - t}s')
