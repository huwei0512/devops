#encoding:utf-8
import os
from flask import Flask

app = Flask(__name__)
app.secret_key = os.urandom(32)

import views