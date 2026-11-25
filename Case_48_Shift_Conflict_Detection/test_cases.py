"""Test cases for Case Study 48: Tuple-Based Employee Shift Conflict Detection."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import solution


def run_tests():
    # Test 1: Time parser validation
    assert solution.parse_time_to_minutes("09:30") == 570
    assert solution.parse_time_to_minutes("25:00") is None
    assert solution.parse_time_to_minutes("bad") is None
    print("[PASS] Test 1: Time string parser and validation")

    valid, invalid, conflicts, bad_emps, good_emps, _ = solution.analyze_shifts(solution.SHIFTS)

    # Test 2: Invalid end <= start shift rejected
    assert len(invalid) == 1
    assert invalid[0][0][0] == "EMP05"
    print("[PASS] Test 2: Invalid shift (end <= start) rejected")

    # Test 3: Partial overlap for EMP01 (12:00-13:00 = 60 mins)
    emp01_conflicts = [c for c in conflicts if c[0] == "EMP01"]
    assert len(emp01_conflicts) == 1
    assert emp01_conflicts[0][5] == "12:00-13:00"
    assert emp01_conflicts[0][6] == 60
    print("[PASS] Test 3: Partial overlap detected with exact overlap duration")

    # Test 4: Back-to-back shifts for EMP02 (08:00-12:00 and 12:00-16:00) do NOT conflict
    assert ("EMP02", "Bhavya") in good_emps
    assert ("EMP02", "Bhavya") not in bad_emps
    print("[PASS] Test 4: Adjacent non-overlapping shifts allowed cleanly")

    # Test 5: Multiple overlaps detected for EMP03 (2 pairwise overlaps among 3 shifts)
    emp03_conflicts = [c for c in conflicts if c[0] == "EMP03"]
    assert len(emp03_conflicts) == 2
    print("[PASS] Test 5: Multi-way shift overlaps detected for EMP03")

    print("\nAll 5 tests passed for Case Study 48.")


if __name__ == "__main__":
    run_tests()
