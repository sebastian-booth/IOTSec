import flask
from flask import *

app = flask.Flask(__name__)

app.secret_key = 'ypes79X32BVb1TyMA0qkHxYddzpVz4qrzJLFgs3zHL8'

app.url_map.strict_slashes = False

@app.route('/')
def hostile():
        print(request.cookies)
        return "HOSTILE"

app.run(debug=True, port=3500)