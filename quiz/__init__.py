# 2d quiz generator
# 
# a bsd-licensed bidimensional quiz generator written in flask
# author: v0idpwn
# v0idpwn.github.io/2dqg

import os

from flask import Flask

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, '/tmp/2dqg.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASK_SETTINGS', silent=True)

import quiz.views
