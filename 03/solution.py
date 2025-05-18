

def parse(filename, memory = {}):
	if filename in memory:
		return memory[filename]
	with open(filename) as f:
		data = [line.rstrip() for line in f]
	res = tuple(data)

	memory[filename] = res
	return res

def part1(filename):
	data = parse(filename)
	res = 0
	for line in data:
		start = 0
		while True:
			k = line.find("mul(", start)
#			print(line[k:k+12])
			start = k + 1
			if k == -1: break
			# x
			j0 = k + len("mul(")
			j = j0
			try:
				while line[j].isnumeric():
					j += 1
				if line[j] != ',':
					continue
			except IndexError:
				continue
			if j == j0:
				continue
			x = int(line[j0:j])
			# y
			j0 = j + 1
			j = j0
			try:
				while line[j].isnumeric():
					j += 1
				if line[j] != ')':
					continue
			except IndexError:
				continue
			if j == j0:
				continue
			y = int(line[j0:j])
			# multiply
#			print(x, y)
			res += x * y
	return res

tests1 = {
  "test1.txt" : 161
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
	data = parse(filename)
	res = 0
	disable = False
	for line in data:
		start, stop = 0, len(line)
		k, kd, ke = [-1]*3
		while True:
			# search
			print("->", f"{disable = }", sep='\t', flush=True)
			k = line.find("mul(", start) if k < start else k
			k = stop if k == -1 else k
			print(f"{k = }", line[k:k+12], sep='\t')
			kd = line.find("don't()", start) if kd < start else kd
			kd = stop if kd == -1 else kd
			print(f"{kd = }")
			ke = line.find("do()", start) if ke < start else ke
			ke = stop if ke == -1 else ke
			print(f"{ke = }")
			# endline
			if k == kd == ke:
				assert k == stop
				break
			# disable
			if kd < min(k, ke):
				disable = True
				start = ke
				continue
			# enable
			m = min(k, kd)
			if ke < m:
				disable = False
				start = m
				continue
			# mul
			assert k < min(kd, ke)
			start = k + 1
			if disable:
				continue
			# x
			j0 = k + len("mul(")
			j = j0
			try:
				while line[j].isnumeric():
					j += 1
				if line[j] != ',':
					continue
			except IndexError:
				continue
			if j == j0:
				continue
			x = int(line[j0:j])
			# y
			j0 = j + 1
			j = j0
			try:
				while line[j].isnumeric():
					j += 1
				if line[j] != ')':
					continue
			except IndexError:
				continue
			if j == j0:
				continue
			y = int(line[j0:j])
			# multiply
			print(x, y)
			res += x * y
	return res

#def part2_ugly(filename):
def part2(filename):
	data = parse(filename)
	data = " ".join(data)
	data = data.split("don't()")
#	print(*data, sep='\n')
	new_data = [data[0]]
	for line in data[1:]:
		k = line.find("do()")
		if k == -1:
			continue
		new_data.append(line[k:])
	print(*(line[:80] for line in new_data), sep='\n')
	res = 0
	for line in new_data:
		start = 0
		while True:
			k = line.find("mul(", start)
#			print(line[k:k+12])
			start = k + 1
			if k == -1: break
			# x
			j0 = k + len("mul(")
			j = j0
			try:
				while line[j].isnumeric():
					j += 1
				if line[j] != ',':
					continue
			except IndexError:
				continue
			if j == j0:
				continue
			x = int(line[j0:j])
			# y
			j0 = j + 1
			j = j0
			try:
				while line[j].isnumeric():
					j += 1
				if line[j] != ')':
					continue
			except IndexError:
				continue
			if j == j0:
				continue
			y = int(line[j0:j])
			# multiply
#			print(x, y)
			res += x * y
	return res









tests2 = {
  "test2.txt" : 48
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
