from itertools import product

X, Y, T = 71, 71, 1024
directions = ((0, 1), (0, -1), (1, 0), (-1, 0))


def parse(filename, memory = {}):
	res = memory.get(filename)
	if res is not None:
		return res
	with open(filename) as f:
		lines = tuple(line.rstrip() for line in f)
	res = tuple(tuple(map(int, line.split(','))) for line in lines)
	assert all(len(t) == 2 for t in res)
	memory[filename] = res
	return res

def solver1(filename):
	data = parse(filename)
	corrupted = set(data[:T])
#	for y in range(Y):
#		for x in range(X):
#			c = '#' if (x, y) in corrupted else '.'
#			print(c, end='')
#		print()
#	print()
	start = (0, 0)
	stop = (X - 1, Y - 1)
	print(T, len(corrupted), len(data), start, stop)
	# flood
	steps = 0
	visited = {}
	front = {start}
	while front:
		visited.update(product(front, (steps,)))
		if stop in front:
			break
		new_front = set()
		for t, d in product(front, directions):
			x = t[0] + d[0]
			y = t[1] + d[1]
			if x not in range(X):
				continue
			if y not in range(Y):
				continue
			tt = (x, y)
			if tt in visited:
				continue
			if tt in corrupted:
				continue
			new_front.add(tt)
		front = new_front
		steps += 1
	else:
		return None
	res = steps
	for y in range(Y):
		for x in range(X):
			t = (x, y)
			c = '#' if t in corrupted else '.'
			c1 = visited.get(t)
			if c1 is not None:
				c = str(c1)[-1]
			print(c, end='')
		print()
	print()
	return res

def solver2(filename):
	global T
	T1 = T
	data = parse(filename)
	start = 0
	stop  = len(data)
	while start < stop - 1:
		T = (start + stop) // 2
		print(f"{start=} {T=} {stop=}")
		ans = solver1(filename)
		if ans is None:
			stop = T
		else:
			start = T
	assert stop == start + 1
	res = data[start]
	print(data[start-2:start+3])
	res = ','.join(map(str, res))
	T = T1
	return res

def main():
	input_file = "input.txt"
	test1_file = "testlist1.txt"
	test2_file = "testlist2.txt"

	print("PART 1")
	solver = solver1
	tests = read_tests(test1_file)
	global X, Y, T
	X1, Y1, T1 = X, Y, T
	X, Y, T = 7, 7, 12
	test_result = list(do_tests(tests, solver, verbose=True))
	X, Y, T = X1, Y1, T1
	if all(test_result):
		print("->", solver(input_file))

	print("PART 2")
	solver = solver2
	tests = read_tests(test2_file)
	X1, Y1, T1 = X, Y, T
	X, Y, T = 7, 7, 12
	test_result = list(do_tests(tests, solver, verbose=True))
	X, Y, T = X1, Y1, T1
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
