# Case Study 37 — Nested Loop Calendar Generator

**Student:** Mareedu Paardhiv | **Roll No:** 26000626

**Syllabus Topics:** Nested loops, pattern/grid generation, alignment, input validation, leap years

## 1. Problem Statement

Generate a formatted monthly calendar using the supplied starting weekday and number of days, correctly aligning weeks and handling valid month lengths.

## 2. Objectives

- Validate supplied month lengths (28, 29, 30, 31) and starting weekday indices (0=Sun to 6=Sat).
- Determine exact February days accurately using leap-year divisibility rules.
- Use nested loops (outer week loop, inner 7-column weekday loop) to align leading blanks and day numbers.
- Produce clear diagnostic errors for invalid day counts or weekday indices.

## 3. Assumptions

- Weekday indexing starts at 0 for Sunday and ends at 6 for Saturday.
- A year is a leap year when divisible by 4 and not 100, or divisible by 400.
- Each date cell occupies a fixed 4-character right-aligned column so columns stay vertically aligned.

## 4. Algorithm

```text
1. START
2. Read calendar title, num_days, and start_weekday (or derive num_days from month & year).
3. Validate num_days in (28, 29, 30, 31) and 0 <= start_weekday <= 6. If invalid, print error and stop.
4. Print title banner and weekday header ('Sun  Mon  Tue  Wed  Thu  Fri  Sat').
5. Compute total_weeks = (start_weekday + num_days + 6) // 7 and set day = 1.
6. Outer loop: for week from 0 to total_weeks - 1:
7.   Initialize row_str = ''.
8.   Inner loop: for col from 0 to 6:
9.     Compute cell_index = week * 7 + col.
10.     If cell_index < start_weekday or day > num_days, append 4 spaces; else append formatted day and increment day.
11.   Print row_str.
12. Print closing separator line.
13. END
```

## 5. Flowchart

![Flowchart](flowchart.png)

## 6. Pseudocode

```text
BEGIN NESTED_LOOP_CALENDAR
    IF num_days NOT IN (28, 29, 30, 31) OR start_weekday < 0 OR start_weekday > 6 THEN
        PRINT "INVALID INPUT"; RETURN FALSE
    END IF

    PRINT title AND "Sun Mon Tue Wed Thu Fri Sat"
    total_weeks <- (start_weekday + num_days + 6) // 7
    day <- 1

    FOR week <- 0 TO total_weeks - 1 DO
        row <- ""
        FOR col <- 0 TO 6 DO
            cell <- (week * 7) + col
            IF cell < start_weekday OR day > num_days THEN
                row <- row + "    "
            ELSE
                row <- row + FORMAT_RIGHT_4(day)
                day <- day + 1
            END IF
        END FOR
        PRINT row
    END FOR
    RETURN TRUE
END
```

## 7. Python Source Code

```python
"""
Case Study 37: Nested Loop Calendar Generator
Name: Mareedu Paardhiv | Roll No: 26000626
"""

WEEKDAYS = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
MONTH_NAMES = (
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
)
VALID_LENGTHS = (28, 29, 30, 31)


def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def get_month_days(month, year):
    if month < 1 or month > 12:
        return None
    if month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    elif month in (4, 6, 9, 11):
        return 30
    else:
        return 29 if is_leap_year(year) else 28


def build_calendar_lines(title, num_days, start_weekday):
    """Build formatted calendar lines using nested loops and validate inputs."""
    if num_days not in VALID_LENGTHS:
        return (False, [f"INVALID: month length {num_days} must be 28, 29, 30, or 31."])

    if start_weekday < 0 or start_weekday > 6:
        return (False, [f"INVALID: starting weekday {start_weekday} must be between 0 (Sun) and 6 (Sat)."])

    lines = []
    width = 28
    lines.append("=" * width)
    lines.append(title.center(width))
    lines.append("=" * width)

    header = ""
    for w in range(7):
        header += f"{WEEKDAYS[w]:>4}"
    lines.append(header)
    lines.append("-" * width)

    total_cells = start_weekday + num_days
    total_weeks = (total_cells + 6) // 7

    day = 1
    for week in range(total_weeks):
        row_str = ""
        for col in range(7):
            cell_index = (week * 7) + col
            if cell_index < start_weekday or day > num_days:
                row_str += "    "
            else:
                row_str += f"{day:>4}"
                day += 1
        lines.append(row_str)

    lines.append("-" * width)
    return (True, lines)


def print_calendar(title, num_days, start_weekday):
    ok, lines = build_calendar_lines(title, num_days, start_weekday)
    for line in lines:
        print("  " + line)
    return ok


def main():
    print("NESTED LOOP MONTHLY CALENDAR GENERATOR\n")

    # 1. October 2026 (31 days, starts Thursday = 4)
    print_calendar("October 2026", 31, 4)
    print()

    # 2. February 2024 Leap Year (29 days, starts Thursday = 4)
    feb_days = get_month_days(2, 2024)
    print_calendar("February 2024 (Leap)", feb_days, 4)
    print()

    # 3. November 2026 (30 days, starts Sunday = 0)
    print_calendar("November 2026", 30, 0)
    print()

    # 4. Validation checks for invalid inputs
    print("VALIDATION CHECKS:")
    print_calendar("Invalid Days Check", 32, 2)
    print_calendar("Invalid Weekday Check", 30, 7)


if __name__ == "__main__":
    main()
```

## 8. Test Cases

| Test ID | Scenario | Expected Result | Status |
| :--- | :--- | :--- | :--- |
| TC-01 | Leap year & century checks (2024, 2026, 1900, 2000) | February returns 29, 28, 28, and 29 days | PASS |
| TC-02 | Month lengths & invalid month (13) | Returns 30/31 accurately and None for month 13 | PASS |
| TC-03 | October 2026 Thursday start alignment | Inserts 16 leading spaces before Day 1 and ends at 31 | PASS |
| TC-04 | 28-day month starting Sunday | Spans exactly 4 week rows with no extra blank row | PASS |
| TC-05 | Invalid month lengths (27, 32) | Rejected with clear validation error | PASS |
| TC-06 | Invalid weekday indices (-1, 7) | Rejected cleanly without building grid | PASS |

Run automated tests: `python3 Case_37_Nested_Loop_Calendar/test_cases.py`

## 9. Output & Output Screenshot

![Output Screenshot](output_screenshot.png)

<details>
<summary>View raw console output (output.txt)</summary>

```text
NESTED LOOP MONTHLY CALENDAR GENERATOR

  ============================
          October 2026        
  ============================
   Sun Mon Tue Wed Thu Fri Sat
  ----------------------------
                     1   2   3
     4   5   6   7   8   9  10
    11  12  13  14  15  16  17
    18  19  20  21  22  23  24
    25  26  27  28  29  30  31
  ----------------------------

  ============================
      February 2024 (Leap)    
  ============================
   Sun Mon Tue Wed Thu Fri Sat
  ----------------------------
                     1   2   3
     4   5   6   7   8   9  10
    11  12  13  14  15  16  17
    18  19  20  21  22  23  24
    25  26  27  28  29        
  ----------------------------

  ============================
         November 2026        
  ============================
   Sun Mon Tue Wed Thu Fri Sat
  ----------------------------
     1   2   3   4   5   6   7
     8   9  10  11  12  13  14
    15  16  17  18  19  20  21
    22  23  24  25  26  27  28
    29  30                    
  ----------------------------

VALIDATION CHECKS:
  INVALID: month length 32 must be 28, 29, 30, or 31.
  INVALID: starting weekday 7 must be between 0 (Sun) and 6 (Sat).
```

</details>

## 10. Conclusion

Nested loops naturally model week-by-weekday grid generation. Fixed-width cell formatting and upfront input validation guarantee crisp alignment across 28-, 29-, 30-, and 31-day calendars.
