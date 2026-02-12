# Task 12: Multi-Bug System Debug

The file `order_system.py` contains three classes that model a simple trading system.
The module has **known defects** — behaviour does not match the specification below.
Your task is to find and fix all the bugs.

There are no hint comments in the code. Read the specification carefully and compare
it with the implementation to locate each defect.

## Class Specifications

### `Order(symbol, price, quantity)`
Represents a single buy order.

- `self.symbol` — the ticker string (e.g. `"AAPL"`)
- `self.price` — the price as a **float** (e.g. `150.0`)
- `self.quantity` — the integer quantity

### `OrderBook`
Maintains a list of `Order` objects and answers queries about them.

- `add_order(order)` — appends the order to the internal list
- `best_bid() -> float` — returns the **highest** price among all orders; raises
  `ValueError` if the book is empty

### `Portfolio`
Tracks a set of positions (symbol → quantity mapping) and calculates their value
using an `OrderBook`.

- `add_position(symbol, quantity)` — records that the portfolio holds `quantity`
  units of `symbol`
- `total_value(order_book) -> float` — iterates over **all** symbols in the portfolio,
  looks up the best bid price for that symbol's orders in `order_book`, and sums
  `price * quantity` for every position

## Expected Behaviour Examples

```python
o = Order("AAPL", 150.0, 10)
assert o.price * 2 == 300.0          # price must be a float

book = OrderBook()
book.add_order(Order("X", 10.0, 1))
book.add_order(Order("X", 15.0, 1))
book.add_order(Order("X", 12.0, 1))
assert book.best_bid() == 15.0       # highest price, not lowest

portfolio = Portfolio()
portfolio.add_position("A", 5)
portfolio.add_position("B", 3)
book2 = OrderBook()
book2.add_order(Order("A", 10.0, 1))
book2.add_order(Order("B", 20.0, 1))
assert portfolio.total_value(book2) == 110.0   # 5*10 + 3*20, both positions counted
```
