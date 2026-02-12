# Task 07: CSV Data Analysis (Python)

Implement data analysis functions in `processor.py` that operate on the provided `sales_data.csv`.

## CSV Schema

```
order_id, customer_id, product, category, quantity, unit_price, order_date
```

- `order_id`: unique integer per row
- `customer_id`: string like `"C001"`
- `product`: product name string
- `category`: one of `"Electronics"`, `"Books"`, `"Furniture"`
- `quantity`: integer units purchased
- `unit_price`: float price per unit
- `order_date`: string in `"YYYY-MM-DD"` format

**Revenue for a row** = `quantity × unit_price`

## What to implement

### `load_data(filepath: str) -> list[dict]`
Load the CSV and return a list of dicts.  Numeric columns (`quantity`, `unit_price`) must be converted to appropriate types (`int` and `float`).

### `total_revenue_by_category(data: list) -> dict`
Return a dict mapping each category name to its total revenue (sum of `quantity × unit_price` across all rows in that category).

### `top_customers(data: list, n: int) -> list`
Return a list of the top `n` customer IDs sorted by their total spend (descending).
If two customers have equal spend, order is unspecified.

### `monthly_sales_trend(data: list) -> dict`
Return a dict mapping `"YYYY-MM"` strings to the total revenue for that month, sorted by key ascending.

### `average_order_value(data: list) -> float`
Return the mean revenue per order (row), rounded to 2 decimal places.

## File to modify

**`processor.py`** — implement all five functions.
Use only the Python standard library (`csv`, `collections`, etc.) — no third-party packages.
