"""
Case Study 48: Tuple-Based Employee Shift Conflict Detection
Name: Mareedu Paardhiv | Roll No: 26000626
"""

# Shift tuples: (emp_id, emp_name, day, start_time, end_time, role)
SHIFTS = [
    ("EMP01", "Aarav", "Monday", "09:00", "13:00", "Helpdesk"),
    ("EMP01", "Aarav", "Monday", "12:00", "16:00", "Lab Duty"),       # overlaps 12:00-13:00 (60m)
    ("EMP01", "Aarav", "Tuesday", "09:00", "13:00", "Helpdesk"),
    ("EMP02", "Bhavya", "Monday", "08:00", "12:00", "Reception"),
    ("EMP02", "Bhavya", "Monday", "12:00", "16:00", "Reception"),     # adjacent, NO overlap
    ("EMP03", "Charan", "Wednesday", "10:00", "15:00", "Server Ops"),
    ("EMP03", "Charan", "Wednesday", "14:30", "18:00", "Network"),    # overlaps 14:30-15:00 (30m)
    ("EMP03", "Charan", "Wednesday", "11:00", "13:00", "Audit"),      # contained inside 10:00-15:00 (120m)
    ("EMP04", "Deepika", "Thursday", "09:30", "17:30", "Support"),
    ("EMP05", "Eshwar", "Friday", "14:00", "11:00", "Security"),      # invalid: end <= start
]


def parse_time_to_minutes(time_str):
    parts = time_str.strip().split(":")
    if len(parts) != 2:
        return None
    hh_str, mm_str = parts[0], parts[1]
    if not (hh_str.isdigit() and mm_str.isdigit()):
        return None
    hh = int(hh_str)
    mm = int(mm_str)
    if hh < 0 or hh > 23 or mm < 0 or mm > 59:
        return None
    return (hh * 60) + mm


def format_minutes(mins):
    hh = mins // 60
    mm = mins % 60
    return f"{hh:02d}:{mm:02d}"


def analyze_shifts(shift_list):
    valid_shifts = []
    invalid_shifts = []

    for shift in shift_list:
        emp_id, name, day, s_str, e_str, role = shift
        s_min = parse_time_to_minutes(s_str)
        e_min = parse_time_to_minutes(e_str)
        if s_min is None or e_min is None or e_min <= s_min:
            invalid_shifts.append((shift, "Invalid time format or end <= start"))
        else:
            valid_shifts.append((emp_id, name, day, s_str, e_str, role, s_min, e_min))

    conflicts = []
    conflicted_employees = []
    all_employees = []

    for sh in valid_shifts:
        emp_pair = (sh[0], sh[1])
        if emp_pair not in all_employees:
            all_employees.append(emp_pair)

    # Compare every pair of valid shifts
    for i in range(len(valid_shifts)):
        id1, name1, day1, s1_str, e1_str, role1, s1, e1 = valid_shifts[i]
        for j in range(i + 1, len(valid_shifts)):
            id2, name2, day2, s2_str, e2_str, role2, s2, e2 = valid_shifts[j]
            if id1 == id2 and day1 == day2:
                # Overlap check for half-open intervals [s1, e1) and [s2, e2)
                if s1 < e2 and s2 < e1:
                    ov_start = max(s1, s2)
                    ov_end = min(e1, e2)
                    ov_mins = ov_end - ov_start
                    conflicts.append((
                        id1,
                        name1,
                        day1,
                        f"{s1_str}-{e1_str} ({role1})",
                        f"{s2_str}-{e2_str} ({role2})",
                        f"{format_minutes(ov_start)}-{format_minutes(ov_end)}",
                        ov_mins,
                    ))
                    if (id1, name1) not in conflicted_employees:
                        conflicted_employees.append((id1, name1))

    conflict_free = []
    for emp in all_employees:
        if emp not in conflicted_employees:
            conflict_free.append(emp)

    # Calculate scheduled hours per employee
    employee_hours = []
    for emp_id, emp_name in all_employees:
        total_mins = 0
        shift_count = 0
        for sh in valid_shifts:
            if sh[0] == emp_id:
                total_mins += (sh[7] - sh[6])
                shift_count += 1
        employee_hours.append((emp_id, emp_name, shift_count, round(total_mins / 60.0, 2)))

    return valid_shifts, invalid_shifts, conflicts, conflicted_employees, conflict_free, employee_hours


def main():
    valid, invalid, conflicts, bad_emps, good_emps, emp_hours = analyze_shifts(SHIFTS)

    print("=" * 94)
    print("                    TUPLE-BASED EMPLOYEE SHIFT CONFLICT DETECTION")
    print("=" * 94)
    print(f"Total Shift Tuples: {len(SHIFTS)} | Valid: {len(valid)} | Invalid: {len(invalid)}")
    print("-" * 94)

    print("\nCONFLICTING SHIFT PAIRS DETECTED:")
    if len(conflicts) == 0:
        print("  None.")
    else:
        for emp_id, name, day, sh1, sh2, ov_range, ov_mins in conflicts:
            print(f"  {emp_id} ({name}) on {day}:")
            print(f"    Shift A: {sh1}  <-->  Shift B: {sh2}")
            print(f"    Overlap: {ov_range} ({ov_mins} minutes)")

    print("\nEMPLOYEE CONFLICT SUMMARY:")
    print("  Employees WITH conflicts   :", ", ".join(f"{eid} ({nm})" for eid, nm in bad_emps))
    print("  Conflict-free employees    :", ", ".join(f"{eid} ({nm})" for eid, nm in good_emps))

    print("\nSCHEDULED WORKLOAD (VALID SHIFTS):")
    for eid, nm, cnt, hrs in emp_hours:
        flag = " [CONFLICT]" if (eid, nm) in bad_emps else " [OK]"
        print(f"  {eid} {nm:<10} : {cnt} shift(s), {hrs:>5.2f} hrs{flag}")

    if len(invalid) > 0:
        print("\nINVALID SHIFT TUPLES:")
        for sh, reason in invalid:
            print(f"  {sh[0]} ({sh[1]}) {sh[2]} {sh[3]}-{sh[4]} -> {reason}")
    print("=" * 94)


if __name__ == "__main__":
    main()
