from flask import Blueprint, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from datetime import datetime

from blueprints.auth import loginRequired
from db.sqlitedb import getDatabase

blueprint = Blueprint('messages', __name__)

@blueprint.route('/test')
def hello():
	print("tessttutututututinnnng")
	return 'test the world'

@blueprint.route('/', methods=['GET', 'POST'])
@loginRequired  # require each user to be logged in before viewing the home page
def index():
	database = getDatabase()
	messages = []
	onlineUsers = []
	
	# if the user is sending a post request - it means they are typing a message to be shown
	if request.method == 'POST':
		enteredText = request.form['messagebox'] # remember to check if request sanitizes the input for me
		if enteredText: #if the message is not empty
			if g.user:
				query = 'INSERT INTO messages (msg, sender_id, sender, profile_img_url) values (?,?,?,?)'
				database.execute(query, (enteredText, g.user['id'], g.user['username'], g.user['profile_img_url'])) # we add a new message to the db
				database.commit()
			else:
				flash('You need to be logged in to chat!')
				
			return redirect(url_for('index')) # we then redirect them back to the current index.html page so they can continue messging
	
	query = 'SELECT * from messages'
	messages = database.execute(query).fetchall() # get a list of all the messages and show them

	query = 'SELECT * from users WHERE isOnline == 1 AND id <> ?'
	onlineUsers = database.execute(query, (str(g.user['id']))).fetchall()
	
	return render_template('index.html', messages=messages, onlineUsers=onlineUsers) # the home page (index) template will display all the messages


