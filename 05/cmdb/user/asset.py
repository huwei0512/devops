#encoding:utf-8

from dbutils import execute_fetch_sql,execute_commit_sql


'''
返回所有资产信息
[{'sn':'','id':'','hostname':'','ip':'',........},
{},
{},
{}]
'''
def get_asset_list():
    _rt_list = []
    _column = 'id,sn,ip,hostname,os,cpu,ram,disk,idc_id,admin,business,purchase_date,warranty,vendor,model'
    _columns = _column.split(',')
    _sql = 'SELECT {column} FROM assets WHERE status=0'.format(column=_column)
    _count,_rt_tuple = execute_fetch_sql(_sql)
    #_rt_tuple => [(id,sn,hostname,ip,....)]
    for _line in _rt_tuple:
        print 'line:',_line
        _rt_list.append(dict(zip(_columns,_line)))
    print '_rt_list:',_rt_list
    return _rt_list

'''
通过主键返回资产信息
None/{}
'''

def get_by_id(aid):
    return None


'''
在创建资产时对输入信息进行检查
True/False,error_msg{}
'''

def validate_create_asset():
    return False,{'cpu':'cpu不是整数','sn':'sn编号重复'}
    #return True,{}


'''
创建资产，操作数据库
返回True/False
'''

def create_asset():
    pass

'''
在修改资产时对输入的信息进行检查
True/False,error_msg{}
'''
def validate_update_asset():
    pass

'''
更新资产，操作数据库
返回True/False
'''
def update_asset():
    pass

'''
删除资产，操作数据库
返回True/False
'''
def delete():
    pass


if __name__ == '__main__':
    print get_asset_list()






































