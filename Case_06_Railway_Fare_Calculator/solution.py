"""
Case Study 06: Railway Fare and Reservation Calculator
Name: Mareedu Paardhiv | Roll No: 26000626
"""

# Class table: (class_code, multiplier, reservation_fee, early_clerkage)
class_info = [
    ("SL", 1.0, 20.0, 60.0),
    ("3A", 2.2, 40.0, 180.0),
    ("2A", 3.2, 50.0, 200.0),
]

# Passenger records: (pnr, name, age, distance_km, travel_class, status)
passengers = [
    ("PNR101", "Ramesh Babu", 65, 620, "3A", "CONFIRMED"),
    ("PNR102", "Anjali Devi", 29, 340, "SL", "CONFIRMED"),
    ("PNR103", "Rohan Sai", 9, 510, "2A", "CONFIRMED"),
    ("PNR104", "Baby Aditi", 3, 400, "3A", "CONFIRMED"),
    ("PNR105", "Suresh Kumar", 42, 750, "2A", "CANCELLED_LATE"),
    ("PNR106", "Meena Kumari", 58, 180, "SL", "CANCELLED_EARLY"),
    ("PNR107", "Vikram Joshi", 34, 450, "3A", "CANCELLED_LAST"),
    ("PNR108", "Invalid Ticket", 25, -50, "SL", "CONFIRMED"),
]

valid_tickets = []
invalid_tickets = []

for p in passengers:
    pnr, name, age, dist, t_class, status = p

    if age < 0 or dist <= 0:
        invalid_tickets.append((pnr, name, "Invalid age or distance"))
        continue

    # Find travel class details
    found_class = False
    mult = 1.0
    res_fee = 0.0
    clerkage = 0.0
    for c in class_info:
        c_code, c_mult, c_res, c_clerk = c
        if c_code == t_class:
            found_class = True
            mult = c_mult
            res_fee = c_res
            clerkage = c_clerk
            break

    if not found_class:
        invalid_tickets.append((pnr, name, "Unknown travel class"))
        continue

    # Progressive distance slabs: 0-100 @ 0.80, 101-500 @ 0.70, >500 @ 0.60
    if dist <= 100:
        dist_fare = dist * 0.80
    elif dist <= 500:
        dist_fare = (100 * 0.80) + ((dist - 100) * 0.70)
    else:
        dist_fare = (100 * 0.80) + (400 * 0.70) + ((dist - 500) * 0.60)

    base_fare = dist_fare * mult

    # Age-based concession
    if age < 5:
        conc_rate = 1.00
        conc_label = "Infant Free"
        applied_res = 0.0
    elif age <= 12:
        conc_rate = 0.50
        conc_label = "Child 50%"
        applied_res = res_fee
    elif age >= 60:
        conc_rate = 0.40
        conc_label = "Senior 40%"
        applied_res = res_fee
    else:
        conc_rate = 0.00
        conc_label = "None"
        applied_res = res_fee

    discounted_fare = base_fare - (base_fare * conc_rate)
    total_fare = round(discounted_fare + applied_res, 2)

    # Cancellation rules
    if status == "CONFIRMED":
        penalty = 0.0
        refund = 0.0
        retained = total_fare
    elif status == "CANCELLED_EARLY":
        penalty = min(total_fare, clerkage)
        refund = round(total_fare - penalty, 2)
        retained = penalty
    elif status == "CANCELLED_LATE":
        pct_pen = round(total_fare * 0.25, 2)
        if clerkage > pct_pen:
            penalty = clerkage
        else:
            penalty = pct_pen
        penalty = min(total_fare, penalty)
        refund = round(total_fare - penalty, 2)
        retained = penalty
    elif status == "CANCELLED_LAST":
        penalty = round(total_fare * 0.50, 2)
        refund = round(total_fare - penalty, 2)
        retained = penalty
    else:
        invalid_tickets.append((pnr, name, "Unknown booking status"))
        continue

    valid_tickets.append((
        pnr, name, age, dist, t_class, conc_label,
        total_fare, status, penalty, refund, retained
    ))

print("=" * 102)
print("                             RAILWAY FARE & RESERVATION SUMMARY")
print("=" * 102)
print(f"{'PNR':<8} {'Passenger':<15} {'Age':>3} {'Dist':>5} {'Cls':<4} {'Concession':<11} "
      f"{'Total':>8} {'Status':<16} {'Penalty':>8} {'Refund':>8}")
print("-" * 102)

gross_billed = 0.0
total_refunds = 0.0
net_revenue = 0.0
confirmed_count = 0
cancelled_count = 0

for t in valid_tickets:
    pnr, name, age, dist, t_class, conc_label, total_f, status, penalty, refund, retained = t
    print(f"{pnr:<8} {name:<15} {age:>3} {dist:>5} {t_class:<4} {conc_label:<11} "
          f"{total_f:>8.2f} {status:<16} {penalty:>8.2f} {refund:>8.2f}")

    gross_billed = gross_billed + total_f
    total_refunds = total_refunds + refund
    net_revenue = net_revenue + retained

    if status == "CONFIRMED":
        confirmed_count = confirmed_count + 1
    else:
        cancelled_count = cancelled_count + 1

print("-" * 102)
print(f"Confirmed: {confirmed_count} | Cancelled: {cancelled_count} | "
      f"Gross Billed: Rs.{gross_billed:.2f} | Refunds: Rs.{total_refunds:.2f} | "
      f"Net Revenue: Rs.{net_revenue:.2f}")
print("=" * 102)

if len(invalid_tickets) > 0:
    print("\nREJECTED BOOKINGS:")
    for pnr, name, reason in invalid_tickets:
        print(f"  {pnr} ({name}): {reason}")
