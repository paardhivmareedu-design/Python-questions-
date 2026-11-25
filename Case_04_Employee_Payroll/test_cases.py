"""Test cases for Case Study 04: Employee Payroll and Deduction Analysis."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import solution


def run_tests():
    # Test 1: Incentive tiers
    assert solution.compute_incentive(4.7) == 5000.0
    assert solution.compute_incentive(4.5) == 5000.0
    assert solution.compute_incentive(3.8) == 2500.0
    assert solution.compute_incentive(3.2) == 0.0
    print("[PASS] Test 1: Incentive tier thresholds")

    # Test 2: Progressive income tax slabs
    assert solution.compute_income_tax(28000.0) == 0.0
    assert abs(solution.compute_income_tax(45000.0) - 1500.0) < 0.01
    assert abs(solution.compute_income_tax(75000.0) - 6000.0) < 0.01
    print("[PASS] Test 2: Progressive income tax slabs")

    # Test 3: Full salary calculation for E101 (Arjun Reddy)
    # basic=45000 -> hra=9000, da=5400, med=1500 -> allow=15900
    # ot=8*250=2000, inc=5000 -> gross=67900
    # pf=5400, pt=200, tax=3000 + 0.2*(7900)=4580 -> ded=10180 -> net=57720
    res = solution.process_employee(solution.EMPLOYEES[0])
    assert res[0] is True
    data = res[1]
    assert data[4] == 15900.0
    assert data[7] == 67900.0
    assert data[11] == 10180.0
    assert data[12] == 57720.0
    print("[PASS] Test 3: E101 gross, deductions, and net salary")

    # Test 4: Low gross employee (no income tax)
    res_low = solution.process_employee(("T1", "Test", "Ops", 18000.0, 0, 3.0))
    assert res_low[0] is True
    # basic=18000, allow=7260, gross=25260 -> tax=0, pt=200, pf=2160
    assert res_low[1][10] == 0.0
    assert res_low[1][9] == 200.0
    print("[PASS] Test 4: Zero income tax below Rs. 30,000 gross")

    # Test 5: Invalid negative salary record rejected
    res_bad = solution.process_employee(solution.EMPLOYEES[6])
    assert res_bad[0] is False
    print("[PASS] Test 5: Negative basic pay rejected")

    # Test 6: Invalid overtime hours rejected
    res_ot = solution.process_employee(("T2", "Test", "HR", 25000.0, -4, 4.0))
    assert res_ot[0] is False
    print("[PASS] Test 6: Negative overtime hours rejected")

    print("\nAll 6 tests passed for Case Study 04.")


if __name__ == "__main__":
    run_tests()
