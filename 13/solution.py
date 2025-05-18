from math import gcd

def parse(filename):
	with open(filename) as f:
		lines = tuple(line.rstrip() for line in f)
	pref1 = len("Button A: ")
	pref2 = len("Prize: ")
	res = []
	for i in range(0, len(lines), 4):
		# buttons
		a = []
		for j in range(2):
			line = lines[i + j]
			line = line[pref1:]
			x, y = line.split(", ")
			x = int(x[2:])
			y = int(y[2:])
			a.append((x,y))
		a = tuple(a)
		# prize
		line = lines[i + 2]
		line = line[pref2:]
		x, y = line.split(", ")
		x = int(x[2:])
		y = int(y[2:])
		b = (x, y)
		# save
		res.append((a,b))
	res = tuple(res)
	return res

def egcd(x, y):
	assert x >= 0
	assert y >= 0
	if x < y:
		d, a, b = egcd(y, x)
		return d, b, a
	if not y:
		return x, 1, 0
	q, r = divmod(x, y)	# x = q*y + r
	d, a0, b0 = egcd(y, r)	# d = a0*y + b0*r
	# d = a0*y + b0*(x - q*y)
	a = b0
	b = a0 - (q * b0)
	assert d == a * x + b * y, f"{x=} {y=} {a=} {b=} ({r=} {a0=} {b0=})"
	return d, a, b

def dot(v, w):
	return (v[0] * w[0]) + (v[1] * w[1])

def minwin(a, b, cost0=3, cost1=1):
	# returns min. cost, moves or None
	if b == (0, 0):
		return 0, (0, 0)
	a0 = a[0]
	a1 = a[1]
	del a
	if a0 == (0, 0):
		if a1 == (0, 0):
			return None
		else:
			a0, a1 = a1, a0
			cost0, cost1 = cost1, cost0
	if a1 == (0, 0):
		xa, ya = a0
		xb, yb = b
		if xa:
			z, r = divmod(xb, xa)
			if yb != z * ya:
				return None
		else:
			assert ya
			z, r = divmod(yb, ya)
			if xb:
				return None
		if r:
			return None
		return z * cost0, (z, 0)
	det = (a0[0] * a1[1]) - (a1[0] * a0[1])
	if det:
		# inverse
		r0 = (a1[1], - a1[0])
		r1 = (- a0[1], a0[0])
		x = dot(r0, b)
		y = dot(r1, b)
		x, r = divmod(x, det)
		if r:
			return None
		y, r = divmod(y, det)
		if r:
			return None
		cost = x * cost0 + y * cost1
		return cost, (x, y)
	print(end='.')
	x0, y0 = a0
	x1, y1 = a1
	xb, yb = b
	n0 = x0 + y0
	n1 = x1 + y1
	nb = xb + yb
	nc, s, t = egcd(n0, n1)
	q, r = divmod(nb, nc)
	if r:
		return None
	delta = (cost0 * n1 - cost1 * n0) // nc
	# nb = q * n0 = q * (s * n0 + t * n1)
	# s' = s + (n1 // nc) * z
	# t' = t - (n0 // nc) * z
	# cost = cost0 * q * s' + cost1 * q * t'
	# cost = q * (cost0 * s + cost1 * t + delta * z)
	# s' >= 0 then z >= - (nc * s) / n1
	# t' >= 0 then z <= (nc * t) / n0
	if delta > 0:
		z, r = divmod(-nc * s, n1)
		if r:
			z += 1
	else:
		z = (nc * t) // n0
	x = q * (s + (n1 // nc) * z)
	y = q * (t - (n0 // nc) * z)
	assert x >= 0
	assert y >= 0
	assert nb == x * n0 + y * n1
	assert xb == x * x0 + y * x1
	assert yb == x * y0 + y * y1
	cost = x * cost0 + y * cost1
	return cost, (x, y)

def solver1(filename):
	res = 0
	for a, b in parse(filename):
		t = minwin(a, b)
		if t is None:
			continue
		cost, (x, y) = t
		assert x <= 100
		assert y <= 100
		res += cost
	return res

def solver2(filename):
	res = 0
	for a, b in parse(filename):
		b = tuple(10000000000000 + n for n in b)
		t = minwin(a, b)
		if t is None:
			continue
		cost, (x, y) = t
		res += cost
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
