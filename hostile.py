import flask # https://flask.palletsprojects.com/en/1.1.x/
from flask import * # https://flask.palletsprojects.com/en/1.1.x/

app = flask.Flask(__name__) # Initiate flask app

app.secret_key = 'ypes79X32BVb1TyMA0qkHxYddzpVz4qrzJLFgs3zHL8' #Set session key different to gui

app.url_map.strict_slashes = False # Dont force trailing / in url

@app.route('/') # default route
def hostile():
        print(request.cookies) # print cookies
        return "HOSTILE"

app.run(debug=True, port=3500) # run on different port to gui