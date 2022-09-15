CREATE TABLE IF NOT EXISTS ftp_uploads(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ftp_ip VARCHAR(50),
    ftp_login VARCHAR(50),
    ftp_password VARCHAR(50),
    remote_file VARCHAR(100),
    local_file VARCHAR(100),
    upload BOOLEAN
);