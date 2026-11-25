"""Test cases for Case Study 06: Railway Fare and Reservation Calculator."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import solution


def run_tests():
    # Test 1: Distance slab calculation
    assert abs(solution.calculate_distance_base(80) - 64.0) < 0.01
    assert abs(solution.calculate_distance_base(300) - 220.0) < 0.01
    assert abs(solution.calculate_distance_base(600) - 420.0) < 0.01
    print("[PASS] Test 1: Distance slab fare calculations")

    # Test 2: Senior citizen concession in 3A (CONFIRMED -> refund 0, net retained = total)
    # 620 km -> 80 + 280 + 72 = 432 base; 3A mult 2.2 -> 950.40; 40% off -> 570.24 + 40 = 610.24
    res_sr = solution.compute_ticket(solution.PASSENGERS[0])
    assert res_sr[0] is True
    assert abs(res_sr[1][8] - 610.24) < 0.01
    assert res_sr[1][5] == "Senior 40%"
    assert res_sr[1][11] == 0.0
    assert abs(res_sr[1][12] - 610.24) < 0.01
    print("[PASS] Test 2: Senior citizen 40% concession and reservation fee")

    # Test 3: Infant (<5 years) travels free with zero reservation fee
    res_inf = solution.compute_ticket(solution.PASSENGERS[3])
    assert res_inf[0] is True
    assert res_inf[1][8] == 0.0
    print("[PASS] Test 3: Infant free travel without reservation charge")

    # Test 4: Child concession (50%)
    res_child = solution.compute_ticket(solution.PASSENGERS[2])
    assert res_child[0] is True
    assert res_child[1][5] == "Child 50%"
    print("[PASS] Test 4: Child 50% concession applied")

    # Test 5: Cancellation penalties (early, late, last minute)
    res_late = solution.compute_ticket(solution.PASSENGERS[4])
    assert res_late[0] is True
    total_f, penalty, refund = res_late[1][8], res_late[1][10], res_late[1][11]
    assert abs(penalty - round(total_f * 0.25, 2)) < 0.01
    assert abs((penalty + refund) - total_f) < 0.01

    res_early = solution.compute_ticket(solution.PASSENGERS[5])
    assert res_early[1][10] == 60.0
    print("[PASS] Test 5: Cancellation penalty and refund computation")

    # Test 6: Invalid distance rejected
    res_bad = solution.compute_ticket(solution.PASSENGERS[7])
    assert res_bad[0] is False
    print("[PASS] Test 6: Negative distance booking rejected")

    print("\nAll 6 tests passed for Case Study 06.")


if __name__ == "__main__":
    run_tests()
