"""
This is an interactive code example for our decision tables
"""

def login_decision_table() -> None:
    doesUsernameExist = _input_to_bool(input("Does the username exist? (y/N): "))

    if doesUsernameExist:
        isPasswordValid = _input_to_bool(input("Is the password correct? (y/N): "))

        if isPasswordValid:
            isAdminUser = _input_to_bool(input("Is the user an admin user? (y/N): "))

            if isAdminUser:
                print("Logged in as admin")

            else:
                print("Logged in as user")
        else:
            print("Invaild Password")
    else:
        print("User not found")

def checkout_decision_table() -> None:
    shipping_cost = None
    isCartNotEmpty = _input_to_bool(input("Is the shopping cart non-empty? (y/N): "))

    if isCartNotEmpty:
        shopping_cart_total = float(input("How much was in the shopping cart? (xxx.xx): "))
        isValidPayment = _input_to_bool(input("Is the payment vaild? (y/N): "))

        if isValidPayment:
            shippingType = input("What is the shipping type? (Overnight, 3-Day, Ground): ").strip().lower()

            match shippingType:
                case "overnight":
                    shipping_cost = 29

                case "3-day":
                    shipping_cost = 19

                case _:
                    shipping_cost = 0

            print(f"Items in cart: {shopping_cart_total}")

            shopping_cart_total *= 1.06 # sales tax
            print(f"Subtotal with sales tax: {shopping_cart_total}")

            print(f"Shipping cost: {shipping_cost}")

            total = shopping_cart_total + shipping_cost
            print(f"Confirm order for {total}?")

        else:
            print("Payment invalid")

    else:
        print("Cannot checkout with empty cart")

def inventory_management_decision_table() -> None:
    isAdminLoggedIn = _input_to_bool(input("Is an admin user logged in? (y/N): "))

    if isAdminLoggedIn:
        isItemInfoComplete = _input_to_bool(input("Is the item info completely filled out? (y/N): "))

        if isItemInfoComplete:
            print("Item added into the database")

        else:
            print("item has missing data, cannot complete")

    else:
        print("Permission Denied")

def sales_report_decision_table() -> None:
    isAdminLoggedIn = _input_to_bool(input("Is an admin user logged in? (y/N): "))

    if isAdminLoggedIn:
        doesReportExist = _input_to_bool(input("Does the report exist? (y/N): "))

        if doesReportExist:
            print("Random_Report.csv")

        else:
             print("Report not found")

    else:
        print("Permission Denied")

def _input_to_bool(x: str) -> bool:
    return x.strip().lower() == 'y'



def main():
    print("[Desision Table Test]")
    print()
    print("1) Login Decision Table")
    print()
    login_decision_table()
    print()
    print("2) Checkout Decision Table")
    print()
    checkout_decision_table()
    print()
    print("3) Inventory Management Decision Table")
    print()
    inventory_management_decision_table()
    print()
    print("4) Sales Report Decision Table")
    print()
    sales_report_decision_table()
    print()
    print("Test done")

main()
