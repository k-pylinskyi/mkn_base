CREATE TABLE IF NOT EXISTS price_data(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    suplier_id INTEGER,
    number VARCHAR(50),
    suplier_number VARCHAR(60),
    manufacturer VARCHAR(50),
    quantity INTEGER,
    price NUMERIC,
    FOREIGN KEY(suplier_id) REFERENCES supliers(id)
);