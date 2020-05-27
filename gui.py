import flask # https://flask.palletsprojects.com/en/1.1.x/
from flask import * # https://flask.palletsprojects.com/en/1.1.x/
import db # Imported local module
from Crypto.Cipher import AES # https://pypi.org/project/pycryptodome/
import flask_login # https://flask-login.readthedocs.io/en/latest/
import socket # Standard python library
import ipaddress # Standard python library

flag = 1

print("Retrieve primary IP of server by entering ""ifconfig"" (Linux - Terminal) or ""ipconfig"" (Windows - CMD)") # Not ideal as usage becomes less user friendly
while flag == 1:
    server_ip = input("Enter server IP or 127.0.0.1 for local device: ") # Get server ip
    try:
        ipaddress.ip_address(server_ip) # if valid
        flag = 0 # end while loop
    except:
        print("Invalid IP") # else repeat

# [4]

app = flask.Flask(__name__) # Initiate flask app
app.config['SESSION_COOKIE_HTTPONLY'] = False # VERY unlikely you will see httponly purposefully being set to false
                                                # from default flask true but some bespoke production platforms may not have manually set the session cookie to be httponly
app.secret_key = '6D4FQsRvlY4L0pzoHXf5wulKPoWPG3Cxz_yHpNU9er8' # Set session key
app.url_map.strict_slashes = False # Dont force trailing / in url

login_manager = flask_login.LoginManager() # Initiate login manager

login_manager.init_app(app) # Point login manager to app

users = {'csc': {'password': 'pass'}} # Declare login information - clear text details (terrible security)

rand_list = [] # Declare empty rand list
cookie_numb = 0 # Declare cookie_numb to 0

class User(flask_login.UserMixin): # Call flask_login.UserMixin into class User
    pass

@login_manager.user_loader
def user_loader(email): # Load username from users variable
    if email not in users: # check if username is valid
        return

    user = User()
    user.id = email # load username into login_manager
    return user


@login_manager.request_loader
def request_loader(request): # Process login
    email = request.form.get('email') # Get username from form
    if email not in users: # check if username valid
        return

    user = User()
    user.id = email # load username into login_manager

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password'] # Check if password matches with the grouped username

    return user

@app.route('/') # define web app landing page
def init():
    return flask.redirect(flask.url_for('login')) # redirect / to login page

@app.route('/login', methods=['GET', 'POST']) # define login page with GET and POST html methods
def login():
    if flask.request.method == 'GET': # If GET is available, display username and password html login
        return '''
               <form action='login' method='POST'>
                <input type='text' name='username' id='username' placeholder='username' required/>
                <input type='password' name='password' id='password' placeholder='password' required/>
                <input type='submit' name='submit'/>
               </form>
               '''

    username = flask.request.form['username'] # get username from username input form
    if username not in users: # if username not in users variable
        return 'Incorrect login' # prevent login
    if flask.request.form['password'] == users[username]['password']: # if form password matches with the grouped username/password varaible
        user = User()
        user.id = username
        flask_login.login_user(user) # Process user login
        return flask.redirect(flask.url_for('protected')) # redirect to protected page

    return 'Incorrect login' # If password wrong return incorrect

# [/4]

@app.route('/protected') # define protected page
@flask_login.login_required # Only accessible via login session
def protected():
            key = b'0123456789abcdef' # define encryption key (must be same as server key)
            iv = b'0123456789abcdef' # define iv (must be same as server iv)
            global cookie_numb # Fetch global variable cookie_numb
            obj2 = AES.new(key,AES.MODE_CBC, iv=iv) # Configure decrypter [5]
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Set variable to TCP socket
            client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Set socket option to allow address reuse
            client.connect((server_ip, 42186)) # port hard coded into gui app - Highly unoptimised production app would not continously connect/disconnect socket
            random_word_encrypt = client.recv(1024) # Retrieve messages from socket
            random_word = obj2.decrypt(random_word_encrypt) # decrypt incoming messages
            random_word = random_word[0: len(random_word)//16] # Remove encryption padding
            random_word = random_word.decode('utf-8') # Decode into readable message
            rand_list.append(random_word) # append decrypted word into list
            cookie_numb = int(cookie_numb) # get current cookie numb from global
            cookie_numb += 1 # increment cookie numb by 1
            cookie_numb = str(cookie_numb) # convert to string
            cookie_name = "Cookie" + cookie_numb # setup cookie name
            resp = make_response(jsonify(rand_list)) # Convert list of words to json
            resp.set_cookie(cookie_name,random_word) # set cookie of response to cookie name and random word
            return resp  # Return page with json list and new cookie

@app.route('/del-cookies') # delete all cookies
@flask_login.login_required
def delete_cookies():
    return '<script>document.cookie.split(";").forEach(function(c) { document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); });</script>' # [6]


@app.route('/logout')
def logout():
    flask_login.logout_user() # logout current session
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler(): # Display when connecting to protected without a login session
    return 'Unauthorized'

# [7]
@app.route('/feedback', methods=['POST', 'GET'])
def index():                                    # A 'feedback' page is unlikely to appear on a IOT platform
    if request.method == 'POST':                # But I needed somewhere to utilise a XSS vulnerability
        db.add_comment(request.form['comment']) # If POST method available add comment from form to database

    search_query = request.args.get('q') # Fetch queries displayed from arg q

    comments = db.get_comments(search_query) # Display comments based on search query

    return render_template('index.html',comments=comments,search_query=search_query) # return index template with comments and search_query

# [/7]

app.run(debug=False) # Run app