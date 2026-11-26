# Case Study 16 — Multi-Day Water Tank Simulation

**Student:** Mareedu Paardhiv | **Roll No:** 26000626

**Syllabus Topics:** Loops, state simulation, conditional clamping, threshold tracking, tuples

## 1. Problem Statement

Process changing inflow and outflow quantities, update water levels, detect overflow and shortages, and determine the first interval in which the tank reaches a specified threshold.

## 2. Objectives

- Simulate daily water level updates from a sequence of `(day, inflow, outflow)` tuples.
- Clamp levels at tank capacity (10,000 L) and zero while accumulating overflow and shortage quantities.
- Flag low-reserve warnings when levels drop below 1,000 L without hitting zero.
- Detect and record the very first day on which the tank reaches or exceeds 8,000 L.

## 3. Assumptions

- Tank capacity is 10,000 L, starting level is 3,500 L, minimum reserve is 1,000 L, and target threshold is 8,000 L.
- End-of-day raw level equals `previous_level + inflow - outflow`.
- Negative inflow or outflow entries are flagged as invalid without modifying tank level.

## 4. Algorithm

```text
1. START
2. Initialize capacity = 10000, level = 3500, min_reserve = 1000, target_threshold = 8000, first_threshold_day = -1.
3. Initialize total_overflow = 0, total_shortage = 0, and empty log lists.
4. For each tuple (day, inflow, outflow) in daily_flows:
5.   Validate inflow >= 0 and outflow >= 0.
6.   Compute raw_level = level + inflow - outflow.
7.   If raw_level > capacity: add excess to total_overflow, set level = capacity, mark OVERFLOW.
8.   Else if raw_level < 0: add deficit to total_shortage, set level = 0, mark SHORTAGE.
9.   Else: set level = raw_level; mark LOW RESERVE if < 1000 else HIGH (>=8000L) or NORMAL.
10.   If first_threshold_day == -1 and level >= 8000, set first_threshold_day = day.
11. Print daily log, first threshold crossing day, total overflow, total shortage, and final water level.
12. END
```

## 5. Flowchart

![Flowchart](flowchart.png)

## 6. Pseudocode

```text
BEGIN WATER_TANK_SIMULATION
    SET level <- 3500, capacity <- 10000, target_threshold <- 8000
    SET first_threshold_day <- -1, total_overflow <- 0, total_shortage <- 0

    FOR EACH (day, inflow, outflow) IN daily_flows DO
        raw_level <- level + inflow - outflow
        overflow <- 0; shortage <- 0

        IF raw_level > capacity THEN
            overflow <- raw_level - capacity
            level <- capacity
            total_overflow <- total_overflow + overflow
        ELSE IF raw_level < 0 THEN
            shortage <- -raw_level
            level <- 0
            total_shortage <- total_shortage + shortage
        ELSE
            level <- raw_level
        END IF

        IF first_threshold_day = -1 AND level >= target_threshold THEN
            first_threshold_day <- day
        END IF
        APPEND (day, inflow, outflow, level, overflow, shortage, status) TO logs
    END FOR

    PRINT daily table, first_threshold_day, totals, and final level
END
```

## 7. Python Source Code

```python
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
```

## 8. Test Cases

| Test ID | Scenario | Expected Result | Status |
| :--- | :--- | :--- | :--- |
| TC-01 | 10-day schedule & Day 5 threshold crossing | Detects Day 5 as first day >= 8,000 L (9,400 L) | PASS |
| TC-02 | Low reserve alert on Day 7 (300 L) | Flags Day 7 as LOW RESERVE below 1,000 L | PASS |
| TC-03 | Shortage clamping on Day 8 | Clamps level at 0 L and records 1,200 L deficit | PASS |
| TC-04 | Final level & zero overflow | Final level 2,500 L on Day 10; total overflow 0 L | PASS |

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

The multi-day simulation tracks dynamic tank levels cleanly using loops and conditionals, prevents impossible negative or over-capacity states, and captures the earliest interval reaching the target threshold.
