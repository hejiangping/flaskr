# -*- coding: UTF-8 -*-

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import sqlite3
from contextlib import closing
import os
from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash


app = Flask(__name__)
app.config.update(dict(
DATABASE = os.path.join(app.root_path, 'flaskr.db'),
DEBUG = True,
SECRET_KEY = 'HeLLoWORld',
USERNAME = 'admin',
PASSWORD = 'default',
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

#数据库
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql') as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.before_request
def before_request():
	g.db=connect_db()

@app.teardown_request
def teardown_request(exception):
	g.db.close()

#主页
@app.route('/')
def index():
	return render_template('layout.html')

#登录
@app.route('/login', methods=['GET', 'POST'])
def  login():
	error=None
	if request.method=='POST':
		cur=g.db.cursor().execute('select username from users')
		usernameList = [str(row[0]) for row in cur.fetchall()]
		if request.form['username'] not in usernameList:
			error =  'Invalid username'
		else:
			cur=g.db.cursor().execute('select password from users where username=(?)',
				[request.form['username']])
			usernameList = [str(row[0]) for row in cur.fetchall()]
			if request.form['password'] not in usernameList:
				error = 'Password error'
			else:
				session['logged_in']=True
				return render_template('layout.html')
	return render_template('login.html',error=error)

#注销
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	return render_template('layout.html')

#注册
@app.route('/register',methods=['GET','POST'])
def register():
	error=None
	msg=None
	if request.method == 'POST':
		if request.form['username'] =='' or request.form['password'] == '':
			error = 'Please fill something'
		else:
			cur = g.db.cursor().execute('select username from users')
 			usernameList = [str(row[0]) for row in cur.fetchall()]
			if request.form['username'] in usernameList:
                			error = 'The username has been registered.'
            		elif len(request.form['password'])<6 or len(request.form['password'])>16:
                			error='Password length need between 6 to 16'
            		else:
                			g.db.cursor().execute('insert into users(username,password)  values(?,?)',
                				[request.form['username'],request.form['password']])
	if error is None:
            	g.db.commit()
            	return render_template('register.html',msg = 'Register Success')
	return render_template('register.html',error = error)



if __name__ == '__main__':
    app.run()









