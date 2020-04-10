import functools

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from db.sqlitedb import getDatabase


blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		confirmPassword = request.form['confpassword']
		database = getDatabase()
		error = None
		
		if not username:
			error = 'Username is required!'
		elif not password:
			error = 'Password is required!'
		elif not confirmPassword:
			error = 'Confirm your password!'
		elif confirmPassword != password:
			error = 'Passwords do not match'
		else:
			query = 'SELECT id from users WHERE username == ?'
			user = database.execute(query, (username,)).fetchone()
			if user is not None:
				error = username + ' is already registered. Try logging in'
			
		if error is None:
			hash_pwd = generate_password_hash(password)
			query = 'INSERT INTO users (username, password) values (?, ?)'
			database.execute(query, (username, hash_pwd))
			database.commit()
			return redirect(url_for('auth.login'))
				
		flash(error)
			
	return render_template('register.html')
		
		
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		database = getDatabase()
		error = None
		
		if not username:
			error = 'Username is required!\n'
		elif not password:
			error = 'Password is required!\n'
		else:
			query = 'SELECT * from users WHERE username == ?'
			user = database.execute(query, (username,)).fetchone()
			if user is None:
				error = username + ' is not registered. Try signing up'
			else:
				hash_pwd = user['password']
				if not check_password_hash(hash_pwd, password):
					error = ' Incorrect password'
					
		if error is None:
			session.clear()
			session['user_id'] = user['id']
			return redirect(url_for('index'))
			
		flash(error)
	
	return render_template('login.html')
		

@blueprint.before_app_request
def loadCurrentUser():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = getDatabase().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()

def loginRequired(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('auth.login'))
			
		return view(**kwargs)
	
	return wrapped_view

@blueprint.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('auth.login'))


