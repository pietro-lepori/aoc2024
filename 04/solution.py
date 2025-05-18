from itertools import repeat, chain
pri = lambda debug, *args, **kwargs: debug and print(*args, **kwargs)

def parse(filename, memory = {}):
	if filename in memory:
		return memory[filename]
	with open(filename) as f:
		data = [line.rstrip() for line in f]
	res = tuple(tuple(line) for line in data)
	res = res, len(res)

	memory[filename] = res
	return res

def part1(filename):
	mat, N = parse(filename)
	def move(start, step):
		x, y = start
		dx, dy = step
		while True:
			if x < 0:
				return
			if y < 0:
				return
			try:
				yield mat[x][y]
			except IndexError:
				return
			x += dx
			y += dy
	res = 0
	for step, it in [
	  [(0, 1), zip(range(N),  repeat(0))]
	, [(1, 0), zip(repeat(0), range(N) )]
	, [(1, 1), chain( zip(range(N),  repeat(0)  )
	                , zip(repeat(0), range(1, N)))]
	, [(1,-1), chain( zip(range(N),  repeat(N-1))
	                , zip(repeat(0), range(N-1) ))]
	]:
		for start in it:
			s = "".join(move(start, step))
			c1 = s.count("XMAS")
			c2 = s.count("SAMX")
			pri(False
			, "---", start, f"{step = }", c1, c2
			, sep='\t'
			)
			res += c1 + c2
	return res

tests1 = {
  "test1.txt" : 18 # 3 3 1 2
}

if __name__ == "__main__":
	print("PART 1")
	for filename, ans in tests1.items():
		if ans is None:
			continue
		res = part1(filename)
		print("PASS" if ans == res else "FAIL"
		, filename
		, f"{ans = } -- {res = }")
	filename = "input.txt"
	res = part1(filename)
	print(">", res)


def part2(filename):
	mat, N = parse(filename)
	target = set("MS")
	res = 0
	for x in range(1, N-1):
		for y in range(1, N-1):
			if (mat[x][y] == 'A'
			  and {mat[x+1][y+1], mat[x-1][y-1]} == target
			  and {mat[x+1][y-1], mat[x-1][y+1]} == target
			):
				res += 1
	return res

tests2 = {
  "test1.txt" : 9
}

if __name__ == "__main__":
	print("PART 2")
	for filename, ans in tests2.items():
		if ans is None:
			continue
		res = part2(filename)
		print("PASS" if ans == res else "FAIL"
		, filename
		, f"{ans = } -- {res = }")
#	exit()
	filename = "input.txt"
	res = part2(filename)
	print(">", res)
