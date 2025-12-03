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
    """Loads all dashboard data from our SQLite database"""
    amount_of_users = db.session.query(User).count()
    items_in_cart = db.session.query(ShoppingCartItem).count()
    bought_carts = ShoppingCart.query.filter_by(is_checked_out=True).all()
    sales_made = len(bought_carts)
    total_revenue = sum(cart.total_cost for cart in bought_carts)

    return (
            amount_of_users,
            items_in_cart,
            sales_made,
            total_revenue,
            bought_carts
            )

@bp.route("/orders")
@admin_required
def orders():
    """Sends a list in format [(ShoppingCart, [(InventoryItems,date_added])]"""

    cart_and_items = []

    bought_carts = ShoppingCart.query.filter_by(is_checked_out=True).all()

    # Please find a better way to do this, this hurts
    for cart in bought_carts:

        items_in_cart = ShoppingCartItem.query.filter_by(shopping_cart_id=cart.id).all()
        inventory_list = []

        for item in items_in_cart:
            inventory_item = InventoryItem.query.filter_by(id=item.inventory_item_id).first()
            inventory_list.append((inventory_item, item.added_to_cart))

        cart_and_items.append((cart, inventory_list))

    return render_template("admin/orders.html", recent_sales=cart_and_items)

@bp.route("/products")
@admin_required
def products():
    all_items = InventoryItem.query.all()
    return render_template("admin/products.html", inventory=all_items)


@bp.route("/user-management")
@admin_required
def user_management():
    pass
