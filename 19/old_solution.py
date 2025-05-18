

dec = "wubrgX"	# X is end of pattern
enc = {c : i for i, c in enumerate(dec)}

def trie_init(l):
	assert isinstance(l, list)
	assert not l
	for _ in dec:
		l.append([])

def trie_add(trie, s):
	for c in s:
		l = trie[enc[c]]
		if not l:
			trie_init(l)
		trie = l
	l = trie[-1]
	if not l:
		trie_init(l)

def trie_print(trie, path=None):
	if not trie:
		return
	path = [] if path is None else path
	l = list(map(int, map(bool, trie)))
	print("".join(path), l, sep='\t')
	for k, good in enumerate(l[:-1]):
		if not good:
			continue
		new_path = path[:]
		new_path.append(dec[k])
		trie_print(trie[k], new_path)

def parse(filename):
	with open(filename) as f:
		lines = tuple(line.rstrip() for line in f)
	tokens = []
	trie_init(tokens)
	for towel in lines[0].split(", "):
		trie_add(tokens, towel)
	assert not lines[1]
	targets = lines[2:]
	return tokens, targets

def decompose(trie, target, pieces=None, verbose=False):
	pieces = [] if pieces is None else pieces
	base_trie = trie
	target = list(reversed(target))
	stack = []
	stack.append((target, pieces))
	while stack:
		target, pieces = stack.pop()
		if verbose or True:
			print("start".upper(), repr("".join(reversed(target))), pieces, sep='\t')
		path = []
		trie = base_trie
		while trie:
			if not target:
				if trie[-1]:
					pieces = tuple(pieces)
					if verbose:
						print("end+", pieces)
					yield pieces
				else:
					if verbose:
						print("end-", "".join(path))
				break
			if trie[-1]:
				assert path
				token = "".join(path)
				if verbose or True:
					print("found", token, pieces, sep='\t')
				new_pieces = pieces[:]
				new_pieces.append(token)
				new_target = target[:]
				stack.append((new_target, new_pieces))
			c = target.pop()
			path.append(c)
			k = enc[c]
			trie = trie[k]
		if verbose:
			print("end-", "".join(path))

def solver1(filename):
	verbose = filename.startswith("test")
#	verbose = True
	tokens, targets = parse(filename)
	if verbose:
		print(dec)
		trie_print(tokens)
		print(targets)
	res = 0
	for pattern in targets:
		print("?", pattern)
		it = decompose(tokens, pattern, verbose=verbose)
		for pieces in it:
			res += 1
			break
	return res

def solver2(filename):
	data = parse(filename)
	res = None
	return res

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
