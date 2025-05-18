

def parse(filename, memory = {}):
	if filename in memory:
		return memory[filename]
	with open(filename) as f:
		data = [line.rstrip() for line in f]
#	res = data

	left = data[:]
	right = data[:]
	for k, line in enumerate(data):
		left[k], right[k] = map(int, line.split())
	res = left, right

	memory[filename] = res
	return res

def part1(filename):
	left, right = parse(filename)
	left.sort()
	right.sort()
	res = sum(abs(x-y) for x, y in zip(left, right))
	return res

tests1 = {
  "test1.txt" : 11
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
