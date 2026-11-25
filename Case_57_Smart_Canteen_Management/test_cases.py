"""Test cases for Case Study 57: Smart Canteen Order and Stock Management."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import solution


def run_tests():
    inv = solution.create_inventory()
    orders = []

    # Test 1: Valid order deducts stock and adds GST correctly
    ok1, msg1 = solution.place_order(inv, orders, "c1", "4")
    assert ok1 is True
    assert len(orders) == 1
    # 4 * 45 = 180.0, GST 5% = 9.0, total = 189.0
    assert orders[0][4] == 180.0 and orders[0][5] == 9.0 and orders[0][6] == 189.0
    assert solution.find_item(inv, "C1")[4] == 16
    assert solution.find_item(inv, "C1")[5] == 4
    print("[PASS] Test 1: Valid order updates stock and calculates GST bill")

    # Test 2: Order exceeding available stock rejected without modifying inventory
    ok2, msg2 = solution.place_order(inv, orders, "C3", "20")
    assert ok2 is False and "only 15 left" in msg2
    assert solution.find_item(inv, "C3")[4] == 15
    print("[PASS] Test 2: Insufficient stock order rejected cleanly")

    # Test 3: Unknown item code rejected
    ok3, msg3 = solution.place_order(inv, orders, "Z9", "2")
    assert ok3 is False and "Unknown item code" in msg3
    print("[PASS] Test 3: Unknown item code rejected")

    # Test 4: Non-numeric or zero quantity rejected
    ok4a, _ = solution.place_order(inv, orders, "C2", "abc")
    ok4b, _ = solution.place_order(inv, orders, "C2", "0")
    ok4c, _ = solution.place_order(inv, orders, "C2", "-5")
    assert ok4a is False and ok4b is False and ok4c is False
    print("[PASS] Test 4: Non-positive and non-numeric quantities rejected")

    # Test 5: Exact remaining stock depletion brings stock to 0
    ok5, _ = solution.place_order(inv, orders, "C3", "15")
    assert ok5 is True and solution.find_item(inv, "C3")[4] == 0
    ok6, _ = solution.place_order(inv, orders, "C3", "1")
    assert ok6 is False
    print("[PASS] Test 5: Full stock depletion and subsequent rejection verified")

    print("\nAll 5 tests passed for Case Study 57.")


if __name__ == "__main__":
    run_tests()
