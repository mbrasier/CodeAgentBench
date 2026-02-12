import csv
from typing import List, Dict


def load_data(filepath: str) -> List[Dict]:
    """Load sales_data.csv and return a list of row dicts.

    Numeric columns must be converted:
        quantity   → int
        unit_price → float

    All other columns remain as strings.

    Args:
        filepath: Absolute or relative path to the CSV file.

    Returns:
        List of dicts, one per CSV row.
    """
    raise NotImplementedError


def total_revenue_by_category(data: List[Dict]) -> Dict[str, float]:
    """Return total revenue (quantity * unit_price) grouped by category.

    Args:
        data: List of row dicts from load_data().

    Returns:
        Dict mapping category name → total revenue.
    """
    raise NotImplementedError


def top_customers(data: List[Dict], n: int) -> List[str]:
    """Return the IDs of the top n customers ranked by total spend (desc).

    Args:
        data: List of row dicts from load_data().
        n:    Number of customers to return.

    Returns:
        List of customer_id strings, highest spender first.
    """
    raise NotImplementedError


def monthly_sales_trend(data: List[Dict]) -> Dict[str, float]:
    """Return total revenue per calendar month, sorted by month ascending.

    Args:
        data: List of row dicts from load_data().

    Returns:
        Dict mapping "YYYY-MM" strings → total revenue, sorted by key.
    """
    raise NotImplementedError


def average_order_value(data: List[Dict]) -> float:
    """Return the mean revenue per order row, rounded to 2 decimal places.

    Args:
        data: List of row dicts from load_data().

    Returns:
        Average order value rounded to 2 dp, or 0.0 if data is empty.
    """
    raise NotImplementedError
