import os
from flask import Flask
from .db import db, init_db, seed_db, reset_db

def create_app(test_config=None):
    # Creates and intializes the app
    app = Flask(__name__)
    app.config["SECRET_KEY"] = 'dev'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Creates the sql database
    db.init_app(app)

    # Create the database tables if they do not exist
    from . import models
    
    with app.app_context():
        db.create_all()

    # Register blueprints
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .payment import bp as payment_bp
    app.register_blueprint(payment_bp)
    
    from .home import bp as home_bp
    app.register_blueprint(home_bp)
    app.add_url_rule("/", endpoint="index")

    from .cart import bp as cart_bp
    app.register_blueprint(cart_bp)

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
    app.cli.add_command(reset_db)
