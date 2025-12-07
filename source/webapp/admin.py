from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, session, g, Response
)
import pathlib
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

    return render_template("admin/dashboard.html", data=data)

def get_dashboard_data():
    # Loads all dashbaord data from our SQL database
    amount_of_users = db.session.query(User).count() # Total customers

    # Counts all items in carts currently, excluding already bought carts
    total_cart_items = 0
    for cart in ShoppingCart.query.filter_by(is_checked_out=False).all(): 
        total_cart_items += len(ShoppingCartItem.query.filter_by(shopping_cart_id=cart.id).all())

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
    # Export sales report as CSV
    bought_carts = ShoppingCart.query.filter_by(is_checked_out=True).all()

    sales_report = "ID,CheckoutDate,Subtotal,Tax,Total\n"
    for cart in bought_carts: # Populate sales report with cart info.
        sales_report += f"{cart.id},{cart.date_checked_out},{cart.sub_total/100.0},{cart.tax/100.0},{cart.total_cost/100.0}\n"

    now = datetime.datetime.now()
    filename = f"lockheed_sales_{now.month}-{now.year}"

    response = Response(sales_report, content_type="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename={filename}.csv"

    flash("Export Successful", "success")

    return response

@bp.route("/products")
@admin_required
def products():
    # View and manage inventory products
    all_items = InventoryItem.query.all()
    return render_template("admin/products.html", inventory=all_items)

@bp.route("/products/add", methods=["GET", "POST"])
@admin_required
def add_item():
    # Add a new product to the inventory
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
        unchecked_filename = name.replace(' ', '_') + extention

        # Checks if filename exists, if it does it will add a number to the end until it doesnt
        filename = filename_validation(unchecked_filename)

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
        flash("Item added successfully", "success")
        return redirect(url_for("admin.products"))

    return render_template("admin/product_handling/product_add.html")

@bp.route("/products/edit/<int:item_id>", methods=["GET", "POST"])
@admin_required
def edit_item(item_id: int):
    # Edit an existing product in the inventory
    item = InventoryItem.query.get_or_404(item_id)

    if request.method == "POST":
        name = request.form.get("name")
        cost = request.form.get("cost")
        desc = request.form.get("desc")
        avail = request.form.get("avail")
        if (avail == 'on'):
            avail = True
        else:
            avail = False

        item.name = name
        item.cost = cost
        item.description = desc
        item.is_available = avail

        file = request.files.get("picture")
        if file and file.filename != "":
            extention = pathlib.Path(file.filename).suffix
            unchecked_filename = name.replace(' ', '_') + extention

            filename = filename_validation(unchecked_filename)

            file_path = f"inventory_pictures/{filename}"
            # Relative paths like this are bad ...
            file.save(f"webapp/static/{file_path}")
            item.picture_path = file_path

        db.session.commit()
        flash("Item updated successfully", "success")
        return redirect(url_for("admin.products"))
    
    return render_template("admin/product_handling/product_edit.html", prod=item)

@bp.route("/products/delete", methods=["POST"])
@admin_required
def item_delete():
    for item_id in request.json:
        item = InventoryItem.query.filter_by(id=item_id).first()

        # Checks if this item is in a bought shopping_cart, if so then just
        # mark false and flash a message
        item_if_in_cart = ShoppingCartItem.query.filter_by(inventory_item_id=item_id).first()
        if item_if_in_cart:
            flash(f"Failed to delete: {item.name}, as its already in someones cart", 'error')
        else:
            flash(f"Deleted: {item.name}", "success")
            db.session.delete(item)

    db.session.commit()

    # Returns a success code to tell the page to reload
    return '', 204

@bp.route("/user-management", methods=["GET", "POST"])
@admin_required
def user_management():
    # View and manage all users
    users = User.query.all()

    return render_template("admin/user_management.html", users=users)

@bp.route("/user-management/delete", methods=["POST"])
@admin_required
def user_delete():
    for user_id in request.json:
        user = User.query.filter_by(id=user_id).first()
        if user:
            flash(f"Deleted: {user.name}", "success")
            db.session.delete(user)
    db.session.commit()
    return '', 204

@bp.route("/user-management/add", methods=["GET", "POST"])
@admin_required
def add_user():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        is_admin = request.form.get("is_admin")

        email_exists = User.query.filter_by(email=email).first()
        if email_exists:
            flash("This email already exists", "error")
            return render_template("admin/user_handling/user_add.html")

        if (is_admin == 'on'):
            is_admin = True
        else:
            is_admin = False
        new_user = User(
                    name=name,
                    email=email,
                    is_admin=is_admin
                )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        new_cart = ShoppingCart(user_id=new_user.id)
        db.session.add(new_cart)
        db.session.commit()

        flash("User added successfully", "success")
        return redirect(url_for("admin.user_management"))

    return render_template("admin/user_handling/user_add.html")

@bp.route("/user-management/promote", methods=["POST"])
@admin_required
def user_promote():
    for user_id in request.json:
        user = User.query.filter_by(id=user_id).first()
        if user:
            user.is_admin = True
            flash(f"Promoted: {user.name}", "success")
            db.session.commit()
        else:
            flash("User does not exist", "error")
    return '', 204

@bp.route("/user-management/demote", methods=["POST"])
@admin_required
def user_demote():
    admin_user_amount = User.query.filter_by(is_admin=True).count()
    if admin_user_amount <= len(request.json):
        flash("At least one user must be an admin", "error")
        return '', 204
    for user_id in request.json:
        user = User.query.filter_by(id=user_id).first()
        if user:
            user.is_admin = False
            flash(f"Demoted: {user.name}", "success")
            db.session.commit()
        else:
            flash("User does not exist", "error")
    return '', 204

def filename_validation(filename: str):
    counter = 1
    path = pathlib.Path(f"webapp/static/inventory_pictures/{filename}")
    new_filename = filename # Just incase the filename doesnt already exist
    print(path.exists())
    while path.exists():
        old_filename = pathlib.Path(filename)
        extention = old_filename.suffix
        name = old_filename.stem
        new_filename = name+f"_{counter}"+extention
        path = pathlib.Path(f"webapp/static/inventory_pictures/{new_filename}")
        counter += 1
    return new_filename

