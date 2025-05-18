

def parse(filename):
	with open(filename) as f:
		lines = tuple(line.rstrip() for line in f)
	grid = []
	for x, line in enumerate(lines):
		if not line:
			restart = x + 1
			break
		row = list(line)
		grid.append(row)
		if x:
			assert len(row) == len(grid[0])
	cmd = "".join(lines[restart:])
	return grid, cmd

def gps(x, y):
	return 100 * x + y

def solver1(filename):
	grid, cmd = parse(filename)
	X = len(grid)
	Y = len(grid[0])
#	uplimit = []
#	for y in range(Y):
#		for x in range(X):
#			if grid[x][y] != '.':
#				continue
#			assert x
#			uplimit.append(x)
#	downlimit = []
#	for y in range(Y):
#		for x in range(X, -1, -1):
#			if grid[x][y] != '.':
#				continue
#			assert x
#			downlimit.append(x)
#	leftlimit = []
#	for x in range(X):
#		for y in range(Y):
#			if grid[x][y] != '.':
#				continue
#			assert y
#			leftlimit.append(y)
#	rightlimit = []
#	for x in range(X):
#		for y in range(Y, -1, -1):
#			if grid[x][y] != '.':
#				continue
#			assert y
#			rightlimit.append(y)
	if filename.startswith("test1"):
		for row in grid:
			print("".join(row))
	x = None
	y = None
	for i, row in enumerate(grid):
		for j, c in enumerate(row):
			if c != "@":
				continue
			x, y = i, j
			break
#	grid[x][y] = '.'
	decode = {
	'<': (0, -1),
	'>': (0, +1),
	'^': (-1, 0),
	'v': (+1, 0),
	}
	for a in cmd:
		dx, dy = decode[a]
		xx = x + dx
		yy = y + dy
		good = True
		while (c := grid[xx][yy]) != '#':
			if c == '.':
				break
			xx += dx
			yy += dy
		else:
			continue
		assert grid[xx][yy] == '.'
		if dx:
			assert dy == 0
			assert y == yy
			for i in range(xx, x, -dx):
				grid[i][y] = grid[i - dx][y]
		if dy:
			assert dx == 0
			assert x == xx
			for j in range(yy, y, -dy):
				grid[x][j] = grid[x][j - dy]
		grid[x][y] = '.'
		x += dx
		y += dy
		if filename.startswith("test1"):
			print(f"\n{a}")
			for row in grid:
				print("".join(row))
	res = 0
	for x in range(X):
		row = grid[x]
		for y in range(Y):
			if row[y] == 'O':
				res += gps(x, y)
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
		value = str(solver(filename))
		res = (value == ans)
		if verbose:
			print("PASS" if res else "FAIL"
			, filename
			, f"{ans = } -- {value = }")
		yield res

if __name__ == "__main__":
	main()
