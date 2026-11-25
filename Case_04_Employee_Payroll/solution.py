"""
Case Study 04: Employee Payroll and Deduction Analysis
Name: Mareedu Paardhiv | Roll No: 26000626
"""

# Monthly allowance and deduction rates
HRA_RATE = 0.20          # 20% of basic pay
DA_RATE = 0.12           # 12% of basic pay
MEDICAL_ALLOWANCE = 1500.0
OVERTIME_RATE = 250.0    # Rs. 250 per extra hour
PF_RATE = 0.12           # 12% Provident Fund on basic pay

# Employee records: (emp_id, name, department, basic_pay, overtime_hours, rating)
EMPLOYEES = [
    ("E101", "Arjun Reddy", "Engineering", 45000.0, 8, 4.7),
    ("E102", "Sneha Rao", "Finance", 38000.0, 4, 4.1),
    ("E103", "Karthik Varma", "Operations", 22000.0, 10, 3.2),
    ("E104", "Divya Nair", "Engineering", 58000.0, 6, 4.8),
    ("E105", "Pranav Sharma", "HR", 28000.0, 0, 3.8),
    ("E106", "Tejaswini K", "Marketing", 32000.0, 12, 4.5),
    ("E107", "Invalid Record", "Support", -15000.0, 3, 3.0),
]


def compute_incentive(rating):
    if rating >= 4.5:
        return 5000.0
    elif rating >= 3.5:
        return 2500.0
    else:
        return 0.0


def compute_income_tax(gross_salary):
    # Progressive monthly tax slabs:
    # 0 - 30,000: 0%, 30,001 - 60,000: 10%, above 60,000: 20%
    if gross_salary <= 30000.0:
        return 0.0
    elif gross_salary <= 60000.0:
        return (gross_salary - 30000.0) * 0.10
    else:
        return (30000.0 * 0.10) + ((gross_salary - 60000.0) * 0.20)


def process_employee(record):
    emp_id, name, dept, basic, ot_hours, rating = record

    if basic <= 0 or ot_hours < 0 or rating < 0 or rating > 5:
        return (False, emp_id, name, dept, "Invalid pay, overtime, or rating values")

    hra = basic * HRA_RATE
    da = basic * DA_RATE
    allowances = hra + da + MEDICAL_ALLOWANCE
    overtime_pay = ot_hours * OVERTIME_RATE
    incentive = compute_incentive(rating)

    gross = basic + allowances + overtime_pay + incentive

    pf = basic * PF_RATE
    prof_tax = 200.0 if gross > 25000.0 else 0.0
    income_tax = compute_income_tax(gross)
    total_deductions = pf + prof_tax + income_tax
    net_salary = gross - total_deductions

    breakdown = (
        emp_id,
        name,
        dept,
        round(basic, 2),
        round(allowances, 2),
        round(overtime_pay, 2),
        round(incentive, 2),
        round(gross, 2),
        round(pf, 2),
        round(prof_tax, 2),
        round(income_tax, 2),
        round(total_deductions, 2),
        round(net_salary, 2),
    )
    return (True, breakdown)


def main():
    processed = []
    rejected = []

    for emp in EMPLOYEES:
        result = process_employee(emp)
        if result[0]:
            processed.append(result[1])
        else:
            rejected.append((result[1], result[2], result[4]))

    print("=" * 98)
    print("                         MONTHLY EMPLOYEE PAYROLL STATEMENT")
    print("=" * 98)
    print(f"{'ID':<6} {'Name':<15} {'Dept':<12} {'Basic':>9} {'Allow.':>9} {'OT+Inc':>9} "
          f"{'Gross':>10} {'Deduct.':>9} {'Net Pay':>10}")
    print("-" * 98)

    total_gross = 0.0
    total_ded = 0.0
    total_net = 0.0
    highest_emp = None

    for row in processed:
        (emp_id, name, dept, basic, allowances, ot_pay, incentive,
         gross, pf, pt, tax, deductions, net) = row

        extra = ot_pay + incentive
        print(f"{emp_id:<6} {name:<15} {dept:<12} {basic:>9.2f} {allowances:>9.2f} "
              f"{extra:>9.2f} {gross:>10.2f} {deductions:>9.2f} {net:>10.2f}")

        total_gross += gross
        total_ded += deductions
        total_net += net

        if highest_emp is None or net > highest_emp[12]:
            highest_emp = row

    print("-" * 98)
    print(f"{'TOTAL':<35} {'':>9} {'':>9} {'':>9} "
          f"{total_gross:>10.2f} {total_ded:>9.2f} {total_net:>10.2f}")
    print("=" * 98)

    print("\nDEDUCTION BREAKDOWN (PF / Prof. Tax / Income Tax):")
    for row in processed:
        emp_id, name, _, _, _, _, _, _, pf, pt, tax, deductions, _ = row
        print(f"  {emp_id} ({name:<14}): PF = Rs.{pf:>7.2f} | PT = Rs.{pt:>6.2f} | "
              f"Tax = Rs.{tax:>7.2f} | Total = Rs.{deductions:>8.2f}")

    if highest_emp is not None:
        print(f"\nHighest Net Salary: {highest_emp[1]} ({highest_emp[0]}) - Rs. {highest_emp[12]:.2f}")

    if len(rejected) > 0:
        print("\nSKIPPED / INVALID RECORDS:")
        for emp_id, name, reason in rejected:
            print(f"  {emp_id} ({name}): {reason}")

    print(f"\nSummary: {len(processed)} valid records processed, {len(rejected)} invalid skipped.")


if __name__ == "__main__":
    main()
