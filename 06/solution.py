

def parse(filename):
	with open(filename) as f:
		lines = tuple(line.rstrip() for line in f)
	L = lines
	X = len(L)
	Y = len(L[0])
	assert all(Y == len(L[x]) for x in range(X))
	res = (L, X, Y)
	return res

def walk(L, start, step, block=None):
	# raises IndexError
	x, y = start
	dx, dy = step
	while True:
		x += dx
		y += dy
		if x < 0 or y < 0:
			yield None
			return
		try:
			c = L[x][y]
		except:
			yield None
			return
		if c == '#':
			return
		if block is not None and (x, y) == block:
			return
		yield x, y

def solver1(filename):
	L, X, Y = parse(filename)
	for x in range(X):
		y = L[x].find('^')
		if y == -1:
			continue
		start = x, y
		break
	dirs = ((-1,0), (0,1), (1,0), (0,-1))
	di = 0
	visited = {start}
	while True:
		step = dirs[di]
#		print(">", start, step)
		di += 1; di %= len(dirs)
		exited = False
		for pos in walk(L, start, step):
			if pos is None:
				exited = True
				break
			visited.add(pos)
		else:
			assert start != pos
			start = pos
		if exited:
			break
	res = len(visited)
	return res

def solver2(filename):
	L, X, Y = parse(filename)
	for x in range(X):
		y = L[x].find('^')
		if y == -1:
			continue
		start = x, y
		break
	dirs = ((-1,0), (0,1), (1,0), (0,-1))
	di = 0
	next_di = 1
	visited = {(start,di)}
	obstacles = set()
	while True:
		step = dirs[di]
		print(">", start, step)
		exited = False
		for pos in walk(L, start, step):
			if pos is None:
				exited = True
				break
			visited.add((pos, di))
			if (pos, next_di) in visited:
				x, y = pos
				dx, dy = step
				ox = x + dx
				oy = y + dy
				if ox not in range(X):
					continue
				if oy not in range(Y):
					continue
				obs = (x,y)
				obstacles.add(obs)
		else:
			assert start != pos
			start = pos
			di = next_di
			next_di = (di+1) % len(dirs)
			visited.add((start,di))
		if exited:
			break
	res = len(obstacles)
	return res

def solver2(filename):
	L, X, Y = parse(filename)
	for x in range(X):
		y = L[x].find('^')
		if y == -1:
			continue
		start = x, y
		break
	# get original path
	dirs = ((-1,0), (0,1), (1,0), (0,-1))
	di = 0
	restart = start
	visited = set()
	while True:
		step = dirs[di]
#		print(">", restart, step)
		di += 1; di %= len(dirs)
		exited = False
		for pos in walk(L, restart, step):
			if pos is None:
				exited = True
				break
			visited.add(pos)
		else:
			assert restart != pos
			restart = pos
		if exited:
			break
	# test all possible interferences
	res = sum(1
	          for block in visited
	          if does_loop(L, start, block))
	return res

def does_loop(L, start, block):
	dirs = ((-1,0), (0,1), (1,0), (0,-1))
	di = 0
	next_di = 1
	visited = {(start, di)}
	while True:
		step = dirs[di]
#		print(">", start, step, block)
		exited = False
		pos = start	# what if walk is empty?
		# TODO: adjust similar parts in other functions
		for pos in walk(L, start, step, block):
			if pos is None:
				exited = True
				break
			record = (pos, di)
			if record in visited:
				return True
			visited.add(record)
		else:
			start = pos
			di = next_di
			next_di = (di + 1) % len(dirs)
		if exited:
			break
	return False

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
#{k: v
#		         for line in f
#		         if print(line.rstrip(), flush=True) or line
#		         if print(line.split(), flush=True) or line
#		         for k, v in line.split()}
	return tests

def do_tests(tests, solver, verbose=False):
	for filename, ans in tests.items():
		if ans is None:
			continue
		value = str(solver(filename))
		ans = str(ans)
		res = (value == ans)
		if verbose:
			print("PASS" if res else "FAIL"
			, filename
			, f"{ans = } -- {value = }")
		yield res

if __name__ == "__main__":
	main()
