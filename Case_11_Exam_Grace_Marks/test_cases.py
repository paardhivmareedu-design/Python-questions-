"""Test cases for Case Study 11: Examination Result and Grace-Mark Validation."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import solution


def run_tests():
    # Test 1: Normal distinction student without grace
    res1 = solution.evaluate_student(solution.STUDENTS[0])
    assert res1[0] is True
    assert res1[1][5] == 0
    assert res1[1][8] == "Distinction"
    print("[PASS] Test 1: Distinction classification with zero grace")

    # Test 2: Eligible for grace across 2 subjects (3 + 2 = 5 <= 10)
    res2 = solution.evaluate_student(solution.STUDENTS[1])
    assert res2[0] is True
    assert res2[1][5] == 5
    assert res2[1][3][0] == 40 and res2[1][3][3] == 40
    assert res2[1][8] == "Second Class"
    print("[PASS] Test 2: Grace marks awarded across two subjects within limits")

    # Test 3: Total grace needed > 10 -> grace NOT awarded, stays Fail
    res3 = solution.evaluate_student(solution.STUDENTS[2])
    assert res3[0] is True
    assert res3[1][5] == 0
    assert res3[1][8] == "Fail"
    print("[PASS] Test 3: Exceeding 10-mark grace pool leaves student failed")

    # Test 4: Single subject needs 8 marks (> 5 per-subject cap) -> Fail
    res4 = solution.evaluate_student(solution.STUDENTS[3])
    assert res4[0] is True
    assert res4[1][5] == 0
    assert res4[1][8] == "Fail"
    print("[PASS] Test 4: Single-subject 5-mark grace limit enforced")

    # Test 5: Marks never exceed MAX_MARKS (100) and invalid >100 rejected
    res_bad = solution.evaluate_student(solution.STUDENTS[7])
    assert res_bad[0] is False
    print("[PASS] Test 5: Out-of-range mark (>100) rejected")

    # Test 6: Pass class boundary (40-49.99%)
    res5 = solution.evaluate_student(solution.STUDENTS[4])
    assert res5[1][8] == "Pass Class"
    print("[PASS] Test 6: Pass Class classification verified")

    print("\nAll 6 tests passed for Case Study 11.")


if __name__ == "__main__":
    run_tests()
