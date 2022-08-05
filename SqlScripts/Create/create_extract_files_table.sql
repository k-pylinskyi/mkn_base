CREATE TABLE IF NOT EXISTS archive_files(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    archive_path VARCHAR(100),
    extract_folder VARCHAR(100),
    archive_type VARCHAR(20)
);