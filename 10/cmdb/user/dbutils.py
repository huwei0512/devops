#encoding:utf-8
import MySQLdb
import gconf

#面向对象思路
class MySQLConnection(object):

    def __init__(self,host,port,user,passwd,db,charset='utf8'):
        #属性
        self.__host = host
        self.__port = port
        self.__user = user
        self.__passwd = passwd
        self.__db = db
        self.__charset = charset
        self.__conn = None
        self.__cur = None
        self.__connection()
        
    def __connection(self):
        try:
            #创建一个数据库的连接
            self.__conn = MySQLdb.connect(host=self.__host,port=self.__port, \
                                   user=self.__user,passwd=self.__passwd, \
                                   db=self.__db,charset=self.__charset)
            print '连接数据库 %s 成功！'%(self.__host)
            self.__cur = self.__conn.cursor()
        except BaseException as e:
            print e

    def fetch(self,sql,args=()):
        _cnt =0
        _rt_tuple = ()
        _cnt = self.execute(sql,args=())
        if self.__cur:
           _rt_tuple = self.__cur.fetchall()
           self.close()
           print "_rt_tuple:",_rt_tuple
        print 'cnt and rt_tuple:',_cnt,_rt_tuple


    def commit(self):
        #成功连接数据库才能commit
        if self.__conn:
            self.__conn.commit()

    def execute(self,sql,args=()):
        _cnt = 0
        if self.__cur:
           _cnt = self.__cur.execute(sql,args)
        return _cnt


    def close(self): 
        #在连接关闭时防止没有flush(将内存数据写入数据库)
        self.commit()
        if self.__cur:
            self.__cur.close()
            self.__cur = None
        if self.__conn:
            self.__conn.close()
            self.__conn = None

   


#函数方式思路
#select 需要使用fetchall，所以我们可以归类
def execute_fetch_sql(sql,args=()):
    return execute_sql(sql,args,True)

#update,insert,delete 都需要commit，所以我们可以将他们归类
def execute_commit_sql(sql,args=()):
    return execute_sql(sql,args,False)

def execute_sql(sql,args=(),fetch=True):
    _conn = None
    _cur = None
    _count =0
    _rt_tuple = ()
    try:
        #创建和数据库的连接
        _conn = MySQLdb.connect(host=gconf.MYSQL_HOST,port=gconf.MYSQL_PORT, \
                               user=gconf.MYSQL_USER,passwd=gconf.MYSQL_PASSWD, \
                               db=gconf.MYSQL_DB,charset=gconf.MYSQL_CHARSET)
        #_conn.autocommit(True)
        #创建游标
        _cur = _conn.cursor()
        #执行SQL
        _count = _cur.execute(sql,args)
        if fetch:
            _rt_tuple = _cur.fetchall()
            print "_rt_tuple:%s" %_rt_tuple
        else:
            _conn.commit()                    #commit和autocommit(True)任选其一
    except BaseException as e:
        print e
    finally:
        if _cur:
           _cur.close()
        if _conn:
           _conn.close()

    return _count,_rt_tuple


def bulker_commit_sql(sql,args_list=[]):
    _conn = None
    _cur = None
    _count =0
    _rt_tuple = ()
    try:
        #创建和数据库的连接
        _conn = MySQLdb.connect(host=gconf.MYSQL_HOST,port=gconf.MYSQL_PORT, \
                               user=gconf.MYSQL_USER,passwd=gconf.MYSQL_PASSWD, \
                               db=gconf.MYSQL_DB,charset=gconf.MYSQL_CHARSET)
        #_conn.autocommit(True)
        #创建游标
        _cur = _conn.cursor()
        for _args in args_list:
            #循环执行SQL
            print sql
            _count+=_cur.execute(sql,_args)
        _conn.commit()                    #commit和autocommit(True)任选其一
    except BaseException as e:
        print e
    finally:
        if _cur:
           _cur.close()
        if _conn:
           _conn.close()

    return _count,_rt_tuple


if __name__ == "__main__":
    conn = MySQLConnection(host=gconf.MYSQL_HOST,port=gconf.MYSQL_PORT, \
                               user=gconf.MYSQL_USER,passwd=gconf.MYSQL_PASSWD, \
                               db=gconf.MYSQL_DB)
    #conn.execute('insert into user_auth(username) values(%s)',('dick123',))
    conn.fetch("select * from user_auth")
    conn.close()
    