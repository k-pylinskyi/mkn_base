CREATE TABLE IF NOT EXISTS price_data(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_id INTEGER,
    supplier_part_number VARCHAR(60),
    part_number VARCHAR(50),
    manufacturer VARCHAR(50),
    part_name VARCHAR(100),
    quantity INTEGER,
    mnk_price NUMERIC,
    FOREIGN KEY(supplier_id) REFERENCES suppliers(id)
);