from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, session, g, Response
)
import pathlib
import csv
import datetime

from webapp.auth import admin_required
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

@bp.route("/orders/export_csv")
@admin_required
def export_csv():
    bought_carts = ShoppingCart.query.filter_by(is_checked_out=True).all()

    sales_report = "ID,CheckoutDate,Subtotal,Tax,Total\n"
    for cart in bought_carts: # Populate sales report with cart info.
        sales_report += f"{cart.id},{cart.date_checked_out},{cart.sub_total/100.0},{cart.tax/100.0},{cart.total_cost/100.0}\n"

    now = datetime.datetime.now()
    filename = f"lockheed_sales_{now.month}-{now.year}"
    
    response = Response(sales_report, content_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename={filename}.csv"

    return response

@bp.route("/products")
@admin_required
def products():
    all_items = InventoryItem.query.all()
    return render_template("admin/products.html", inventory=all_items)
  
@bp.route("/products/add", methods=["GET", "POST"])
@admin_required
def add_item():
    if request.method == "POST":
        name = request.form.get("name")
        cost = request.form.get("cost")
        desc = request.form.get("desc")
        avail = request.form.get("avail")
        if (avail == 'on'):
            avail = True
        else:
            avail = False

        file = request.files["picture"]
        extention = pathlib.Path(file.filename).suffix
        filename = name.replace(' ', '_') + extention

        file_path = f"inventory_pictures/{filename}"
        # Relative paths like this are bad ...
        file.save(f"webapp/static/{file_path}")

        new_item = InventoryItem(
                    is_available=avail, 
                    name=name, 
                    cost=cost, 
                    description=desc, 
                    picture_path=file_path
                )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('admin.products'))

    return render_template("admin/product_handling/product_add.html")

@bp.route("/products/edit/<int:item_id>", methods=["GET", "POST"])
@admin_required
def edit_item(item_id: int):
    item = InventoryItem.query.filter_by(id=item_id).first()
    # TODO: POST action
    return render_template("admin/product_handling/product_edit.html", prod=item)

@bp.route("/products/delete", methods=["POST"])
@admin_required
def delete():
    for item_id in request.json:
        item = InventoryItem.query.filter_by(id=item_id).delete()
    db.session.commit()

    # Returns a success code to tell the page to reload
    return '', 204

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
