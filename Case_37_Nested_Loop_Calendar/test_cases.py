"""Test cases for Case Study 37: Nested Loop Calendar Generator."""
import os
import subprocess
import sys

SOL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "solution.py")


def run_tests():
    res = subprocess.run([sys.executable, SOL_PATH], capture_output=True, text=True)
    assert res.returncode == 0
    out = res.stdout

    # Test 1: October 2026 starts on Thursday (16 leading spaces before '   1') and has 31 days
    assert "October 2026" in out
    assert "                   1   2   3" in out
    assert "  25  26  27  28  29  30  31" in out
    print("[PASS] Test 1: October 2026 Thursday start and 31 days aligned")

    # Test 2: February 2024 leap year has 29 days
    assert "February 2024 (Leap)" in out
    assert "  25  26  27  28  29" in out
    print("[PASS] Test 2: Leap year February 2024 shows 29 days")

    # Test 3: November 2026 Sunday start has 30 days
    assert "November 2026" in out
    assert "     1   2   3   4   5   6   7" in out
    assert "  29  30" in out
    print("[PASS] Test 3: November 2026 Sunday start and 30 days aligned")

    # Test 4: Invalid month length and weekday index flagged
    assert "INVALID: month length 32 must be 28, 29, 30, or 31." in out
    assert "INVALID: starting weekday 7 must be between 0 (Sun) and 6 (Sat)." in out
    print("[PASS] Test 4: Invalid day count and weekday rejected cleanly")

    print("\nAll 4 tests passed for Case Study 37.")


if __name__ == "__main__":
    run_tests()
