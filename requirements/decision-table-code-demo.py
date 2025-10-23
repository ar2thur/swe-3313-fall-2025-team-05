import random


def login_decision_table(doesUsernameExist: bool, isPasswordValid: bool, isAdminUser: bool) -> bool:
    if doesUsernameExist:

        if isPasswordValid:

            if isAdminUser:
                print("Logged in as admin")
                return True

            else:
                print("Logged in as user")
                return True
        else:
            print("Invaild Password")
            return False
    else:
        print("User not found")
        return False

def test_login_decision_table():
    assert True == (login_decision_table(True, True, False)) # Log in user True
    assert True == (login_decision_table(True, True, True)) # Log in admin True

    assert False == (login_decision_table(True, False, False)) # Show invalid password False
    assert False == (login_decision_table(True, False, True)) # Show invalid password False

    assert False == (login_decision_table(False, False, False)) # Show user does not exist False
    assert False == (login_decision_table(False, True, False)) # Show user does not exist False
    assert False == (login_decision_table(False, False, True)) # Show user does not exist False
    assert False == (login_decision_table(False, True, True)) # Show user does not exist False


def checkout_decision_table(isCartNotEmpty: bool, shippingType: str, isValidPayment: bool) -> bool:
    shipping_cost = None
    if not isCartNotEmpty:

        if isValidPayment:
            random_shopping_cart_total = random.randint(10, 30)
            match shippingType:
                case "Overnight":
                    shipping_cost = 29

                case "3-Day":
                    shipping_cost = 19

                case _:
                    shipping_cost = 0

            print(f"Items in cart: {random_shopping_cart_total}")

            random_shopping_cart_total *= 1.6 # sales tax
            print(f"Subtotal with sales tax: {random_shopping_cart_total}")

            print(f"Shipping cost: {shipping_cost}")

            total = random_shopping_cart_total + shipping_cost
            print(f"Confirm order for {total}?")

            return True

        else:
            print("Payment invalid")
            return False

    else:
        print("Cannot checkout with empty cart")
        return False


def test_checkout_decision_table():
    assert True == checkout_design_table(False, "Overnight", True) #show confirm True
    assert True == checkout_design_table(False, "3-Day", True) # show confirm True
    assert True == checkout_design_table(False, "Ground", True) # show confirm True

    assert False == checkout_design_table(True, "Ground", True) # Cart empty False
    assert False == checkout_design_table(True, "Ground", False) # Cart empty False
    assert False == checkout_design_table(False, "Ground", False) # Payment invalid False


def inventory_management_decision_table(isAdminLoggedIn: bool, isItemInfoComplete: bool) -> bool:
    if isAdminLoggedIn:

        if isItemInfoComplete:
            print("Item added into the database")
            return True

        else:
            print("item has missing data, cannot complete")
            return False

    else:
        print("Permission Denied")
        return False


def test_inventory_management_decision_table():
    assert True == inventory_management_decision_table(True, True)

    assert False == inventory_management_decision_table(True, False)
    assert False == inventory_management_decision_table(False, True)
    assert False == inventory_management_decision_table(False, False)

def sales_report_decision_table(isAdminLoggedIn: bool, doesReportExist: bool) -> bool:
    if isAdminLoggedIn:

        if doesReportExist:
            print("Here is the Report")
            return True

        else:
             print("Report not found")
             return False

    else:
        print("Permission Denied")
        return False


def test_sales_report_decision_table():
    assert True == sales_report_decision_table(True, True)
    
    assert False == sales_report_decision_table(True, False)
    assert False == sales_report_decision_table(False, False)

