import sqlite3

from flask import current_app, g
from flask.cli import with_appcontext
import click


# This file is kind of independent of the webchat project - but is needed for the database to allow users to log in
# and messages to be saved


# here we either create a new instance of the sqlite database or use the previously created one
# for the connections and requests
def getDatabase():
	if 'db' not in g:
		g.db = sqlite3.connect(
			current_app.config['DATABASE'],
			detect_types=sqlite3.PARSE_DECLTYPES
		)
		g.db.row_factory = sqlite3.Row
		
	return g.db
		
# close the database whenever the app has closed		
def closeDatabase(e=None):
	database = g.pop('db', None)
	if database is not None:
		database.close()
		
# this initializes the actual sqlite database - dropping the tables if they existed and then recreating them		
def initDatabase():
	database = getDatabase()
	with current_app.open_resource('../db/schema.sql') as f:
		database.executescript(f.read().decode('utf8'))
		

# setup the terminal command that initializes the database
@click.command('initDatabaseCLI')
@with_appcontext
def initDatabaseCLICommand():
	initDatabase()
	click.echo('*** Database initialized *****')
	

# connect the database to the actual pythion app 
def initAppDatabase(app):
	# close the previous database connection if there is one
	app.teardown_appcontext(closeDatabase)
	#add the databse cli command to the current app obj
	app.cli.add_command(initDatabaseCLICommand)
		
		
