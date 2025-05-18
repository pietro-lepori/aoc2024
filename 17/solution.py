import z3

def parse(filename):
	with open(filename) as f:
		lines = tuple(line.rstrip() for line in f)
	pre0 = len("Register A: ")
	pre1 = len("Program: ")
	a, b, c = map(int, (lines[k][pre0:] for k in range(3)))
	p = tuple(map(int, lines[4][pre1:].split(',')))
	pc = 0
	return (a, b, c, pc), p

def read_combo(state, arg):
	state = state[:3]
	assert arg >= 0
	if arg <= 3:
		return arg
	return state[arg - 4]

def command(f, combo=False):
	def wrapper(state, arg, out_list):
		if combo:
			arg = read_combo(state, arg)
		pc = state[-1]
		state = f(state, arg, out_list)
		if len(state) == 3:
			state = (*state, pc + 2)
		assert len(state) == 4
		return state
	wrapper.__name__ = f.__name__
	return wrapper

def command_combo(f):
	return command(f, True)

@command_combo
def adv(state, arg, out_list):
	a, b, c, pc = state
#	neg = (a < 0)
#	a = -a if neg else a
	res = a >> arg
#	res = -res if neg else res
	res = res, b, c
	return res

@command
def bxl(state, arg, out_list):
	a, b, c, pc = state
	res = b ^ arg
	res = a, res, c
	return res

@command_combo
def bst(state, arg, out_list):
	a, b, c, pc = state
	res = arg & 7
	res = a, res, c
	return res

@command
def jnz(state, arg, out_list):
	a, b, c, pc = state
	if a:
		return a, b, c, arg
	else:
		return a, b, c

@command
def bxc(state, arg, out_list):
	a, b, c, pc = state
	res = b ^ c
	res = a, res, c
	return res

@command_combo
def out(state, arg, out_list):
	a, b, c, pc = state
	arg &= 7
	out_list.append(arg)
	res = a, b, c
	return res

@command_combo
def bdv(state, arg, out_list):
	a, b, c, pc = state
#	neg = (a < 0)
#	a = -a if neg else a
	res = a >> arg
#	res = -res if neg else res
	res = a, res, c
	return res

@command_combo
def cdv(state, arg, out_list):
	a, b, c, pc = state
	res = a >> arg
	res = a, b, res
	return res

def run(state, p):
	a, b, c, pc = state
	op = {
	0 : adv,
	1 : bxl,
	2 : bst,
	3 : jnz,
	4 : bxc,
	5 : out,
	6 : bdv,
	7 : cdv
	}
	out_list = []
	limit = range(len(p))
	while True:
#		print(state, out_list)
		assert all(x >= 0 for x in state)
		pc = state[-1]
		if pc not in limit:
			break
		cmd = op[p[pc]]
		arg = p[pc + 1]
#		print(cmd.__name__, arg)
		state = cmd(state, arg, out_list)
	return tuple(out_list)

def solver1(filename):
	state, p = parse(filename)
	res = ",".join(map(str, run(state, p)))
	return res

class Expr:
	@staticmethod
	def wrap(obj):
		if isinstance(obj, Expr):
			return obj
		if isinstance(obj, int):
			return ExprInt(obj)
	# to override
	def to_solver(self):
		raise NotImplementedError
	def __init__(self, *args, **kwargs):
		raise NotImplementedError
	def __str__(self):
		raise NotImplementedError
	# create classes to encode operations
	def __rshift__(self, other):
		return ExprShift(self, other)
	def __rrshift__(self, other):
		return ExprShift(other, self)
	def __and__(self, other):
		return ExprAnd(self, other)
	def __rand__(self, other):
		return ExprAnd(other, self)
	def __xor__(self, other):
		return ExprXor(self, other)
	def __rxor__(self, other):
		return ExprXor(other, self)
	def __eq__(self, other):
		return ConstrEq(self, other)
	def __ne__(self, other):
		return ConstrNe(self, other)
	def __lt__(self, other):
		return ConstrLt(self, other)

class ExprInt(Expr):
	def __init__(self, n):
		self.n = n
	def __str__(self):
		return str(self.n)
	def to_solver(self):
		return self.n

class ExprAnd(Expr):
	def __init__(self, a, b):
		self.a = Expr.wrap(a)
		self.b = Expr.wrap(b)
	def __str__(self):
		a, b = self.a, self.b
		return f"({a} & {b})"
	def to_solver(self):
		a = self.a.to_solver()
		b = self.b.to_solver()
		return a & b

class ExprXor(Expr):
	def __init__(self, a, b):
		self.a = Expr.wrap(a)
		self.b = Expr.wrap(b)
	def __str__(self):
		a, b = self.a, self.b
		return f"({a} ^ {b})"
	def to_solver(self):
		a = self.a.to_solver()
		b = self.b.to_solver()
		return a ^ b

class ExprShift(Expr):
	def __init__(self, a, b):
		if (isinstance(b, int)
		and isinstance(a, ExprShift)
		and isinstance(a.b, ExprInt)):
			b += a.b.n
			a = a.a
		self.a = Expr.wrap(a)
		self.b = Expr.wrap(b)
	def __str__(self):
		a, b = self.a, self.b
		return f"({a} >> {b})"
	def to_solver(self):
		a = self.a.to_solver()
		b = self.b.to_solver()
		return a >> b

class ExprVar(Expr):
	def __init__(self, name, size=64):
		assert isinstance(name, str)
		self.name = name
		self.var = z3.BitVec(name, size)
	def __str__(self):
		return self.name
	def to_solver(self):
		return self.var

class ConstrEq:
	def __init__(self, a, b):
		self.a = Expr.wrap(a)
		self.b = Expr.wrap(b)
	def __str__(self):
		a, b = self.a, self.b
		return f"{a} == {b}"
	def to_solver(self):
		a = self.a.to_solver()
		b = self.b.to_solver()
		return a == b

class ConstrNe:
	def __init__(self, a, b):
		self.a = Expr.wrap(a)
		self.b = Expr.wrap(b)
	def __str__(self):
		a, b = self.a, self.b
		return f"{a} != {b}"
	def to_solver(self):
		a = self.a.to_solver()
		b = self.b.to_solver()
		return a != b

class ConstrLt:
	def __init__(self, a, b):
		self.a = Expr.wrap(a)
		self.b = Expr.wrap(b)
	def __str__(self):
		a, b = self.a, self.b
		return f"{a} < {b}"
	def to_solver(self):
		a = self.a.to_solver()
		b = self.b.to_solver()
		return a < b


def run2(state, p, target_len, out_list=None, constraints=None):
	a, b, c, pc = state
	op = {
	0 : adv,
	1 : bxl,
	2 : bst,
	3 : None,
	4 : bxc,
	5 : out,
	6 : bdv,
	7 : cdv
	}
	out_list = [] if out_list is None else out_list
	constraints = [] if constraints is None else constraints
	limit = range(len(p))
	while True:
		if len(out_list) > target_len:
			return
#		print(state, out_list)
		pc = state[-1]
		if pc not in limit:
			break
		arg = p[pc + 1]
		k = p[pc]
		if k == 3:
			regis = state[:-1]
			a = regis[0]
			# try a == 0 in a recursive call
			pc = state[-1] + 2
			state1 = (*regis, pc)
			out_list1 = out_list[:]
			constraints1 = constraints[:]
			constraints1.append(a == 0)
			yield from run2(state1, p, target_len, out_list1, constraints1)
			# else jump
			state = (*regis, arg)
			constraints.append(a != 0)
			continue
		cmd = op[k]
#		print(cmd.__name__, arg)
		state = cmd(state, arg, out_list)
	if len(out_list) == target_len:
		yield tuple(out_list), tuple(constraints)

def solver2(filename):
	state, p = parse(filename)
	print(p)
	op = {
	0 : adv,
	1 : bxl,
	2 : bst,
	3 : jnz,
	4 : bxc,
	5 : out,
	6 : bdv,
	7 : cdv
	}
	for k in range(0, len(p), 2):
		cmd = op[p[k]].__name__
		arg = p[k + 1]
		print(cmd, arg)
	print()
	a = ExprVar("A")
#	a = ExprVar("A", 48)	# bug !!!
	state = (a, *state[1:])
#	state = (z3.BitVec("A", 48), *state[1:])
	branches = []
	for out_list, constraints in run2(state, p, len(p)):
		print("\n".join(map(str, out_list)))
		print("---")
		print("\n".join(map(str, constraints)))
		print("\n")
		s = z3.Solver()
		branches.append(s)
		s.add(*(c.to_solver()
		        for c in constraints))
		s.add(*((e == x).to_solver()
		        for e, x in zip(out_list, p)))
	best = None
	while branches:
		s = branches.pop()
		if best is not None:
			s.add((a < best).to_solver())
		ans = s.check()
		print(ans)
		if ans == z3.sat:
			x = s.model().eval(a.to_solver()).as_long()
			print(s.statistics())
			print("...", x)
			assert best is None or x < best
			best = x
		else:
			print(s.statistics())
			continue
		branches.append(s)
	res = best
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
