nodes = list("abcz")
adj = {
'a': ('b', 'z'),
'b': ('c', 'z'),
'c': ('z')}

counter = 0
def maximal_cliques(adj, nodes, partial=tuple()):
	# gives all the maximal cliques... and some more
	global counter
	call_id = counter
	counter += 1
	print(f"<{call_id}\t{nodes}\t{partial}")
	best = True
	l = list(nodes)
	while l:
		x = l.pop()
		assert (not partial) or x < partial[0]
		record = adj.get(x)
		s = set(record) if record is not None else set()
		if not all(y in s for y in partial):
			continue
		best = False
		new_partial = (x, *partial)
		new_nodes = l
		yield from maximal_cliques(adj, new_nodes, new_partial)
	if best:
		assert partial == tuple(sorted(partial))
		print('+', partial)
		yield partial
	print(f"{call_id}>")

res = list(maximal_cliques(adj, nodes))
print()
print(*res, sep='\n')
