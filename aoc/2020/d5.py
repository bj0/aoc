from aocd import data

seats = data.splitlines()

seen = set()
for seat in seats:
    u, l = 0, 127
    for d in seat[:7]:
        c = (l - u) // 2 + u
        if d == "F":
            l = c
        else:
            u = c
    r = l

    u, l = 0, 7
    for d in seat[7:]:
        c = (l - u) // 2 + u
        if d == "L":
            l = c
        else:
            u = c
    c = l

    seen.add((r, c, r * 8 + c))

# 892
print(f"part 1: {max(seen, key=lambda x: x[2])}")

ids = [x[2] for x in seen]

all = {(r, c, r * 8 + c) for r in range(128) for c in range(8)}
missing = all - seen

# 625
print(f"part 2:{next(id for (r, c, id) in missing if id + 1 in ids and id - 1 in ids)}")

# trixy way

ids = [
    int(line.replace("F", "0").replace("B", "1").replace("L", "0").replace("R", "1"), 2)
    for line in data.splitlines()
]

print(f"p1: {max(ids)}")
print(f"p2: {next(i for i in range(min(ids), max(ids)) if i not in ids)}")
