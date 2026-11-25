"""
Case Study 28: Repeated Transaction Detection
Name: Mareedu Paardhiv | Roll No: 26000626
"""

HIGH_VALUE_THRESHOLD = 50000.0

# Transaction list: (txn_id, account_no, amount, merchant)
TRANSACTIONS = [
    ("TXN901", "AC1001", 4200.0, "CampusStore"),
    ("TXN902", "AC1002", 18500.0, "TechMart"),
    ("TXN903", "AC1001", 4200.0, "CampusStore"),   # same account+amount+merchant repeat
    ("TXN904", "AC1003", 72000.0, "ElectroHub"),   # exceeds threshold
    ("TXN902", "AC1002", 18500.0, "TechMart"),      # duplicate txn_id AND repeat pattern
    ("TXN905", "AC1004", 1250.0, "BookHouse"),
    ("TXN906", "AC1005", 55000.0, "GoldCorner"),   # exceeds threshold
    ("TXN907", "AC1005", 55000.0, "GoldCorner"),   # repeat pattern + threshold
    ("TXN908", "AC1006", -500.0, "CafePoint"),     # invalid negative amount
]


def analyze_transactions(txns, threshold=HIGH_VALUE_THRESHOLD):
    seen_ids = []
    seen_patterns = []

    # First pass: count occurrences of txn_ids and (account, amount, merchant) patterns
    id_counts = []
    pattern_counts = []

    for txn in txns:
        txn_id, acc, amt, merch = txn
        pattern = (acc, amt, merch)

        # Track txn_id count using parallel lists
        found_id = False
        for i in range(len(seen_ids)):
            if seen_ids[i] == txn_id:
                id_counts[i] += 1
                found_id = True
                break
        if not found_id:
            seen_ids.append(txn_id)
            id_counts.append(1)

        # Track (account, amount, merchant) pattern count
        found_pat = False
        for i in range(len(seen_patterns)):
            if seen_patterns[i] == pattern:
                pattern_counts[i] += 1
                found_pat = True
                break
        if not found_pat:
            seen_patterns.append(pattern)
            pattern_counts.append(1)

    suspicious = []
    clean = []

    for idx in range(len(txns)):
        txn_id, acc, amt, merch = txns[idx]
        pattern = (acc, amt, merch)
        reasons = []

        # Check duplicate txn_id
        for i in range(len(seen_ids)):
            if seen_ids[i] == txn_id and id_counts[i] > 1:
                reasons.append(f"Duplicate ID ({id_counts[i]}x)")
                break

        # Check repeated account+amount+merchant pattern
        for i in range(len(seen_patterns)):
            if seen_patterns[i] == pattern and pattern_counts[i] > 1:
                reasons.append(f"Repeat Pattern ({pattern_counts[i]}x)")
                break

        # Check amount validity and threshold
        if amt <= 0:
            reasons.append("Invalid amount (<=0)")
        elif amt > threshold:
            reasons.append(f"Above Rs.{threshold:.0f}")

        if len(reasons) > 0:
            suspicious.append((idx + 1, txn_id, acc, amt, merch, reasons))
        else:
            clean.append((idx + 1, txn_id, acc, amt, merch))

    return clean, suspicious


def main():
    clean, suspicious = analyze_transactions(TRANSACTIONS)

    print("=" * 92)
    print(f"          REPEATED TRANSACTION & THRESHOLD AUDIT (Limit: Rs.{HIGH_VALUE_THRESHOLD:.0f})")
    print("=" * 92)
    print(f"Total Transactions Scanned : {len(TRANSACTIONS)}")
    print(f"Clean Transactions         : {len(clean)}")
    print(f"Suspicious Entries Flagged : {len(suspicious)}")
    print("-" * 92)

    print("\nSUSPICIOUS ENTRIES:")
    print(f"{'Row':>3} {'Txn ID':<8} {'Account':<8} {'Amount':>10} {'Merchant':<14} {'Flags'}")
    print("-" * 92)
    for row_no, txn_id, acc, amt, merch, reasons in suspicious:
        flag_text = "; ".join(reasons)
        print(f"{row_no:>3} {txn_id:<8} {acc:<8} {amt:>10.2f} {merch:<14} {flag_text}")

    print("\nCLEAN TRANSACTIONS:")
    print("-" * 92)
    for row_no, txn_id, acc, amt, merch in clean:
        print(f"  Row {row_no}: {txn_id} | {acc} | Rs.{amt:>8.2f} | {merch}")
    print("=" * 92)


if __name__ == "__main__":
    main()
