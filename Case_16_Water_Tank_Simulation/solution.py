"""
Case Study 16: Multi-Day Water Tank Simulation
Name: Mareedu Paardhiv | Roll No: 26000626
"""

TANK_CAPACITY = 10000      # litres
INITIAL_LEVEL = 3500       # litres
MIN_RESERVE = 1000         # low-water alert level (litres)
TARGET_THRESHOLD = 8000    # high-level threshold to detect first crossing

# Daily schedule: (day, inflow_litres, outflow_litres)
DAILY_FLOWS = [
    (1, 2200, 1400),
    (2, 1800, 1600),
    (3, 2500, 1100),
    (4, 2400, 1000),   # reaches >= 8000 here
    (5, 3000, 900),    # overflow occurs here
    (6, 500, 4200),
    (7, 400, 5800),    # low reserve alert
    (8, 300, 1800),    # critical shortage (deficit)
    (9, 2600, 800),
    (10, 1900, 1200),
]


def simulate_tank(schedule, capacity=TANK_CAPACITY, initial=INITIAL_LEVEL,
                  min_reserve=MIN_RESERVE, threshold=TARGET_THRESHOLD):
    level = initial
    logs = []
    first_threshold_day = None
    total_overflow = 0
    total_shortage = 0
    overflow_days = []
    shortage_days = []

    for entry in schedule:
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
            total_overflow += overflow
            overflow_days.append(day)
            status = "OVERFLOW"
        elif raw_level < 0:
            shortage = -raw_level
            level = 0
            total_shortage += shortage
            shortage_days.append(day)
            status = "SHORTAGE"
        else:
            level = raw_level
            if level < min_reserve:
                status = "LOW RESERVE"
            elif level >= threshold:
                status = "HIGH (>=8000L)"

        if first_threshold_day is None and level >= threshold:
            first_threshold_day = day

        logs.append((day, inflow, outflow, level, overflow, shortage, status))

    summary = (
        level,
        first_threshold_day,
        total_overflow,
        total_shortage,
        overflow_days,
        shortage_days,
    )
    return logs, summary


def main():
    logs, summary = simulate_tank(DAILY_FLOWS)
    final_level, first_day, tot_ovf, tot_shrt, ovf_days, shrt_days = summary

    print("=" * 84)
    print(f"       MULTI-DAY WATER TANK SIMULATION (Capacity: {TANK_CAPACITY}L | Start: {INITIAL_LEVEL}L)")
    print("=" * 84)
    print(f"{'Day':>3} {'Inflow(L)':>10} {'Outflow(L)':>11} {'EndLevel(L)':>12} "
          f"{'Overflow':>9} {'Shortage':>9}  {'Status'}")
    print("-" * 84)

    for row in logs:
        day, inf, outf, lvl, ovf, shrt, status = row
        print(f"{day:>3} {inf:>10} {outf:>11} {lvl:>12} {ovf:>9} {shrt:>9}  {status}")

    print("-" * 84)
    if first_day is not None:
        print(f"First day reaching threshold ({TARGET_THRESHOLD}L): Day {first_day}")
    else:
        print(f"Threshold ({TARGET_THRESHOLD}L) was never reached.")

    print(f"Total Overflow : {tot_ovf} L (Days: {ovf_days if ovf_days else 'None'})")
    print(f"Total Shortage : {tot_shrt} L (Days: {shrt_days if shrt_days else 'None'})")
    print(f"Final Water Level (Day {len(DAILY_FLOWS)}): {final_level} L")
    print("=" * 84)


if __name__ == "__main__":
    main()
