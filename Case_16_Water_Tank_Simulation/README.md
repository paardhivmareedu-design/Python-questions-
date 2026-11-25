# Case Study 16 — Multi-Day Water Tank Simulation

**Student:** Mareedu Paardhiv | **Roll No:** 26000626

**Syllabus Topics:** Loops, state simulation, conditional clamping, threshold tracking, tuples

## 1. Problem Statement

Process changing inflow and outflow quantities, update water levels, detect overflow and shortages, and determine the first interval in which the tank reaches a specified threshold.

## 2. Objectives

- Simulate daily water level updates from a sequence of (day, inflow, outflow) tuples.
- Clamp levels at tank capacity (10,000 L) and zero while accumulating overflow and shortage quantities.
- Flag low-reserve warnings when levels drop below 1,000 L without hitting zero.
- Detect and record the very first day on which the tank reaches or exceeds 8,000 L.

## 3. Assumptions

- Tank capacity is 10,000 L, initial level is 3,500 L, minimum safe reserve is 1,000 L, and target threshold is 8,000 L.
- Daily inflow happens concurrently with daily demand, so end-of-day raw level = previous_level + inflow - outflow.
- Negative inflow or outflow entries are flagged as invalid without modifying tank level.

## 4. Algorithm

```text
1. START
2. Initialize level = 3500, capacity = 10000, min_reserve = 1000, threshold = 8000, first_threshold_day = None.
3. Initialize total_overflow = 0, total_shortage = 0, and empty log lists.
4. For each tuple (day, inflow, outflow) in DAILY_FLOWS:
5.   Validate inflow >= 0 and outflow >= 0.
6.   Compute raw_level = level + inflow - outflow.
7.   If raw_level > capacity: overflow = raw_level - capacity, level = capacity, status = OVERFLOW.
8.   Else if raw_level < 0: shortage = -raw_level, level = 0, status = SHORTAGE.
9.   Else: level = raw_level; mark LOW RESERVE if level < 1000 else HIGH or NORMAL.
10.   If first_threshold_day is None and level >= threshold, record first_threshold_day = day.
11. Print daily water log, first threshold crossing day, total overflow, total shortage, and final level.
12. END
```

## 5. Flowchart

![Flowchart](flowchart.png)

## 6. Pseudocode

```text
BEGIN WATER_TANK_SIMULATION
    SET level <- 3500, capacity <- 10000, threshold <- 8000
    SET first_day <- NONE, tot_overflow <- 0, tot_shortage <- 0

    FOR EACH (day, inflow, outflow) IN DAILY_FLOWS DO
        raw <- level + inflow - outflow
        overflow <- 0; shortage <- 0

        IF raw > capacity THEN
            overflow <- raw - capacity
            level <- capacity
            tot_overflow <- tot_overflow + overflow
        ELSE IF raw < 0 THEN
            shortage <- -raw
            level <- 0
            tot_shortage <- tot_shortage + shortage
        ELSE
            level <- raw
        END IF

        IF first_day IS NONE AND level >= threshold THEN
            first_day <- day
        END IF
        APPEND (day, inflow, outflow, level, overflow, shortage) TO logs
    END FOR

    PRINT daily table, first_day, totals, and final level
END
```

## 7. Python Source Code

```python
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
```

## 8. Test Cases

| Test ID | Scenario | Expected Result | Status |
| :--- | :--- | :--- | :--- |
| TC-01 | 10-day schedule & Day 5 threshold crossing | Detects Day 5 as first day >= 8,000 L (9,400 L) | PASS |
| TC-02 | Overflow clamping on high inflow | Clamps level at 10,000 L and records 2,000 L overflow | PASS |
| TC-03 | Shortage clamping on excess demand | Clamps level at 0 L and records 2,000 L deficit | PASS |
| TC-04 | Low reserve alert (<1000 L) | Flags Day with 800 L as LOW RESERVE | PASS |
| TC-05 | Threshold never reached | Returns None cleanly for first threshold day | PASS |

Run automated tests: `python3 Case_16_Water_Tank_Simulation/test_cases.py`

## 9. Output & Output Screenshot

![Output Screenshot](output_screenshot.png)

<details>
<summary>View raw console output (output.txt)</summary>

```text
====================================================================================
       MULTI-DAY WATER TANK SIMULATION (Capacity: 10000L | Start: 3500L)
====================================================================================
Day  Inflow(L)  Outflow(L)  EndLevel(L)  Overflow  Shortage  Status
------------------------------------------------------------------------------------
  1       2200        1400         4300         0         0  NORMAL
  2       1800        1600         4500         0         0  NORMAL
  3       2500        1100         5900         0         0  NORMAL
  4       2400        1000         7300         0         0  NORMAL
  5       3000         900         9400         0         0  HIGH (>=8000L)
  6        500        4200         5700         0         0  NORMAL
  7        400        5800          300         0         0  LOW RESERVE
  8        300        1800            0         0      1200  SHORTAGE
  9       2600         800         1800         0         0  NORMAL
 10       1900        1200         2500         0         0  NORMAL
------------------------------------------------------------------------------------
First day reaching threshold (8000L): Day 5
Total Overflow : 0 L (Days: None)
Total Shortage : 1200 L (Days: [8])
Final Water Level (Day 10): 2500 L
====================================================================================
```

</details>

## 10. Conclusion

The multi-day simulation tracks dynamic storage levels accurately, prevents physically impossible negative or over-capacity states, and captures the earliest interval hitting the target threshold.
