"""
Case Study 28: Repeated Transaction Detection
Name: Mareedu Paardhiv | Roll No: 26000626
"""

high_value_limit = 50000.0

# Transaction records: (txn_id, account_no, amount, merchant)
transactions = [
    ("TXN901", "AC1001", 4200.0, "CampusStore"),
    ("TXN902", "AC1002", 18500.0, "TechMart"),
    ("TXN903", "AC1001", 4200.0, "CampusStore"),   # repeated account+amount+merchant
    ("TXN904", "AC1003", 72000.0, "ElectroHub"),   # exceeds threshold
    ("TXN902", "AC1002", 18500.0, "TechMart"),      # duplicate txn_id and repeat pattern
    ("TXN905", "AC1004", 1250.0, "BookHouse"),     # clean
    ("TXN906", "AC1005", 55000.0, "GoldCorner"),   # exceeds threshold + repeat
    ("TXN907", "AC1005", 55000.0, "GoldCorner"),   # exceeds threshold + repeat
    ("TXN908", "AC1006", -500.0, "CafePoint"),     # invalid negative amount
]

# Pass 1: Count occurrences of txn_ids and (account, amount, merchant) patterns
seen_ids = []
id_counts = []
seen_patterns = []
pattern_counts = []

for txn in transactions:
    txn_id, acc, amt, merch = txn
    pattern = (acc, amt, merch)

    found_id = False
    for i in range(len(seen_ids)):
        if seen_ids[i] == txn_id:
            id_counts[i] = id_counts[i] + 1
            found_id = True
            break
    if not found_id:
        seen_ids.append(txn_id)
        id_counts.append(1)

    found_pat = False
    for i in range(len(seen_patterns)):
        if seen_patterns[i] == pattern:
            pattern_counts[i] = pattern_counts[i] + 1
            found_pat = True
            break
    if not found_pat:
        seen_patterns.append(pattern)
        pattern_counts.append(1)

# Pass 2: Flag suspicious entries and isolate clean entries
suspicious = []
clean = []

for idx in range(len(transactions)):
    txn_id, acc, amt, merch = transactions[idx]
    pattern = (acc, amt, merch)
    reasons = []

    for i in range(len(seen_ids)):
        if seen_ids[i] == txn_id and id_counts[i] > 1:
            reasons.append(f"Duplicate ID ({id_counts[i]}x)")
            break

    for i in range(len(seen_patterns)):
        if seen_patterns[i] == pattern and pattern_counts[i] > 1:
            reasons.append(f"Repeat Pattern ({pattern_counts[i]}x)")
            break

    if amt <= 0:
        reasons.append("Invalid amount (<=0)")
    elif amt > high_value_limit:
        reasons.append(f"Above Rs.{high_value_limit:.0f}")

    if len(reasons) > 0:
        suspicious.append((idx + 1, txn_id, acc, amt, merch, reasons))
    else:
        clean.append((idx + 1, txn_id, acc, amt, merch))

print("=" * 92)
print(f"          REPEATED TRANSACTION & THRESHOLD AUDIT (Limit: Rs.{high_value_limit:.0f})")
print("=" * 92)
print(f"Total Transactions Scanned : {len(transactions)}")
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
