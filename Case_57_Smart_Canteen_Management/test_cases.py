"""Test cases for Case Study 57: Smart Canteen Order and Stock Management."""
import os
import subprocess
import sys

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOL_PATH = os.path.join(CASE_DIR, "solution.py")
DEMO_IN = os.path.join(CASE_DIR, "demo_input.txt")


def run_with_input(text_in):
    res = subprocess.run([sys.executable, SOL_PATH], input=text_in, capture_output=True, text=True)
    assert res.returncode == 0
    return res.stdout


def run_tests():
    # Test 1: Valid order computes bill + 5% GST and updates stock
    out1 = run_with_input("2\nC1\n4\n5\n")
    assert "ORDER #1 CONFIRMED: 4 x Masala Dosa (C1) | Stock left: 16" in out1
    assert "Subtotal: Rs.180.00 | GST (5%): Rs.9.00 | Bill Total: Rs.189.00" in out1
    print("[PASS] Test 1: Valid order updates stock and calculates GST bill")

    # Test 2: Order exceeding available stock rejected cleanly
    out2 = run_with_input("2\nC3\n20\n5\n")
    assert "REJECTED: Requested 20 x Veg Fried Rice, only 15 left in stock." in out2
    assert "Orders Fulfilled : 0" in out2
    print("[PASS] Test 2: Insufficient stock order rejected cleanly")

    # Test 3: Unknown item code rejected cleanly
    out3 = run_with_input("2\nZ9\n5\n")
    assert "REJECTED: Unknown item code 'Z9'." in out3
    print("[PASS] Test 3: Unknown item code rejected")

    # Test 4: Non-numeric and zero quantity rejected without crashing
    out4 = run_with_input("2\nC2\nabc\n2\nC2\n0\n5\n")
    assert "REJECTED: Quantity must be a positive whole number." in out4
    assert "REJECTED: Quantity must be at least 1." in out4
    print("[PASS] Test 4: Non-numeric and zero quantities rejected")

    # Test 5: Full demo_input.txt flow verifies depletion OUT and daily revenue
    demo_text = open(DEMO_IN).read()
    out5 = run_with_input(demo_text)
    assert "C3     Veg Fried Rice          70.00        OUT       15" in out5
    assert "Orders Fulfilled : 4" in out5
    assert "Total Revenue    : Rs. 1606.50" in out5
    print("[PASS] Test 5: Full demo script stock depletion and revenue verified")

    print("\nAll 5 tests passed for Case Study 57.")


if __name__ == "__main__":
    run_tests()
