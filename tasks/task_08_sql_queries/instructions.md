# Task 08: SQL Analytics Queries

Write SQL queries in `queries.sql` to answer five analytical questions about an e-commerce database.

## Schema

```sql
customers  (id INTEGER, name TEXT, email TEXT, joined_date TEXT)
products   (id INTEGER, name TEXT, category TEXT, price REAL)
orders     (id INTEGER, customer_id INTEGER, order_date TEXT, status TEXT)
order_items(order_id INTEGER, product_id INTEGER, quantity INTEGER, unit_price REAL)
```

`order_date` and `joined_date` are in `"YYYY-MM-DD"` format.
Revenue for a line item = `quantity × unit_price`.

## Queries to write

Edit `queries.sql`.  Each query is delimited by a `-- QUERY_N:` comment and must end with a semicolon.  Do not change the delimiters.

### Query 1 — Top 5 customers by lifetime value
Return `name` and `total_spent` (sum of all their line-item revenues), ordered by `total_spent` descending, limited to 5 rows.  Only include customers who have at least one order.

### Query 2 — Monthly revenue
Return `month` (formatted as `"YYYY-MM"`) and `revenue` (total for that month), for **all** months that have orders, ordered by `month` ascending.

### Query 3 — Top 3 products by units sold
Return `name` and `total_quantity` (sum of quantities across all order items), ordered by `total_quantity` descending, limited to 3 rows.

### Query 4 — Customers with no orders
Return the `name` of every customer who has never placed an order, ordered by `name` ascending.

### Query 5 — Average order value by category
Return `category` and `avg_order_value` (average revenue per order that contains at least one item from that category), ordered by `avg_order_value` descending.
`avg_order_value` should be rounded to 2 decimal places.

## Files

- **`schema.sql`** — reference schema (read-only, used by the evaluator to create the DB).
- **`queries.sql`** — **write your queries here**.
