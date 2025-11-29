import functools

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, session, g
)

from webapp.db import db
from webapp.models import User, ShoppingCart

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register():
    # Handle user registration
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        error = None

        if not name:
            error = "Name is required."
        elif not email:
            error = "Email is required."
        elif not password:
            error = "Password is required."
        elif User.query.filter_by(email=email).first() is not None:
            error = "A user with that email already exists."

        if error is None:
            user = User(
                name=name,
                email=email,
                is_admin=False,
            )
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            new_cart = ShoppingCart(user_id=user.id)
            db.session.add(new_cart)
            db.session.commit()
        
            flash("Registration successful. Please log in.")
            return redirect(url_for("auth.login"))

        flash(error)

    # GET request or error case
    return render_template("auth/register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    # Handle user login
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        error = None

        user = User.query.filter_by(email=email).first()

        if user is None:
            error = "Incorrect email."
        elif not user.check_password(password):
            error = "Incorrect password."

        if error is None:
            # log the user in
            session.clear()
            session["user_id"] = user.id
            session["is_admin"] = user.is_admin

            # change "index" if your home route has another endpoint name
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    # Handle user logout
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("index"))
    # again, change "index" if needed


@bp.before_app_request
def load_logged_in_user():
    # Runs before every request. Loads g.user from the session.
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

@bp.before_app_request
def load_admin_status():
    # Loads g.is_admin from the session.
    g.is_admin = bool(session.get("is_admin", False))


def login_required(view):
    # Decorator to protect routes that require login.
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view


def admin_required(view):
    # Decorator to protect routes that require admin privileges.
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        if not g.is_admin:
            flash("Admin access required.")
            return redirect(url_for("index"))
        return view(**kwargs)

    return wrapped_view
