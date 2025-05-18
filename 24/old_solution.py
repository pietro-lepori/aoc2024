import z3

f_and = lambda x, y: x & y
f_or  = lambda x, y: x ^ y ^ (x & y)
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

class BMono:
	def __init__(self, vars):
		vars = frozenset(vars)
		assert all(isinstance(v, str) for v in vars)
		self._value = vars
	def __eq__(self, other):
		if type(self) != type(other):
			return False
		return self._value == other._value
	def __hash__(self):
		return(hash((type(self), self._value)))
	def __iter__(self):
		return iter(self._value)
	def __str__(self):
		res = "*".join(sorted(self))
		res = f"({res})"
		return res
	def __mul__(self, other):
		cls = type(self)
		assert isinstance(other, cls)
		res = self._value | other._value
		res = cls(res)
		return res

class BPoly:
	def __init__(self, *monomials):
		s = set()
		for m in monomials:
			assert isinstance(m, BMono)
			if m in s:
				s.discard(m)
			else:
				s.add(m)
		self._value = frozenset(s)
	@classmethod
	def var(cls, name):
		return cls(BMono((name,)))
	def __iter__(self):
		return iter(self._value)
	def __eq__(self, other):
		if type(self) != type(other):
			return False
		return self._value == other._value
	def __hash__(self):
		return(hash((type(self), self._value)))
	def __str__(self):
		res = "\n+".join(sorted(map(str, self)))
		res = f"[{res}]"
		return res
	def __bool__(self):
		return bool(self._value)
	def __add__(self, other):
		return self ^ other
	def __mul__(self, other):
		return self & other
	def __xor__(self, other):
		cls = type(self)
		res = cls(*self, *other)
		return res
	def __and__(self, other):
		cls = type(self)
		res = cls(*(a * b
		            for a in self
		            for b in other))
		return res

def solver2(filename):
	n = 45
	facts = parse(filename)
	assert all(f"{i}{j:02}" in facts
	           for i in "xyz"
	           for j in range(n))
	assert f"z{n:02}" in facts
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
	true_z = []
	carry = BPoly()
	for i in range(n):
		print(f"{i}...")
		sx = f"x{i:02}"
		sy = f"y{i:02}"
		x = BPoly.var(sx)
		y = BPoly.var(sy)
		facts[sx] = x
		facts[sy] = y
		xpy = x + y
		w = carry + xpy
		true_z.append(w)
		carry = f_or(x * y, carry * xpy)
	true_z.append(carry)
	for i, w in enumerate(true_z):
		print(f"{i}...")
		sz = f"z{i:02}"
		z = fact_eval(facts, sz)
		if z != w:
			print("!", sz)
			print(z)
			print(w)
			print()
	return None
	res = sorted(var
	             for var in facts
	             if var[0] == 'z')
	res = [fact_eval(facts, var) for var in res]
	print(res)
	res = sum(b << n for n, b in enumerate(res))
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
