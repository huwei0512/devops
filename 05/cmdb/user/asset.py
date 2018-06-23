#encoding:utf-8

from dbutils import execute_fetch_sql,execute_commit_sql


def get_idc_list():
    return [('1','上海'),('2','北京'),('3','香港'),('4','上海-浦东')]

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
    _columns = ('id','sn','ip','hostname','os','cpu','ram','disk','idc_id','admin','business','purchase_date','warranty','vendor','model','status')
    _sql = 'select * from assets where id = %s'
    _count,_rt_tuple = execute_fetch_sql(_sql,(aid,))
    #返回list
    _rt_list = []  
    for _line in _rt_tuple:
        _rt_list.append(dict(zip(_columns,_line)))
    return _rt_list[0] if len(_rt_list) > 0 else None


def get_by_sn(sn):
    _columns = ('id','sn','ip','hostname','os','cpu','ram','disk','idc_id','admin','business','purchase_date','warranty','vendor','model','status')
    _sql = 'select * from assets where sn = %s'
    _count,_rt_tuple = execute_fetch_sql(_sql,(sn,))
    #返回list
    _rt_list = []  
    for _line in _rt_tuple:
        _rt_list.append(dict(zip(_columns,_line)))
    return _rt_list[0] if len(_rt_list) > 0 else None 


'''
在创建资产时对输入信息进行检查
True/False,error_msg{}
'''

def validate_create_asset(_sn,_ip,_hostname,_os,_cpu,_ram,_disk,_idc_id,_admin,_business,_purchase_date,_warranty,_vendor,_model):
    if _sn.strip() == '':
        return False,u'sn编号不能为空'
    #检查sn编码是否重复
    #get_by_sn()   #通过此函数直接在数据库中检索sn是否存在
    elif get_by_sn(_sn):
        return False,u'sn编码已存在,请重新输入！'
    elif _ip.strip() == '':
        return False,u'IP地址不能为空'
    elif _hostname.strip() == '':
        return False,u'主机名不能为空'
    elif _os.strip() == '':
        return False,u'操作系统不能为空'
    elif _admin.strip() == '':
        return False,u'使用人不能为空'
    elif _business.strip() == '':
        return False,u'业务不能为空'
    elif _warranty.strip() == '':
        return False,u'保修日期不能为空'
    elif int(_warranty) < 1 or int(_warranty) > 5:
        return False,u'保修日期必须是1到5的数字'
    elif _vendor.strip() == '':
        return False,u"供应商不能为空"
    elif _model.strip() == '':
        return False,u"型号不能为空"
        
    return True,''
    #return True,{}


'''
创建资产，操作数据库
返回True/False
'''

def create_asset(sn,ip,hostname,os,cpu,ram,disk,idc_id,admin,business,purchase_date,warranty,vendor,model):
    _sql = 'insert into assets(sn,ip,hostname,os,cpu,ram,disk,idc_id,admin,business,purchase_date,warranty,vendor,model) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    _args = (sn,ip,hostname,os,cpu,ram,disk,idc_id,admin,business,purchase_date,warranty,vendor,model)
    execute_commit_sql(_sql,_args)

'''
在修改资产时对输入的信息进行检查
True/False,error_msg{}
'''
def validate_update_asset(_sn,_ip,_hostname,_os,_cpu,_ram,_disk,_idc_id,_admin,_business,_purchase_date,_warranty,_vendor,_model,_aid):
    if get_by_id(_aid) is None:
        print 'get_user:%s',get_by_id(_aid)
        return False,u'资产信息不存在!'
    elif _sn.strip() == '':
        return False,u'sn编号不能为空'
    #检查sn编码是否重复
    #get_by_sn()   #通过此函数直接在数据库中检索sn是否存在
    elif get_by_sn(_sn):
        return False,u'sn编码已存在,请重新输入！'
    elif _ip.strip() == '':
        return False,u'IP地址不能为空'
    elif _hostname.strip() == '':
        return False,u'主机名不能为空'
    elif _os.strip() == '':
        return False,u'操作系统不能为空'
    elif _admin.strip() == '':
        return False,u'使用人不能为空'
    elif _business.strip() == '':
        return False,u'业务不能为空'
    elif _warranty.strip() == '':
        return False,u'保修日期不能为空'
    elif int(_warranty) < 1 or int(_warranty) > 5:
        return False,u'保修日期必须是1到5的数字'
    elif _vendor.strip() == '':
        return False,u"供应商不能为空"
    elif _model.strip() == '':
        return False,u"型号不能为空"
        
    return True,''

'''
更新资产，操作数据库
返回True/False
'''
def update_asset(sn,ip,hostname,os,cpu,ram,disk,idc_id,admin,business,purchase_date,warranty,vendor,model,aid):
    _sql = 'update assets set sn=%s,ip=%s,hostname=%s,os=%s,cpu=%s,ram=%s,disk=%s,idc_id=%s,admin=%s,business=%s,purchase_date=%s,warranty=%s,vendor=%s,model=%s where id=%s'
    _args = (sn,ip,hostname,os,cpu,ram,disk,idc_id,admin,business,purchase_date,warranty,vendor,model,aid)
    execute_commit_sql(_sql,_args)

'''
删除资产，操作数据库
返回True/False
'''
def delete_asset(aid):
    _sql = 'update assets set status=1 where id=%s'
    _args = (aid,)
    execute_commit_sql(_sql,_args)


if __name__ == '__main__':
    print get_asset_list()






































