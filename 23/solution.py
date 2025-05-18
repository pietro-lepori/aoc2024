

def parse(filename):
	with open(filename) as f:
		edges = tuple(line.rstrip().split('-') for line in f)
	adj = {}
	nodes = set()
	for a, b in edges:
		if b < a:
			a, b = b, a
		assert a < b
		nodes.add(a)
		nodes.add(b)
		l = adj.get(a)
		if l is None:
			l = []
			adj[a] = l
		l.append(b)
	new_adj = {}
	for k, l in adj.items():
		l.sort()
		t = tuple(l)
		s = frozenset(t)
		assert len(s) == len(t)
		new_adj[k] = (t, s)
	adj = new_adj
	return nodes, adj

def triplets(adj):
	for a, (t, _) in adj.items():
		n = len(t)
		for i, b in enumerate(t):
			record_b = adj.get(b)
			if record_b is None:
				continue
			s = record_b[1]
			for j in range(i + 1, n):
				c = t[j]
				if c in s:
					yield a, b, c

def solver1(filename):
	_, adj = parse(filename)
	if filename.startswith("test"):
		for t in triplets(adj):
			good = any(x[0] == 't' for x in t)
			print('+' if good else ' ', *t)
	res = sum(1
	          for t in triplets(adj)
	          if any(x[0] == 't' for x in t))
	return res

def maximal_cliques(adj, nodes, partial=tuple()):
	# gives all the maximal cliques... and some more
	best = True
	l = list(nodes)
	while l:
		x = l.pop()
#		assert (not partial) or x < partial[0]
		record = adj.get(x)
		s = record[1] if record is not None else set()
		if not all(y in s for y in partial):
			continue
		best = False
		new_partial = (x, *partial)
		new_nodes = l
		yield from maximal_cliques(adj, new_nodes, new_partial)
	if best:
#		assert partial == tuple(sorted(partial))
		yield partial

def solver2(filename):
	nodes, adj = parse(filename)
	nodes = tuple(sorted(nodes))
	res = max(maximal_cliques(adj, nodes), key=len)
	return ",".join(res)

def main():
	input_file = "input.txt"
	test1_file = "testlist1.txt"
	test2_file = "testlist2.txt"

	print("PART 1")
	solver = solver1
	tests = read_tests(test1_file)
	test_result = list(do_tests(tests, solver, verbose=True))
	if all(test_result):
		print("->", solver(input_file))

	print("PART 2")
	solver = solver2
	tests = read_tests(test2_file)
	test_result = list(do_tests(tests, solver, verbose=True))
	if all(test_result):
		print("->", solver(input_file))

def read_tests(filename):
	with open(filename) as f:
		tests = dict(line.split() for line in f)
	return tests

def do_tests(tests, solver, verbose=False):
	for filename, ans in tests.items():
		if ans is None:
			continue
		ans = str(ans)
		try:
			value = str(solver(filename))
		except:
			print("ERROR", filename, flush=True, end="\n\n")
			raise
		res = (value == ans)
		if verbose:
			print("PASS" if res else "FAIL"
			, filename
			, f"{ans = } -- {value = }")
		yield res

if __name__ == "__main__":
	main()
