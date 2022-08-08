import ftplib


class FtpConnection:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.ftp = ftplib.FTP(host)
        self.ftp.login(username, password)
        self.ftp.dir()

    def upload_file(self, local_file, remote_file):
        with open(local_file, 'rb') as f:
            self.ftp.storbinary('STOR ' + remote_file, f)
        self.ftp.quit()

    def download_file(self, remote_file, local_file):
        with open(local_file, "wb") as f:
            self.ftp.retrbinary("RETR " + remote_file, f.write)
        self.ftp.quit()

    def get_file_list(self):
        self.ftp.dir()

    def quit(self):
        self.ftp.quit()