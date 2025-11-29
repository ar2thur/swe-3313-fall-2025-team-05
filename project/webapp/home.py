from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, session, g
)

from webapp.auth import login_required, admin_required
from webapp.db import db
from webapp.models import InventoryItem, User, ShoppingCart, ShoppingCartItem

bp = Blueprint("home", __name__)

@bp.route("/")
@login_required
def index():
    # Load all products
    user_shopping_cart_uuid = ShoppingCart.query.filter_by(user_id=g.user.id, is_checked_out=False).first()
    users_shopping_cart_items = ShoppingCartItem.query.filter_by(shopping_cart_id=user_shopping_cart_uuid).all()
    
    total = 0
    for cart_item in users_shopping_cart_items:
        total += InventoryItem.query.filter_by(id=cart_item.inventory_item_id).first().cost

    total /= 100  # Convert cents to dollars

    user_shopping_cart_length = len(users_shopping_cart_items)

    products = InventoryItem.query.filter_by(is_available=True).all()
    return render_template("home.html", products=products, item_count=user_shopping_cart_length, sub_total=total)
