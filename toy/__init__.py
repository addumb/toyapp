import sqlite3
import time

from flask import Flask, request, render_template, request, session, g, redirect, url_for, abort, flash

DATABASE = 'db.sqlite'
DEBUG = True
SECRET_KEY = 'f04cts3084tuv;eoz8vnz;eorg8uzn;'
USERNAME = 'admin'
PASSWORD = 'totallysecure'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

import toy.views
