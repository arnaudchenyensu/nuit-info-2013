# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~

    A microblog example application written as Flask tutorial with
    Flask and sqlite3.

    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
# from flaskext.bcrypt import Bcrypt

# WTForm
from flask_wtf import Form
from wtforms import PasswordField, SubmitField, TextField, Form
from wtforms.validators import DataRequired

# Database
from database import db_session
from database import init_db
from models import User

import httplib
import requests
import os

# create our little application :)
app = Flask(__name__)
# bcrypt = Bcrypt(app)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE='/tmp/test.db',
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
# app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# Create the login form.
class LoginForm(Form):
    username = TextField('username')
    email = TextField('email')
    password = PasswordField('password')
    submit = SubmitField('Login')


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


# def init_db():
#     """Creates the database tables."""
#     with app.app_context():
#         db = get_db()
#         with app.open_resource('schema.sql', mode='r') as f:
#             db.cursor().executescript(f.read())
#         db.commit()



def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


# @app.teardown_appcontext
# def close_db(error):
#     """Closes the database again at the end of the request."""
#     if hasattr(g, 'sqlite_db'):
#         g.sqlite_db.close()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# Resource for User Class
@app.route('/users', methods=['POST'])
def add_user():
    form = LoginForm(request.values)
    u = User(form.username.data, form.email.data, form.password.data)
    db_session.add(u)
    db_session.commit()
    # return u
    # User.query.all()
    # [<User u'admin'>]
    # User.query.filter(User.name == 'admin').first()
    # <User u'admin'>
    return render_template('login.html', form=form)


@app.route('/')
def home():
    if 'logged_in' in session:
        return render_template('home.html')
    else:
        form = LoginForm()
        return render_template('login.html', form=form)

@app.route('/searchbyimage')
def searchbyimage():
    return render_template('searchbyimage.html')

@app.route('/uploadimage', methods=['POST'])
def uploadimage():
    uploadedfile = request.files['url_image']
    print uploadedfile
    path = os.path.join('/home/equipe1/www/goodcommerce/images_tmp', uploadedfile.filename)
    uploadedfile.save(path)

    headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
    }
    r = requests.get('http://www.google.fr/searchbyimage?image_url=' + 'http://nuitdelinfo.univ-reunion.fr:2057/' + uploadedfile.filename, headers=headers)
    print r.status_code
    # print r.text.encode('ascii')
    body = r.text
    body = body.encode('utf-8')
    sbiq = '"sbiq":"'
    sbiqpos = body.find(sbiq)
    quotepos = body.find('"',sbiqpos + len(sbiq)) 
    print body[sbiqpos:sbiqpos+50]
    print body[sbiqpos + len(sbiq) : quotepos]

    # file = open('/tmp/googleresult', 'w')
    # file.write(r.text)
    # file.close()

    print r.request.headers

    return redirect(url_for('home'))

@app.route('/entries')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if request.method == 'POST':
        db = get_db()
    	cur = db.execute('select username, password from users where username = ? and password = ?', [request.form['username'], request.form['password']])
	results = cur.fetchall()
	for row in results:
	    username = row[0]
            password = row[1]
            print "-> logged in : username=%s,password=%s" % (username, password)

        if len(results) <= 0:
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('home'))
    flash('ERROR')
    return render_template('login.html', error=error, form=form)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0',port=2053)
