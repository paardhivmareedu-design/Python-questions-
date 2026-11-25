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
