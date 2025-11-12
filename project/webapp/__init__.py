import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# this initializes a SQLAlchemy connection to our database
# you must import this into every file that needs database access. 
# refer to here: https://flask-sqlalchemy.readthedocs.io/en/stable/quickstart/
db = SQLAlchemy()

def create_app(test_config=None):
    # Creates and intializes the app
    app = Flask(__name__)
    app.config["SECRET_KEY"] = 'dev'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

    # Creates the sql database
    db.init_app(app)

    with app.app_context():
        from . import models
        db.create_all()

    # Makes sure the apps instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    return app



