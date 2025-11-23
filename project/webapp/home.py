from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, session, g
)

from webapp.auth import login_required, admin_required
from webapp.db import db
from webapp.models import InventoryItem, User

bp = Blueprint("home", __name__)

@bp.route("/")
@login_required
def index():
    # Load all products
    products = InventoryItem.query.all()
    print(products)
    return render_template("home.html", products=products)


