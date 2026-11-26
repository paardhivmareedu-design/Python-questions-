"""Test cases for Case Study 43: Multi-Branch Sales Matrix Comparison."""
import os
import subprocess
import sys

SOL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "solution.py")


def run_tests():
    res = subprocess.run([sys.executable, SOL_PATH], capture_output=True, text=True)
    assert res.returncode == 0
    out = res.stdout

    # Test 1: Branch totals
    assert "Vijayawada" in out and "449" in out
    assert "Guntur" in out and "372" in out
    assert "Visakhapatnam" in out and "595" in out
    assert "Tirupati" in out and "392" in out
    print("[PASS] Test 1: Branch totals verified across nested list matrix")

    # Test 2: Product totals and grand total (1808)
    assert "Product Total" in out and "336" in out and "407" in out
    assert "575" in out and "490" in out and "1808" in out
    print("[PASS] Test 2: Product totals and grand total (1808) verified")

    # Test 3: Best product per branch
    assert "Vijayawada      -> Phone (164 units)" in out
    assert "Guntur          -> Tablet (130 units)" in out
    assert "Visakhapatnam   -> Headphones (190 units)" in out
    assert "Tirupati        -> Phone (135 units)" in out
    print("[PASS] Test 3: Best-performing product identified for each branch")

    # Test 4: Ranking and peak day
    assert "#1 Visakhapatnam" in out and "#4 Guntur" in out
    assert "Peak Sales Day: Fri (416 units)" in out
    print("[PASS] Test 4: Branch ranking order and peak sales day verified")

    print("\nAll 4 tests passed for Case Study 43.")


if __name__ == "__main__":
    run_tests()
