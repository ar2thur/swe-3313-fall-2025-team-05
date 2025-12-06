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
    # Admin dashboard view
    data = get_dashboard_data()

    return render_template("admin/dashboard.html", data=data)

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

@bp.route("/products/edit/<int:product_id>", methods=["GET", "POST"])
@admin_required
def edit_product(product_id):
    # Edit an existing product in the inventory
    product = InventoryItem.query.get_or_404(product_id) # added get_or_404 for safety

    if request.method == "POST":
        model_name = request.form["model_name"]
        cost = int(request.form["cost"])
        description = request.form["description"]
        upload_picture = request.files.get("static/inventory_pictures")
        #category = request.form["type"] ?include this?

        product.name = model_name
        product.cost = cost
        product.description = description
        
        if upload_picture and upload_picture.filename:
            # i'll come back to this later- i'm lost
            picture_path = f"static/inventory_pictures/{upload_picture.filename}"
    
        db.session.commit()
        flash("Product updated successfully.")
        return redirect(url_for("admin.manage_products"))
    
    return render_template("admin/edit_product.html", product=product)

@bp.route("/products/delete/<int:product_id>", methods=["GET","POST"])
@admin_required
def delete_product(product_id):
    # Delete a product from the inventory
    product = InventoryItem.query.get_or_404(product_id) # added get_or_404 for safety

    if request.method == "POST":
        db.session.delete(product)
        db.session.commit()
        flash("Product deleted successfully.")
        return redirect(url_for("admin.manage_products"))
    
    return render_template("admin/delete_product.html", product=product)

@bp.route("/user-management", methods=["GET", "POST"])
@admin_required
def user_management():
    # View and manage all users
    users = User.query.all()

    if request.method == "POST":
        user_id = request.form.get("user_id")
        action = request.form.get("action")

        if not user_id:
            flash("No user selected.")
            return redirect(url_for("admin.user_management"))

        user = User.query.get_or_404(int(user_id))

        if action == "Demote" and user.is_admin: # must be the same string in user_management.html
            admin_count = User.query.filter_by(is_admin=True).count()
            if admin_count == 1:
                flash("Cannot demote the last admin user.")
                return redirect(url_for("admin.user_management"))
        
        if action == "Make Admin": # must be the same string in user_management.html
            if user.is_admin:
                flash(f"{user.name} is already an admin.")
            else:
                user.is_admin = True
                flash(f"{user.name} promoted to admin.")

        elif action == "Demote":
            if not user.is_admin:
                flash(f"{user.name} is already a regular user.")
            else:
                user.is_admin = False
                flash(f"{user.name} demoted to regular user.")

        db.session.commit()
        return redirect(url_for("admin.user_management"))

    return render_template("admin/user_management.html", users=users)