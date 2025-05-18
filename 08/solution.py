from itertools import product, count

def parse(filename):
	with open(filename) as f:
		lines = tuple(line.rstrip() for line in f)
	X = len(lines)
	Y = len(lines[0])
	ants = {}
	for x, line in enumerate(lines):
		assert len(line) == Y
		for y, c in enumerate(line):
			if c == '.':
				continue
			coo = (x,y)
			if c not in ants:
				ants[c] = [coo]
			else:
				ants[c].append(coo)
	for k in ants:
		ants[k] = tuple(ants[k])
	res = (X, Y, ants)
	return res

def solver1(filename):
	X, Y, ants = parse(filename)
	res = set()
	for l in ants.values():
		for a0, a1 in product(l, repeat=2):
			if a0 == a1:
				continue
			x0, y0 = a0
			x1, y1 = a1
			x = x0 + (x0 - x1)
			y = y0 + (y0 - y1)
			if x not in range(X):
				continue
			if y not in range(Y):
				continue
			res.add((x,y))
	res = len(res)
	return res

def solver2(filename):
	X, Y, ants = parse(filename)
	res = set()
	for l in ants.values():
		for a0, a1 in product(l, repeat=2):
			if a0 == a1:
				continue
			x0, y0 = a0
			x1, y1 = a1
			for k in count():
				x = x0 + (k * (x0 - x1))
				y = y0 + (k * (y0 - y1))
				if x not in range(X):
					break
				if y not in range(Y):
					break
				res.add((x,y))
	res = len(res)
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
		value = str(solver(filename))
		res = (value == ans)
		if verbose:
			print("PASS" if res else "FAIL"
			, filename
			, f"{ans = } -- {value = }")
		yield res

if __name__ == "__main__":
	main()
