"""Test cases for Case Study 16: Multi-Day Water Tank Simulation."""
import os
import subprocess
import sys

SOL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "solution.py")


def run_tests():
    res = subprocess.run([sys.executable, SOL_PATH], capture_output=True, text=True)
    assert res.returncode == 0
    out = res.stdout

    # Test 1: First day reaching >= 8000L is Day 5 (9400L)
    assert "9400" in out and "HIGH (>=8000L)" in out
    assert "First day reaching threshold (8000L): Day 5" in out
    print("[PASS] Test 1: First 8000L threshold interval detected (Day 5)")

    # Test 2: Low reserve alert on Day 7 (300L)
    assert "300" in out and "LOW RESERVE" in out
    print("[PASS] Test 2: Low reserve alert triggered on Day 7")

    # Test 3: Shortage on Day 8 (1200L deficit, level clamped at 0)
    assert "1200  SHORTAGE" in out
    assert "Total Shortage : 1200 L (Days: [8])" in out
    print("[PASS] Test 3: Shortage clamping and total deficit verified")

    # Test 4: Final water level at Day 10 is 2500L and zero overflow
    assert "Total Overflow : 0 L (Days: None)" in out
    assert "Final Water Level (Day 10): 2500 L" in out
    print("[PASS] Test 4: Final water level and overflow totals verified")

    print("\nAll 4 tests passed for Case Study 16.")


if __name__ == "__main__":
    run_tests()
