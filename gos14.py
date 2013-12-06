from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

# WTForm
from flask_wtf import Form
from wtforms import PasswordField, SubmitField, TextField, Form
from wtforms.validators import DataRequired

# Database
from database import db_session
from database import init_db
from models import User, Entry

# Flask-Login
from flask.ext.login import LoginManager, login_user, login_required, current_user

import httplib
import requests
import os
import json
import urllib

# create our little application :)
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
login_manager = LoginManager()
login_manager.init_app(app)

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
    """Template for the login form."""
    username = TextField('username')
    email = TextField('email')
    password = PasswordField('password')
    submit = SubmitField('Login')


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# Resource for User Class
@app.route('/users', methods=['GET', 'POST'])
def users():
    """
    If methods == 'POST', a new user is created,
    if methods == 'GET', a list of all user is displayed.
    """
    if request.method == 'POST':
        form = LoginForm(request.values)
        u = User(form.username.data, form.email.data, form.password.data)
        db_session.add(u)
        db_session.commit()
        flash('Account created! You can now login!')
        return render_template('login.html', form=form)
    if request.method == 'GET':
        users = User.query.all()
        return render_template('users.html', users=users)


@app.route('/')
def home():
    """Display the defaut page."""
    if 'logged_in' in session:
        db = get_db()
        cur = db.execute('select id, title, text from entries order by id desc')
        entries = cur.fetchall()
        print(entries)
        return render_template('home.html', users=entries)
    else:
        form = LoginForm()
        return render_template('login.html', form=form)

@app.route('/entries', methods=['GET','POST'])
def entries():
    """
    If methods == 'POST', a new entry is created,
    if methods == 'GET', a list of entries is displayed.
    """
    if request.method == 'GET':
        db = get_db()
        cur = db.execute('select id, title, text from entries order by id desc')
        entries = cur.fetchall()
        return render_template('entries.html', entries=entries)
    if request.method == 'POST':
        if not session.get('logged_in'):
            abort(401)
        # db = get_db()
        # db.execute('insert into entries (title, text) values (?, ?)',
                     # [request.form['title'], request.form['text']])
        entry = Entry(request.form['title'], request.form['text'])
        db_session.add(entry)
        db_session.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('entries'))

@app.route('/entries/<int:entry_id>')
def show_entry(entry_id):
    """Display a specific entry."""
    entry = Entry.query.get(entry_id)
    return render_template('show_entry.html', entry=entry)


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Performs the login option."""
    form = LoginForm(request.values)
    error = None
    if request.method == 'POST':
        user = User.query.filter_by(username = form.username.data).first()
        if user is not None and user.password == form.password.data:
            session['logged_in'] = True
            login_user(user)
            flash('You were logged in')
            return redirect(url_for('home'))
    flash('Username/password incorrect')
    return render_template('login.html', error=error, form=form)

@app.route('/searchbyimage')
def searchbyimage():
    return render_template('searchbyimage.html')

@app.route('/help')
def help():
    return render_template('help.html');
@app.route('/uploadimage', methods=['POST'])
def uploadimage():
    uploadedfile = request.files['url_image']
    print uploadedfile
    path = os.path.join('images_tmp', uploadedfile.filename)
    uploadedfile.save(path)

    headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
    }
    r = requests.get('http://www.google.fr/searchbyimage?image_url=' + 'http://nuitdelinfo.univ-reunion.fr:2057/' + uploadedfile.filename, headers=headers)
    print r.status_code
    body = r.text
    body = body.encode('utf-8')
    sbiq = '"sbiq":"'
    sbiqpos = body.find(sbiq)
    quotepos = body.find('"',sbiqpos + len(sbiq)) 
    
    # keywords contains very precise description of the image but we only take the first keyword for simplicity
    keywords = body[sbiqpos + len(sbiq) : quotepos]
    keyword = keywords[:keywords.find(' ')]
    print keyword
    os.remove(os.path.join('images_tmp', uploadedfile.filename))

    # api_key = open(".freebase_api_key").read()
    service_url = 'https://www.googleapis.com/freebase/v1/mqlread'
    params = '[{  "type": "/business/consumer_product", "id": null, "name~=": "' + keyword + '" }]'
    url = service_url + '?query=' + params
    topic = json.loads(urllib.urlopen(url).read())
    return json.dumps(topic)
#    for property in topic['property']:
#        print property + ':'
#        for value in topic['property'][property]['values']:
#            print ',' + value['text'].encode('utf-8')
#    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    """Logout the user."""
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=2053)
