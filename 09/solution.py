from dataclasses import dataclass

@dataclass
class Block:
	id: int
	size: int
	prev: object
	post: object = None
	def insert_before(self, id, size):
		old_prev = self.prev
		o = Block(id, size, old_prev, self)
		old_prev.post = o
		self.prev = o
	def remove(self):
		prev = self.prev
		post = self.post
		self.prev = None
		self.post = None
		if prev is not None:
			prev.post = post
		if post is not None:
			post.prev = prev
	def __iter__(self):
		p = self
		while p is not None:
			yield p.id, p.size
			p = p.post

@dataclass
class BlockList:
	first: Block = None
	last: Block = None
	def append(self, id, size):
		old_last = self.last
		last = Block(id, size, old_last)
		if self.first is None:
			self.first = last
			assert old_last is None
			self.last = last
			return
		assert old_last.post is None
		assert last.post is None
		old_last.post = last
		self.last = last
	def coalesce(self, compress=True):
		p = self.first
		p1 = p.post if p is not None else None
		while p1 is not None:
			if (p.id != p1.id
			  and not (compress and p1.size == 0)):
				p = p1
				p1 = p.post
				continue
			p.size += p1.size
			p1.remove()
			p1 = p.post
		self.last = p
	def __iter__(self):
		first = self.first
		if first is None:
			return
		yield from first

def parse(filename):
	with open(filename) as f:
		line = next(f).rstrip()
	res = BlockList()
	for k, c in enumerate(line):
		size = int(c)
		id = None if k % 2 else k // 2
		res.append(id,size)
	return res

def solver1(filename):
	blocks = parse(filename)
	# simulate
	blocks.coalesce()
	a = blocks.first
	b = blocks.last
	while a is not b:
		if a.id is not None:
			a = a.post
			continue
		free = a
		if free.size == 0:
			a = free.post
			free.remove()
			continue
		if b.id is None:
			b = b.prev
			continue
		file = b
		if file.size == 0:
			b = file.prev
			file.remove()
			continue
		file_id = file.id
#		print("---", file_id, free.size, file.size)
		if file.size > free.size:
			size = free.size
			reminder = file.size - free.size
		else:
			size = file.size
			reminder = 0
		free.insert_before(file_id, size)
		free.size -= size
		file.size = reminder
	# compute
	blocks.coalesce()
	res = 0
	addr = 0
	done = False
	for n, size in blocks:
		assert size
#		print(n, size, sep='\t')
		if n is None:
			done = True if size else done
			continue
		elif done and size:
			assert False
#			print("!!!")
		addr1 = addr + size
		res += (n * size * (addr + addr1 - 1)) // 2
		addr = addr1
	return res

def solver2(filename):
	blocks = parse(filename)
	# simulate
	blocks.coalesce()
	a = blocks.first
	b = blocks.last
	while a is not b:
		if b.id is None or b.id < 0:
			b = b.prev
			continue
		if a.id is not None:
			a = a.post
			continue
		file = b
		file_id = file.id
		size = file.size
		p = a
		free = None
		print(id(file), file.id, file.size, [t for t in a])
		while True:
			print("- ", id(p), p.id, p.size)
			if p is file:
				break
			if p.id is not None:
				p = p.post
				continue
			if p.size < size:
				p = p.post
				continue
			free = p
			break
		if free is None:
			b = b.prev
			continue
		file_id = -(file_id + 1)
		free.size -= size
		free.insert_before(file_id, size)
		b = file.prev
		file.remove()
		a = blocks.first
	# compute
	blocks.coalesce(compress=True)
	res = 0
	addr = 0
	for n, size in blocks:
		print(n, size, res, sep='\t')
		addr1 = addr + size
		if n is not None:
			if n < 0:
				n = (-n) - 1
			res += (n * size * (addr + addr1 - 1)) // 2
		addr = addr1
	return res

def main():
	input_file = "input.txt"
	test1_file = "testlist1.txt"
	test2_file = "testlist2.txt"

	print("PART 1")
	solver = solver1
	tests = read_tests(test1_file)
	test_result = list(do_tests(tests, solver, verbose=True))
#	exit()
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
