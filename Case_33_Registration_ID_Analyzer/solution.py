"""
Case Study 33: Campus Registration Identifier Analyzer
Name: Mareedu Paardhiv | Roll No: 26000626
"""

VALID_YEARS = ("21", "22", "23", "24", "25", "26")
BRANCHES = [
    ("CSE", "Computer Science"),
    ("ECE", "Electronics & Comm."),
    ("EEE", "Electrical Engg."),
    ("MEC", "Mechanical Engg."),
    ("CIV", "Civil Engg."),
    ("AID", "AI & Data Science"),
]

SAMPLE_IDS = [
    "26-CSE-0626",
    "26-AID-0104",
    "25-ECE-0318",
    "24-MEC-0045",
    "23-CIV-0211",
    "26-CSE-0524",
    "22-EEE-0098",
    "26-cse-0112",     # lowercase branch code -> invalid
    "26CSE0626",       # missing hyphens -> invalid
    "19-CSE-0401",     # admission year out of range -> invalid
    "25-BIO-0120",     # unknown branch code -> invalid
    "26-ECE-0000",     # serial 0000 -> invalid
    "26-CSE-0626",     # duplicate valid ID
]


def lookup_branch_name(code):
    for b_code, b_name in BRANCHES:
        if b_code == code:
            return b_name
    return None


def analyze_reg_id(raw_id):
    reg_id = raw_id.strip()
    errors = []

    # Expected format: YY-BBB-NNNN (length 11)
    if len(reg_id) != 11:
        errors.append(f"Expected length 11 (YY-BBB-NNNN), got {len(reg_id)}")
        return (False, reg_id, None, errors)

    if reg_id[2] != "-" or reg_id[6] != "-":
        errors.append("Missing or misplaced '-' separator at index 2 or 6")

    year_part = reg_id[0:2]
    branch_part = reg_id[3:6]
    serial_part = reg_id[7:11]

    # Validate year
    if not year_part.isdigit():
        errors.append(f"Year code '{year_part}' must be 2 digits")
    elif year_part not in VALID_YEARS:
        errors.append(f"Admission year '20{year_part}' outside allowed range 2021-2026")

    # Validate branch
    if not (branch_part.isalpha() and branch_part.isupper()):
        errors.append(f"Branch code '{branch_part}' must be 3 uppercase letters")
    elif lookup_branch_name(branch_part) is None:
        errors.append(f"Unknown branch code '{branch_part}'")

    # Validate serial number
    if not serial_part.isdigit():
        errors.append(f"Serial '{serial_part}' must be 4 digits")
    elif serial_part == "0000":
        errors.append("Serial number cannot be '0000'")

    if len(errors) > 0:
        return (False, reg_id, None, errors)

    full_year = "20" + year_part
    branch_name = lookup_branch_name(branch_part)
    extracted = (reg_id, full_year, branch_part, branch_name, serial_part)
    return (True, reg_id, extracted, [])


def main():
    valid_records = []
    invalid_records = []
    seen_ids = []
    duplicate_ids = []

    for item in SAMPLE_IDS:
        ok, cleaned, info, errors = analyze_reg_id(item)
        if ok:
            if cleaned in seen_ids:
                duplicate_ids.append(cleaned)
            else:
                seen_ids.append(cleaned)
                valid_records.append(info)
        else:
            invalid_records.append((cleaned, errors))

    print("=" * 88)
    print("                     CAMPUS REGISTRATION IDENTIFIER ANALYZER")
    print("=" * 88)
    print("VALID RECORDS (EXTRACTED COMPONENTS):")
    print(f"{'Reg ID':<14} {'Batch Year':<12} {'Branch':<8} {'Department':<22} {'Roll Serial'}")
    print("-" * 88)

    for reg_id, year, b_code, b_name, serial in valid_records:
        print(f"{reg_id:<14} {year:<12} {b_code:<8} {b_name:<22} {serial}")

    # Branch-wise classification counts (using parallel list)
    print("\nCLASSIFICATION BY BRANCH:")
    for b_code, b_name in BRANCHES:
        cnt = 0
        for _, _, rec_b, _, _ in valid_records:
            if rec_b == b_code:
                cnt += 1
        if cnt > 0:
            print(f"  {b_code} ({b_name}): {cnt} student(s)")

    # Year-wise classification counts
    print("\nCLASSIFICATION BY ADMISSION YEAR:")
    for y_code in VALID_YEARS:
        full_y = "20" + y_code
        cnt = 0
        for _, rec_y, _, _, _ in valid_records:
            if rec_y == full_y:
                cnt += 1
        if cnt > 0:
            print(f"  Batch {full_y}: {cnt} student(s)")

    print("\nINVALID IDENTIFIERS:")
    print("-" * 88)
    for bad_id, errs in invalid_records:
        print(f"  '{bad_id}' -> {'; '.join(errs)}")

    if len(duplicate_ids) > 0:
        print("\nDUPLICATE VALID IDENTIFIERS DETECTED:")
        for dup in duplicate_ids:
            print(f"  - {dup} (appeared more than once)")

    print("-" * 88)
    print(f"Summary: {len(valid_records)} unique valid, {len(duplicate_ids)} duplicate, "
          f"{len(invalid_records)} invalid (out of {len(SAMPLE_IDS)} inputs).")
    print("=" * 88)


if __name__ == "__main__":
    main()
