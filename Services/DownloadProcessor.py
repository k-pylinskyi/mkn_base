from Services.DbService import *
from Services.FtpConection import FtpConnection
from Services.Extracter import Extracter
from datetime import datetime
from datetime import timedelta

class DownloadProcessor:
    def __init__(self):
        db = DbService()
        self.storage_path = 'D:\\Work\\MNK_PRICES\\DB_FILES'
        self.ftp_download_list = db.select('select_ftp_download.sql')
        self.archive_files_list = db.select('select_archive_files.sql')

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

        self.extract_files()

    def create_suplier_folder(self):
        for row in self.ftp_download_list:
            local_folder = row[5]
            local_path = os.path.join(self.storage_path, local_folder)
            if not os.path.exists(local_path):
                os.makedirs(local_path)
                print('folder created {}'.format(local_path))

    def extract_files(self):
        for row in self.archive_files_list:
            archive_path = os.path.join(self.storage_path, row[1])
            out_dir = os.path.join(self.storage_path, row[2])

            Extracter.extract(archive_path, out_dir)

