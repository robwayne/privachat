import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from db.sqlitedb import getDatabase

blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		#get the data from the registration form
		username = request.form['username']
		password = request.form['password']
		confirmPassword = request.form['confpassword']
		database = getDatabase()
		error = None
		
		# check to ensure passwords and username are all valid and non-empty
		if not username:
			error = 'Username is required!'
		elif not password:
			error = 'Password is required!'
		elif not confirmPassword:
			error = 'Confirm your password!'
		elif confirmPassword != password:
			error = 'Passwords do not match'
		else:
			# here im checking if the username already exists,
			query = 'SELECT id from users WHERE username == ?'
			user = database.execute(query, (username,)).fetchone()
			if user is not None: # if it does - show the error message that user already exists
				error = username + ' is already registered. Try logging in'
			
		if error is None:
			# if we have valid pwd and username we can then register the user
			hash_pwd = generate_password_hash(password)
			query = 'INSERT INTO users (username, password) values (?, ?)'
			database.execute(query, (username, hash_pwd))
			database.commit()
			return redirect(url_for('auth.login'))
				
		flash(error) #if there are errors show the errors
			
	return render_template('register.html')
		
		
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		#get the data from the login form
		username = request.form['username']
		password = request.form['password']
		database = getDatabase()
		error = None
		
		#check if username and pwds are valid like before 
		if not username:
			error = 'Username is required!\n'
		elif not password:
			error = 'Password is required!\n'
		else:
			query = 'SELECT * from users WHERE username == ?'
			user = database.execute(query, (username,)).fetchone()
			if user is None: # if the username isnt regiastered tell them to sign up/register
				error = username + ' is not registered. Try signing up'
			else:
				hash_pwd = user['password']
				if not check_password_hash(hash_pwd, password):
					error = ' Incorrect password'
					
		if error is None:
			# if there are no errors we can clear the previous session and then log the user in
			session.clear()
			session['user_id'] = user['id']
			return redirect(url_for('index'))
			
		flash(error)
	
	return render_template('login.html')
		
# i used this to allow me to check before every user request if the user is logged in
@blueprint.before_app_request
def loadCurrentUser():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None # set to none if there isnt a current user logged in
    else:
        g.user = getDatabase().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone() # set the sessions current user

@blueprint.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('auth.login'))

#I used this function to ensure each user is logged in -  it is used later in messages.py
def loginRequired(view):
	@functools.wraps(view)
	def wrappedView(**kwargs):
		if g.user is None: # if the user isnt logged in
			return redirect(url_for('auth.login')) # redirect them to the login page 
			
		return view(**kwargs)
	
	return wrappedView