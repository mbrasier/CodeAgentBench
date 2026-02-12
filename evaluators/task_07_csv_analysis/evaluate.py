#!/usr/bin/env python3
"""Evaluator for Task 07: CSV Data Analysis"""
import sys
import os
import importlib.util

TASK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '..', '..', 'tasks', 'task_07_csv_analysis')
CSV_PATH = os.path.join(TASK_DIR, 'sales_data.csv')


def load_solution():
    path = os.path.join(TASK_DIR, 'processor.py')
    if not os.path.exists(path):
        print("[FAIL] processor.py not found")
        sys.exit(1)
    spec = importlib.util.spec_from_file_location("processor", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def approx_eq(a, b, tol=0.02):
    return abs(a - b) <= tol


passed = failed = 0


def check(name, fn, validator):
    global passed, failed
    try:
        got = fn()
        ok, msg = validator(got)
        if ok:
            print(f"[PASS] {name}")
            passed += 1
        else:
            print(f"[FAIL] {name}: {msg} (got {got!r})")
            failed += 1
    except NotImplementedError:
        print(f"[FAIL] {name}: not implemented")
        failed += 1
    except Exception as e:
        print(f"[FAIL] {name}: {type(e).__name__}: {e}")
        failed += 1


def main():
    sol = load_solution()

    # ── load_data ────────────────────────────────────────────────────────────
    check(
        "load_data row count",
        lambda: len(sol.load_data(CSV_PATH)),
        lambda v: (v == 25, f"expected 25 rows, got {v}")
    )
    check(
        "load_data quantity is int",
        lambda: type(sol.load_data(CSV_PATH)[0]['quantity']),
        lambda v: (v is int, f"expected int, got {v}")
    )
    check(
        "load_data unit_price is float",
        lambda: type(sol.load_data(CSV_PATH)[0]['unit_price']),
        lambda v: (v is float, f"expected float, got {v}")
    )

    # ── total_revenue_by_category ────────────────────────────────────────────
    # Pre-compute expected values from the CSV
    # Electronics rows and their revenues:
    # 1: 1*1299.99, 3: 3*29.99, 5: 1*1299.99, 7: 1*149.99, 9: 1*1299.99,
    # 10: 2*29.99, 13: 1*399.99, 14: 1*1299.99, 15: 1*149.99, 16: 2*399.99,
    # 20: 4*29.99, 21: 1*399.99, 22: 1*1299.99, 23: 2*149.99
    elec = (1299.99 + 3*29.99 + 1299.99 + 149.99 + 1299.99 + 2*29.99 +
            399.99 + 1299.99 + 149.99 + 2*399.99 + 4*29.99 + 399.99 +
            1299.99 + 2*149.99)
    # Books: 2: 2*39.99, 6: 39.99, 12: 3*39.99, 19: 39.99, 24: 39.99
    books = 2*39.99 + 39.99 + 3*39.99 + 39.99 + 39.99
    # Furniture: 4: 449.99, 8: 2*299.99, 11: 449.99, 17: 299.99, 18: 449.99, 25: 299.99
    furn = 449.99 + 2*299.99 + 449.99 + 299.99 + 449.99 + 299.99

    def get_rev():
        data = sol.load_data(CSV_PATH)
        return sol.total_revenue_by_category(data)

    check(
        "revenue by category has 3 keys",
        lambda: len(get_rev()),
        lambda v: (v == 3, f"expected 3 categories, got {v}")
    )
    check(
        "electronics revenue",
        lambda: get_rev().get('Electronics', 0),
        lambda v: (approx_eq(v, elec), f"expected ~{elec:.2f}, got {v:.2f}")
    )
    check(
        "books revenue",
        lambda: get_rev().get('Books', 0),
        lambda v: (approx_eq(v, books), f"expected ~{books:.2f}, got {v:.2f}")
    )
    check(
        "furniture revenue",
        lambda: get_rev().get('Furniture', 0),
        lambda v: (approx_eq(v, furn), f"expected ~{furn:.2f}, got {v:.2f}")
    )

    # ── top_customers ────────────────────────────────────────────────────────
    # C001: 1299.99+89.97+149.99+399.99+39.99+299.99 = 2279.92
    # C002: 79.98+1299.99+449.99+799.98+39.99       = 2669.93
    # C003: 449.99+599.98+1299.99+119.96             = 2469.92
    # C004: 39.99+59.98+399.99                       = 499.96
    # C005: 1299.99+119.97+299.99+299.98             = 2019.93
    # C006: 149.99+449.99+1299.99                    = 1899.97
    # Sorted desc: C002, C003, C001, C005, C006, C004

    def get_top(n):
        data = sol.load_data(CSV_PATH)
        return sol.top_customers(data, n)

    check(
        "top 1 customer",
        lambda: get_top(1),
        lambda v: (v == ['C002'], f"expected ['C002'], got {v}")
    )
    check(
        "top 3 customers",
        lambda: get_top(3),
        lambda v: (v == ['C002', 'C003', 'C001'], f"expected ['C002','C003','C001'], got {v}")
    )
    check(
        "top_customers returns n items",
        lambda: len(get_top(4)),
        lambda v: (v == 4, f"expected 4 items, got {v}")
    )

    # ── monthly_sales_trend ──────────────────────────────────────────────────
    def get_monthly():
        data = sol.load_data(CSV_PATH)
        return sol.monthly_sales_trend(data)

    check(
        "monthly trend has 7 months",
        lambda: len(get_monthly()),
        lambda v: (v == 7, f"expected 7 months (Jan–Jul 2023), got {v}")
    )
    check(
        "monthly keys are sorted",
        lambda: list(get_monthly().keys()),
        lambda v: (v == sorted(v), f"months not sorted: {v}")
    )
    # Jan 2023: 1299.99 + 79.98 + 89.97 + 449.99 = 1919.93
    jan = 1299.99 + 79.98 + 89.97 + 449.99
    check(
        "january 2023 revenue",
        lambda: get_monthly().get('2023-01', 0),
        lambda v: (approx_eq(v, jan), f"expected ~{jan:.2f}, got {v:.2f}")
    )

    # ── average_order_value ──────────────────────────────────────────────────
    # Total revenue / 25 rows
    total = elec + books + furn
    expected_avg = round(total / 25, 2)

    check(
        "average_order_value",
        lambda: sol.average_order_value(sol.load_data(CSV_PATH)),
        lambda v: (approx_eq(v, expected_avg), f"expected ~{expected_avg}, got {v}")
    )

    print(f"\nResults: {passed}/{passed + failed} tests passed")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
