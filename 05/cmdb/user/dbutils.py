#encoding:utf-8
import MySQLdb
import gconf

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