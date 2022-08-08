from Services.DbService import *
from Services.FtpConection import FtpConnection

class DownloadProcessor:
    def __init__(self):
        db = DbService()
        self.storage_path = 'D:\\Work\\MNK_PRICES\\DB_FILES'
        self.ftp_download_list = db.select('select_ftp_download.sql')

    def download(self):
        self.create_suplier_folder()
        for row in self.ftp_download_list:
            ip = row[1]
            login = row[2]
            passw = row[3]
            remote = row[4]
            local = row[5]
            filename = row[6]

            ftp = FtpConnection(ip, login, passw)
            local_file = os.path.join(self.storage_path, local, filename)
            ftp.download_file(remote, local_file)
    def create_suplier_folder(self):
        for row in self.ftp_download_list:
            local_folder = row[5]
            local_path = os.path.join(self.storage_path, local_folder)
            if not os.path.exists(local_path):
                os.makedirs(local_path)
                print('created {}'.format(local_folder))
