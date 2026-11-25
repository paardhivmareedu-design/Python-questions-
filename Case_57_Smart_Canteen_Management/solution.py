"""
Case Study 57: Smart Canteen Order and Stock Management
Name: Mareedu Paardhiv | Roll No: 26000626
"""

GST_RATE = 0.05  # 5% GST on canteen bills

# Initial menu items: (code, name, unit_price, initial_stock)
INITIAL_MENU = [
    ("C1", "Masala Dosa", 45.0, 20),
    ("C2", "Idli Sambar", 30.0, 25),
    ("C3", "Veg Fried Rice", 70.0, 15),
    ("C4", "Filter Coffee", 20.0, 30),
    ("C5", "Samosa Plate", 25.0, 18),
]


def create_inventory():
    # Mutable list of lists: [code, name, price, initial_stock, current_stock, sold_qty]
    inventory = []
    for code, name, price, stock in INITIAL_MENU:
        inventory.append([code, name, price, stock, stock, 0])
    return inventory


def find_item(inventory, code):
    target = code.strip().upper()
    for item in inventory:
        if item[0] == target:
            return item
    return None


def show_menu(inventory):
    print("\n  " + "-" * 58)
    print(f"  {'Code':<6} {'Item Name':<18} {'Price(Rs)':>10} {'Available':>10} {'Sold':>8}")
    print("  " + "-" * 58)
    for code, name, price, init_stk, cur_stk, sold in inventory:
        stock_note = str(cur_stk) if cur_stk > 0 else "OUT"
        print(f"  {code:<6} {name:<18} {price:>10.2f} {stock_note:>10} {sold:>8}")
    print("  " + "-" * 58)


def place_order(inventory, orders_log, code_input, qty_input):
    item = find_item(inventory, code_input)
    if item is None:
        return (False, f"REJECTED: Unknown item code '{code_input.strip()}'.")

    qty_clean = qty_input.strip()
    if not qty_clean.isdigit():
        return (False, "REJECTED: Quantity must be a positive whole number.")

    qty = int(qty_clean)
    if qty <= 0:
        return (False, "REJECTED: Quantity must be at least 1.")

    code, name, price, init_stk, cur_stk, sold = item
    if qty > cur_stk:
        return (False, f"REJECTED: Requested {qty} x {name}, only {cur_stk} left in stock.")

    subtotal = round(price * qty, 2)
    gst = round(subtotal * GST_RATE, 2)
    total = round(subtotal + gst, 2)

    # Update inventory in place
    item[4] = cur_stk - qty
    item[5] = sold + qty

    order_no = len(orders_log) + 1
    order_record = (order_no, code, name, qty, subtotal, gst, total)
    orders_log.append(order_record)

    msg = (f"ORDER #{order_no} CONFIRMED: {qty} x {name} ({code}) | Stock left: {item[4]}\n"
           f"    Subtotal: Rs.{subtotal:.2f} | GST (5%): Rs.{gst:.2f} | Bill Total: Rs.{total:.2f}")
    return (True, msg)


def print_summary(inventory, orders_log):
    total_units = 0
    total_subtotal = 0.0
    total_gst = 0.0
    total_revenue = 0.0

    for _, _, _, qty, sub, gst, tot in orders_log:
        total_units += qty
        total_subtotal += sub
        total_gst += gst
        total_revenue += tot

    print("\n  " + "=" * 58)
    print("               DAILY CANTEEN SALES & STOCK SUMMARY")
    print("  " + "=" * 58)
    print(f"  Orders Fulfilled : {len(orders_log)}")
    print(f"  Total Items Sold : {total_units}")
    print(f"  Gross Sales      : Rs. {total_subtotal:.2f}")
    print(f"  GST Collected    : Rs. {total_gst:.2f}")
    print(f"  Total Revenue    : Rs. {total_revenue:.2f}")
    show_menu(inventory)


def main():
    inventory = create_inventory()
    orders_log = []

    print("=" * 62)
    print("          SMART CANTEEN ORDER & STOCK MANAGEMENT SYSTEM")
    print("=" * 62)

    while True:
        print("\n  MENU: 1. View Stock  2. Place Order  3. Order History  4. Daily Summary  5. Exit")
        choice = input("  Enter choice (1-5): ").strip()

        if choice == "1":
            print()
            show_menu(inventory)
        elif choice == "2":
            code = input("\n  Enter item code (C1-C5): ")
            if find_item(inventory, code) is None:
                print(f"\n  REJECTED: Unknown item code '{code.strip()}'.")
                continue
            qty = input("  Enter quantity: ")
            ok, message = place_order(inventory, orders_log, code, qty)
            print("\n  " + message)
        elif choice == "3":
            if len(orders_log) == 0:
                print("\n  No orders recorded yet.")
            else:
                print("\n  ---- ORDER HISTORY ----")
                for ord_no, code, name, qty, sub, gst, tot in orders_log:
                    print(f"  #{ord_no:<2} {code} {name:<16} x{qty:<3} -> Rs.{tot:>7.2f}")
        elif choice == "4":
            print()
            print_summary(inventory, orders_log)
        elif choice == "5":
            print()
            print_summary(inventory, orders_log)
            print("  Closing canteen counter. Goodbye!")
            break
        else:
            print("\n  INVALID CHOICE: Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
