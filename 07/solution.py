

def parse(filename):
	res = []
	with open(filename) as f:
		for line in f:
			y, xs = line.split(':')
			y = int(y)
			xs = tuple(map(int, xs.split()))
			res.append((y, xs))
	res = tuple(res)
	return res

def concat_div_old(y, x):
	x = str(x)
	y = str(y)
	if y.endswith(x):
		if x == y:
			return ""
		return int(y[:-len(x)])
	return None

def concat_div(y, x):
	if y < 10:
		return None
	if x == 0:
		q, r = divmod(y, 10)
		return None if r else q
	d = y - x
	if d < 0:
		return None
	e = 0
	tmp = x
	while tmp:
		tmp //= 10
		e += 1
#	assert e == len(str(x)), f"{x} ({e = })"
	p, r = divmod(d, 10**e)
	if r:
		return None
#	assert y == p * 10**e + x
	return p

def is_valid(y, xs, concat=False, verbose=False):
	assert xs
	x = xs[-1]
	xs = xs[:-1]
	if not xs:
		return x == y
	if concat:
		p = concat_div(y, x)
		if not p:
			con_route = False
		else:
			con_route = is_valid(p, xs, concat)
		if con_route:
			return True
	q, r = divmod(y, x)
	if r:
		mul_route = False
	else:
		mul_route = is_valid(q, xs, concat)
	if mul_route:
#		print(mul_route, y, x, xs)
		return True
	d = y - x
	if d < 0:
		add_route = False
	else:
		add_route = is_valid(d, xs, concat)
#	print(add_route, mul_route, y, x, xs)
	return add_route

def solver1(filename):
	data = parse(filename)
#	print(*data, sep='\n')
#	print("---")
	res = sum(y for y, xs in data if is_valid(y, xs))
	return res

def solver2(filename):
	data = parse(filename)
	res = sum(y for y, xs in data if is_valid(y, xs, concat=True, verbose=True))
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
