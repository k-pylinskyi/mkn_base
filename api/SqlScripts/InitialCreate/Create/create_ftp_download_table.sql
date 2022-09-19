CREATE TABLE IF NOT EXISTS ftp_download(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ftp_ip VARCHAR(50),
    ftp_login VARCHAR(50),
    ftp_password VARCHAR(50),
    remote_file VARCHAR(100),
    supplier_id INTEGER,
    local_file_name VARCHAR(50),
    FOREIGN KEY(supplier_id) REFERENCES suppliers(id)
);