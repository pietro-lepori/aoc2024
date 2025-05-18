

def sol(data):
	l = [int(x.split()[0]) for x in data]
	r = [int(x.split()[1]) for x in data]
	l.sort()
	r.sort()
	res = 0
	while l:
		x = l.pop()
		cr = 0
		while r:
			y = r.pop()
			if y > x:
				continue
			if y == x:
				cr += 1
				continue
			r.append(y)
			break
		cl = 1
		while l:
			y = l.pop()
			if y > x:
				assert False
			if y == x:
				cl += 1
				continue
			l.append(y)
			break
		res += x * cr * cl
	return str(res)
