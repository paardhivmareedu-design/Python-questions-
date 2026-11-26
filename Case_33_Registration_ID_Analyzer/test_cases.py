"""Test cases for Case Study 33: Campus Registration Identifier Analyzer."""
import os
import subprocess
import sys

SOL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "solution.py")


def run_tests():
    res = subprocess.run([sys.executable, SOL_PATH], capture_output=True, text=True)
    assert res.returncode == 0
    out = res.stdout

    # Test 1: Valid ID component extraction
    assert "26-CSE-0626    2026         CSE      Computer Science       0626" in out
    assert "25-ECE-0318    2025         ECE      Electronics & Comm.    0318" in out
    print("[PASS] Test 1: Valid IDs parsed into year, branch, department, and serial")

    # Test 2: Branch and year classifications
    assert "CSE (Computer Science): 2 student(s)" in out
    assert "Batch 2026: 3 student(s)" in out
    print("[PASS] Test 2: Branch and admission batch counts verified")

    # Test 3: Format rejections (lowercase, missing hyphen, bad year, unknown branch, 0000)
    assert "'26-cse-0112' -> Branch code 'cse' must be 3 uppercase letters" in out
    assert "'26CSE0626' -> Expected length 11 (YY-BBB-NNNN), got 9" in out
    assert "'19-CSE-0401' -> Admission year '2019' outside allowed range 2021-2026" in out
    assert "'25-BIO-0120' -> Unknown branch code 'BIO'" in out
    assert "'26-ECE-0000' -> Serial number cannot be '0000'" in out
    print("[PASS] Test 3: All 5 malformed ID patterns rejected with specific reasons")

    # Test 4: Duplicate detection and summary count
    assert "26-CSE-0626 (appeared more than once)" in out
    assert "Summary: 7 unique valid, 1 duplicate, 5 invalid (out of 13 inputs)." in out
    print("[PASS] Test 4: Duplicate identifier flagged and summary verified")

    print("\nAll 4 tests passed for Case Study 33.")


if __name__ == "__main__":
    run_tests()
