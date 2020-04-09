import sqlite3

from flask import current_app, g
from flask.cli import with_appcontext
import click

def getDatabase():
	if 'db' not in g:
		g.db = sqlite3.connect(
			current_app.config['DATABASE'],
			detect_types=sqlite3.PARSE_DECLTYPES
		)
		g.db.row_factory = sqlite3.Row
		
	return g.db
		
		
def closeDatabase(e=None):
	database = g.pop('db', None)
	if database is not None:
		database.close()
		
		
def initDatabase():
	database = getDatabase()
	with current_app.open_resource('../db/schema.sql') as f:
		database.executescript(f.read().decode('utf8'))
		

@click.command('initDatabaseCLI')
@with_appcontext
def initDatabaseCLICommand():
	print("inside module3")
	initDatabase()
	click.echo('*** Database initialized *****')
	
	
def initAppDatabase(app):
	print("inside module")
	# close the previous database connection if there is one
	app.teardown_appcontext(closeDatabase)
	print("inside module2")
	#add the databse cli command to the current app obj
	app.cli.add_command(initDatabaseCLICommand)
		
		
