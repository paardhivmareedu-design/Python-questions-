"""Test cases for Case Study 48: Tuple-Based Employee Shift Conflict Detection."""
import os
import subprocess
import sys

SOL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "solution.py")


def run_tests():
    res = subprocess.run([sys.executable, SOL_PATH], capture_output=True, text=True)
    assert res.returncode == 0
    out = res.stdout

    # Test 1: Valid vs invalid shift tuple count
    assert "Total Shift Tuples: 10 | Valid: 9 | Invalid: 1" in out
    assert "EMP05 (Eshwar) Friday 14:00-11:00 -> Invalid time format or end <= start" in out
    print("[PASS] Test 1: Invalid reversed shift rejected cleanly")

    # Test 2: Partial overlap for EMP01 (60 minutes)
    assert "EMP01 (Aarav) on Monday:" in out
    assert "Overlap: 12:00-13:00 (60 minutes)" in out
    print("[PASS] Test 2: Partial shift overlap duration detected")

    # Test 3: Multi-way overlaps for EMP03 (30 mins and 120 mins)
    assert "Overlap: 14:30-15:00 (30 minutes)" in out
    assert "Overlap: 11:00-13:00 (120 minutes)" in out
    print("[PASS] Test 3: Multiple overlaps detected for EMP03")

    # Test 4: Adjacent shifts (EMP02 08:00-12:00 and 12:00-16:00) remain conflict-free
    assert "Conflict-free employees    : EMP02 (Bhavya), EMP04 (Deepika)" in out
    assert "EMP02 Bhavya     : 2 shift(s),  8.00 hrs [OK]" in out
    print("[PASS] Test 4: Adjacent non-overlapping shifts marked OK")

    print("\nAll 4 tests passed for Case Study 48.")


if __name__ == "__main__":
    run_tests()
