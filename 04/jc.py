#encoding=utf-8

def fab(n):
    #n! = 1 * 2 * 3 * 4 * .... * n
    #0! = 1
    if n < 0:
       return None
    elif n ==0:
       return 1
    else:
       rt =1 
       for i in range(1,n+1):
            rt *= i
       return rt


print fab(3)
print fab(4)

def fab2(n):
	if n == 0:
		return 1
	return n * fab2(n -1)



print fab2(3)
print fab2(4)