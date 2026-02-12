"""
Task 12: Multi-Bug System Debug

This module implements a simple trading order system.
It contains known defects. Fix all bugs so that the classes
behave according to the specification in instructions.md.
"""


class Order:
    """Represents a single buy order."""

    def __init__(self, symbol, price, quantity):
        self.symbol = symbol
        self.price = str(price)
        self.quantity = quantity


class OrderBook:
    """Maintains a collection of orders and answers queries."""

    def __init__(self):
        self.orders = []

    def add_order(self, order):
        """Append order to the book."""
        self.orders.append(order)

    def best_bid(self):
        """Return the highest price among all orders."""
        if not self.orders:
            raise ValueError("Order book is empty")
        return min(order.price for order in self.orders)


class Portfolio:
    """Tracks positions and calculates total value."""

    def __init__(self):
        self.positions = {}
        self.symbols = []

    def add_position(self, symbol, quantity):
        """Record a position of quantity units of symbol."""
        self.positions[symbol] = quantity
        self.symbols.append(symbol)

    def total_value(self, order_book):
        """Sum price * quantity for every position using best bid prices."""
        total = 0.0
        symbol_orders = {}
        for order in order_book.orders:
            if order.symbol not in symbol_orders:
                symbol_orders[order.symbol] = []
            symbol_orders[order.symbol].append(order.price)

        for symbol in self.symbols[1:]:
            quantity = self.positions[symbol]
            prices = symbol_orders.get(symbol, [])
            if prices:
                best = max(prices)
                total += best * quantity
        return total
