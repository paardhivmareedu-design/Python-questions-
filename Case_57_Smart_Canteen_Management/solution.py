"""
Case Study 57: Smart Canteen Order and Stock Management
Name: Mareedu Paardhiv | Roll No: 26000626
"""

gst_rate = 0.05  # 5% GST

# Menu items: (code, name, unit_price, initial_stock)
initial_menu = [
    ("C1", "Masala Dosa", 45.0, 20),
    ("C2", "Idli Sambar", 30.0, 25),
    ("C3", "Veg Fried Rice", 70.0, 15),
    ("C4", "Filter Coffee", 20.0, 30),
    ("C5", "Samosa Plate", 25.0, 18),
]

# Mutable inventory list: [code, name, price, initial_stock, current_stock, sold_qty]
inventory = []
for code, name, price, stock in initial_menu:
    inventory.append([code, name, price, stock, stock, 0])

orders_log = []

print("=" * 62)
print("          SMART CANTEEN ORDER & STOCK MANAGEMENT SYSTEM")
print("=" * 62)

while True:
    print("\n  MENU: 1. View Stock  2. Place Order  3. Order History  4. Daily Summary  5. Exit")
    choice = input("  Enter choice (1-5): ").strip()

    if choice == "1":
        print("\n  " + "-" * 58)
        print(f"  {'Code':<6} {'Item Name':<18} {'Price(Rs)':>10} {'Available':>10} {'Sold':>8}")
        print("  " + "-" * 58)
        for code, name, price, init_stk, cur_stk, sold in inventory:
            if cur_stk > 0:
                stock_text = str(cur_stk)
            else:
                stock_text = "OUT"
            print(f"  {code:<6} {name:<18} {price:>10.2f} {stock_text:>10} {sold:>8}")
        print("  " + "-" * 58)

    elif choice == "2":
        code_in = input("\n  Enter item code (C1-C5): ").strip().upper()
        selected_item = None
        for item in inventory:
            if item[0] == code_in:
                selected_item = item
                break

        if selected_item is None:
            print(f"\n  REJECTED: Unknown item code '{code_in}'.")
            continue

        qty_in = input("  Enter quantity: ").strip()
        if not qty_in.isdigit():
            print("\n  REJECTED: Quantity must be a positive whole number.")
            continue

        qty = int(qty_in)
        if qty <= 0:
            print("\n  REJECTED: Quantity must be at least 1.")
            continue

        code, name, price, init_stk, cur_stk, sold = selected_item
        if qty > cur_stk:
            print(f"\n  REJECTED: Requested {qty} x {name}, only {cur_stk} left in stock.")
            continue

        subtotal = round(price * qty, 2)
        gst = round(subtotal * gst_rate, 2)
        total = round(subtotal + gst, 2)

        # Update inventory in place
        selected_item[4] = cur_stk - qty
        selected_item[5] = sold + qty

        order_no = len(orders_log) + 1
        orders_log.append((order_no, code, name, qty, subtotal, gst, total))

        print(f"\n  ORDER #{order_no} CONFIRMED: {qty} x {name} ({code}) | Stock left: {selected_item[4]}")
        print(f"    Subtotal: Rs.{subtotal:.2f} | GST (5%): Rs.{gst:.2f} | Bill Total: Rs.{total:.2f}")

    elif choice == "3":
        if len(orders_log) == 0:
            print("\n  No orders recorded yet.")
        else:
            print("\n  ---- ORDER HISTORY ----")
            for ord_no, code, name, qty, sub, gst, tot in orders_log:
                print(f"  #{ord_no:<2} {code} {name:<16} x{qty:<3} -> Rs.{tot:>7.2f}")

    elif choice == "4" or choice == "5":
        total_units = 0
        total_subtotal = 0.0
        total_gst = 0.0
        total_revenue = 0.0

        for _, _, _, qty, sub, gst, tot in orders_log:
            total_units = total_units + qty
            total_subtotal = total_subtotal + sub
            total_gst = total_gst + gst
            total_revenue = total_revenue + tot

        print("\n  " + "=" * 58)
        print("               DAILY CANTEEN SALES & STOCK SUMMARY")
        print("  " + "=" * 58)
        print(f"  Orders Fulfilled : {len(orders_log)}")
        print(f"  Total Items Sold : {total_units}")
        print(f"  Gross Sales      : Rs. {total_subtotal:.2f}")
        print(f"  GST Collected    : Rs. {total_gst:.2f}")
        print(f"  Total Revenue    : Rs. {total_revenue:.2f}")

        print("\n  " + "-" * 58)
        print(f"  {'Code':<6} {'Item Name':<18} {'Price(Rs)':>10} {'Available':>10} {'Sold':>8}")
        print("  " + "-" * 58)
        for code, name, price, init_stk, cur_stk, sold in inventory:
            if cur_stk > 0:
                stock_text = str(cur_stk)
            else:
                stock_text = "OUT"
            print(f"  {code:<6} {name:<18} {price:>10.2f} {stock_text:>10} {sold:>8}")
        print("  " + "-" * 58)

        if choice == "5":
            print("  Closing canteen counter. Goodbye!")
            break

    else:
        print("\n  INVALID CHOICE: Please enter a number from 1 to 5.")
