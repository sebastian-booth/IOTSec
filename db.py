# all code from [3]
import sqlite3 # Standard Python Library


def connect_db():
    db = sqlite3.connect('database.db') # Create/connect to database Requires elevated privalges to run (ie from cmd/terminal or pycharm running as admin)
    db.cursor().execute('CREATE TABLE IF NOT EXISTS comments ' # Create table comments with int ID (Primary Key) and comment text attributes
                        '(id INTEGER PRIMARY KEY, '
                        'comment TEXT)')
    db.commit() # Commit changes
    return db


def add_comment(comment):
    db = connect_db() # Connect to DB
    db.cursor().execute('INSERT INTO comments (comment) ' # Insert comment with passed in variable
                        'VALUES (?)', (comment,))
    db.commit() # Commit changes


def get_comments(search_query=None):
    db = connect_db() # Connect to DB
    results = [] # Initialise results list
    get_all_query = 'SELECT comment FROM comments' # Get all comments
    for (comment,) in db.cursor().execute(get_all_query).fetchall(): # Append get_all_query output to results list.
        if search_query is None or search_query in comment:
            results.append(comment)
    return results
