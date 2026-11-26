"""Test cases for Case Study 28: Repeated Transaction Detection."""
import os
import subprocess
import sys

SOL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "solution.py")


def run_tests():
    res = subprocess.run([sys.executable, SOL_PATH], capture_output=True, text=True)
    assert res.returncode == 0
    out = res.stdout

    # Test 1: Summary counts
    assert "Total Transactions Scanned : 9" in out
    assert "Clean Transactions         : 1" in out
    assert "Suspicious Entries Flagged : 8" in out
    print("[PASS] Test 1: Clean vs suspicious transaction totals verified")

    # Test 2: Duplicate ID detected for TXN902
    assert "TXN902" in out and "Duplicate ID (2x)" in out
    print("[PASS] Test 2: Duplicate transaction ID flagged")

    # Test 3: Repeat pattern detected for TXN901 / TXN903
    assert "TXN901" in out and "TXN903" in out and "Repeat Pattern (2x)" in out
    print("[PASS] Test 3: Repeated payment pattern flagged")

    # Test 4: High-value threshold and negative amount detected
    assert "TXN904" in out and "Above Rs.50000" in out
    assert "TXN908" in out and "Invalid amount (<=0)" in out
    print("[PASS] Test 4: High-value breach and invalid amount flagged")

    # Test 5: Clean transaction isolated
    assert "Row 6: TXN905 | AC1004 | Rs. 1250.00 | BookHouse" in out
    print("[PASS] Test 5: Clean transaction isolated accurately")

    print("\nAll 5 tests passed for Case Study 28.")


if __name__ == "__main__":
    run_tests()
