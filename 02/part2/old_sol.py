def sol(data):
	res = 0
	for l in data:
		l = list(map(int, l.split()))
		assert len(l) > 1
		d = [x-y for x, y in zip(l, l[1:])]
#		print(l, d)
		if is_safe(d, range(1,4)): res += 1
		elif is_safe(d, range(-3,0)): res += 1
	return str(res)

def is_safe(d, limits):
	for k, x in enumerate(d):
		if x in limits:
			continue
		restart = k + 1
		reminder = x
		break
	else:
		return True
	if restart == len(d):
		return True
	if reminder + d[restart] not in limits:
		return False
	return all(x in limits for x in d[restart + 1:])
