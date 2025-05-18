from itertools import product

def parse(filename):
	with open(filename) as f:
		lines = tuple(line.rstrip() for line in f)
	res = []
	for line in lines:
		row = []
		res.append(row)
		for c in line:
			row.append([int(c), set()])
	return res

def solver1(filename):
	data = parse(filename)
	res = 0
	for h in range(9,-1,-1):
		for x, row in enumerate(data):
			for y, l in enumerate(row):
				v = l[0]
				if v != h:
					continue
				if h == 9:
					l[1] = {(x,y)}
					continue
				for dx, dy in ((0,1),(0,-1),(1,0),(-1,0)):
					xx = x + dx
					yy = y + dy
					if xx < 0 or yy < 0:
						continue
					try:
						v, tail_reach = data[xx][yy]
					except IndexError:
						continue
					if v == h + 1:
						l[1].update(tail_reach)
				if h == 0:
					res += len(l[1])
	return res

def solver2(filename):
	data = parse(filename)
	res = 0
	for h in range(9,-1,-1):
		for x, row in enumerate(data):
			for y, l in enumerate(row):
				v = l[0]
				l[1] = l[1] if l[1] else 0
				if v != h:
					continue
				if h == 9:
#					l[1] = {(x,y): 1}
					l[1] = 1
					continue
				for dx, dy in ((0,1),(0,-1),(1,0),(-1,0)):
					xx = x + dx
					yy = y + dy
					if xx < 0 or yy < 0:
						continue
					try:
						v, tail_reach = data[xx][yy]
					except IndexError:
						continue
					if v == h + 1:
						l[1] += tail_reach
#						for end in tail_reach:
#							if end in l[1]:
#								l[1][end] += tail_reach[end]
#							else:
#								l[1][end] = tail_reach[end]
				if h == 0:
					res += l[1]
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
