from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, session, g
)

from webapp.auth import login_required, admin_required
from webapp.db import db
from webapp.models import InventoryItem, User, ShoppingCart, ShoppingCartItem

bp = Blueprint("admin", __name__)

@bp.route("/dashboard")
@admin_required
def dashboard():
    # Admin dashboard view
    data = get_dashboard_data()

    return render_template("admin/dashboard.html",
                           data=data
                           )

def get_dashboard_data():
    # Loads all dashbaord data from our SQL database
    amount_of_users = db.session.query(User).count() # Total customers
    total_cart_items = db.session.query(ShoppingCartItem).count() # All items ever added to carts
    orders = ShoppingCart.query.filter_by(is_checked_out=True).all() # Total orders completed (list)
    total_orders = len(orders) # Total number of orders
    total_revenue = sum(order.total_cost for order in orders) # Total revenue from all orders (sales)

    return  {
            "amount_of_users": amount_of_users, 
            "total_cart_items": total_cart_items, 
            "total_orders": total_orders, 
            "total_revenue": total_revenue,
            "orders": orders
            }

@bp.route("/orders")
@admin_required
def view_orders():
    # View all orders placed by customers
    carts = ShoppingCart.query.filter_by(is_checked_out=True).all()

    orders = []

    for cart in carts:
        user = User.query.get(cart.user_id)

        cart_items = ShoppingCartItem.query.filter_by(shopping_cart_id=cart.id).all()

        for cart_item in cart_items:
            inventory_item = InventoryItem.query.get(cart_item.inventory_item_id)

            orders.append({
                "order_id": cart.id,
                "user_name": user.name,
                "model_name": inventory_item.name,
                "date": cart.date_checked_out,
                "cost": inventory_item.cost
                # Might need more fields here later. Do we add 'Type/ category'??
            })

    return render_template("admin/orders.html", orders=orders)

@bp.route("/products")
@admin_required
def manage_products():
    # View and manage all products in inventory
    products = InventoryItem.query.all()

    return render_template("admin/products.html", products=products)

@bp.route("/products/add", methods=["GET", "POST"])
@admin_required
def add_product():
    # Add a new product to the inventory
    if request.method == "POST":
        model_name = request.form["model_name"]
        cost = int(request.form["cost"])
        description = request.form["description"]
        upload_picture = request.files.get("static/inventory_pictures")
        #category = request.form["type"] ?include this?

        new_product = InventoryItem(
            name = model_name,
            cost = cost,
            description = description,
            is_available = True)
        
        if upload_picture and upload_picture.filename:
            # i'll come back to this later- i'm lost
            picture_path = f"static/inventory_pictures/{upload_picture.filename}"
        
        
        db.session.add(new_product)
        db.session.commit()
        flash("Product added successfully.")
        return redirect(url_for("admin.manage_products"))

    return render_template("admin/add_product.html")