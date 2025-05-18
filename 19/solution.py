

def parse(filename):
	with open(filename) as f:
		lines = tuple(line.rstrip() for line in f)
	tokens = lines[0].split(", ")
	tokens.sort(key=len)
	assert not lines[1]
	targets = lines[2:]
	return tokens, targets

def constructible(s, tokens):
	stop = len(s)
	visited = set()
	front = [0]
	while front:
		k = front.pop()
		if k in visited:
			continue
		visited.add(k)
		for t in tokens:
			n = k + len(t)
			if n in visited:
				continue
			if s.startswith(t, k):
				if n == stop:
					return True
				front.append(n)
	return False

def solver1(filename):
	tokens, targets = parse(filename)
	res = sum(1 for s in targets if constructible(s, tokens))
	return res

def paths(s, tokens):
	lens = len(s)
	reaches = [[] for _ in s]
	for t in tokens:
		n = len(t)
		k = -1
		while True:
			k = s.find(t, k + 1)
			if k == -1:
				break
			reaches[k].append(k + n)
#	assert all(len(l) == len(set(l)) for l in reaches), str(reaches)
	res = [None] * (lens + 1)
	res[-1] = 1
	for k in reversed(range(lens)):
		res[k] = sum(res[j] for j in reaches[k])
	res = res[0]
	return res

def solver2(filename):
	tokens, targets = parse(filename)
	res = sum(paths(s, tokens) for s in targets)
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
