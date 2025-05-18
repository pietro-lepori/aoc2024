

def parse(filename):
	with open(filename) as f:
		lines = tuple(line.rstrip() for line in f)
	requirements = []
	updates = []
	section = 0
	for k, line in enumerate(lines):
		if not line:
			section += 1
			continue
		if section == 0:
			a, b = map(int, line.split('|'))
			requirements.append((a,b))
		elif section == 1:
			pages = tuple(map(int, line.split(',')))
			updates.append(pages)
		else:
			assert False
	res = tuple(requirements), tuple(updates)
	return res

def update_is_sorted(pages, rules):
	res =  all((p1, p2) in rules
	           for k, p1 in enumerate(pages, 1)
	           for p2 in pages[k:])
	return res

def solver1(filename):
	requirements, updates = parse(filename)
	rules = set(requirements)
	res = 0
	for pages in updates:
		if not update_is_sorted(pages, rules):
			continue
		n = len(pages)
		assert n%2
		res += pages[n//2]
	return res

from functools import cmp_to_key

def update_sort(pages, rules):
	def cmp(p1, p2):
		if p1 == p2: return 0
		if (p1, p2) in rules: return 1
		if (p2, p1) in rules: return -1
		assert False
	return tuple(sorted(pages, key=cmp_to_key(cmp)))

def solver2(filename):
	requirements, updates = parse(filename)
	rules = set(requirements)
	res = 0
	for pages in updates:
		if update_is_sorted(pages, rules):
			continue
		pages = update_sort(pages, rules)
		n = len(pages)
		assert n%2
		res += pages[n//2]
	return res

def main():
	input_file = "input.txt"
	test1_file = "testlist1.txt"
	test2_file = "testlist2.txt"

	print("PART 1")
	solver = solver1
	tests = read_tests(test1_file)
#	tests = {"test1.txt" : 143}
	test_result = list(do_tests(tests, solver, verbose=True))
	if all(test_result):
		print("->", solver(input_file))

	print("PART 2")
	solver = solver2
	tests = read_tests(test2_file)
#	tests = {"test1.txt" : 123}
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
