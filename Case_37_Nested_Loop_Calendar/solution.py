"""
Case Study 37: Nested Loop Calendar Generator
Name: Mareedu Paardhiv | Roll No: 26000626
"""

weekdays = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
valid_lengths = (28, 29, 30, 31)

# Calendar requests: (title, month_number, year, start_weekday_0_to_6, override_days_or_0)
# When override_days > 0, it directly tests month-length validation
calendar_requests = [
    ("October 2026", 10, 2026, 4, 0),          # 31 days, starts Thu (4)
    ("February 2024 (Leap)", 2, 2024, 4, 0),   # leap year -> 29 days, starts Thu (4)
    ("November 2026", 11, 2026, 0, 0),         # 30 days, starts Sun (0)
    ("Invalid Days Check", 1, 2026, 2, 32),    # invalid day count 32
    ("Invalid Weekday Check", 4, 2026, 7, 0),  # invalid weekday 7
]

print("NESTED LOOP MONTHLY CALENDAR GENERATOR\n")

for req in calendar_requests:
    title, month, year, start_weekday, override_days = req

    # Determine days in month (using leap year rule for February)
    if override_days > 0:
        num_days = override_days
    elif month < 1 or month > 12:
        num_days = -1
    elif month in (1, 3, 5, 7, 8, 10, 12):
        num_days = 31
    elif month in (4, 6, 9, 11):
        num_days = 30
    else:
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            num_days = 29
        else:
            num_days = 28

    # Validate month length and starting weekday
    if num_days not in valid_lengths:
        print(f"  INVALID: month length {num_days} must be 28, 29, 30, or 31.")
        continue

    if start_weekday < 0 or start_weekday > 6:
        print(f"  INVALID: starting weekday {start_weekday} must be between 0 (Sun) and 6 (Sat).")
        continue

    # Print formatted calendar header
    width = 28
    print("  " + ("=" * width))
    print("  " + title.center(width))
    print("  " + ("=" * width))

    header = ""
    for w in range(7):
        header = header + f"{weekdays[w]:>4}"
    print("  " + header)
    print("  " + ("-" * width))

    # Print weeks and days using nested loops
    total_cells = start_weekday + num_days
    total_weeks = (total_cells + 6) // 7

    day = 1
    for week in range(total_weeks):
        row_str = ""
        for col in range(7):
            cell_index = (week * 7) + col
            if cell_index < start_weekday or day > num_days:
                row_str = row_str + "    "
            else:
                row_str = row_str + f"{day:>4}"
                day = day + 1
        print("  " + row_str)

    print("  " + ("-" * width))
    print()
