# Case Study 06 — Railway Fare and Reservation Calculator

**Student:** Mareedu Paardhiv | **Roll No:** 26000626

**Syllabus Topics:** Distance slabs, nested conditionals, tuples, lists, concessions, cancellations

## 1. Problem Statement

Calculate fares for multiple passengers using distance slabs, travel classes, age-based concessions, reservation fees, and specified cancellation penalties.

## 2. Objectives

- Calculate progressive distance-based fares across three kilometer slabs.
- Apply class multipliers (SL, 3A, 2A), age-based concessions, and flat reservation fees.
- Evaluate confirmed versus cancelled bookings (early, late, last-minute) to compute penalties and refunds.
- Reject invalid bookings such as negative distance or unknown travel class.

## 3. Assumptions

- Distance rates: Rs. 0.80/km for 0-100 km, Rs. 0.70/km for 101-500 km, and Rs. 0.60/km beyond 500 km.
- Class multipliers & reservation fees: SL (1.0x, Rs. 20), 3A (2.2x, Rs. 40), 2A (3.2x, Rs. 50).
- Concessions on base fare: Infant (<5) travels free with Rs. 0 reservation fee; Child (5-12) gets 50% off; Senior (>=60) gets 40% off.
- Cancellation penalties: Early (>48h) = flat clerkage (SL 60 / 3A 180 / 2A 200); Late (12-48h) = max(clerkage, 25% fare); Last-minute (<12h) = 50% fare.
- Confirmed tickets have Rs. 0 penalty and Rs. 0 refund; net revenue equals total fares retained after refunds.

## 4. Algorithm

```text
1. START
2. Define class_info lookup tuples and the passengers list.
3. For each passenger tuple, unpack (pnr, name, age, dist, t_class, status).
4. Validate age >= 0, dist > 0, valid travel class via a lookup loop, and valid status.
5. Compute dist_fare progressively across 0-100 km, 101-500 km, and >500 km slabs.
6. Multiply by class multiplier, apply age-based concession, and add reservation fee (0 if age < 5) to get total_fare.
7. If status is CONFIRMED, set penalty = 0, refund = 0, retained = total_fare.
8. Otherwise apply early, late, or last-minute cancellation rules to calculate penalty, refund, and retained.
9. Print formatted passenger summary, revenue totals, and rejected bookings.
10. END
```

## 5. Flowchart

![Flowchart](flowchart.png)

## 6. Pseudocode

```text
BEGIN RAILWAY_FARE_CALCULATOR
    DEFINE class_info <- [("SL", 1.0, 20, 60), ("3A", 2.2, 40, 180), ("2A", 3.2, 50, 200)]

    FOR EACH p IN passengers DO
        UNPACK (pnr, name, age, dist, cls, status) <- p
        IF age < 0 OR dist <= 0 OR cls NOT FOUND THEN
            APPEND (pnr, name, "Invalid input") TO invalid_tickets
            CONTINUE
        END IF

        COMPUTE slab distance fare and multiply by class multiplier
        APPLY age concession (<5 free, 5-12 half fare, >=60 40% off)
        ADD reservation fee (0 if age < 5) -> total_fare

        IF status = "CONFIRMED" THEN
            penalty <- 0; refund <- 0; retained <- total_fare
        ELSE
            COMPUTE penalty by cancellation tier
            refund <- total_fare - penalty
            retained <- penalty
        END IF
        APPEND ticket tuple TO valid_tickets
    END FOR

    PRINT fare table, confirmed/cancelled counts, and net revenue
END
```

## 7. Python Source Code

```python
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
```

## 8. Test Cases

| Test ID | Scenario | Expected Result | Status |
| :--- | :--- | :--- | :--- |
| TC-01 | Senior citizen 40% concession in 3A (PNR101) | Total Rs. 610.24; Confirmed refund Rs. 0.00 | PASS |
| TC-02 | Child 50% concession in 2A (PNR103) | Concession 'Child 50%' and total Rs. 635.60 | PASS |
| TC-03 | Infant (<5) free ticket (PNR104) | Total fare and reservation fee both Rs. 0.00 | PASS |
| TC-04 | Cancellation tiers (Early, Late, Last-Min) | Penalties Rs. 60.00, Rs. 420.50, and Rs. 377.50 | PASS |
| TC-05 | Revenue summary & invalid distance (PNR108) | Net revenue Rs. 2,371.84; invalid ticket rejected | PASS |

Run automated tests: `python3 Case_06_Railway_Fare_Calculator/test_cases.py`

## 9. Output & Output Screenshot

![Output Screenshot](output_screenshot.png)

<details>
<summary>View raw console output (output.txt)</summary>

```text
======================================================================================================
                             RAILWAY FARE & RESERVATION SUMMARY
======================================================================================================
PNR      Passenger       Age  Dist Cls  Concession     Total Status            Penalty   Refund
------------------------------------------------------------------------------------------------------
PNR101   Ramesh Babu      65   620 3A   Senior 40%    610.24 CONFIRMED            0.00     0.00
PNR102   Anjali Devi      29   340 SL   None          268.00 CONFIRMED            0.00     0.00
PNR103   Rohan Sai         9   510 2A   Child 50%     635.60 CONFIRMED            0.00     0.00
PNR104   Baby Aditi        3   400 3A   Infant Free     0.00 CONFIRMED            0.00     0.00
PNR105   Suresh Kumar     42   750 2A   None         1682.00 CANCELLED_LATE     420.50  1261.50
PNR106   Meena Kumari     58   180 SL   None          156.00 CANCELLED_EARLY     60.00    96.00
PNR107   Vikram Joshi     34   450 3A   None          755.00 CANCELLED_LAST     377.50   377.50
------------------------------------------------------------------------------------------------------
Confirmed: 4 | Cancelled: 3 | Gross Billed: Rs.4106.84 | Refunds: Rs.1735.00 | Net Revenue: Rs.2371.84
======================================================================================================

REJECTED BOOKINGS:
  PNR108 (Invalid Ticket): Invalid age or distance
```

</details>

## 10. Conclusion

The program models multi-slab railway pricing, passenger concessions, and tiered cancellation refunds using straightforward lists, tuples, conditional statements, and loops. Confirmed and cancelled revenues reconcile accurately against gross billing.
