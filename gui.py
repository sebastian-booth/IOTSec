# data gen code from https://stackoverflow.com/a/15042327
# Login code from https://github.com/maxcountryman/flask-login

import flask
from flask import make_response
from flask import jsonify
from flask import session
from flask import redirect
from flask import url_for
import time
import test
import random
import string
import flask_login
import socket

app = flask.Flask(__name__)

app.secret_key = 'dv7XzvYUOigmX32oOBL5cbEAzylQOtFJf/4Nk0fVKZY'

login_manager = flask_login.LoginManager()

login_manager.init_app(app)

users = {'sbooth_csc': {'password': 'pass'}}

rand_list = []
cookie_numb = 0

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user

@app.route('/')
def init():
    return flask.redirect(flask.url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='username' id='username' placeholder='username' required/>
                <input type='password' name='password' id='password' placeholder='password' required/>
                <input type='submit' name='submit'/>
               </form>
               '''

    username = flask.request.form['username']
    if username not in users:
        return 'Incorrect login'
    if flask.request.form['password'] == users[username]['password']:
        user = User()
        user.id = username
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))

    return 'Incorrect login'

@app.route('/protected')
@flask_login.login_required
def protected():
            global cookie_numb
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            client.connect(("localhost", 42180))
            random_string = client.recv(1024)
            random_string = random_string.decode("utf-8")
            rand_list.append(random_string)
            cookie_numb = int(cookie_numb)
            cookie_numb += 1
            cookie_numb = str(cookie_numb)
            cookie_name = "Cookie" + cookie_numb
            resp = make_response(jsonify(rand_list))
            resp.set_cookie(cookie_name,random_string)
            return resp  # text/html is required for most browsers to show the partial page immediately

@app.route('/del-cookies')
@flask_login.login_required
def delete_cookies(): # All cookie delete script from https://stackoverflow.com/a/27374365
    return '<script>document.cookie.split(";").forEach(function(c) { document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); });</script>'


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

app.run(debug=True)