def sol(data):
	l = [int(x.split()[0]) for x in data]
	r = [int(x.split()[1]) for x in data]
	l.sort()
	r.sort()
	res = sum(abs(x-y) for x, y in zip(l,r))
	return str(res)
