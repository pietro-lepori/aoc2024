

def parse(filename):
	with open(filename) as f:
		lines = tuple(line.rstrip() for line in f)
	res = tuple(map(int, lines[0].split()))
	return res

def f(n, x, memory={}):
	if n == 0:
		return 1
	if n < 0:
		assert False
	t = (n, x)
	if t in memory:
		return memory[t]
	s = str(x)
	if x == 0:
		l = [1]
	elif len(s) % 2 == 0:
		h = len(s) // 2
		l = [s[:h], s[h:]]
		l = list(map(int, l))
	else:
		l = [x * 2024]
	res = sum(f(n - 1, y) for y in l)
	memory[t] = res
#	print(t, res)
	return res

def solver1(filename):
	data = parse(filename)
	res = sum(f(25, x) for x in data)
	return res

def solver2(filename):
	data = parse(filename)
	res = sum(f(75, x) for x in data)
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
#	tests = read_tests(test2_file)
	tests = {}
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
