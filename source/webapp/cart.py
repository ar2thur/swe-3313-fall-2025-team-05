from datetime import datetime
from flask import Blueprint, flash, render_template, redirect, url_for, g
from webapp.auth import login_required
from webapp.db import db
from webapp.models import ShoppingCart, ShoppingCartItem, InventoryItem

bp = Blueprint("cart", __name__, url_prefix="/cart")


@bp.route("/")
@login_required
def view_cart():
    # View the contents of the shopping cart
    cart = ShoppingCart.query.filter_by(user_id=g.user.id, is_checked_out=False).first()
    subtotal = 0
    if cart is None:
        items = []
    else:
        shopping_cart_items = ShoppingCartItem.query.filter_by(shopping_cart_id=cart.id).all()
        items = []
        for cart_item in shopping_cart_items:
            item = InventoryItem.query.filter_by(id=cart_item.inventory_item_id).first()
            subtotal += item.cost
            items.append(item)


    return render_template("cart/view_cart.html", items=items, subtotal=subtotal)


@bp.route("/view/<int:item_id>", methods=["GET"])
@login_required
def view_item(item_id):
    # View details of a specific item in the cart
    item = InventoryItem.query.get(item_id)
    if item is None:
        return "Item not found", 404

    return render_template("cart/view_item.html", item=item)


@bp.route("/add/<int:item_id>", methods=["POST"])
@login_required
def add_to_cart(item_id):
    # Add an item to the shopping cart
    item = InventoryItem.query.get(item_id)
    if item is None or not item.is_available:
        return "Item not available", 404

    item.is_available = False

    cart = ShoppingCart.query.filter_by(user_id=g.user.id, is_checked_out=False).first()

    new_item = ShoppingCartItem(
        shopping_cart_id=cart.id,
        inventory_item_id=item.id,
        added_to_cart=datetime.now()
    )
    db.session.add(new_item)
    db.session.commit()

    flash(f"{item.name} added to cart.", "success")
    return redirect(url_for("index"))


@bp.route("/remove/<int:item_id>", methods=["POST"])
@login_required
def remove_from_cart(item_id):
    # Remove an item from the shopping cart
    cart = ShoppingCart.query.filter_by(user_id=g.user.id, is_checked_out=False).first()

    if cart is None:
        flash("Your cart is empty", "error")
        return redirect(url_for("cart.view_cart"))

    cart_item = ShoppingCartItem.query.filter_by(
        shopping_cart_id=cart.id,
        inventory_item_id=item_id
    ).first()

    # Marks item as available again
    item = InventoryItem.query.filter_by(id=item_id).first()
    item.is_available = True

    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()

    flash(f"Removed {item.name} from cart", "success")

    return redirect(url_for("cart.view_cart"))
