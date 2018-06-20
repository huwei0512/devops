#encoding:utf-8
import json
import gconf
from dbutils import execute_fetch_sql,execute_commit_sql
'''获取所有用户的信息
返回值：[  
             {"username":"kk","password":"123456","age":29},
             {"username":"dick","password":"huwei123","age":25}
        ]
'''

def get_users(): 
    _columns = ('id','username','password','age')
    _sql = 'select * from user_auth' 
    print _sql
    #初始化参数
    _rt_list = []
    _count,_rt_tuple = execute_fetch_sql(_sql)

    for _line in _rt_tuple:
    #(6L,u'dick',u'wdwqedwqewqdsadwqdwqdwqw',29L)
         _rt_list.append(dict(zip(_columns,_line)))
    print '_rt_list:',_rt_list
    return _rt_list
    

'''保存用户数据到文件中
'''
def save_users(users):
    fhandler = open(gconf.USER_FILE,'wb')
    fhandler.write(json.dumps(users))
    fhandler.close()

'''验证用户名，密码是否正确
返回值：True/Flase
'''

def validate_login(username,password):
    _sql = 'select * from user_auth where username=%s and password=md5(%s)'  #无非就是查询count
    #_sql = 'select * from user_auth where username="{username}" and password=md5("{password}")'.format(username=username,password=password)
    _count,_rt_tuple = execute_fetch_sql(_sql,(username,password))
    # return _count != 0
    if _count == 0:
        return False
    else:
        return True
    

'''检查新建用户信息
返回值：True/False，错误信息
'''
def validate_add_user(username,password,age):
    if username.strip() == '':
        return False,u"用户名不能为空"

    #检查用户名是否重复
    #get_user_by_name()   #通过此函数直接在数据库中检索用户名是否存在
    if get_user_by_name(username):
        return False,u'用户名已存在'

    #密码要求长度必须大于等于6
    if len(password) < 6:
        return False,u'密码必须大于等于6'

    if not str(age).isdigit() or int(age) <= 0 or int(age) > 100:
        return False,u'年龄必须是0到100的数字'

    return True,''

'''添加用户信息
'''
def add_user(username,password,age):
    _sql = 'insert into user_auth(username,password,age) values(%s,md5(%s),%s)'
    args = (username,password,age)
    execute_commit_sql(_sql,args)

'''获取用户信息
'''
def get_user(uid):
    _columns = ('id','username','password','age')
    _sql = 'select * from user_auth where id = %s'
    _count,_rt_tuple = execute_fetch_sql(_sql,(uid,))
    #返回list
    _rt_list = []  
    for _line in _rt_tuple:
        _rt_list.append(dict(zip(_columns,_line)))
        print '_rt_list(get_user):%s',_rt_list
    return _rt_list[0] if len(_rt_list) > 0 else None

'''
_rt = get_users([('id',uid)])
    print '_rt:%s',_rt
    return _rt[0] if len(_rt) > 0 else None
'''


'''检查更新用户信息
返回值：True/False，错误信息
'''
def validate_update_user(uid,username,password,age):
    if get_user(uid) is None:
        print 'get_user:%s',get_user(uid)
        return False,u'用户信息不存在!'

    if username.strip() == '':
        return False,u'用户名不能为空'
     
    _user = get_user_by_name(username)
    if _user and _user.get('id') !=int(uid):
        return False,u'用户名已存在'

    #密码要求长度必须大于等于6
    if len(password) < 6:
        return False,u'密码必须大于等于6'

    if not str(age).isdigit() or int(age) <= 0 or int(age) > 100:
        return False,u'年龄必须是0到100的数字'

    return True,''


'''更新用户信息
'''
def update_user(uid,username,password,age):
    _sql = 'update user_auth set username=%s,password=md5(%s),age=%s where id=%s'
    _args = (username,password,age,uid)
    execute_commit_sql(_sql,_args)


'''删除用户信息
'''
def delete_user(uid):
    _sql = 'delete from user_auth where id=%s'
    _args = (uid,)
    execute_commit_sql(_sql,_args)

def get_user_by_name(username):
    _columns = ('id','username','password','age')
    _sql = 'select * from user_auth where username = %s'
    _count,_rt_tuple = execute_fetch_sql(_sql,(username,))
    #返回list
    _rt_list = []  
    for _line in _rt_tuple:
        _rt_list.append(dict(zip(_columns,_line)))
    return _rt_list[0] if len(_rt_list) > 0 else None

def validate_admin_passwd(uid,upasswd,admin_user,admin_passwd):
    #检查管理员密码
    if not validate_login(admin_user,admin_passwd):
        return False,u'管理员密码错误'

    if get_user(uid) is None:
        return False,u'用户信息不存在!'

    #密码要求长度必须大于等于6
    if len(upasswd) < 6:
        return False,u'密码必须大于等于6'

    return True,u''
     

def update_user_passwd(uid,upasswd):
    _sql = 'update user_auth set password=md5(%s) where id=%s'
    execute_commit_sql(_sql,(upasswd,uid))

'''
_rt = get_users([('username',username)])
    print '_rt:%s',_rt
    return _rt[0] if len(_rt) > 0 else None
'''



if __name__ == "__main__":
    _is_ok, _error = validate_update_user('ada', 'ada23', 26)
    print _is_ok, _error
    _is_ok, _error = validate_update_user('ada1', 'ada23', 26)
    print _is_ok, _error
    _is_ok, _error = validate_update_user('ada1', 'ada2d3', 'abc')
    print _is_ok, _error
    _is_ok, _error = validate_update_user('xiaoxia', 'ada2d3', 26)
    print _is_ok, _error