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
        if apt:
            address += " #" + apt
        zip_code = request.form.get("zip_code", "").strip()
        city = request.form.get("city", "").strip()
        state = request.form.get("state", "").strip()
        phone = request.form.get("phone", "").replace("-","").strip()

        # Payment information.
        card = request.form.get("card", "").strip()
        formatted_card = card
        if len(card) > 4: # Only show the last 4 digits of the card number.
            mask_size = len(card) - 4
            last_digits = card[-4:]
            formatted_card = ("*" * mask_size) + last_digits

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
                                        "card":formatted_card,"shipping_cost":shipping_cost}

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

    cart_items = ShoppingCartItem.query.filter_by(shopping_cart_id=cart.id).all()
    items = get_items(cart_items)

    logistics = Logistics.query.first()
    sub_total = 0
    for item in items: # Add up cost of all items in cart.
        sub_total += item.cost
    tax = int(sub_total * (logistics.tax / 100))
    shipping_info = session.get("shipping_info", {})
    if shipping_info is None: # Prevent from error if no shipping info found.
        return redirect(url_for("payment.pay"))
    shipping_cost = shipping_info.get("shipping_cost")
    total = sub_total + shipping_cost + tax
    cart.sub_total = sub_total
    cart.tax = tax
    cart.total_cost = total

    if request.method == "POST": # Payment confirmed.
        action = request.form.get("action")

        if action == "complete": # Pressed complete order button.
            cart.is_checked_out = True
            cart.date_checked_out = datetime.datetime.now()

            db.session.commit()
            return redirect(url_for("payment.receipt", cart_id=cart.id))
        elif action == "cancel": # Pressed cancel order button.
            # Empty out cart.
            cart.sub_total = 0
            cart.tax = 0
            cart.total_cost = 0

            for cart_item in cart_items:
                item = InventoryItem.query.filter_by(id=cart_item.inventory_item_id).first()
                item.is_available = True

                if cart_item:
                    db.session.delete(cart_item)
            db.session.commit()
            flash("Order cancelled successfully.")
            return redirect(url_for("home.index"))
    return render_template("payment/confirm.html", items=items, cart=cart, shipping_cost=shipping_cost, tax_percent=logistics.tax)

@bp.route("/receipt/<uuid:cart_id>", methods=["GET", "POST"])
@login_required
def receipt(cart_id):
    cart = ShoppingCart.query.filter_by(id=cart_id, user_id=g.user.id).first()
    shipping_info = session.get("shipping_info", {})
    if shipping_info is None: # Prevent from error if no shipping info found.
        return redirect(url_for("payment.pay"))
    if cart is None:
        return redirect(url_for("home.index"))
    if not cart.is_checked_out:
        return redirect(url_for("home.index"))

    cart_items = ShoppingCartItem.query.filter_by(shopping_cart_id=cart.id).all()
    items = get_items(cart_items)

    new_cart = ShoppingCart(user_id=g.user.id)
    db.session.add(new_cart)
    db.session.commit()

    if request.method == "POST": # Continue shopping button is pressed.
        return redirect(url_for("home.index"))
    return render_template("payment/receipt.html", cart=cart, items=items, shipping_info=shipping_info)

# Get the corresponding inventory items from cart items.
def get_items(cart_items):
    items = []
    for cart_item in cart_items:
        item = InventoryItem.query.get(cart_item.inventory_item_id)
        if item:
            items.append(item)
    return items