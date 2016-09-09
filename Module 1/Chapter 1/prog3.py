def fib(n):
	a=0
	b=1
	for i in range(n):
		temp=a
		a=b
		b=temp+b
	return a

for i in range (0,10):
	print (fib(i))
