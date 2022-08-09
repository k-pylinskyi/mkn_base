CREATE TABLE IF NOT EXISTS archive_extract(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_folder VARCHAR(100),
    archive_file VARCHAR(100),
    extract_folder VARCHAR(100)
);