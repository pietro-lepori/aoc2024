def sol(data):
	res = 0
	for l in data:
		l = list(map(int, l.split()))
		assert len(l) > 2
		d = [x-y for x, y in zip(l[1:], l)]
		if is_safe(d, range(1,4)):
			res += 1
			continue
		if is_safe(d, range(-3,0)):
			res += 1
	return str(res)

def is_safe(d, limits, err = 1):
	for k, x in enumerate(d):
		if x in limits:
			continue
		stop = k
		reminder = x
		break
	else:
		return True
	if err == 0:
		return False
	if stop + 1 == len(d):
		return True
	if stop == 0:
		new_ds = [
		  d[1:] ,
		  [reminder + d[1], *d[2:]] ]
	else:
		new_ds = [
		  [reminder + d[stop-1], *d[stop+1:]] ,
		  [reminder + d[stop+1], *d[stop+2:]] ]
	return any(is_safe(d1, limits, err - 1) for d1 in new_ds)
