

def parse(filename):
	with open(filename) as f:
		lines = tuple(line.rstrip() for line in f)
	res = lines
	return res

def solver1(filename):
	lines = parse(filename)
	ccs = []
	data_counter = 0
	cc_counter = 0
	for x, line in enumerate(lines):
		ccs_row = []
		ccs.append(ccs_row)
		for y, c in enumerate(line):
			connects = []
			for dx, dy in ((-1,0),(0,-1)):
				x1 = x + dx
				y1 = y + dy
				if x1 < 0 or y1 < 0:
					continue
				c1 = lines[x + dx][y + dy]
				if c == c1:
					cc1 = ccs[x1][y1]
					connects.append(cc1)
			len_connects = len(connects)
			if len_connects == 2:
				dp = 0
				cc, cc2 = connects
				if cc[0] is None:
					cc = cc[1]
				datum = cc[0]
				assert datum is not None
				if cc2[0] is None:
					cc2 = cc2[1]
				datum2 = cc2[0]
				assert datum2 is not None
				if datum[2] != datum2[2]:
					backlog = cc[1]
					backlog2 = cc2[1]
					datum[0] += datum2[0]
					datum[1] += datum2[1]
					cc2[0] = None
					cc2[1] = cc
					backlog.append(cc2)
					backlog += backlog2
					for cc3 in backlog2:
						cc3[1] = cc
			elif len_connects == 1:
				dp = 2
				cc = connects[0]
				if cc[0] is None:
					cc = cc[1]
				datum = cc[0]
				assert datum is not None
			elif len_connects == 0:
				dp = 4
				datum = [0, 0, data_counter]
				data_counter += 1
				# schema: datum, overwrites, id
				# schema: None, refers to, id
				cc = [datum, [], cc_counter]
				cc_counter += 1
			else:
				assert False
			datum[0] += 1	# area
			datum[1] += dp	# perimeter
			if False and filename == "test5.txt":
				print(x, y, datum, cc)
			ccs_row.append(cc)
	data = {}
	for row in ccs:
		for cc in row:
			datum = cc[0]
			if datum is not None:
				data[datum[2]] = datum
	if False and filename == "test5.txt":
		print()
		print(*data.values(), sep='\n')
	res = sum(d[0] * d[1] for d in data.values())
	return res

def solver2(filename):
	lines = parse(filename)
	ccs = []
	data_counter = 0
	cc_counter = 0
	for x, line in enumerate(lines):
		ccs_row = []
		ccs.append(ccs_row)
		for y, c in enumerate(line):
			connects = []
			for dx, dy in ((-1,-1),(-1,0),(-1,1),(0,-1)):
				x1 = x + dx
				y1 = y + dy
				if x1 < 0 or y1 < 0:
					connects.append(False)
					continue
				try:
					c1 = lines[x1][y1]
				except IndexError:
					connects.append(False)
					continue
				connects.append(c == c1)
			cc1 = ccs[x - 1][y] if connects[1] else None
			cc2 = ccs[x][y - 1] if connects[3] else None
			if cc1 is None and cc2 is None:
				ds = 4
				# schema: area, sides, id
				datum = [0, 0, data_counter]
				data_counter += 1
				# schema: datum, overwrites, id
				# schema: None, refers to, id
				cc = [datum, [], cc_counter]
				cc_counter += 1
			elif cc1 is not None and cc2 is not None:
				ds = 0 if connects[2] else -2
				cc = cc1
				if cc[0] is None:
					cc = cc[1]
				datum = cc[0]
				assert datum is not None
				if cc2[0] is None:
					cc2 = cc2[1]
				datum2 = cc2[0]
				assert datum2 is not None
				if datum[2] != datum2[2]:
					backlog = cc[1]
					backlog2 = cc2[1]
					datum[0] += datum2[0]
					datum[1] += datum2[1]
					cc2[0] = None
					cc2[1] = cc
					backlog.append(cc2)
					backlog += backlog2
					for cc3 in backlog2:
						cc3[1] = cc
			elif cc1 is None:
				assert cc2 is not None
				ds = 2 if connects[0] else 0
				cc = cc2
				if cc[0] is None:
					cc = cc[1]
				datum = cc[0]
				assert datum is not None
			else:
				assert cc1 is not None
				assert cc2 is None
				ds = connects[0] + connects[2]
				ds *= 2
				cc = cc1
				if cc[0] is None:
					cc = cc[1]
				datum = cc[0]
				assert datum is not None
			datum[0] += 1	# area
			datum[1] += ds	# sides
			if False and filename == "test5.txt":
				print(x, y, datum, cc)
			ccs_row.append(cc)
	data = {}
	for row in ccs:
		for cc in row:
			datum = cc[0]
			if datum is not None:
				data[datum[2]] = datum
	if False and filename == "test5.txt":
		print()
		print(*data.values(), sep='\n')
	res = sum(d[0] * d[1] for d in data.values())
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
