"""Test cases for Case Study 43: Multi-Branch Sales Matrix Comparison."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import solution


def run_tests():
    bp_totals, b_totals, p_totals, d_totals, best_per_branch, ranked = solution.analyze_sales(
        solution.SALES_MATRIX
    )

    # Test 1: Branch totals match manual sums
    # Vijayawada: 70+95+164+120 = 449
    # Guntur: 56+130+106+80 = 372
    # Visakhapatnam: 130+105+170+190 = 595
    # Tirupati: 80+77+135+100 = 392
    assert b_totals == [449, 372, 595, 392]
    print("[PASS] Test 1: Branch totals verified across 3D matrix")

    # Test 2: Product totals match across branches
    # Laptop: 70+56+130+80 = 336
    # Tablet: 95+130+105+77 = 407
    # Phone: 164+106+170+135 = 575
    # Headphones: 120+80+190+100 = 490
    assert p_totals == [336, 407, 575, 490]
    print("[PASS] Test 2: Product-wise totals verified")

    # Test 3: Grand total consistency (sum of branch totals == sum of product totals == sum of day totals)
    assert sum(b_totals) == sum(p_totals) == sum(d_totals) == 1808
    print("[PASS] Test 3: Matrix cross-total consistency (1808 units)")

    # Test 4: Best product per branch
    assert best_per_branch[0] == ("Vijayawada", "Phone", 164)
    assert best_per_branch[1] == ("Guntur", "Tablet", 130)
    assert best_per_branch[2] == ("Visakhapatnam", "Headphones", 190)
    assert best_per_branch[3] == ("Tirupati", "Phone", 135)
    print("[PASS] Test 4: Best-performing product identified for each branch")

    # Test 5: Branch ranking order
    assert [name for _, name in ranked] == ["Visakhapatnam", "Vijayawada", "Tirupati", "Guntur"]
    print("[PASS] Test 5: Branch ranking order descending verified")

    print("\nAll 5 tests passed for Case Study 43.")


if __name__ == "__main__":
    run_tests()
