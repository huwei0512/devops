
def default_cmp(x,y):
	if x > y:
		return True
	else:
		return False

def default_key(x):
	   return x


def sortlist(listsort,key=None,cmp=None):
	if key is None:
		key = default_key
	if cmp is None:
		cmp = default_cmp
	listsort = listsort[:]
	for j in range(len(listsort) -1):
		for i in range(len(listsort) -1):
			ele1 = key(listsort[i])
			ele2 = key(listsort[i+1])
			cmp_result = cmp(ele1,ele2)
			if cmp_result:
				listsort[i],listsort[i+1] = listsort[i+1],listsort[i]

	return listsort

print __name__
                      
if __name__ == "__main__":

	sort_list = [{'name':'dick','age':30,'sex':'male'},{'name':'sophie','age':28,'sex':'female'},{'name':'maria','age':31,'sex':'female'}]
	print sortlist(sort_list,key=lambda x : x['age'],cmp=cmp)
 