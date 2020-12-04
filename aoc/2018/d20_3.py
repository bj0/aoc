import networkx

graph = networkx.Graph()
x = y = 0
stack = []

for char in """^NNNNN(EEEEE|NNN)NNNNN$"""[1:-1]:
    if char == '(':
        stack.append((x, y))
    elif char == ')':
        x, y = stack.pop()
    elif char == '|':
        x, y = stack[-1]
    else:
        position = x, y
        x += (char == 'E') - (char == 'W')
        y += (char == 'S') - (char == 'N')
        graph.add_edge(position, (x, y))

distances = networkx.algorithms.shortest_path_length(graph, (0, 0))
print('ans (part 1): %d' % max(distances.values()))
print('ans (part 2): %d' % sum(value >= 1000 for value in distances.values()))