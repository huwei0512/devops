#encoding:utf-8
import sys,os,time,json
reload(sys)
sys.setdefaultencoding('utf-8')           #设置命令行为utf-8

from flask import Flask                   #从flask包导入Flask类
from flask import render_template         #从flask包导入render_template函数
from flask import request                 #从flask包导入request对象
from flask import redirect                #从flask包导入redirect函数
from flask import url_for
from flask import session
from functools import wraps
from flask import flash
import loganalysisdb as loganalysis                   #导入loganalysis模块
import userdb as user                #导入userdb模块
import time
import log2db
import asset
from user import app  #  user模块下的app变量(Flask对象)
from models import User

def login_required(func):

    @wraps(func)
    def wrapper():
        if session.get('user') is None:
            return redirect('/login/')
        rt = func()
        return rt
    return wrapper



'''打开用户登录页面
'''
@app.route('/')                            #将url path=/的请求交由index函数处理
def index():
    return render_template('login.html')   #加载login.html模板，并返回页面内容


@app.route("/logs/")
@login_required
def logs():

    topn = request.args.get('topn',10)
    topn = int(topn) if str(topn).isdigit() else 10
    
    rt_list = loganalysis.get_topn(topn=topn)
    return render_template('logs.html',rt_list=rt_list,title="topn_log")

'''用户登录信息检查
'''
@app.route('/login/',methods=["POST","GET"])       #将url path=/login/的POST或GET请求交由login函数处理
def login():

    params = request.args if request.method == "GET" else request.form

    username = params.get("username","")           #接收用户提交的数据
    password = params.get("password","")
    
    #需要验证用户名密码是否正确
    _user = User.validate_login(username,password)
    if _user:
        session['user'] = _user
        return redirect("/users/")                 #跳转到url /users/
    else:
        #登录失败
        return render_template("login.html",username=username,error=u"用户名或密码错误！")

'''用户列表显示
'''
@app.route("/users/")                              #将url path=/users/的GET请求交由users函数处理
def users():
    #获取所有用户信息
    _users = User.get_list()
    print 'view_user:',_users
    return render_template("users.html",user_list=_users)  #加载渲染user.html模板

'''跳转到新建用户信息输入的页面
'''
@app.route("/user/create/")                       #将url path=/user/create/的GET请求交由create_user处理
@login_required 
def create_user():
    return render_template('user_create.html')     #加载渲染user_create.html

'''存储新建用户的信息
'''
@app.route("/user/update-inputuser/",methods=['POST'])          #将url path=/user/add的POST请求交由add_user函数处理
@login_required 
def add_user():
    username = request.form.get("username",'')
    password = request.form.get("password",'')
    age = request.form.get('age','')
    # gender = request.form.get("gerder",'0')
    # hobby = request.form.getlist('hobby')
    # img = request.files.get("img")
    # if img:
    #     print img.filename
    #     img.save('/tmp/dick.txt')
    # print request.form
    # print gender
    # print hobby

    #检查用户信息
    _is_ok,_error = User.validate_add(username,password,age)
    if _is_ok:
        User.add(username,password,age)
    return json.dumps({'_is_ok':_is_ok,'error':_error})
        # return redirect(url_for('users'))        #跳转到用户列表url_for
    

'''打开用户信息修改页面
'''
@app.route("/user/modify/")          #将url path=/user/modify的POST请求交由modify_user函数处理
@login_required 
def modify_user():
    uid = request.args.get('id','')
    _user = user.get_user(uid)
    _uid = ""
    _error = ""
    _username = ""
    _password = ""
    _age = ""
    if _user is None:
        _error = "用户信息不存在"
    else:
        _uid = _user.get("id")
        _username = _user.get("username")
        _password = _user.get("password")
        _age = _user.get("age")
    return render_template('user_modify.html',error=_error,password=_password,age=_age,username=_username,uid=_uid)

'''保存修改用户数据
'''
@app.route('/user/charge-user/',methods=['POST'])               #将url path=/user/update/的POST请求交由update_user函数处理
@login_required 
def update_user():
    uid = request.form.get('userid','')
    username = request.form.get('username','')
    password = request.form.get('password','')
    age = request.form.get('age','')
    
    #检查用户信息
    _is_ok,_error = user.validate_update_user(uid,username,password,age)
    if _is_ok:
        user.update_user(uid,username,password,age)
    return json.dumps({'_is_ok':_is_ok,'error':_error})



@app.route('/user/delete/')        
@login_required 
def delete_user():
    uid = request.args.get('id','')
    user.delete_user(uid)
    flash("删除用户信息成功")
    return redirect('/users/')

@app.route('/logout/')        
def login_out():
    session.clear()
    #del session['user']
    #del session['id']
    print session
    return redirect('/')

@app.route("/uploadlogs/",methods=["POST"])
def uploadlogs():
    _file = request.files.get('logfile')
    if _file:
        _filepath = 'temp/%s' % time.time()
        _file.save(_filepath)
        log2db.log2db(_filepath)
    return redirect('/logs/')


@app.route('/test/',methods=['POST','GET'])        
def test():
    print 'request.args:',request.args
    print 'request.form:',request.form
    print 'request.files:',request.files
    print 'request.headers:',request.headers
    return render_template('test.html')

@app.route('/user/charge-password/',methods=['POST'])               #将url path=/user/update/的POST请求交由update_user函数处理
@login_required 
def modify_user_passwd():
    user_id = request.form.get('userid','')
    admin_passwd = request.form.get('admin-password','')
    user_passwd = request.form.get('user-password','')
    
    #检查管理员密码信息
    _is_ok,_error = user.validate_admin_passwd(user_id,user_passwd,session['user']['username'],admin_passwd)
    if _is_ok:
       user.update_user_passwd(user_id,user_passwd)
    return json.dumps({'_is_ok':_is_ok,'error':_error})

'''资产列表显示
'''
@app.route("/assets/")
@login_required
def assets():
    #获取所有资产信息
    _assets = asset.get_asset_list()
    return render_template("assets.html",assets=_assets,idcs_dict=dict(asset.get_idc_list()))

@app.route('/asset/create/',methods=['POST','GET'])
@login_required
def asset_create():
    
    return render_template('asset_create.html',idcs=asset.get_idc_list())

@app.route('/asset/add/',methods=['POST','GET'])
@login_required
def asset_add():
    #检查用户信息
    _is_ok,_error = asset.validate_create_asset(request.form)
    if _is_ok:
        asset.create_asset(request.form)
    return json.dumps({'_is_ok':_is_ok,'error':_error,'success':'资产添加成功'})


@app.route('/asset/modify/',methods=['POST','GET'])
@login_required
def asset_modify():
    _id = request.args.get('id', '')
    _asset = asset.get_by_id(_id)
    return render_template('asset_modify.html',asset=_asset,idcs=asset.get_idc_list())

@app.route('/asset/update/',methods=['POST','GET'])
@login_required
def asset_update():
    #检查用户信息
    _is_ok,_error = asset.validate_update_asset(request.form)
    if _is_ok:
        asset.update_asset(request.form)
    return json.dumps({'_is_ok':_is_ok,'error':_error,'success':'资产修改成功'})



@app.route('/asset/delete/')        
@login_required 
def delete_asset():
    aid = request.args.get('id','')
    asset.delete_asset(aid)
    flash("删除资产信息成功")
    return redirect('/assets/')