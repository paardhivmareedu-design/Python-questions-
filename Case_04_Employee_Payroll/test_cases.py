"""Test cases for Case Study 04: Employee Payroll and Deduction Analysis."""
import os
import subprocess
import sys

SOL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "solution.py")


def run_tests():
    res = subprocess.run([sys.executable, SOL_PATH], capture_output=True, text=True)
    assert res.returncode == 0
    out = res.stdout

    # Test 1: Check E101 Arjun Reddy values (basic 45000, allow 15900, OT+Inc 7000, gross 67900, ded 10180, net 57720)
    assert "E101" in out and "67900.00" in out and "10180.00" in out and "57720.00" in out
    print("[PASS] Test 1: E101 gross salary, deductions, and net pay verified")

    # Test 2: Check middle slab employee E102 (gross 55160, tax 2516, net 47884)
    assert "E102" in out and "55160.00" in out and "2516.00" in out and "47884.00" in out
    print("[PASS] Test 2: E102 progressive 10% tax slab verified")

    # Test 3: Check highest earner identification (E104 Divya Nair)
    assert "Highest Net Salary: Divya Nair (E104) - Rs. 69488.00" in out
    print("[PASS] Test 3: Highest net salary earner identified")

    # Test 4: Check company totals
    assert "333360.00" in out and "46542.00" in out and "286818.00" in out
    print("[PASS] Test 4: Company payroll totals verified")

    # Test 5: Check invalid record E107 skipped
    assert "E107 (Invalid Record)" in out
    assert "6 valid records processed, 1 invalid skipped." in out
    print("[PASS] Test 5: Invalid negative salary record skipped cleanly")

    print("\nAll 5 tests passed for Case Study 04.")


if __name__ == "__main__":
    run_tests()
