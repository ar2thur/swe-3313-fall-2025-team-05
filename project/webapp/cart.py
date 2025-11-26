from flask import Blueprint, flash, render_template, redirect, session, url_for, g
from .auth import login_required
from .db import ShoppingCart, ShoppingCartItem, InventoryItem, db

bp = Blueprint("cart", __name__, url_prefix="/cart")


@bp.route("/view", methods=["GET"])
@login_required
def view_cart():
    # View the contents of the shopping cart
    cart_id = session.get("cart_id")
    if not cart_id:
        items = []
    else:
        items = ShoppingCartItem.query.filter_by(shopping_cart_id=cart_id).all()

    return render_template("view_cart.html", items=items)


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

    cart = ShoppingCart.query.filter_by(user_id=g.user.id, is_checked_out=False).first()
    
    if cart is None:
        cart = ShoppingCart(user_id=g.user.id)
        db.session.add(cart)
        db.session.commit()

    new_item = ShoppingCartItem(
        shopping_cart_id=cart.id,
        inventory_item_id=item.id,
        added_to_cart="Just now"  # later, use actual timestamp
    )
    db.session.add(new_item)
    db.session.commit()

    flash("Item added to cart.")
    return redirect(url_for("cart.view_cart"))        


@bp.route("/checkout", methods=["POST"])
@login_required
def checkout():
    # Checkout the shopping cart
    cart = ShoppingCart.query.filter_by(user_id=g.user.id, is_checked_out=False).first()
    
    if cart is None:
        return redirect(url_for("cart.view_cart"))

    cart.is_checked_out = True
    db.session.commit()

    return render_template("cart/checkout_success.html")


@bp.route("/remove/<int:item_id>", methods=["POST"])
@login_required
def remove_from_cart(item_id):
    # Remove an item from the shopping cart
    cart = ShoppingCart.query.filter_by(user_id=g.user.id, is_checked_out=False).first()
    
    if cart is None:
        return redirect(url_for("cart.view_cart"))

    cart_item = ShoppingCartItem.query.filter_by(
        shopping_cart_id=cart.id,
        inventory_item_id=item_id
    ).first()

    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()

    return redirect(url_for("cart.view_cart"))