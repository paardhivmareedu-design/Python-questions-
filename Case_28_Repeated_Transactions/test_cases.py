"""Test cases for Case Study 28: Repeated Transaction Detection."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import solution


def run_tests():
    clean, suspicious = solution.analyze_transactions(solution.TRANSACTIONS)

    # Test 1: Only TXN905 (BookHouse) is completely clean in sample dataset
    assert len(clean) == 1
    assert clean[0][1] == "TXN905"
    print("[PASS] Test 1: Clean transaction isolated accurately")

    # Test 2: Duplicate TXN ID flagged for TXN902
    txn902_rows = [item for item in suspicious if item[1] == "TXN902"]
    assert len(txn902_rows) == 2
    assert any("Duplicate ID" in r for r in txn902_rows[0][5])
    print("[PASS] Test 2: Duplicate transaction ID detected")

    # Test 3: Repeated pattern with different TXN IDs (TXN901 & TXN903)
    txn901 = [item for item in suspicious if item[1] == "TXN901"][0]
    assert any("Repeat Pattern" in r for r in txn901[5])
    print("[PASS] Test 3: Repeated account-amount-merchant pattern flagged")

    # Test 4: High value threshold violation
    txn904 = [item for item in suspicious if item[1] == "TXN904"][0]
    assert any("Above Rs." in r for r in txn904[5])
    print("[PASS] Test 4: Threshold violation > Rs.50,000 flagged")

    # Test 5: Negative amount flagged as invalid
    txn908 = [item for item in suspicious if item[1] == "TXN908"][0]
    assert any("Invalid" in r for r in txn908[5])
    print("[PASS] Test 5: Invalid non-positive amount caught")

    print("\nAll 5 tests passed for Case Study 28.")


if __name__ == "__main__":
    run_tests()
