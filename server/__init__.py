from flask import Flask, render_template, current_app
import os
import functools

from db import sqlitedb
from auth.auth import blueprint as auth_blueprint
from messages.messages import blueprint as messages_blueprint

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
    
app.register_blueprint(auth_blueprint)
app.register_blueprint(messages_blueprint)
app.add_url_rule('/', endpoint='index')

sqlitedb.initAppDatabase(app)


# return app