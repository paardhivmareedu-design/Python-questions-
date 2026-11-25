"""
Case Study 06: Railway Fare and Reservation Calculator
Name: Mareedu Paardhiv | Roll No: 26000626
"""

# Travel class multipliers and flat reservation fees
CLASS_INFO = [
    ("SL", "Sleeper", 1.0, 20.0, 60.0),
    ("3A", "AC 3-Tier", 2.2, 40.0, 180.0),
    ("2A", "AC 2-Tier", 3.2, 50.0, 200.0),
]

# Passenger records:
# (ticket_id, name, age, distance_km, travel_class, booking_status)
# booking_status: CONFIRMED, CANCELLED_EARLY (>48h), CANCELLED_LATE (12-48h), CANCELLED_LAST (<12h)
PASSENGERS = [
    ("PNR101", "Ramesh Babu", 65, 620, "3A", "CONFIRMED"),
    ("PNR102", "Anjali Devi", 29, 340, "SL", "CONFIRMED"),
    ("PNR103", "Rohan Sai", 9, 510, "2A", "CONFIRMED"),
    ("PNR104", "Baby Aditi", 3, 400, "3A", "CONFIRMED"),
    ("PNR105", "Suresh Kumar", 42, 750, "2A", "CANCELLED_LATE"),
    ("PNR106", "Meena Kumari", 58, 180, "SL", "CANCELLED_EARLY"),
    ("PNR107", "Vikram Joshi", 34, 450, "3A", "CANCELLED_LAST"),
    ("PNR108", "Invalid Ticket", 25, -50, "SL", "CONFIRMED"),
]


def get_class_details(code):
    for item in CLASS_INFO:
        c_code, c_name, mult, res_fee, clerkage = item
        if c_code == code:
            return item
    return None


def calculate_distance_base(distance):
    # Slabs: 0-100 km @ 0.80, 101-500 km @ 0.70, >500 km @ 0.60
    if distance <= 100:
        return distance * 0.80
    elif distance <= 500:
        return (100 * 0.80) + ((distance - 100) * 0.70)
    else:
        return (100 * 0.80) + (400 * 0.70) + ((distance - 500) * 0.60)


def get_concession_rate(age):
    if age < 5:
        return 1.00, "Infant Free"
    elif age <= 12:
        return 0.50, "Child 50%"
    elif age >= 60:
        return 0.40, "Senior 40%"
    else:
        return 0.00, "None"


def compute_ticket(passenger):
    pnr, name, age, distance, t_class, status = passenger

    if age < 0 or distance <= 0:
        return (False, pnr, name, "Invalid age or distance")

    cls_details = get_class_details(t_class)
    if cls_details is None:
        return (False, pnr, name, "Unknown travel class")

    _, class_name, multiplier, res_fee, clerkage = cls_details

    base_fare = calculate_distance_base(distance) * multiplier
    conc_rate, conc_label = get_concession_rate(age)
    concession_amt = base_fare * conc_rate
    discounted_fare = base_fare - concession_amt

    applied_res_fee = 0.0 if age < 5 else res_fee
    total_fare = round(discounted_fare + applied_res_fee, 2)

    if status == "CONFIRMED":
        penalty = 0.0
        refund = 0.0
        net_retained = total_fare
    elif status == "CANCELLED_EARLY":
        penalty = min(total_fare, clerkage)
        refund = round(total_fare - penalty, 2)
        net_retained = penalty
    elif status == "CANCELLED_LATE":
        penalty = max(clerkage, round(total_fare * 0.25, 2))
        penalty = min(total_fare, penalty)
        refund = round(total_fare - penalty, 2)
        net_retained = penalty
    elif status == "CANCELLED_LAST":
        penalty = round(total_fare * 0.50, 2)
        refund = round(total_fare - penalty, 2)
        net_retained = penalty
    else:
        return (False, pnr, name, "Unknown booking status")

    return (
        True,
        (
            pnr,
            name,
            age,
            distance,
            t_class,
            conc_label,
            round(base_fare, 2),
            applied_res_fee,
            total_fare,
            status,
            penalty,
            refund,
            net_retained,
        ),
    )


def main():
    valid_tickets = []
    invalid_tickets = []

    for p in PASSENGERS:
        res = compute_ticket(p)
        if res[0]:
            valid_tickets.append(res[1])
        else:
            invalid_tickets.append((res[1], res[2], res[3]))

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
        (pnr, name, age, dist, t_cls, conc_lbl, base_f, res_f,
         total_f, status, penalty, refund, retained) = t

        print(f"{pnr:<8} {name:<15} {age:>3} {dist:>5} {t_cls:<4} {conc_lbl:<11} "
              f"{total_f:>8.2f} {status:<16} {penalty:>8.2f} {refund:>8.2f}")

        gross_billed += total_f
        total_refunds += refund
        net_revenue += retained
        if status == "CONFIRMED":
            confirmed_count += 1
        else:
            cancelled_count += 1

    print("-" * 102)
    print(f"Confirmed: {confirmed_count} | Cancelled: {cancelled_count} | "
          f"Gross Billed: Rs.{gross_billed:.2f} | Refunds: Rs.{total_refunds:.2f} | "
          f"Net Revenue: Rs.{net_revenue:.2f}")
    print("=" * 102)

    if len(invalid_tickets) > 0:
        print("\nREJECTED BOOKINGS:")
        for pnr, name, reason in invalid_tickets:
            print(f"  {pnr} ({name}): {reason}")


if __name__ == "__main__":
    main()
