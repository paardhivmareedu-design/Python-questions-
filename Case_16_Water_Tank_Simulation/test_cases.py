"""Test cases for Case Study 16: Multi-Day Water Tank Simulation."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import solution


def run_tests():
    logs, summary = solution.simulate_tank(solution.DAILY_FLOWS)
    final_level, first_day, tot_ovf, tot_shrt, ovf_days, shrt_days = summary

    # Test 1: Check first threshold crossing (Day 4: 3500 + 800 + 200 + 1400 + 1400 = 7300? Wait let's verify!)
    # Day1: 3500 + 800 = 4300
    # Day2: 4300 + 200 = 4500
    # Day3: 4500 + 1400 = 5900
    # Day4: 5900 + 1400 = 7300 -> Day5: 7300 + 2100 = 9400 >= 8000! Wait let's check exact arithmetic
    assert len(logs) == 10
    assert first_day == 5
    print("[PASS] Test 1: First interval crossing 8000L threshold detected accurately")

    # Test 2: Overflow case on synthetic schedule
    ovf_logs, ovf_sum = solution.simulate_tank([(1, 9000, 1000)], capacity=10000, initial=4000)
    assert ovf_logs[0][3] == 10000
    assert ovf_sum[2] == 2000
    assert ovf_sum[4] == [1]
    print("[PASS] Test 2: Overflow capped at tank capacity and excess measured")

    # Test 3: Shortage case on synthetic schedule
    sh_logs, sh_sum = solution.simulate_tank([(1, 500, 4500)], capacity=10000, initial=2000)
    assert sh_logs[0][3] == 0
    assert sh_sum[3] == 2000
    assert sh_sum[5] == [1]
    print("[PASS] Test 3: Shortage clamped at 0L and deficit recorded")

    # Test 4: Low reserve warning triggered without shortage
    low_logs, _ = solution.simulate_tank([(1, 200, 2900)], capacity=10000, initial=3500, min_reserve=1000)
    assert low_logs[0][3] == 800
    assert low_logs[0][6] == "LOW RESERVE"
    print("[PASS] Test 4: Low reserve alert triggered below 1000L")

    # Test 5: Threshold never reached returns None
    _, no_thr = solution.simulate_tank([(1, 500, 400)], capacity=10000, initial=1000, threshold=8000)
    assert no_thr[1] is None
    print("[PASS] Test 5: Unreached threshold handled cleanly")

    print("\nAll 5 tests passed for Case Study 16.")


if __name__ == "__main__":
    run_tests()
