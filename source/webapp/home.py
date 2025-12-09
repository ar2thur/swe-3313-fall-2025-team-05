from flask import (
    Blueprint, flash, render_template, request,
    session, redirect, url_for, g
)
from sqlalchemy import desc, asc
from webapp.auth import login_required
from webapp.db import db
from webapp.models import InventoryItem, ShoppingCart, ShoppingCartItem

bp = Blueprint("home", __name__)


@bp.route("/")
@login_required
def index():
    # This function loads all user cart data into the session
    load_session_data()
    products = InventoryItem.query.filter_by(is_available=True).all()

    return render_template("home.html", products=products)


@bp.route("/search", methods=["POST"])
@login_required
def search():
    # This function allows users to search or filter products
    search_term = request.form.get("search-term").strip()
    sort_by = request.form.get("sort-by")
    min_price = request.form.get("min-price")
    max_price = request.form.get("max-price")

    filter_categories = []
    is_air = request.form.get("Aircraft")
    if is_air == 'on':
        filter_categories.append("Aircraft")
    is_miss = request.form.get("Missiles")
    if is_miss == 'on':
        filter_categories.append("Missiles")
    is_rot = request.form.get("Rotary")
    if is_rot == 'on':
        filter_categories.append("Rotary")
    is_spsy = request.form.get("Space-Systems")
    if is_spsy == 'on':
        filter_categories.append("Space Systems")

    query = db.session.query(InventoryItem)
    print(request.form)
    # Search term
    if search_term:
        query = query.filter(InventoryItem.name.ilike(f"%{search_term}%"))
    # Categories
    if filter_categories:
        query = query.filter(InventoryItem.category.in_(filter_categories))

    # Price range
    if min_price:
        min_price = int(min_price) * 100  # to convert to cents
    if max_price:
        max_price = int(max_price) * 100

    if min_price and max_price:
        query = query.filter(InventoryItem.cost.between(min_price, max_price))
    elif min_price:
        query = query.filter(InventoryItem.cost >= min_price)
    elif max_price:
        query = query.filter(InventoryItem.cost <= max_price)

    # Sorting
    if sort_by:
        sort_by = sort_by.split(',')
        sort_column = getattr(InventoryItem, sort_by[0])
        if sort_by[1] == 'desc':
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))

    products = query.all()

    if not products:
        flash(f"No products found for '{search_term}'", "error")

    print(products)

    return render_template("home.html", products=products)


def load_session_data():
    # Load all products
    user_shopping_cart_uuid = ShoppingCart.query.filter_by(
        user_id=g.user.id,
        is_checked_out=False
    ).first().id
    users_shopping_cart_items = ShoppingCartItem.query.filter_by(
        shopping_cart_id=user_shopping_cart_uuid
    ).all()

    total = 0
    for cart_item in users_shopping_cart_items:
        total += InventoryItem.query.filter_by(
            id=cart_item.inventory_item_id
        ).first().cost

    total /= 100  # Convert cents to dollars
    user_shopping_cart_length = len(users_shopping_cart_items)

    session["cart_length"] = user_shopping_cart_length
    session["cart_total"] = total
