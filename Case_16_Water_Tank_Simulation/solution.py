"""
Case Study 16: Multi-Day Water Tank Simulation
Name: Mareedu Paardhiv | Roll No: 26000626
"""

capacity = 10000          # maximum tank capacity in litres
level = 3500              # starting water level in litres
min_reserve = 1000        # low reserve alert threshold
target_threshold = 8000   # high-level threshold to detect first crossing

# Daily flow schedule: (day_number, inflow_litres, outflow_litres)
daily_flows = [
    (1, 2200, 1400),
    (2, 1800, 1600),
    (3, 2500, 1100),
    (4, 2400, 1000),
    (5, 3000, 900),    # crosses 8000L threshold here
    (6, 500, 4200),
    (7, 400, 5800),    # drops below 1000L reserve
    (8, 300, 1800),    # shortage occurs here
    (9, 2600, 800),
    (10, 1900, 1200),
]

logs = []
first_threshold_day = -1
total_overflow = 0
total_shortage = 0
overflow_days = []
shortage_days = []

for entry in daily_flows:
    day, inflow, outflow = entry

    if inflow < 0 or outflow < 0:
        logs.append((day, inflow, outflow, level, 0, 0, "INVALID FLOW"))
        continue

    raw_level = level + inflow - outflow
    overflow = 0
    shortage = 0
    status = "NORMAL"

    if raw_level > capacity:
        overflow = raw_level - capacity
        level = capacity
        total_overflow = total_overflow + overflow
        overflow_days.append(day)
        status = "OVERFLOW"
    elif raw_level < 0:
        shortage = -raw_level
        level = 0
        total_shortage = total_shortage + shortage
        shortage_days.append(day)
        status = "SHORTAGE"
    else:
        level = raw_level
        if level < min_reserve:
            status = "LOW RESERVE"
        elif level >= target_threshold:
            status = "HIGH (>=8000L)"

    if first_threshold_day == -1 and level >= target_threshold:
        first_threshold_day = day

    logs.append((day, inflow, outflow, level, overflow, shortage, status))

print("=" * 84)
print(f"       MULTI-DAY WATER TANK SIMULATION (Capacity: {capacity}L | Start: 3500L)")
print("=" * 84)
print(f"{'Day':>3} {'Inflow(L)':>10} {'Outflow(L)':>11} {'EndLevel(L)':>12} "
      f"{'Overflow':>9} {'Shortage':>9}  {'Status'}")
print("-" * 84)

for row in logs:
    day, inf, outf, lvl, ovf, shrt, status = row
    print(f"{day:>3} {inf:>10} {outf:>11} {lvl:>12} {ovf:>9} {shrt:>9}  {status}")

print("-" * 84)
if first_threshold_day != -1:
    print(f"First day reaching threshold ({target_threshold}L): Day {first_threshold_day}")
else:
    print(f"Threshold ({target_threshold}L) was never reached.")

if len(overflow_days) > 0:
    ovf_text = str(overflow_days)
else:
    ovf_text = "None"

if len(shortage_days) > 0:
    shrt_text = str(shortage_days)
else:
    shrt_text = "None"

print(f"Total Overflow : {total_overflow} L (Days: {ovf_text})")
print(f"Total Shortage : {total_shortage} L (Days: {shrt_text})")
print(f"Final Water Level (Day {len(daily_flows)}): {level} L")
print("=" * 84)
