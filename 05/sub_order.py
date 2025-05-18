from collections import deque
from sys import argv

filename = argv[1] if len(argv) > 1 else "input.txt"

elements = set()
relation = []
updates = []
with open(filename) as f:
	it = iter(f)
	for line in it:
		line = line.rstrip()
		if not line:
			break
		a, b = map(int, line.split('|'))
		elements.add(a)
		elements.add(b)
		relation.append((a,b))
	for line in it:
		line = line.rstrip()
		line = tuple(map(int, line.split(',')))
		updates.append(line)
elements = tuple(sorted(elements))
relation = tuple(relation)
updates = tuple(updates)

adj = {x: [] for x in elements}
for x, y in relation:
	adj[x].append(y)

def reach(start, restricted=None):
	res = set()
	q = deque([start])
	while q:
		x = q.popleft()
		for y in adj[x]:
			if restricted is not None:
				if y not in restricted:
					continue
			if y in res:
				continue
			res.add(y)
			q.append(y)
	return res

def is_in_a_total_order(l):
	l = frozenset(l)
	for x in l:
		if x in reach(x, l):
			return False, x, x
	l = list(l)
	while l:
		x = l.pop()
		for y in l:
			if not ((x in adj[y]) or (y in adj[x])):
				return False, x, y
	return True,

counter = 0
for l in updates:
	ans, *bad = is_in_a_total_order(l)
	if not ans:
		print(f"the relation restricted on {l} is not a total order: {bad}")
		counter += 1
		x, y = bad
		if x != y:
			print('\t', x, adj[x])
			print('\t', y, adj[y])
print()
print(f"found {counter} / {len(updates)} exceptions")
