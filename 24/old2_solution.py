import z3

f_and = lambda x, y: x & y
f_or  = lambda x, y: x | y
f_xor = lambda x, y: x ^ y

op_decode = {
  "AND": f_and,
  "OR": f_or,
  "XOR": f_xor,
}

def parse(filename):
	with open(filename) as f:
		lines = tuple(line.rstrip() for line in f)
	facts = {}
	it = iter(lines)
	for line in it:
		if not line:
			break
		key, value = line.split(": ")
		value = bool(int(value))
		facts[key] = value
	else:
		assert False
	for line in it:
		value, key = line.split(" -> ")
		arg0, op, arg1 = value.split(" ")
		value = op, arg0, arg1
		facts[key] = value
	return facts

def fact_eval(facts, key, op_decode=op_decode):
	res_key = key
	stack = [key]
	while stack:
		key = stack[-1]
		value = facts[key]
		if not isinstance(value, tuple):
			stack.pop()
			continue
		op, *args = value
		unknown = [k
		           for k in args
		           if isinstance(facts[k], tuple)]
		if unknown:
			stack += unknown
			continue
		op = op_decode[op]
		args = [facts[k] for k in args]
		value = op(*args)
		facts[key] = value
		stack.pop()
	res = facts[res_key]
	return res

def solver1(filename):
	facts = parse(filename)
	print(*facts.items(), sep='\n', end="\n\n")
	res = sorted(var
	             for var in facts
	             if var[0] == 'z')
	res = [fact_eval(facts, var) for var in res]
	print(res)
	res = sum(b << n for n, b in enumerate(res))
	return res

def dependency(facts, key, memory):
	if key in memory:
		return memory[key]
	value = facts.get(key)
	if not isinstance(value, tuple):
		res = frozenset()
		memory[key] = res
		return res
	memory[key] = None
	children = frozenset(value[1:])
	descendants = [dependency(facts, k, memory)
	               for k in children]
	if any(x is None for x in descendants):
		res = None
		return res
	res = frozenset.union(children, *descendants)
	memory[key] = res
	return res

def solver2(filename):
	n = 45
	facts = parse(filename)
	assert all(f"{i}{j:02}" in facts
	           for i in "xyz"
	           for j in range(n))
	assert f"z{n:02}" in facts
	# isolate base facts for dependency analisys
	base_facts = {}
	for k, v in facts.items():
		if k[0] in "xy":
			assert k[1:].isdigit()
			assert int(k[1:]) in range(n)
			continue
		base_facts[k] = v
		if k[0] == 'z':
			assert k[1:].isdigit()
			assert int(k[1:]) in range(n + 1)
	print("size:", len(base_facts))
	print(*base_facts.items(), sep='\n', end="\n\n")
	base_dependency = {}
	for key in sorted(base_facts):
		l = len(dependency(facts, key, base_dependency))
		print(key, l)
	print()
	# find wrong output
	true_z = []
	carry = False
	for i in range(n):
		sx = f"x{i:02}"
		sy = f"y{i:02}"
		x = z3.Bool(sx)
		y = z3.Bool(sy)
		facts[sx] = x
		facts[sy] = y
		xpy = z3.Xor(x, y)
		w = z3.Xor(carry, xpy)
		true_z.append(w)
		carry = z3.Or(z3.And(x, y)
		             , z3.And(carry, xpy))
	true_z.append(carry)
	op_decode = {
	  "AND": z3.And,
	  "OR": z3.Or,
	  "XOR": z3.Xor,
	}
	wrong_bits = []
	s = z3.Solver()
	for i, w in enumerate(true_z):
		print(f"{i}...")
		sz = f"z{i:02}"
		z = fact_eval(facts, sz, op_decode)
		s.add(z != w)
		wrong = s.check()
		s.reset()
		assert wrong in (z3.sat, z3.unsat)
		if wrong == z3.sat:
			wrong_bits.append(sz)
			print("!", sz)
	print(base_dependency["z13"])
	# find possible swaps
	candidates = set(wrong_bits)
	candidates.update(*(base_dependency[b]
	                    for b in wrong_bits))
	print(len(candidates), "candidates")
	return None

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
