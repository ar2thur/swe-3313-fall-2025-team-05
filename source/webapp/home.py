from flask import (
    Blueprint, flash, render_template, request,
    session, redirect, url_for, g
)
from difflib import SequenceMatcher
from webapp.auth import login_required
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
    # This function allows users to search for products by name
    search_term = request.form.get("search-term").strip()
    # Do nothing if search term is empty
    if not search_term:
        return redirect(url_for('home.index'))
    
    # Case-insensitive substring searcch 
    products = InventoryItem.query.filter(InventoryItem.is_available==True, InventoryItem.name.ilike(f"%{search_term}%")).all()

    if not products:
        flash(f"No products found for '{search_term}'", "error")

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
