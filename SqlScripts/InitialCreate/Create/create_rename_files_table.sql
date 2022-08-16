CREATE TABLE IF NOT EXISTS rename_files(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_folder VARCHAR(50),
    old_file_name VARCHAR(50),
    new_file_name VARCHAR(50)
);