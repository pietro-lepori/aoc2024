from collections import deque
from sys import argv

filename = argv[1] if len(argv) > 1 else "input.txt"

relation = []
elements = set()
with open(filename) as f:
	for line in f:
		line = line.rstrip()
		if not line:
			break
		a, b = map(int, line.split('|'))
		elements.add(a)
		elements.add(b)
		relation.append((a,b))
elements = sorted(elements)

adj = {x: [] for x in elements}
for x, y in relation:
	adj[x].append(y)

def reach(start):
	res = set()
	q = deque([start])
	while q:
		x = q.popleft()
		for y in adj[x]:
			if y in res: continue
			res.add(y)
			q.append(y)
	return res

print(f"{elements = }")
counter = 0
for x in elements:
	if x in reach(x):
		print(f"{x} is in a cycle")
		counter += 1
print()
print(f"{counter} / {len(elements)} are in a cycle")
