from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, session, g
)

from webapp.auth import admin_required
from webapp.db import db
from webapp.models import InventoryItem, User, ShoppingCart, ShoppingCartItem

bp = Blueprint("admin", __name__)

@bp.route("/dashboard")
@admin_required
def dashboard():

    data = get_dashboard_data()

    return render_template("admin/dashboard.html",
                           nusers=data[0],
                           ncarts=data[1],
                           nsales=data[2],
                           nrevenue=data[3],
                           recent_sales=data[4]
                           )

def get_dashboard_data():

    amount_of_users = db.session.query(User).count()
    items_in_cart = db.session.query(ShoppingCartItem).count()
    bought_carts = ShoppingCart.query.filter_by(is_checked_out=True).all()
    sales_made = len(bought_carts)
    total_revenue = sum(cart.total_cost for cart in bought_carts)



    return (amount_of_users, items_in_cart, sales_made, total_revenue, bought_carts)


