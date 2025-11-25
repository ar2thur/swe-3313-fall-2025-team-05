import datetime

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, session, g
)
from .auth import login_required
from .models import ShoppingCart, ShoppingCartItem, InventoryItem, Logistics
from .db import db

bp = Blueprint("payment", __name__, url_prefix="/payment")

# Pay now button is pressed on shopping cart page.
@bp.route("/", methods=["GET", "POST"])
@login_required
def pay():
    logistics = Logistics.query.first()

    if request.method == "POST":
        # Shipping information.
        address = request.form.get("address", "").strip()
        apt = request.form.get("apt", "").strip() # optional
        zip_code = request.form.get("zip_code", "").strip()
        city = request.form.get("city", "").strip()
        state = request.form.get("state", "").strip()
        phone = request.form.get("phone", "").replace("-","").strip()

        # Payment information.
        card = request.form.get("card", "").strip()
        expiration = request.form.get("expiration", "").strip()
        cvv = request.form.get("cvv", "").strip()

        # Shipping option.
        shipping = request.form.get("shipping", "")

        error = None

        if not address:
            error = "Street address is required."
        elif not zip_code:
            error = "Zip code is required."
        elif not city:
            error = "City is required."
        elif not state:
            error = "State is required."
        elif not phone:
            error = "Phone number is required."
        elif not card:
            error = "Card number is required."
        elif not expiration:
            error = "Expiration date is required."
        elif not cvv:
            error = "CVV code is required."
        elif not shipping:
            error = "Shipping option selection is required."

        if error is None: # All required fields filled. Can confirm order.
            # Determine cost of shipping.
            shipping_cost = logistics.ground_shipping
            if shipping == "overnight":
                shipping_cost = logistics.overnight_shipping
            elif shipping == "three_day":
                shipping_cost = logistics.three_day_shipping

            session["shipping_info"] = {"address":address,"zip_code":zip_code,
                                        "city":city,"state":state,"phone":phone,
                                        "card":card,"shipping_cost":shipping_cost}

            return redirect(url_for("payment.confirm"))

        flash(error)

    return render_template("payment/pay.html", logistics=logistics)

# Confirm order button is pressed on pay now page.
@bp.route("/confirm", methods=["GET", "POST"])
@login_required
def confirm():
    cart = ShoppingCart.query.filter_by(user_id=g.user.id, is_checked_out=False).first()
    if cart is None:
        return redirect(url_for("home.index"))

    logistics = Logistics.query.first()
    tax = cart.sub_total * logistics.tax
    shipping_info = session.get("shipping_info", {})
    shipping_cost = shipping_info.get("shipping_cost")
    total = cart.sub_total + shipping_cost + tax

    cart_items = ShoppingCartItem.query.filter_by(shopping_cart_id=cart.id).all()
    items = get_items(cart_items)

    if request.method == "POST": # Payment confirmed.
        action = request.form.get("action")

        if action == "complete": # Pressed complete order button.
            cart.tax = tax
            cart.total_cost = total
            for item in items:
                item.is_available = False
            cart.is_checked_out = True
            cart.date_checked_out = datetime.datetime.now()

            db.session.commit()

            return redirect(url_for("payment.receipt", cart_id=cart.id))
        elif action == "cancel": # Pressed cancel order button.
            return redirect(url_for("home.index"))

    return render_template("payment/confirm.html",items=items)

@bp.route("/receipt/<int:cart_id>", methods=["GET", "POST"])
@login_required
def view_receipt(cart_id):
    cart = ShoppingCart.query.filter_by(user_id=g.user.id, is_checked_out=False).first()
    shipping_info = session.get("shipping_info", {})
    if cart is None:
        return redirect(url_for("home.index"))

    if not cart.is_checked_out:
        return redirect(url_for("home.index"))

    cart_items = ShoppingCartItem.query.filter_by(shopping_cart_id=cart.id).all()
    items = get_items(cart_items)

    if request.method == "POST":
        return redirect(url_for("home"))

    return render_template("payment/receipt.html", cart=cart, items=items, shipping_info=shipping_info)

# Get the corresponding inventory items from cart items.
def get_items(cart_items):
    items = []
    for cart_item in cart_items:
        item = InventoryItem.query.get(cart_item.inventory_item_id)
        if item:
            items.append(cart_item)
    return items