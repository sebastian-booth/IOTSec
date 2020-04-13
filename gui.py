# data gen code from https://stackoverflow.com/a/15042327
# Login code from https://github.com/maxcountryman/flask-login
# Encryption code from https://pypi.org/project/pycrypto/

# TODO:
# Pretty much done

import flask
from flask import *
import db
from Crypto.Cipher import AES
import flask_login
import socket

app = flask.Flask(__name__)
app.config['SESSION_COOKIE_HTTPONLY'] = False # VERY unlikely you will see httponly purposefully being set to false
                                                # from default flask true but some bespoke production platforms
app.secret_key = '6D4FQsRvlY4L0pzoHXf5wulKPoWPG3Cxz_yHpNU9er8' # may not have manually set the session cookie to be httponly

app.url_map.strict_slashes = False

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
            key = b'0123456789abcdef'
            iv = b'0123456789abcdef'
            global cookie_numb
            obj2 = AES.new(key,AES.MODE_CBC, iv=iv) # change key and iv at some point
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            client.connect(("192.168.1.146", 42186)) # IP and port of IOT devices usually hard coded into gui app
            random_word_encrypt = client.recv(1024)
            random_word = obj2.decrypt(random_word_encrypt)
            random_word = random_word[0: len(random_word)//16]
            random_word = random_word.decode('utf-8')
            rand_list.append(random_word)
            cookie_numb = int(cookie_numb)
            cookie_numb += 1
            cookie_numb = str(cookie_numb)
            cookie_name = "Cookie" + cookie_numb
            resp = make_response(jsonify(rand_list))
            resp.set_cookie(cookie_name,random_word)
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

@app.route('/feedback', methods=['POST', 'GET']) # Code from https://github.com/bgres/xss-demo/blob/master/app.py
def index():                                    # A 'feedback' page is unlikely to appear on a IOT platform
    if request.method == 'POST':                # But I needed somewhere to utilise a XSS vulnerability
        db.add_comment(request.form['comment'])

    search_query = request.args.get('q')

    comments = db.get_comments(search_query)

    return render_template('index.html',comments=comments,search_query=search_query)


app.run(debug=True)