"""Test cases for Case Study 11: Examination Result and Grace-Mark Validation."""
import os
import subprocess
import sys

SOL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "solution.py")


def run_tests():
    res = subprocess.run([sys.executable, SOL_PATH], capture_output=True, text=True)
    assert res.returncode == 0
    out = res.stdout

    # Test 1: Normal distinction student without grace
    assert "26B01   Nikhil Varma" in out and "82.40  Distinction" in out
    print("[PASS] Test 1: Distinction classification verified")

    # Test 2: Eligible for grace across 2 subjects (26B02: +3, +2 = 5 grace -> Second Class)
    assert "26B02 (Bhavana Rao): Grace applied -> Maths +3 (37->40), Digital Logic +2 (38->40)" in out
    assert "55.40  Second Class" in out
    print("[PASS] Test 2: Two-subject grace policy within pool verified")

    # Test 3: Total grace needed > 10 (26B03) -> stays Fail
    assert "26B03 (Charan Teja): Grace not eligible" in out
    print("[PASS] Test 3: Total 10-mark grace pool cap enforced")

    # Test 4: Single subject cap > 5 (26B04) -> stays Fail
    assert "26B04 (Keerthi S): Grace not eligible -> Failed in Maths(32)" in out
    print("[PASS] Test 4: Single-subject 5-mark grace cap enforced")

    # Test 5: Invalid >100 mark rejected and summary counts accurate
    assert "26B08 (Bad Data): Mark 105 out of valid range 0..100" in out
    assert "Summary: 5 Passed (2 via grace), 2 Failed, 1 Invalid." in out
    print("[PASS] Test 5: Out-of-range mark rejection and summary verified")

    print("\nAll 5 tests passed for Case Study 11.")


if __name__ == "__main__":
    run_tests()
