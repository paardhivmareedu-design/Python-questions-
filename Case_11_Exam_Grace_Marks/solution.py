"""
Case Study 11: Examination Result and Grace-Mark Validation
Name: Mareedu Paardhiv | Roll No: 26000626
"""

subjects = ["Maths", "Physics", "Python", "Digital Logic", "English"]
max_marks = 100
pass_marks = 40
max_grace_pool = 10
max_grace_per_subject = 5

# Student records: (roll_no, name, marks_list)
students = [
    ("26B01", "Nikhil Varma", [84, 79, 91, 76, 82]),
    ("26B02", "Bhavana Rao", [37, 65, 72, 38, 60]),    # needs 3 + 2 = 5 grace -> PASS
    ("26B03", "Charan Teja", [35, 36, 37, 68, 70]),    # needs 12 > 10 -> FAIL
    ("26B04", "Keerthi S", [32, 74, 81, 69, 77]),      # Maths 32 needs 8 > 5 -> FAIL
    ("26B05", "Prashanth K", [42, 41, 44, 40, 43]),    # Pass Class
    ("26B06", "Swathi Reddy", [98, 95, 99, 92, 94]),   # Distinction
    ("26B07", "Manoj Kumar", [54, 58, 36, 52, 61]),    # needs 4 in Python -> PASS
    ("26B08", "Bad Data", [50, 105, 60, 70, 80]),      # invalid (>100)
]

results = []
invalid = []

for stu in students:
    roll, name, marks = stu

    # Validate subject count and mark boundaries (0..100)
    if len(marks) != len(subjects):
        invalid.append((roll, name, "Subject count mismatch"))
        continue

    bad_mark = False
    bad_val = 0
    for m in marks:
        if m < 0 or m > max_marks:
            bad_mark = True
            bad_val = m
            break

    if bad_mark:
        invalid.append((roll, name, f"Mark {bad_val} out of valid range 0..{max_marks}"))
        continue

    # Check failed subjects and grace-mark eligibility
    total_needed = 0
    can_save = True
    for m in marks:
        if m < pass_marks:
            gap = pass_marks - m
            total_needed = total_needed + gap
            if gap > max_grace_per_subject:
                can_save = False

    if total_needed > max_grace_pool:
        can_save = False

    final_marks = []
    grace_used = []
    for m in marks:
        final_marks.append(m)
        grace_used.append(0)

    grace_applied = 0
    if total_needed > 0 and can_save:
        for i in range(len(final_marks)):
            if final_marks[i] < pass_marks:
                gap = pass_marks - final_marks[i]
                updated = final_marks[i] + gap
                if updated > max_marks:
                    updated = max_marks
                grace_used[i] = updated - final_marks[i]
                final_marks[i] = updated
                grace_applied = grace_applied + grace_used[i]

    # Check final failed subjects and calculate division
    failed_subjects = []
    for i in range(len(final_marks)):
        if final_marks[i] < pass_marks:
            failed_subjects.append(f"{subjects[i]}({final_marks[i]})")

    total_score = 0
    for m in final_marks:
        total_score = total_score + m

    pct = round((total_score / (len(subjects) * max_marks)) * 100.0, 2)

    if len(failed_subjects) > 0:
        division = "Fail"
    elif pct >= 75.0:
        division = "Distinction"
    elif pct >= 60.0:
        division = "First Class"
    elif pct >= 50.0:
        division = "Second Class"
    else:
        division = "Pass Class"

    results.append((roll, name, marks, final_marks, grace_used, grace_applied,
                    total_score, pct, division, failed_subjects))

print("=" * 96)
print("                    EXAMINATION RESULT & GRACE-MARK VALIDATION REPORT")
print("=" * 96)
print(f"{'Roll':<7} {'Name':<14} {'Original Marks':<21} {'Final Marks':<21} "
      f"{'Grace':>5} {'Total':>5} {'Pct%':>6}  {'Result'}")
print("-" * 96)

pass_count = 0
grace_count = 0

for row in results:
    roll, name, orig, final, g_used, g_total, tot, pct, div, failed = row

    orig_str = ""
    final_str = ""
    for i in range(len(orig)):
        orig_str = orig_str + f"{orig[i]:>3} "
        final_str = final_str + f"{final[i]:>3} "

    print(f"{roll:<7} {name:<14} {orig_str:<21} {final_str:<21} "
          f"{g_total:>5} {tot:>5} {pct:>6.2f}  {div}")

    if div != "Fail":
        pass_count = pass_count + 1
    if g_total > 0:
        grace_count = grace_count + 1

print("-" * 96)
print("\nGRACE-MARK & FAILURE DETAILS:")
for row in results:
    roll, name, orig, final, g_used, g_total, tot, pct, div, failed = row
    if g_total > 0:
        details = []
        for i in range(len(subjects)):
            if g_used[i] > 0:
                details.append(f"{subjects[i]} +{g_used[i]} ({orig[i]}->{final[i]})")
        print(f"  {roll} ({name}): Grace applied -> {', '.join(details)}")
    elif len(failed) > 0:
        print(f"  {roll} ({name}): Grace not eligible -> Failed in {', '.join(failed)}")

if len(invalid) > 0:
    print("\nINVALID INPUT RECORDS:")
    for roll, name, msg in invalid:
        print(f"  {roll} ({name}): {msg}")

print("-" * 96)
print(f"Summary: {pass_count} Passed ({grace_count} via grace), "
      f"{len(results) - pass_count} Failed, {len(invalid)} Invalid.")
