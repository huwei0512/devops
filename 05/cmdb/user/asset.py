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
    _sql = 'select * from assets where status=0 and id=%s' #status=0,把正常的值拿出来，因为被删除的值的status=1.不写的话，都拿出来
    _count,_rt_tuple = execute_fetch_sql(_sql,(aid,))
    #返回list
    _rt_list = []  
    for _line in _rt_tuple:
        _rt_list.append(dict(zip(_columns,_line)))
    return None if _count == 0 else _rt_list[0]


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

def validate_create_asset(get_form):
    _is_ok = True
    _errors = {}
    rt =get_asset_list()
    '''
    字符串类型: sn,ip,hostname,os,admin,business,vendor,model
    检查是否为空(不允许),最小长度,最大长度
    '''
    for _key in 'sn,ip,hostname,os,admin,business,vendor,model'.split(','):
        _value = get_form.get(_key, '').strip()
        if _value == '':
            _is_ok = False
            _errors[_key] = '%s不允许为空' % _key
        elif len(_value) > 64:
            _is_ok = False
            _errors[_key] = '%s不允许超过64个字符' % _key

    #判断某些列重复
    for _rrt in rt:
        if _rrt['ip'] == get_form.get('ip', ''):
            _is_ok = False
            _errors['ip'] = '新增资产中的IP正在使用中，请重新分配！'
        elif _rrt['sn'] == get_form.get('sn', ''):
            _is_ok = False
            _errors['sn'] = 'sn编码已经存在，请重新填写！'
    '''
    取值选项:idc_id
    '''
    if get_form.get('idc_id') not in [str(_value[0]) for _value in get_idc_list()]:
        _is_ok = False
        _errors['idc'] = '机房选择不正确'

    '''
    数字类型: cpu,ram,disk,warranty
    检查数字类型isdigit, 最大值, 最小值
    '''
    _rules = {
        'cpu' : {'min' : 2, 'max' : 64},
        'ram' : {'min' : 64, 'max' : 1024},
        'disk' : {'min' : 512, 'max' : 10240},
        'warranty' : {'min' : 1, 'max' : 5},
    }
    for _key in 'cpu,ram,disk,warranty'.split(','):
        _value = get_form.get(_key, '').strip()
        if not _value.isdigit():
            _is_ok = False
            _errors[_key] = '%s不是整数' % _key
        else:
            _value = int(_value)
            _min = _rules.get(_key).get('min')
            _max = _rules.get(_key).get('max')
            if _value < _min or _value > _max:
                _is_ok = False
                _errors[_key] = '%s取值范围应该为%s ~ %s' % (_key, _min, _max)

    '''
    日期类型: purchase_date
    '''
    if not get_form.get('purchase_date', ''):
        _is_ok = False
        _errors['purchase_date'] = '采购日期不同为空'

    return _is_ok, _errors
    #return False,{"cpu":"cpu不是整数"，"id":"id已经重复"} 

'''
创建资产，操作数据库
返回True/False
'''

def create_asset(get_form):
    _column_str = 'sn,ip,hostname,os,cpu,ram,disk,idc_id,admin,business,purchase_date,warranty,vendor,model'
    _columns = _column_str.split(',')
    _args = []
    for _column in _columns:
        _args.append(get_form.get(_column, ''))
        #通过Python去拼sql语句
    _sql = 'INSERT INTO assets({columns}) VALUES({values})'.format(columns=_column_str, values=','.join(['%s'] * len(_columns)))
    execute_commit_sql(_sql, _args)

    # _sql = 'insert into assets(sn,ip,hostname,os,cpu,ram,disk,idc_id,admin,business,purchase_date,warranty,vendor,model) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    # _args = (sn,ip,hostname,os,cpu,ram,disk,idc_id,admin,business,purchase_date,warranty,vendor,model,aid)
    # execute_commit_sql(_sql,_args)


'''
在修改资产时对输入的信息进行检查
True/False,error_msg{}
'''
def validate_update_asset(get_form):
    _is_ok = True
    _errors = {}
    rt = get_asset_list()
    _aid = get_form.get('id','')


    if get_by_id(_aid) is None:
        print 'get_user:%s',get_by_id(_aid)
        _is_ok = False
        _errors['ass'] = '资产信息不存在!'
    '''
    字符串类型: sn,ip,hostname,os,admin,business,vendor,model
    检查是否为空(不允许),最小长度,最大长度
    '''
    for _key in 'sn,ip,hostname,os,admin,business,vendor,model'.split(','):
        _value = get_form.get(_key, '').strip()
        if _value == '':
            _is_ok = False
            _errors[_key] = '%s不允许为空' % _key
        elif len(_value) > 64:
            _is_ok = False
            _errors[_key] = '%s不允许超过64个字符' % _key

    '''
    取值选项:idc_id
    '''
    if get_form.get('idc_id') not in [str(_value[0]) for _value in get_idc_list()]:
        _is_ok = False
        _errors['idc'] = '机房选择不正确'
        

    '''
    数字类型: cpu,ram,disk,warranty
    检查数字类型isdigit, 最大值, 最小值
    '''
    _rules = {
        'cpu' : {'min' : 2, 'max' : 64},
        'ram' : {'min' : 64, 'max' : 1024},
        'disk' : {'min' : 512, 'max' : 10240},
        'warranty' : {'min' : 1, 'max' : 5},
    }
    for _key in 'cpu,ram,disk,warranty'.split(','):
        _value = get_form.get(_key, '').strip()
        if not _value.isdigit():
            _is_ok = False
            _errors[_key] = '%s不是整数' % _key
        else:
            _value = int(_value)
            _min = _rules.get(_key).get('min')
            _max = _rules.get(_key).get('max')
            if _value < _min or _value > _max:
                _is_ok = False
                _errors[_key] = '%s取值范围应该为%s ~ %s' % (_key, _min, _max)

    #如果没有修改肯定是和它本身是一样的,要加上输入的ip不等于当前修改资产
    for _rrt in rt:
        if _rrt['ip'] == get_form.get('ip', ''):
            _is_ok = False
            _errors['ip'] = '{IP}正在使用中，请重新填写！'.format(IP=get_form.get('ip', ''))

    '''
    日期类型: purchase_date
    '''
    if not get_form.get('purchase_date', ''):
        _is_ok = False
        _errors['purchase_date'] = '采购日期不同为空'

    return _is_ok, _errors
    #return False,{"cpu":"cpu不是整数"，"id":"id已经重复"} 


    # if get_by_id(_aid) is None:
    #     print 'get_user:%s',get_by_id(_aid)
    #     return False,u'资产信息不存在!'
    # elif _sn.strip() == '':
    #     return False,u'sn编号不能为空'
    # #检查sn编码是否重复
    # #get_by_sn()   #通过此函数直接在数据库中检索sn是否存在
    # elif _ip.strip() == '':
    #     return False,u'IP地址不能为空'
    # elif _hostname.strip() == '':
    #     return False,u'主机名不能为空'
    # elif _os.strip() == '':
    #     return False,u'操作系统不能为空'
    # elif _admin.strip() == '':
    #     return False,u'使用人不能为空'
    # elif _business.strip() == '':
    #     return False,u'业务不能为空'
    # elif _warranty.strip() == '':
    #     return False,u'保修日期不能为空'
    # elif int(_warranty) < 1 or int(_warranty) > 5:
    #     return False,u'保修日期必须是1到5的数字'
    # elif _vendor.strip() == '':
    #     return False,u"供应商不能为空"
    # elif _model.strip() == '':
    #     return False,u"型号不能为空"
        
    # return True,''

'''
更新资产，操作数据库
返回True/False
'''
def update_asset(get_form):
    _column_str = 'sn,ip,hostname,os,cpu,ram,disk,idc_id,admin,business,purchase_date,warranty,vendor,model'
    _columns = _column_str.split(',')
    _values = []
    _args = []
    for _column in _columns:
        _values.append('{column}=%s'.format(column=_column))
        _args.append(get_form.get(_column, ''))
    _args.append(get_form.get('id'))
    #通过Python去拼sql语句
    _sql = 'UPDATE assets SET {values} WHERE id=%s'.format(values=','.join(_values))
    execute_commit_sql(_sql, _args)

    # _sql = 'update assets set sn=%s,ip=%s,hostname=%s,os=%s,cpu=%s,ram=%s,disk=%s,idc_id=%s,admin=%s,business=%s,purchase_date=%s,warranty=%s,vendor=%s,model=%s where id=%s'
    # _args = (sn,ip,hostname,os,cpu,ram,disk,idc_id,admin,business,purchase_date,warranty,vendor,model,aid)
    # execute_commit_sql(_sql,_args)

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






































