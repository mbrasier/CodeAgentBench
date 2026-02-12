#!/usr/bin/env python3
"""
Evaluator for Task 08: SQL Analytics Queries.

Creates an in-memory SQLite database, populates it with test data,
parses each labelled query from queries.sql, runs it, and checks results.
"""
import sys
import os
import re
import sqlite3

TASK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '..', '..', 'tasks', 'task_08_sql_queries')
QUERIES_FILE = os.path.join(TASK_DIR, 'queries.sql')

passed = failed = 0

# ── Test data ─────────────────────────────────────────────────────────────────
SEED_SQL = """
INSERT INTO customers VALUES
  (1,'Alice','alice@example.com','2022-01-01'),
  (2,'Bob','bob@example.com','2022-02-15'),
  (3,'Carol','carol@example.com','2022-03-10'),
  (4,'Dave','dave@example.com','2022-04-20'),
  (5,'Eve','eve@example.com','2022-05-05'),
  (6,'Frank','frank@example.com','2022-06-01');

INSERT INTO products VALUES
  (1,'Laptop','Electronics',999.99),
  (2,'Phone','Electronics',599.99),
  (3,'Novel','Books',14.99),
  (4,'Cookbook','Books',24.99),
  (5,'Headphones','Electronics',149.99),
  (6,'Desk Chair','Furniture',299.99);

INSERT INTO orders VALUES
  (1,1,'2023-01-10','completed'),
  (2,2,'2023-01-20','completed'),
  (3,1,'2023-02-05','completed'),
  (4,3,'2023-02-15','completed'),
  (5,2,'2023-03-10','completed'),
  (6,4,'2023-03-20','completed'),
  (7,5,'2023-04-01','completed'),
  (8,1,'2023-04-15','completed');

INSERT INTO order_items VALUES
  (1,1,1,999.99),
  (2,2,2,599.99),
  (3,5,1,149.99),
  (4,3,3,14.99),
  (5,1,1,999.99),
  (6,4,2,24.99),
  (7,2,1,599.99),
  (8,6,1,299.99);
"""
# Revenue per order:
# Order 1 → 999.99  (Alice, Electronics)
# Order 2 → 2*599.99 = 1199.98  (Bob, Electronics)   ← qty=2 for phone
# Order 3 → 149.99  (Alice, Electronics)
# Order 4 → 3*14.99 = 44.97  (Carol, Books)           ← qty=3 for novel
# Order 5 → 999.99  (Bob, Electronics)
# Order 6 → 2*24.99 = 49.98  (Dave, Books)            ← qty=2 for cookbook
# Order 7 → 599.99  (Eve, Electronics)
# Order 8 → 299.99  (Alice, Furniture)
#
# Customer totals:
#   Alice: 999.99 + 149.99 + 299.99 = 1449.97
#   Bob:   1199.98 + 999.99         = 2199.97
#   Carol: 44.97
#   Dave:  49.98
#   Eve:   599.99
#   Frank: (no orders)
#
# Monthly:
#   2023-01: 999.99 + 1199.98 = 2199.97
#   2023-02: 149.99 + 44.97   = 194.96
#   2023-03: 999.99 + 49.98   = 1049.97
#   2023-04: 599.99 + 299.99  = 899.98


def build_db():
    con = sqlite3.connect(':memory:')
    con.row_factory = sqlite3.Row
    con.executescript("""
        CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, email TEXT, joined_date TEXT);
        CREATE TABLE products  (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL);
        CREATE TABLE orders    (id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT);
        CREATE TABLE order_items (order_id INTEGER, product_id INTEGER, quantity INTEGER, unit_price REAL,
                                  PRIMARY KEY(order_id, product_id));
    """)
    con.executescript(SEED_SQL)
    return con


def parse_queries(path):
    """Return dict {1: sql_text, 2: sql_text, ...} from the labelled file."""
    if not os.path.exists(path):
        return {}
    text = open(path).read()
    queries = {}
    pattern = re.compile(
        r'--\s*QUERY_(\d+).*?\n(.*?)--\s*END_QUERY_\1',
        re.DOTALL | re.IGNORECASE
    )
    for m in pattern.finditer(text):
        n = int(m.group(1))
        sql = m.group(2).strip()
        # Strip comment lines, keep only non-empty SQL
        lines = [l for l in sql.splitlines()
                 if l.strip() and not l.strip().startswith('--')]
        queries[n] = '\n'.join(lines)
    return queries


def run_query(con, sql):
    try:
        cur = con.execute(sql)
        return cur.fetchall(), None
    except Exception as e:
        return None, str(e)


def check(name, rows, err, validator):
    global passed, failed
    if err:
        print(f"[FAIL] {name}: SQL error: {err}")
        failed += 1
        return
    if rows is None:
        print(f"[FAIL] {name}: query not found or empty")
        failed += 1
        return
    ok, msg = validator(rows)
    if ok:
        print(f"[PASS] {name}")
        passed += 1
    else:
        print(f"[FAIL] {name}: {msg}")
        failed += 1


def main():
    if not os.path.exists(QUERIES_FILE):
        print("[FAIL] queries.sql not found")
        sys.exit(1)

    queries = parse_queries(QUERIES_FILE)
    con = build_db()

    def q(n):
        sql = queries.get(n, '')
        if not sql:
            return None, f"Query {n} is empty or missing"
        return run_query(con, sql)

    # ── Query 1: Top 5 customers by lifetime value ───────────────────────────
    rows, err = q(1)
    check(
        "Q1 top 5 customers by lifetime value",
        rows, err,
        lambda rows: (
            len(rows) >= 1
            and rows[0][0] == 'Bob'
            and abs(rows[0][1] - 2199.97) < 0.02
            and (len(rows) < 2 or rows[1][0] == 'Alice'),
            f"expected Bob first (2199.97), got {[(r[0], r[1]) for r in rows[:3]]}"
        )
    )

    # ── Query 2: Monthly revenue ─────────────────────────────────────────────
    rows, err = q(2)
    check(
        "Q2 monthly revenue row count",
        rows, err,
        lambda rows: (len(rows) == 4, f"expected 4 months, got {len(rows)}")
    )
    check(
        "Q2 first month is 2023-01",
        rows, err,
        lambda rows: (rows[0][0] == '2023-01', f"expected '2023-01', got {rows[0][0] if rows else 'N/A'}")
    )
    check(
        "Q2 Jan revenue",
        rows, err,
        lambda rows: (abs(rows[0][1] - 2199.97) < 0.02,
                      f"expected Jan revenue ~2199.97, got {rows[0][1] if rows else 'N/A'}")
    )

    # ── Query 3: Top 3 products by units sold ────────────────────────────────
    # Phone qty=2+1=3, Novel qty=3, Laptop qty=1+1=2  →  Phone/Novel tied at 3, then Laptop at 2
    rows, err = q(3)
    check(
        "Q3 returns 3 rows",
        rows, err,
        lambda rows: (len(rows) == 3, f"expected 3 rows, got {len(rows)}")
    )
    check(
        "Q3 top products are Phone and Novel (3 units each) and Laptop",
        rows, err,
        lambda rows: (
            {rows[0][0], rows[1][0]} == {'Phone', 'Novel'} and rows[2][0] == 'Laptop',
            f"unexpected order: {[r[0] for r in rows]}"
        )
    )

    # ── Query 4: Customers with no orders ────────────────────────────────────
    rows, err = q(4)
    check(
        "Q4 finds Frank (no orders)",
        rows, err,
        lambda rows: (len(rows) == 1 and rows[0][0] == 'Frank',
                      f"expected [Frank], got {[r[0] for r in rows]}")
    )

    # ── Query 5: Avg order value by category ─────────────────────────────────
    # Electronics orders: 1(999.99), 2(1199.98), 3(149.99), 5(999.99), 7(599.99)
    #   avg = (999.99+1199.98+149.99+999.99+599.99)/5 = 3949.94/5 = 789.99
    # Books orders: 4(44.97), 6(49.98)
    #   avg = (44.97+49.98)/2 = 47.475 → 47.48
    # Furniture orders: 8(299.99)
    #   avg = 299.99
    rows, err = q(5)
    check(
        "Q5 returns 3 categories",
        rows, err,
        lambda rows: (len(rows) == 3, f"expected 3 categories, got {len(rows)}")
    )
    check(
        "Q5 electronics avg ~789.99",
        rows, err,
        lambda rows: (
            any(r[0] == 'Electronics' and abs(r[1] - 789.99) < 0.02 for r in rows),
            f"Electronics avg should be ~789.99, got {[(r[0], r[1]) for r in rows]}"
        )
    )

    print(f"\nResults: {passed}/{passed + failed} tests passed")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
