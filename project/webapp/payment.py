from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, session
)
from .auth import login_required

bp = Blueprint("payment", __name__, url_prefix="/payment")

# Pay now button is pressed on shopping cart page.
@bp.route("/", methods=["GET", "POST"])
@login_required
def pay():
    card = expiration = cvv = shipping = ""
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
            return redirect(url_for("payment.confirm"))

        flash(error)

    return render_template("payment/pay.html")

# Confirm order button is pressed on pay now page.
@bp.route("/confirm", methods=["GET", "POST"])
@login_required
def confirm():
    if request.method == "POST":
        return redirect(url_for("payment.receipt"))

    return render_template("payment/confirm.html")

@bp.route("/receipt/<int:cart_id>", methods=["GET"])
@login_required
def view_receipt():
    return
