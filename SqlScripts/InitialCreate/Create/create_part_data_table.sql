CREATE TABLE IF NOT EXISTS price_data(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_id INTEGER,
    number VARCHAR(50),
    supplier_number VARCHAR(60),
    manufacturer VARCHAR(50),
    quantity INTEGER,
    price NUMERIC,
    FOREIGN KEY(supplier_id) REFERENCES suppliers(id)
);