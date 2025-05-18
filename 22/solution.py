

def parse(filename):
	with open(filename) as f:
		lines = tuple(int(line.rstrip()) for line in f)
	res = lines
	return res

def f(x, s):
	s ^= x
	s &= 16777215
	return s

def step(s):
	s = f(s << 6, s)
	s = f(s >> 5, s)
	s = f(s << 11, s)
	return s

def run(s):
	while True:
		yield s
		s = step(s)

def nth(s, n):
	for k, x in enumerate(run(s)):
		if k == n:
			return x

def solver1(filename):
	data = parse(filename)
	res = sum(nth(s, 2000) for s in data)
	return res

def buy(s, n = 2000):
	it = (int(str(x)[-1]) for x, _ in zip(run(s), range(n + 1)))
	k = []
	x = next(it)
	for _ in range(4):
		y = next(it)
		k.append(y - x)
		x = y
	k = tuple(k)
	res = {k: x}
	for y in it:
		k = (*k[1:], y - x)
		x = y
#		if n < 100:
#			print(k, x)
		if k not in res:
			res[k] = x
	return res


def solver2(filename):
	data = parse(filename)
	if filename.startswith("test"):
#		d = buy(123, 10)
		return sum(buy(s).get((-2,1,-1,3), 0) for s in data)
	data = [buy(s) for s in data]
	keys = set.union(*(set(d) for d in data))
	print("keys")
	res = max(sum(d.get(k, 0) for d in data) for k in keys)
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
