import sqlite3
import random
from flask import Flask, session, render_template, request, g # type: ignore

app = Flask(__name__)
app.secret_key = "hqauiodhiuashiudiuashdihqwiodhiqw"

@app.route("/")
def index():
    data = get_db()
    return str(data)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('list.db')
        cursor = db.cursor()
        cursor.execute("select * from groceries")
    return cursor.fetchall()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run()