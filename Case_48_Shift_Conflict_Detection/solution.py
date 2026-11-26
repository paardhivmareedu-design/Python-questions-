"""
Case Study 48: Tuple-Based Employee Shift Conflict Detection
Name: Mareedu Paardhiv | Roll No: 26000626
"""

# Shift tuples: (emp_id, emp_name, day, start_time, end_time, role)
shifts = [
    ("EMP01", "Aarav", "Monday", "09:00", "13:00", "Helpdesk"),
    ("EMP01", "Aarav", "Monday", "12:00", "16:00", "Lab Duty"),       # overlaps 12:00-13:00
    ("EMP01", "Aarav", "Tuesday", "09:00", "13:00", "Helpdesk"),
    ("EMP02", "Bhavya", "Monday", "08:00", "12:00", "Reception"),
    ("EMP02", "Bhavya", "Monday", "12:00", "16:00", "Reception"),     # adjacent, no overlap
    ("EMP03", "Charan", "Wednesday", "10:00", "15:00", "Server Ops"),
    ("EMP03", "Charan", "Wednesday", "14:30", "18:00", "Network"),    # overlaps 14:30-15:00
    ("EMP03", "Charan", "Wednesday", "11:00", "13:00", "Audit"),      # overlaps 11:00-13:00
    ("EMP04", "Deepika", "Thursday", "09:30", "17:30", "Support"),
    ("EMP05", "Eshwar", "Friday", "14:00", "11:00", "Security"),      # invalid: end <= start
]

valid_shifts = []
invalid_shifts = []

# Step 1: Parse time strings and validate each shift tuple
for shift in shifts:
    emp_id, name, day, s_str, e_str, role = shift

    s_parts = s_str.strip().split(":")
    e_parts = e_str.strip().split(":")

    s_min = -1
    e_min = -1

    if len(s_parts) == 2 and s_parts[0].isdigit() and s_parts[1].isdigit():
        sh = int(s_parts[0])
        sm = int(s_parts[1])
        if 0 <= sh <= 23 and 0 <= sm <= 59:
            s_min = (sh * 60) + sm

    if len(e_parts) == 2 and e_parts[0].isdigit() and e_parts[1].isdigit():
        eh = int(e_parts[0])
        em = int(e_parts[1])
        if 0 <= eh <= 23 and 0 <= em <= 59:
            e_min = (eh * 60) + em

    if s_min == -1 or e_min == -1 or e_min <= s_min:
        invalid_shifts.append((shift, "Invalid time format or end <= start"))
    else:
        valid_shifts.append((emp_id, name, day, s_str, e_str, role, s_min, e_min))

# Collect unique valid employees
all_employees = []
for sh in valid_shifts:
    emp_pair = (sh[0], sh[1])
    if emp_pair not in all_employees:
        all_employees.append(emp_pair)

# Step 2: Compare every pair of valid shifts for overlap
conflicts = []
conflicted_employees = []

for i in range(len(valid_shifts)):
    id1, name1, day1, s1_str, e1_str, role1, s1, e1 = valid_shifts[i]
    for j in range(i + 1, len(valid_shifts)):
        id2, name2, day2, s2_str, e2_str, role2, s2, e2 = valid_shifts[j]

        if id1 == id2 and day1 == day2:
            if s1 < e2 and s2 < e1:
                if s1 > s2:
                    ov_start = s1
                else:
                    ov_start = s2

                if e1 < e2:
                    ov_end = e1
                else:
                    ov_end = e2

                ov_mins = ov_end - ov_start
                ov_range = f"{ov_start // 60:02d}:{ov_start % 60:02d}-{ov_end // 60:02d}:{ov_end % 60:02d}"

                conflicts.append((
                    id1, name1, day1,
                    f"{s1_str}-{e1_str} ({role1})",
                    f"{s2_str}-{e2_str} ({role2})",
                    ov_range, ov_mins
                ))
                if (id1, name1) not in conflicted_employees:
                    conflicted_employees.append((id1, name1))

conflict_free = []
for emp in all_employees:
    if emp not in conflicted_employees:
        conflict_free.append(emp)

# Display report
print("=" * 94)
print("                    TUPLE-BASED EMPLOYEE SHIFT CONFLICT DETECTION")
print("=" * 94)
print(f"Total Shift Tuples: {len(shifts)} | Valid: {len(valid_shifts)} | Invalid: {len(invalid_shifts)}")
print("-" * 94)

print("\nCONFLICTING SHIFT PAIRS DETECTED:")
if len(conflicts) == 0:
    print("  None.")
else:
    for emp_id, name, day, sh1, sh2, ov_range, ov_mins in conflicts:
        print(f"  {emp_id} ({name}) on {day}:")
        print(f"    Shift A: {sh1}  <-->  Shift B: {sh2}")
        print(f"    Overlap: {ov_range} ({ov_mins} minutes)")

bad_text_list = []
for eid, nm in conflicted_employees:
    bad_text_list.append(f"{eid} ({nm})")

good_text_list = []
for eid, nm in conflict_free:
    good_text_list.append(f"{eid} ({nm})")

print("\nEMPLOYEE CONFLICT SUMMARY:")
print("  Employees WITH conflicts   :", ", ".join(bad_text_list))
print("  Conflict-free employees    :", ", ".join(good_text_list))

print("\nSCHEDULED WORKLOAD (VALID SHIFTS):")
for eid, nm in all_employees:
    total_mins = 0
    shift_count = 0
    for sh in valid_shifts:
        if sh[0] == eid:
            total_mins = total_mins + (sh[7] - sh[6])
            shift_count = shift_count + 1
    hrs = round(total_mins / 60.0, 2)
    if (eid, nm) in conflicted_employees:
        flag = "[CONFLICT]"
    else:
        flag = "[OK]"
    print(f"  {eid} {nm:<10} : {shift_count} shift(s), {hrs:>5.2f} hrs {flag}")

if len(invalid_shifts) > 0:
    print("\nINVALID SHIFT TUPLES:")
    for sh, reason in invalid_shifts:
        print(f"  {sh[0]} ({sh[1]}) {sh[2]} {sh[3]}-{sh[4]} -> {reason}")
print("=" * 94)
