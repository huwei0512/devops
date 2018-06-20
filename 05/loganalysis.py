#encoding:utf-8

def get_topn(logfile,topn=10):      
      handler = open(logfile,'r')
      rt_dict = {}
      while True:
            line = handler.readline()
            if line == "":
               break
            nodes = line.split()
            ip,url,code = nodes[0],nodes[6],nodes[8]
            key = (ip,url,code)
            if key not in rt_dict:
                  rt_dict[key] = 1
            else:
                 rt_dict[key] = rt_dict[key] +1
      handler.close()

      rt_list = rt_dict.items()
      for j in range(0,topn):
          for i in range(0,len(rt_list) - 1):
                if rt_list[i][1] > rt_list[i+1][1]:
                     temp = rt_list[i]
                     rt_list[i] = rt_list[i+1]
                     rt_list[i+1] = temp
      
      return rt_list[-1:-topn-1:-1]
      

if __name__ == "__main__":
    logfile = "/root/example.log"
    
    print get_topn(topn=5,logfile=logfile)