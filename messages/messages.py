from flask import Blueprint, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from datetime import datetime

from auth.auth import loginRequired
from db.sqlitedb import getDatabase

blueprint = Blueprint('messages', __name__)

# https://flask.palletsprojects.com/en/1.1.x/tutorial/blog/

@blueprint.route('/')
def index():
    database = getDatabase()
    now = datetime.now()
    messages = database.execute('SELECT * from messages').fetchall()
    messages = [{"id":"1", "sender": 'robert', 'sent_at':now, 'msg':'my first simulated message'}]
    return render_template('index.html', messages=messages)
     