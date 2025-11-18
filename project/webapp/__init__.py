import os
from flask import Flask
from .db import db, init_db, seed_db

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

    add_cli_commands(app)

    # Makes sure the apps instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    return app


def add_cli_commands(app):
    app.cli.add_command(seed_db)
    app.cli.add_command(init_db)

