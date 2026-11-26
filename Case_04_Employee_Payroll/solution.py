"""
Case Study 04: Employee Payroll and Deduction Analysis
Name: Mareedu Paardhiv | Roll No: 26000626
"""

# Monthly allowance and deduction rates
hra_rate = 0.20          # 20% of basic pay
da_rate = 0.12           # 12% of basic pay
medical = 1500.0         # fixed medical allowance
ot_rate = 250.0          # Rs. 250 per overtime hour
pf_rate = 0.12           # 12% Provident Fund on basic pay

# Employee records: (emp_id, name, department, basic_pay, overtime_hours, rating)
employees = [
    ("E101", "Arjun Reddy", "Engineering", 45000.0, 8, 4.7),
    ("E102", "Sneha Rao", "Finance", 38000.0, 4, 4.1),
    ("E103", "Karthik Varma", "Operations", 22000.0, 10, 3.2),
    ("E104", "Divya Nair", "Engineering", 58000.0, 6, 4.8),
    ("E105", "Pranav Sharma", "HR", 28000.0, 0, 3.8),
    ("E106", "Tejaswini K", "Marketing", 32000.0, 12, 4.5),
    ("E107", "Invalid Record", "Support", -15000.0, 3, 3.0),
]

processed = []
rejected = []

for emp in employees:
    emp_id, name, dept, basic, ot_hours, rating = emp

    # Validate input values
    if basic <= 0 or ot_hours < 0 or rating < 0 or rating > 5:
        rejected.append((emp_id, name, "Invalid pay, overtime, or rating"))
        continue

    # Calculate earnings
    hra = basic * hra_rate
    da = basic * da_rate
    allowances = hra + da + medical
    ot_pay = ot_hours * ot_rate

    if rating >= 4.5:
        incentive = 5000.0
    elif rating >= 3.5:
        incentive = 2500.0
    else:
        incentive = 0.0

    gross = basic + allowances + ot_pay + incentive

    # Calculate progressive deductions
    pf = basic * pf_rate
    if gross > 25000.0:
        prof_tax = 200.0
    else:
        prof_tax = 0.0

    # Progressive tax slabs: 0-30k (0%), 30k-60k (10%), above 60k (20%)
    if gross <= 30000.0:
        tax = 0.0
    elif gross <= 60000.0:
        tax = (gross - 30000.0) * 0.10
    else:
        tax = (30000.0 * 0.10) + ((gross - 60000.0) * 0.20)

    total_ded = pf + prof_tax + tax
    net_pay = gross - total_ded

    processed.append((
        emp_id, name, dept, basic, allowances,
        ot_pay + incentive, gross, pf, prof_tax, tax, total_ded, net_pay
    ))

# Display formatted payroll statement
print("=" * 96)
print("                         MONTHLY EMPLOYEE PAYROLL STATEMENT")
print("=" * 96)
print(f"{'ID':<6} {'Name':<15} {'Dept':<12} {'Basic':>9} {'Allow.':>9} {'OT+Inc':>9} "
      f"{'Gross':>10} {'Deduct.':>9} {'Net Pay':>10}")
print("-" * 96)

total_gross = 0.0
total_deductions = 0.0
total_net = 0.0
highest_id = ""
highest_name = ""
highest_net = -1.0

for row in processed:
    emp_id, name, dept, basic, allow, extra, gross, pf, pt, tax, ded, net = row
    print(f"{emp_id:<6} {name:<15} {dept:<12} {basic:>9.2f} {allow:>9.2f} "
          f"{extra:>9.2f} {gross:>10.2f} {ded:>9.2f} {net:>10.2f}")

    total_gross = total_gross + gross
    total_deductions = total_deductions + ded
    total_net = total_net + net

    if net > highest_net:
        highest_net = net
        highest_id = emp_id
        highest_name = name

print("-" * 96)
print(f"{'TOTAL':<65} {total_gross:>10.2f} {total_deductions:>9.2f} {total_net:>10.2f}")
print("=" * 96)

print("\nDEDUCTION BREAKDOWN (PF / Prof. Tax / Income Tax):")
for row in processed:
    emp_id, name, dept, basic, allow, extra, gross, pf, pt, tax, ded, net = row
    print(f"  {emp_id} ({name:<14}): PF = Rs.{pf:>7.2f} | PT = Rs.{pt:>6.2f} | "
          f"Tax = Rs.{tax:>7.2f} | Total = Rs.{ded:>8.2f}")

if highest_name != "":
    print(f"\nHighest Net Salary: {highest_name} ({highest_id}) - Rs. {highest_net:.2f}")

if len(rejected) > 0:
    print("\nSKIPPED / INVALID RECORDS:")
    for emp_id, name, reason in rejected:
        print(f"  {emp_id} ({name}): {reason}")

print(f"\nSummary: {len(processed)} valid records processed, {len(rejected)} invalid skipped.")
