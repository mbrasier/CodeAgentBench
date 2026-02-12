#!/usr/bin/env python3
"""Evaluator for Task 12: Multi-Bug System Debug"""
import sys
import os
import importlib.util

TASK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '..', '..', 'tasks', 'task_12_multi_bug_system')


def load_solution():
    path = os.path.join(TASK_DIR, 'order_system.py')
    if not os.path.exists(path):
        print("[FAIL] order_system.py not found")
        sys.exit(1)
    spec = importlib.util.spec_from_file_location("order_system", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


passed = failed = 0


def check(name, fn, expected):
    global passed, failed
    try:
        got = fn()
        if got == expected:
            print(f"[PASS] {name}")
            passed += 1
        else:
            print(f"[FAIL] {name}: expected {expected!r}, got {got!r}")
            failed += 1
    except Exception as e:
        print(f"[FAIL] {name}: {type(e).__name__}: {e}")
        failed += 1


def check_raises(name, fn, exc_type):
    """Pass if fn() raises exc_type, fail otherwise."""
    global passed, failed
    try:
        fn()
        print(f"[FAIL] {name}: expected {exc_type.__name__}, got no exception")
        failed += 1
    except exc_type:
        print(f"[PASS] {name}")
        passed += 1
    except Exception as e:
        print(f"[FAIL] {name}: expected {exc_type.__name__}, got {type(e).__name__}: {e}")
        failed += 1


def main():
    sol = load_solution()
    Order = sol.Order
    OrderBook = sol.OrderBook
    Portfolio = sol.Portfolio

    # -- Order.price type (Bug 1: price stored as str instead of float) -------
    check("Order.price is float",
          lambda: type(Order("AAPL", 150.0, 10).price),
          float)
    check("Order.price arithmetic",
          lambda: Order("AAPL", 150.0, 10).price * 2,
          300.0)

    # -- OrderBook.best_bid returns MAX not min (Bug 2) -----------------------
    def make_book_bids():
        book = OrderBook()
        book.add_order(Order("X", 10.0, 1))
        book.add_order(Order("X", 15.0, 1))
        book.add_order(Order("X", 12.0, 1))
        return book

    check("best_bid returns highest price",
          lambda: make_book_bids().best_bid(),
          15.0)
    check("best_bid with single order",
          lambda: (lambda b: b.best_bid())(
              (lambda b: (b.add_order(Order("Y", 42.0, 1)), b)[1])(OrderBook())
          ),
          42.0)
    check_raises("best_bid empty book raises ValueError",
                 lambda: OrderBook().best_bid(),
                 ValueError)

    # -- Portfolio.total_value includes ALL symbols (Bug 3) -------------------
    def make_portfolio_two():
        portfolio = Portfolio()
        portfolio.add_position("A", 5)
        portfolio.add_position("B", 3)
        book = OrderBook()
        book.add_order(Order("A", 10.0, 1))
        book.add_order(Order("B", 20.0, 1))
        return portfolio.total_value(book)

    check("total_value includes all positions",
          make_portfolio_two,
          110.0)  # 5*10 + 3*20

    def make_portfolio_one():
        portfolio = Portfolio()
        portfolio.add_position("Z", 7)
        book = OrderBook()
        book.add_order(Order("Z", 8.0, 1))
        return portfolio.total_value(book)

    check("total_value single position",
          make_portfolio_one,
          56.0)  # 7*8

    # -- Integration test: all three bugs must be fixed -----------------------
    def integration():
        book = OrderBook()
        book.add_order(Order("AAPL", 150.0, 10))
        book.add_order(Order("AAPL", 155.0, 5))
        book.add_order(Order("GOOG", 2800.0, 2))
        book.add_order(Order("GOOG", 2750.0, 3))

        portfolio = Portfolio()
        portfolio.add_position("AAPL", 10)
        portfolio.add_position("GOOG", 2)

        bid = book.best_bid()               # max of all: 2800.0
        value = portfolio.total_value(book)  # 10*155 + 2*2800 = 1550 + 5600 = 7150
        return (bid, value)

    check("integration best_bid and total_value",
          integration,
          (2800.0, 7150.0))

    print(f"\nResults: {passed}/{passed + failed} tests passed")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
