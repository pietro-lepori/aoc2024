def sol(data):
	res = 0
	for l in data:
		l = list(map(int, l.split()))
		assert len(l) > 1
		d = [x-y for x, y in zip(l, l[1:])]
#		print(l, d)
		if all(x in range(1,4) for x in d): res += 1
		if all(x in range(-3,0) for x in d): res += 1
	return str(res)
