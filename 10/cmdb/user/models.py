#encoding:utf-8
from dbutils import MySQLConnection

class User(object):

    def __init__(self,id,username,password,age):
        self.id = id
        self.username = username
        self.password = password
        self.age = age

    @classmethod
    def validate_login(cls,username,password):
        _column = ("id","username")
        _sql = 'select id,username from user_auth where username=%s and password=md5(%s)'  #无非就是查询count
        _count,_rt_tuple = MySQLConnection.execute_sql(_sql,(username,password))
        print "_rt_tuple:",_rt_tuple
        return dict(zip(_column,_rt_tuple[0])) if _count != 0 else None

    @classmethod
    def get_list(cls): 
        _columns = ('id','username','password','age')
        _sql = 'select * from user_auth'
        print _sql
        _count,_rt_tuple = MySQLConnection.execute_sql(_sql)

        #初始化参数
        _rt_list = []
        #return [ User(**dict(zip(_columns,_line))) for _line in _rt_tuple]
        for _line in _rt_tuple:
        #(6L,u'dick',u'wdwqedwqewqdsadwqdwqdwqw',29L)
            _user_dict = dict(zip(_columns,_line))
            _user = User(_user_dict['id'],_user_dict['username'],_user_dict['password'],_user_dict['age'])
            #_user = User(**_user_dict)
            _rt_list.append(_user)
        return _rt_list


        '''检查新建用户信息
    返回值：True/False，错误信息
    '''
    @classmethod
    def validate_add(cls,username,password,age):
        if username.strip() == '':
            return False,u"用户名不能为空"

        #检查用户名是否重复
        #get_user_by_name()   #通过此函数直接在数据库中检索用户名是否存在
        if cls.get_user_by_name(username):  #类方法则使用类进行调用
            return False,u'用户名已存在'

        #密码要求长度必须大于等于6
        if len(password) < 6:
            return False,u'密码必须大于等于6'

        if not str(age).isdigit() or int(age) <= 0 or int(age) > 100:
            return False,u'年龄必须是0到100的数字'

        return True,''

    '''添加用户信息
    '''
    @classmethod
    def add(cls,username,password,age):
        _sql = 'insert into user_auth(username,password,age) values(%s,md5(%s),%s)'
        args = (username,password,age)
        MySQLConnection.execute_sql(_sql,args,False)

    @classmethod
    def get_user_by_name(cls,username):
        _columns = ('id','username','password','age')
        _sql = 'select * from user_auth where username = %s'
        _count,_rt_tuple = MySQLConnection.execute_sql(_sql,(username,))
        #返回list
        _rt_list = []  
        for _line in _rt_tuple:
            _rt_list.append(dict(zip(_columns,_line)))
        return _rt_list[0] if len(_rt_list) > 0 else None

if __name__ == "__main__":
    print User.validate_login("dick","123456")
    print User.validate_login("dick","1234156")