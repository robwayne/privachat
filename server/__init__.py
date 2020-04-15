from flask import Flask, render_template, redirect, url_for
import os
import functools

from db import sqlitedb
from blueprints.auth import blueprint as auth_blueprint
from blueprints.chats import blueprint as chats_blueprint

# https://flask.palletsprojects.com/en/1.1.x/tutorial/database/

# create and configure the app
app=Flask(__name__, template_folder='templates', instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'privachat.sqlite'),
)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    print(" *** Couldn't create instance path directory ***")
    

 #here im also registering all the authentication and message views with the app   
app.register_blueprint(auth_blueprint)
app.register_blueprint(chats_blueprint)

# setting the home to be '/' and to use the chat url
@app.route('/')
def redirectToChat():
    return redirect(url_for('chats.index'), code=302)


sqlitedb.initAppDatabase(app)