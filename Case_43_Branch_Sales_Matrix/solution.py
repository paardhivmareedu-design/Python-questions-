"""
Case Study 43: Multi-Branch Sales Matrix Comparison
Name: Mareedu Paardhiv | Roll No: 26000626
"""

BRANCHES = ["Vijayawada", "Guntur", "Visakhapatnam", "Tirupati"]
PRODUCTS = ["Laptop", "Tablet", "Phone", "Headphones"]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]

# 3D nested list: SALES_MATRIX[branch_index][product_index][day_index] (units sold)
SALES_MATRIX = [
    # Vijayawada
    [
        [12, 15, 11, 14, 18],   # Laptop = 70
        [18, 20, 16, 19, 22],   # Tablet = 95
        [30, 28, 35, 31, 40],   # Phone = 164 (best)
        [22, 24, 20, 25, 29],   # Headphones = 120
    ],
    # Guntur
    [
        [10, 12, 9, 11, 14],    # Laptop = 56
        [24, 26, 22, 28, 30],   # Tablet = 130 (best)
        [20, 19, 21, 22, 24],   # Phone = 106
        [15, 16, 14, 18, 17],   # Headphones = 80
    ],
    # Visakhapatnam
    [
        [22, 25, 24, 28, 31],   # Laptop = 130
        [19, 21, 20, 22, 23],   # Tablet = 105
        [32, 34, 30, 36, 38],   # Phone = 170
        [35, 38, 34, 40, 43],   # Headphones = 190 (best)
    ],
    # Tirupati
    [
        [14, 16, 15, 17, 18],   # Laptop = 80
        [15, 14, 16, 15, 17],   # Tablet = 77
        [25, 27, 24, 29, 30],   # Phone = 135 (best)
        [18, 20, 19, 21, 22],   # Headphones = 100
    ],
]


def analyze_sales(matrix):
    num_branches = len(matrix)
    num_products = len(matrix[0])
    num_days = len(matrix[0][0])

    # branch_product_totals[b][p] = 5-day sum for product p at branch b
    branch_product_totals = []
    branch_totals = []
    product_totals = [0] * num_products
    day_totals = [0] * num_days

    for b in range(num_branches):
        row_totals = []
        b_sum = 0
        for p in range(num_products):
            p_sum = 0
            for d in range(num_days):
                val = matrix[b][p][d]
                p_sum += val
                day_totals[d] += val
            row_totals.append(p_sum)
            product_totals[p] += p_sum
            b_sum += p_sum
        branch_product_totals.append(row_totals)
        branch_totals.append(b_sum)

    # Best-performing product for each branch
    best_per_branch = []
    for b in range(num_branches):
        max_units = branch_product_totals[b][0]
        best_names = [PRODUCTS[0]]
        for p in range(1, num_products):
            val = branch_product_totals[b][p]
            if val > max_units:
                max_units = val
                best_names = [PRODUCTS[p]]
            elif val == max_units:
                best_names.append(PRODUCTS[p])
        best_per_branch.append((BRANCHES[b], ", ".join(best_names), max_units))

    # Rank branches descending using simple selection sort
    ranked_branches = []
    for b in range(num_branches):
        ranked_branches.append((branch_totals[b], BRANCHES[b]))
    for i in range(len(ranked_branches)):
        best_idx = i
        for j in range(i + 1, len(ranked_branches)):
            if ranked_branches[j][0] > ranked_branches[best_idx][0]:
                best_idx = j
        ranked_branches[i], ranked_branches[best_idx] = ranked_branches[best_idx], ranked_branches[i]

    return branch_product_totals, branch_totals, product_totals, day_totals, best_per_branch, ranked_branches


def main():
    bp_totals, b_totals, p_totals, d_totals, best_per_branch, ranked_branches = analyze_sales(SALES_MATRIX)
    grand_total = sum(b_totals)

    print("=" * 84)
    print("              MULTI-BRANCH SALES MATRIX COMPARISON (5-DAY UNITS SOLD)")
    print("=" * 84)
    header = f"{'Branch':<16}"
    for prod in PRODUCTS:
        header += f"{prod:>12}"
    header += f"{'Branch Total':>16}"
    print(header)
    print("-" * 84)

    for b in range(len(BRANCHES)):
        line = f"{BRANCHES[b]:<16}"
        for p in range(len(PRODUCTS)):
            line += f"{bp_totals[b][p]:>12}"
        line += f"{b_totals[b]:>16}"
        print(line)

    print("-" * 84)
    prod_line = f"{'Product Total':<16}"
    for pt in p_totals:
        prod_line += f"{pt:>12}"
    prod_line += f"{grand_total:>16}"
    print(prod_line)
    print("=" * 84)

    print("\nBEST-PERFORMING PRODUCT BY BRANCH:")
    for branch_name, prod_name, units in best_per_branch:
        print(f"  {branch_name:<15} -> {prod_name} ({units} units)")

    print("\nBRANCH RANKING (HIGHEST TO LOWEST SALES):")
    for rank in range(len(ranked_branches)):
        tot, b_name = ranked_branches[rank]
        share = (tot / grand_total) * 100.0
        print(f"  #{rank + 1} {b_name:<15} : {tot:>4} units ({share:.1f}% share)")

    print("\nDAILY SALES TOTALS ACROSS ALL BRANCHES:")
    peak_day_idx = 0
    for d in range(len(DAYS)):
        if d_totals[d] > d_totals[peak_day_idx]:
            peak_day_idx = d
        print(f"  {DAYS[d]}: {d_totals[d]} units")
    print(f"  Peak Sales Day: {DAYS[peak_day_idx]} ({d_totals[peak_day_idx]} units)")


if __name__ == "__main__":
    main()
