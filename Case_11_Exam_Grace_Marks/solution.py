"""
Case Study 11: Examination Result and Grace-Mark Validation
Name: Mareedu Paardhiv | Roll No: 26000626
"""

SUBJECTS = ["Maths", "Physics", "Python", "Digital Logic", "English"]
MAX_MARKS = 100
PASS_MARKS = 40
MAX_GRACE_POOL = 10
MAX_GRACE_PER_SUBJECT = 5

# Student records: (roll_no, name, marks_list)
STUDENTS = [
    ("26B01", "Nikhil Varma", [84, 79, 91, 76, 82]),
    ("26B02", "Bhavana Rao", [37, 65, 72, 38, 60]),    # needs 3 + 2 = 5 grace -> PASS
    ("26B03", "Charan Teja", [35, 36, 37, 68, 70]),    # needs 5 + 4 + 3 = 12 > 10 -> FAIL
    ("26B04", "Keerthi S", [32, 74, 81, 69, 77]),      # Maths 32 needs 8 > 5 -> FAIL
    ("26B05", "Prashanth K", [42, 41, 44, 40, 43]),    # just pass -> Pass Class
    ("26B06", "Swathi Reddy", [98, 95, 99, 92, 94]),   # Distinction
    ("26B07", "Manoj Kumar", [54, 58, 36, 52, 61]),    # needs 4 grace in Python -> PASS
    ("26B08", "Bad Data", [50, 105, 60, 70, 80]),      # invalid (>100)
]


def classify_percentage(pct, passed_all):
    if not passed_all:
        return "Fail"
    if pct >= 75.0:
        return "Distinction"
    elif pct >= 60.0:
        return "First Class"
    elif pct >= 50.0:
        return "Second Class"
    else:
        return "Pass Class"


def evaluate_student(student):
    roll, name, marks = student

    if len(marks) != len(SUBJECTS):
        return (False, roll, name, "Subject count mismatch")

    for m in marks:
        if m < 0 or m > MAX_MARKS:
            return (False, roll, name, f"Mark {m} out of valid range 0..{MAX_MARKS}")

    # Check failed subjects and compute grace needed
    needed_list = []
    total_needed = 0
    can_save_with_grace = True

    for i in range(len(marks)):
        if marks[i] < PASS_MARKS:
            shortfall = PASS_MARKS - marks[i]
            needed_list.append((i, shortfall))
            total_needed += shortfall
            if shortfall > MAX_GRACE_PER_SUBJECT:
                can_save_with_grace = False

    if total_needed > MAX_GRACE_POOL:
        can_save_with_grace = False

    final_marks = []
    grace_used = []
    for i in range(len(marks)):
        final_marks.append(marks[i])
        grace_used.append(0)

    grace_applied = 0
    if len(needed_list) > 0 and can_save_with_grace:
        for idx, shortfall in needed_list:
            # Ensure marks never exceed MAX_MARKS
            updated = min(MAX_MARKS, final_marks[idx] + shortfall)
            grace_used[idx] = updated - final_marks[idx]
            final_marks[idx] = updated
            grace_applied += grace_used[idx]

    failed_subjects = []
    for i in range(len(final_marks)):
        if final_marks[i] < PASS_MARKS:
            failed_subjects.append(f"{SUBJECTS[i]}({final_marks[i]})")

    passed_all = (len(failed_subjects) == 0)
    total_score = sum(final_marks)
    percentage = round((total_score / (len(SUBJECTS) * MAX_MARKS)) * 100.0, 2)
    division = classify_percentage(percentage, passed_all)

    return (
        True,
        (
            roll,
            name,
            list(marks),
            final_marks,
            grace_used,
            grace_applied,
            total_score,
            percentage,
            division,
            failed_subjects,
        ),
    )


def main():
    results = []
    invalid = []

    for stu in STUDENTS:
        res = evaluate_student(stu)
        if res[0]:
            results.append(res[1])
        else:
            invalid.append((res[1], res[2], res[3]))

    print("=" * 96)
    print("                    EXAMINATION RESULT & GRACE-MARK VALIDATION REPORT")
    print("=" * 96)
    print(f"{'Roll':<7} {'Name':<14} {'Original Marks':<21} {'Final Marks':<21} "
          f"{'Grace':>5} {'Total':>5} {'Pct%':>6}  {'Result'}")
    print("-" * 96)

    pass_count = 0
    grace_beneficiaries = 0

    for row in results:
        roll, name, orig, final, g_used, g_total, tot, pct, div, failed = row
        orig_str = " ".join(f"{m:>3}" for m in orig)
        final_str = " ".join(f"{m:>3}" for m in final)
        print(f"{roll:<7} {name:<14} {orig_str:<21} {final_str:<21} "
              f"{g_total:>5} {tot:>5} {pct:>6.2f}  {div}")

        if div != "Fail":
            pass_count += 1
        if g_total > 0:
            grace_beneficiaries += 1

    print("-" * 96)
    print("\nGRACE-MARK & FAILURE DETAILS:")
    for row in results:
        roll, name, orig, final, g_used, g_total, tot, pct, div, failed = row
        if g_total > 0:
            details = []
            for i in range(len(SUBJECTS)):
                if g_used[i] > 0:
                    details.append(f"{SUBJECTS[i]} +{g_used[i]} ({orig[i]}->{final[i]})")
            print(f"  {roll} ({name}): Grace applied -> {', '.join(details)}")
        elif len(failed) > 0:
            print(f"  {roll} ({name}): Grace not eligible -> Failed in {', '.join(failed)}")

    if len(invalid) > 0:
        print("\nINVALID INPUT RECORDS:")
        for roll, name, msg in invalid:
            print(f"  {roll} ({name}): {msg}")

    print("-" * 96)
    print(f"Summary: {pass_count} Passed ({grace_beneficiaries} via grace), "
          f"{len(results) - pass_count} Failed, {len(invalid)} Invalid.")


if __name__ == "__main__":
    main()
