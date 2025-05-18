import heapq

directions = ((0, 1), (0, -1), (1, 0), (-1, 0))

def parse(filename):
	with open(filename) as f:
		lines = tuple(line.rstrip() for line in f)
	maze = {}
	for x, line in enumerate(lines):
		for y, c in enumerate(line):
			t = (x, y)
			if c == 'S':
				start = t
				c = '.'
			elif c == 'E':
				stop = t
				c = '.'
			pass
			if c == '.':
				maze[t] = []	# neighbours
			elif c == '#':
				pass
			else:
				assert False
	for (x, y), neighbours in maze.items():
		for dx, dy in directions:
			xx = x + dx
			yy = y + dy
			t = (xx, yy)
			if t in maze:
				neighbours.append(t)
	return maze, start, stop

def solver1(filename):
	maze, start, stop = parse(filename)
	assert all(len(l) in range(1,5) for l in maze.values())
	# remove close ends
	bad = [(t, l[0])
	       for t, l in maze.items()
	       if len(l) == 1 and t != start and t != stop]
	while bad:
		k, t = bad.pop()
		del maze[k]
		l = [tt for tt in maze[t] if tt != k]
		maze[t] = l
		if len(l) == 1 and t != start and t != stop:
			bad.append((t, l[0]))
	# change values schema: {direction: destination}
	new_maze = {}
	for t, l in maze.items():
		x, y = t
		v = {}
		for tt in l:
			xx, yy = tt
			dx = xx - x
			dy = yy - y
			v[(dx, dy)] = tt
		new_maze[t] = v
	maze = new_maze
	# Dijkstra
	visited = set()	# {(position, direction)}
	front = [(0, start, (0, 1))]	# [(cost, position, direction)], heapq
	res = None
	while front:
		cost, t, d = front[0]
		if t == stop:
			res = cost
			break
		if (t, d) in visited:
			heapq.heappop(front)
			continue
		popped = False
		tt = maze[t].get(d)
		if tt is not None:
			record = (cost + 1, tt, d)
			heapq.heapreplace(front, record)
			popped = True
		dx, dy = d
		if dx:
			assert dy == 0
			rotated = ((0, 1), (0, -1))
		else:
			assert dy
			rotated = ((1, 0), (-1, 0))
		for dd in rotated:
			if (t, dd) in visited:
				continue
			record = (cost + 1000, t, dd)
			if popped:
				heapq.heappush(front, record)
			else:
				heapq.heapreplace(front, record)
				popped = True
		if not popped:
			heapq.heappop(front)
		visited.add((t, d))
	return res

def solver2(filename):
	maze, start, stop = parse(filename)
	assert all(len(l) in range(1,5) for l in maze.values())
	# remove close ends
	bad = [(t, l[0])
	       for t, l in maze.items()
	       if len(l) == 1 and t != start and t != stop]
	while bad:
		k, t = bad.pop()
		del maze[k]
		l = [tt for tt in maze[t] if tt != k]
		maze[t] = l
		if len(l) == 1 and t != start and t != stop:
			bad.append((t, l[0]))
	# change values schema: {direction: destination}
	new_maze = {}
	for t, l in maze.items():
		x, y = t
		v = {}
		for tt in l:
			xx, yy = tt
			dx = xx - x
			dy = yy - y
			v[(dx, dy)] = tt
		new_maze[t] = v
	maze = new_maze
	# Dijkstra
	visited = {}	# {(position, direction): (cost, {parents})}
	front = [(0, start, (0, 1), None)]	# [(cost, position, direction, origin)], heapq
	stop_limit = None
	while front:
		cost, t, d, origin = front[0]
		old_visit = visited.get((t, d))
		if old_visit is not None:
			assert origin is not None
			old_cost, parents = old_visit
			if cost == old_cost:
				parents.add(origin)
			else:
				assert cost > old_cost
			heapq.heappop(front)
			continue
		if stop_limit is None:
			if t == stop:
				stop_limit = cost
		elif cost > stop_limit:
			break
		popped = False
		tt = maze[t].get(d)
		if tt is not None:
			record = (cost + 1, tt, d, (t, d))
			heapq.heapreplace(front, record)
			popped = True
		dx, dy = d
		if dx:
			assert dy == 0
			rotated = ((0, 1), (0, -1))
		else:
			assert dy
			rotated = ((1, 0), (-1, 0))
		for dd in rotated:
			if (t, dd) in visited:
				continue
			record = (cost + 1000, t, dd, (t, d))
			if popped:
				heapq.heappush(front, record)
			else:
				heapq.heapreplace(front, record)
				popped = True
		if not popped:
			heapq.heappop(front)
		parents = {origin} if origin is not None else set()
		visited[(t, d)] = (cost, parents)
	# find paths
	res = set()
	front = set.union(*(visit[1]
	                    for d in directions
	                    if (visit := visited.get((stop, d))) is not None))
	while front:
		k = front.pop()
		res.add(k)
		parents = visited[k][1]
		for kk in parents:
			assert kk != k
			if kk in res:
				continue
			front.add(kk)
	res = {t for t, _ in res}
	res.add(stop)
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
