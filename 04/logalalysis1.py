#encoding:utf-8
handler = open('example.log','r')
rt_dict = {}
#统计
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
#print rt_dict
#排序
rt_list = rt_dict.items()
for j in range(0,10):
    for i in range(0,len(rt_list) - 1):
          if rt_list[i][1] > rt_list[i+1][1]:
               temp = rt_list[i]
               rt_list[i] = rt_list[i+1]
               rt_list[i+1] = temp
handler = open('result.txt','w')
for node in rt_list[-1:-11:-1]:
    #((ip,url,code),value)
    print node[1],node[0][0],node[0][1],node[0][2]
handler.write('%s %s %s %s\n ' %(node[1],node[0][0],node[0][1],node[0][2]))
handler.close()
page_tpl = '''
<!DOCTYPE html>
<html>
   <head>
       <meta charset='utf-8'/>
       <title>{title}</title>
   </head>
   <body>
       <table>
           <thead>
              <tr>
                 {thead}
              </tr>
           </thead>
           <tbody>
           <tr>
              {tbody}
            </tr>
          </tbody>
         </table>
      </body>
</html>
'''
title = 'OP 10访问日志'
thead = '<th>IP</th><th>Url</th><th>Code</th><th>次数</th>'
tbody = ''
for node in rt_list[-1:-11:-1]:
       tbody +='<tr><td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td></tr>' % (node[1],node[0][0],node[0][1],node[0][2])
htmlhandler = open('TOP_10.html','w')
htmlhandler.write(page_tpl.format(title=title,thead=thead,tbody=tbody))
htmlhandler.close()