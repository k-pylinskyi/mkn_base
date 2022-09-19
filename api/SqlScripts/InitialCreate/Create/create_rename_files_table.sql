CREATE TABLE IF NOT EXISTS rename_files(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER,
    old_file_name VARCHAR(50),
    new_file_name VARCHAR(50),
    FOREIGN KEY(file_id) REFERENCES ftp_download(id)
);