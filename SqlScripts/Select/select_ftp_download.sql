SELECT
ftp.id,
ftp.ftp_ip,
ftp.ftp_login,
ftp.ftp_password,
ftp.remote_file,
supplier.supplier_folder,
ftp.local_file_name,
rename.old_file_name,
rename.new_file_name
FROM (ftp_download as ftp
INNER JOIN suppliers as supplier
ON ftp.supplier_id = supplier.id)
LEFT JOIN rename_files as rename
ON ftp.id = rename.file_id