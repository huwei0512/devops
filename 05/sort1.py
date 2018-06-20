
def default_cmp(x,y):
	if x > y:
		return True
	else:
		return False

def default_key(x):
	   return x


def sortlist(listsort,key,cmp):
	 listsort = listsort[:]
     for j in range(len(listsort) -1):
             for i in range(len(listsort) -1):
                  #if key(work_list[i]) > key(work_list[i+1]):
                  ele1 = key(listsort[i])
                  ele2 = key(listsort[i+1])
                  #if cmp(key(work_list[i]),key(work_list[i+1])):
                  cmp_result = cmp(ele1,ele2)
                  if cmp_result:
                  	    listsort[i],listsort[i+1] = listsort[i+1],listsort[i]
     return listsort
                      


sort_list = [{'name':'dick','age':30,'sex':'male'},{'name':'sophie','age':28,'sex':'female'},{'name':'maria','age':31,'sex':'female'}]
sort_list(work_list,lambda x : x["age"])
print work_list  