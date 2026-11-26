"""Test cases for Case Study 06: Railway Fare and Reservation Calculator."""
import os
import subprocess
import sys

SOL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "solution.py")


def run_tests():
    res = subprocess.run([sys.executable, SOL_PATH], capture_output=True, text=True)
    assert res.returncode == 0
    out = res.stdout

    # Test 1: Senior citizen 40% concession in 3A (PNR101 -> 610.24)
    assert "PNR101" in out and "Senior 40%" in out and "610.24" in out
    print("[PASS] Test 1: Senior citizen 40% concession and 3A fare verified")

    # Test 2: Child 50% concession in 2A (PNR103 -> 635.60)
    assert "PNR103" in out and "Child 50%" in out and "635.60" in out
    print("[PASS] Test 2: Child 50% concession verified")

    # Test 3: Infant (<5) travels free without reservation charge (PNR104 -> 0.00)
    assert "PNR104" in out and "Infant Free" in out
    print("[PASS] Test 3: Infant free travel verified")

    # Test 4: Cancellation penalties and refunds
    assert "PNR105" in out and "420.50" in out and "1261.50" in out
    assert "PNR106" in out and "60.00" in out and "96.00" in out
    assert "PNR107" in out and "377.50" in out
    print("[PASS] Test 4: Early, late, and last-minute cancellation rules verified")

    # Test 5: Revenue summary and rejected invalid booking
    assert "Gross Billed: Rs.4106.84 | Refunds: Rs.1735.00 | Net Revenue: Rs.2371.84" in out
    assert "PNR108 (Invalid Ticket): Invalid age or distance" in out
    print("[PASS] Test 5: Revenue totals and invalid distance rejection verified")

    print("\nAll 5 tests passed for Case Study 06.")


if __name__ == "__main__":
    run_tests()
