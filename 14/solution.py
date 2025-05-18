from itertools import product

Y = 101
X = 103

def parse(filename):
	with open(filename) as f:
		lines = tuple(line.rstrip() for line in f)
	res = []
	for line in lines:
		p, v = line.split()
		p = tuple(map(int, p[2:].split(',')))
		v = tuple(map(int, v[2:].split(',')))
		res.append((p,v))
	return tuple(res)

def sim(p, v, t):
	x, y = p
	dx, dy = v
	x += t * dx
	x %= X
	y += t * dy
	y %= Y
#	print(x, y, sep='\t')
	return x, y

def solver1(filename):
	if filename == "test1.txt" and False:
		p, v = (2,4), (2,-3)
		for t in range(6):
			p1 = sim(p, v, t)
			print(t, p1)
	mx = X // 2
	my = Y // 2
	q1, q2, q3, q4 = [0] * 4
	for p, v in parse(filename):
		x, y = sim(p, v, 100)
		if x < mx and y < my:
			q1 += 1
		if x > mx and y < my:
			q2 += 1
		if x < mx and y > my:
			q3 += 1
		if x > mx and y > my:
			q4 += 1
	res = q1 * q2 * q3 * q4
	return res

def show(figure):
	for y in range(Y):
		for x in range(X):
			if (x, y) in figure:
				print('#', end='')
			else:
				print(' ', end='')
		print()

def solver2(filename):
	data = parse(filename)
	for t in range(101*103):
		figure = set()
		for p, v in data:
			p1 = sim(p, v, t)
			figure.add(p1)
		goods = 0
		for x, y in figure:
			nei = 0
			for dx, dy in product(range(-1,2), repeat=2):
				if dx == 0 and dy == 0:
					continue
				if (x + dx, y + dy) in figure:
					nei += 1
			if nei >= 2:
				goods += 1
		if goods >= len(figure) // 2:
			print(t)
			show(figure)
			print()
	res = None
	return res

def main():
	input_file = "input.txt"
	test1_file = "testlist1.txt"
	test2_file = "testlist2.txt"

	global X, Y

	print("PART 1")
	solver = solver1
	tests = read_tests(test1_file)
	X = 11
	Y = 7
	test_result = list(do_tests(tests, solver, verbose=True))
	X = 101
	Y = 103
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
