CREATE TABLE IF NOT EXISTS suppliers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50),
    group_id INTEGER,
    currency_id INTEGER,
    supplier_folder VARCHAR(100),
    FOREIGN KEY(group_id) REFERENCES suplier_groups(id),
    FOREIGN KEY(currency_id) REFERENCES currencies(id)
);