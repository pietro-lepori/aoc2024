import heapq

def parse(filename):
	with open(filename) as f:
		lines = tuple(line.rstrip() for line in f)
	assert len(lines) == 1
	line = lines[0]
	free = []
	files = []
	position = 0
	for j, c in enumerate(line):
		size = int(c)
		start = position
		position += size
		t = (start, size)
		if j & 1:
			free.append(t)
		else:
			files.append(t)
	return free, files

def checksum(start, size, file_id):
	res = 2 * start
	res += size - 1
	res *= size
	res //= 2
	res *= file_id
	return res

def solver1(filename):
	free, files = parse(filename)
	free.reverse()
	res = 0
	space = 0
	size = 0
	while True:
		if not space:
			while free:
				start_free, space = free.pop()
				if space:
					break
			else:
				break
		if not size:
			while files:
				start_file, size = files.pop()
				file_id = len(files)
				if size:
					break
			else:
				break
		if start_file < start_free:
			assert file_id == len(files)
			t = start_file, size
			files.append(t)
			break
		k = min(size, space)
		block_checksum = checksum(start_free, k, file_id)
#		print((start_file, size), (start_free, space), file_id, k, block_checksum)
		res += block_checksum
		size -= k
		start_free += k
		space -= k
	file_id = len(files)
	while files:
		start, size = files.pop()
		file_id -= 1
		block_checksum = checksum(start, size, file_id)
		res += block_checksum
	return res

def solver2(filename):
	free, files = parse(filename)
	new_free = [[] for _ in range(10)]
	new_free[0] = None
	for start, size in free:
		if not size:
			continue
		new_free[size].append(start)
	free = new_free
	for k in range(1, 10):
		heapq.heapify(free[k])
	res = 0
	file_id = len(files)
	while files:
		start_file, size = files.pop()
		file_id -= 1
#		print('<', file_id, size, start_file)
		start_free, space = min((
		  (start, k)
		  for k in range(size, 10)
		  if (h := free[k])
		  if (start := h[0]) < start_file
		), default=(None, 0))
		if space:
#			print('-', space, start_free)
			heapq.heappop(free[space])
		else:
#			print('>', file_id, size, start_file)
			res += checksum(start_file, size, file_id)
			continue
#		print('>', file_id, size, start_free)
		res += checksum(start_free, size, file_id)
		space -= size
		if not space:
			continue
		start_free += size
#		print('+', space, start_free)
		h = free[space]
		heapq.heappush(h, start_free)
#	return
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
