from flask import Blueprint, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from datetime import datetime

from blueprints.auth import loginRequired
from db.sqlitedb import getDatabase
from inspect import getmembers

blueprint = Blueprint('chats', __name__, url_prefix='/chat')

def getOnlineUsers(db):
	query = 'SELECT * from users WHERE isOnline == 1 AND id <> ?'
	onlineUsers = db.execute(query, (str(g.user['id']))).fetchall()
	return onlineUsers
	
def getMessages(db, forChatId=None):
	query = ("SELECT distinct users.username, users.profile_img_url, "
		"messages.sender_id, messages.msg, messages.time_sent FROM ((users "
		"JOIN messages ON users.id == messages.sender_id) "
		"LEFT JOIN chats ON messages.belongs_to == chats.id) WHERE messages.belongs_to")

	messages = []
	if forChatId:
		print("CHAT_ID", forChatId)
		query += " == ?"
		messages = db.execute(query, (forChatId,)).fetchall()
	else:
		query += " is NULL"
		messages = db.execute(query).fetchall()

	print('MESSAGES', messages)
	return messages

@blueprint.route('/', methods=['GET', 'POST'])
@loginRequired  # require each user to be logged in before viewing the home page
def index():
	database = getDatabase()
	messages = []
	
	# if the user is sending a post request - it means they are typing a message to be shown
	if request.method == 'POST':
		enteredText = request.form['messagebox'] # remember to check if request sanitizes the input for me
		if enteredText: #if the message is not empty
			if g.user:
				query = 'INSERT INTO messages (msg, sender_id) values (?,?)'
				database.execute(query, (enteredText, g.user['id'])) # we add a new message to the db
				database.commit()
			else:
				flash('You need to be logged in to chat!')
				
			return redirect(url_for('chats.index')) # we then redirect them back to the current index.html page so they can continue messging
	
	messages = getMessages(database) # get a list of all the messages and show them
	for message in messages:
		print(message['username'])
	onlineUsers = getOnlineUsers(database)
	
	return render_template('index.html', messages=messages, onlineUsers=onlineUsers, title='Universal Chat') # the home page (index) template will display all the messages

@blueprint.route('/<author_id>/<receiver_id>', methods=['GET', 'POST'])
@loginRequired  # require each user to be logged in before viewing the home page
def privateChat(author_id, receiver_id):
	database = getDatabase()
	onlineUsers = getOnlineUsers(database)
	messages = []

	# find the chat and its id that is specific to these users
	query = ("SELECT chats.id FROM chats "
			"LEFT JOIN users ON chats.author_id == users.id "
			"WHERE chats.author_id == ? AND chats.receiver_id == ?")

	chatId = database.execute(query, (author_id, receiver_id)).fetchone()

	#reverse query and check again if nothing found
	if not chatId:
		chatId = database.execute(query, (receiver_id, author_id)).fetchone()

	#if still no chat is found - assume it doesnt exist and create a new one
	if not chatId:
		query = 'INSERT INTO chats (author_id, receiver_id) values (?,?)'
		lastInsertedRowId = database.execute(query, (author_id, receiver_id)).lastrowid
		query = 'SELECT id FROM chats WHERE rowid == ?'
		chatId = database.execute(query, (lastInsertedRowId,)).fetchone()

	chatId = chatId['id'] if chatId else 0

	if request.method == 'POST': 
		enteredText = request.form['messagebox'] # remember to check if request sanitizes the input for me
		if enteredText: #if the message is not empty
			if g.user:
				query = 'INSERT INTO messages (msg, sender_id, belongs_to) values (?,?,?)'
				database.execute(query, (enteredText, g.user['id'], chatId)) # we add a new message to the db
				database.commit()
			else:
				flash('You need to be logged in to chat!')
				
			return redirect(request.url) 

	messages = getMessages(database, forChatId=chatId)
	return render_template('index.html', messages=messages, onlineUsers=onlineUsers, title='Private Message')

