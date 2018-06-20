#encoding:utf-8

from flask import Flask
from flask import render_template
import loganalysis
import time


app = Flask(__name__)

@app.route('/')
def index():
    return 'hello,reboot'


@app.route("/logs/")
def logs():
    logfile = "/root/example.log"

    rt_list = loganalysis.get_topn(logfile=logfile)
    return render_template('logs.html',rt_list=rt_list,title="topn_log")


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=9003,debug=True)