"""Test cases for Case Study 37: Nested Loop Calendar Generator."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import solution


def run_tests():
    # Test 1: Leap year vs non-leap year February
    assert solution.get_month_days(2, 2024) == 29
    assert solution.get_month_days(2, 2026) == 28
    assert solution.get_month_days(2, 1900) == 28
    assert solution.get_month_days(2, 2000) == 29
    print("[PASS] Test 1: Leap year and century rules verified")

    # Test 2: Month length lookup
    assert solution.get_month_days(4, 2026) == 30
    assert solution.get_month_days(10, 2026) == 31
    assert solution.get_month_days(13, 2026) is None
    print("[PASS] Test 2: Standard month lengths and invalid month check")

    # Test 3: Alignment check for October 2026 (starts on Thursday = index 4)
    ok, lines = solution.build_calendar_lines("October 2026", 31, 4)
    assert ok is True
    first_week_row = lines[5]
    # 4 blank weekday slots (16 spaces) before day '   1'
    assert first_week_row.startswith("                " + "   1")
    assert "  31" in lines[-2]
    print("[PASS] Test 3: Leading blank alignment and final day verified")

    # Test 4: Sunday start (index 0) with 28 days fits in exactly 4 week rows
    ok2, lines2 = solution.build_calendar_lines("Feb Non-Leap", 28, 0)
    assert ok2 is True
    # 5 header lines + 4 week rows + 1 footer line = 10 lines
    assert len(lines2) == 10
    print("[PASS] Test 4: 28-day month starting Sunday spans exactly 4 rows")

    # Test 5: Invalid month length rejected
    ok_bad1, _ = solution.build_calendar_lines("Bad Month", 32, 1)
    assert ok_bad1 is False
    ok_bad2, _ = solution.build_calendar_lines("Bad Month", 27, 1)
    assert ok_bad2 is False
    print("[PASS] Test 5: Invalid month lengths (27, 32) rejected")

    # Test 6: Invalid weekday index rejected
    ok_bad3, _ = solution.build_calendar_lines("Bad Weekday", 30, 7)
    assert ok_bad3 is False
    ok_bad4, _ = solution.build_calendar_lines("Bad Weekday", 30, -1)
    assert ok_bad4 is False
    print("[PASS] Test 6: Out-of-range starting weekday rejected")

    print("\nAll 6 tests passed for Case Study 37.")


if __name__ == "__main__":
    run_tests()
