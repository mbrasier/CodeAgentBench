-- E-commerce database schema (reference — used by the evaluator)

CREATE TABLE customers (
    id          INTEGER PRIMARY KEY,
    name        TEXT    NOT NULL,
    email       TEXT    NOT NULL,
    joined_date TEXT    NOT NULL   -- YYYY-MM-DD
);

CREATE TABLE products (
    id       INTEGER PRIMARY KEY,
    name     TEXT    NOT NULL,
    category TEXT    NOT NULL,
    price    REAL    NOT NULL
);

CREATE TABLE orders (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    order_date  TEXT    NOT NULL,   -- YYYY-MM-DD
    status      TEXT    NOT NULL
);

CREATE TABLE order_items (
    order_id   INTEGER NOT NULL REFERENCES orders(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity   INTEGER NOT NULL,
    unit_price REAL    NOT NULL,
    PRIMARY KEY (order_id, product_id)
);
