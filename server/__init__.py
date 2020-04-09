from flask import Flask, render_template, current_app
import os
from db import sqlitedb

# https://flask.palletsprojects.com/en/1.1.x/tutorial/database/


# create and configure the app
app=Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'privachat.sqlite'),
)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    print(" *** Couldn't create instance path directory ***")

# a simple page that says hello
@app.route('/hello')
def hello():
    return 'Hello, World!'


@app.route('/login')
def login():
    # login_path = os.path.join(current_app.instance_path, 'login.html')
    # return render_template(login_path)
    return 'login'

sqlitedb.initAppDatabase(app)

# return app