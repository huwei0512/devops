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
    def get_users(cls): 
        _columns = ('id','username','password','age')
        _sql = 'select * from user_auth' 
        print _sql
        #初始化参数
        _rt_list = []
        _count,_rt_tuple = MySQLConnection.execute_sql(_sql)

        #return [ User(**dict(zip(_columns,_line))) for _line in _rt_tuple]
        for _line in _rt_tuple:
        #(6L,u'dick',u'wdwqedwqewqdsadwqdwqdwqw',29L)
            _user_dict = dict(zip(_columns,_line))
             _user = User(_user_dict['id'],_user_dict['username'],_user_dict['password'],_user_dict['age'])
            #_user = User(**_user_dict)
            print '_user:',_user
            _rt_list.append(_user)
        print '_rt_list:',_rt_list
        return _rt_list

if __name__ == "__main__":
    print User.validate_login("dick","123456")
    print User.validate_login("dick","1234156")