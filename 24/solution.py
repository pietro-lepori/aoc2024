

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

def fact_eval(facts, key):
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
	# isolate base facts
	base_facts = {}
	for k, v in facts.items():
		if k[0] in "xy":
			assert k[1:].isdigit()
			assert int(k[1:]) in range(n)
			continue
		if k[0] == 'z':
			assert k[1:].isdigit()
			assert int(k[1:]) in range(n + 1)
		assert isinstance(v, tuple)
		v = v[0], frozenset((v[1:]))
		base_facts[k] = v
	facts = base_facts
	print("size:", len(facts))
	print(*facts.items(), sep='\n', end="\n\n")
	# reverse
	stcaf = {}
	for k, v in facts.items():
		assert v not in stcaf
		stcaf[v] = k
#	nodes = sorted(facts)
#	requires = {x: [] for x in nodes}
#	for k, (_, args) in facts.items():
#		for a in args:
#			requires[k].append(a)
	# translate to right network
	missing = set()
	badset = set()
	rosetta = {}
	for i in range(n):
		key = f"S{i:02}"
		args = f"x{i:02}", f"y{i:02}"
		args = frozenset(args)
		value = ("XOR", args)
		try:
			rosetta[key] = stcaf[value]
		except KeyError:
			missing.add(key)
			print('!', key)
			for k, v in facts.items():
				if v[0] != 'XOR':
					continue
				if any(a in args for a in v[1]):
					print(k, v)
	for i in range(n):
		key = f"P{i:02}"
		args = f"x{i:02}", f"y{i:02}"
		args = frozenset(args)
		value = ("AND", args)
		try:
			rosetta[key] = stcaf[value]
		except KeyError:
			missing.add(key)
			print('!', key)
			for k, v in facts.items():
				if v[0] != 'AND':
					continue
				if any(a in args for a in v[1]):
					print(k, v)
	for i in range(1, n):
		key = f"z{i:02}"
		op, args = facts[key]
		a = rosetta.get(f"S{i:02}")
		key1 = f"C{i:02}"
		if op != 'XOR' or a not in args:
			missing.add(key1)
			badset.update({key})
			print("!", key, op, *args, a)
			continue
		b, c = args
		if c != a:
			b = c
		assert b != a
		rosetta[key1] = b
	for i in range(1, n):
		key = rosetta.get(f"C{i:02}")
		key1 = f"M{i - 1:02}"
		if key is not None:
			op, args = facts[key]
			a = rosetta.get(f"P{i:02}")
		if (key is None
		   or op != 'OR'
		   or a not in args
		   ):
			missing.add(key1)
			print("!", key1)
			if key:
				badset.update({key})
				print("!", key, op, *args, a)
			continue
		b, c = args
		if c != a:
			b = c
		assert b != a
		rosetta[key1] = b
	return
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
