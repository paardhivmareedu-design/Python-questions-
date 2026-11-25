"""Test cases for Case Study 33: Campus Registration Identifier Analyzer."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import solution


def run_tests():
    # Test 1: Valid ID extraction
    ok, reg, info, errs = solution.analyze_reg_id("26-CSE-0626")
    assert ok is True
    assert info == ("26-CSE-0626", "2026", "CSE", "Computer Science", "0626")
    assert errs == []
    print("[PASS] Test 1: Valid ID parsed into year, branch, department, and serial")

    # Test 2: Whitespace trimmed cleanly
    ok2, reg2, info2, _ = solution.analyze_reg_id("  25-ECE-0318  ")
    assert ok2 is True and info2[0] == "25-ECE-0318"
    print("[PASS] Test 2: Leading/trailing whitespace trimmed")

    # Test 3: Lowercase branch rejected
    ok3, _, _, errs3 = solution.analyze_reg_id("26-cse-0112")
    assert ok3 is False and len(errs3) >= 1
    print("[PASS] Test 3: Lowercase branch code rejected")

    # Test 4: Wrong length / missing separators rejected
    ok4, _, _, _ = solution.analyze_reg_id("26CSE0626")
    assert ok4 is False
    print("[PASS] Test 4: Malformed separator / wrong length rejected")

    # Test 5: Out-of-range admission year rejected
    ok5, _, _, errs5 = solution.analyze_reg_id("19-CSE-0401")
    assert ok5 is False and any("year" in e.lower() for e in errs5)
    print("[PASS] Test 5: Invalid admission year rejected")

    # Test 6: Zero serial number 0000 rejected
    ok6, _, _, errs6 = solution.analyze_reg_id("26-ECE-0000")
    assert ok6 is False and any("0000" in e for e in errs6)
    print("[PASS] Test 6: Zero serial '0000' rejected")

    print("\nAll 6 tests passed for Case Study 33.")


if __name__ == "__main__":
    run_tests()
