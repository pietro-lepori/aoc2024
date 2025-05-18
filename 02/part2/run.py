from sol import sol

for k in range(1,2):
	filename = f"test{k}.txt"
	with open(filename) as f:
		data = [line.strip() for line in f]
		ans = data.pop()
		res = sol(data)
		print(filename, f"{ans == res}", ans, res, sep='\t')

filename = "in.txt"
with open(filename) as f:
	data = [line.strip() for line in f]
	res = sol(data)
	print(filename, res, sep='\t')
