import threading
import shutil
from Services.DbService import *
from Services.FtpConection import FtpConnection
from Services.Extracter import Extracter


def run_parallel(func, data):
    threads = []
    for data_row in data:
        thread = threading.Thread(
            target=func,
            args=[data_row]
        )
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()


class DownloadProcessor:
    def __init__(self):
        db = DbService()
        self.storage_path = 'D:\\Work\\MNK_PRICES\\DB_FILES'
        self.ftp_download_list = db.select('select_ftp_download.sql')
        self.archive_files_list = db.select('select_archive_extract.sql')
        self.rename_files_list = db.select('select_rename_files.sql')
        self.init_supplier_folders()

    def download_parallel(self):
        run_parallel(self.download_one, self.ftp_download_list)

    def download_one(self, data_row):
        try:
            ip = data_row[1]
            login = data_row[2]
            password = data_row[3]
            remote = data_row[4]
            local = data_row[5]
            filename = data_row[6]

            ftp = FtpConnection(ip, login, password)
            local_file = os.path.join(self.storage_path, local, filename)
            ftp.download_file(remote, local_file)

        except Exception as ex:
            print('Downloading file error')
            print(ex)

    def extract_parallel(self):
        run_parallel(self.extract_one, self.archive_files_list)

    def extract_one(self, data_row):
        archive_path = os.path.join(self.storage_path, data_row[1], 'archive', data_row[2])
        out_dir = os.path.join(self.storage_path, data_row[1], data_row[3])

        print('Extracting {} ...'.format(archive_path))
        try:
            Extracter.extract(archive=archive_path, outdir=out_dir)
        except Exception as ex:
            print('Extracting file error')
            print(ex)

    def rename_parallel(self):
        run_parallel(self.rename_one, self.rename_files_list)

    def rename_one(self, data_row):
        old_file_name = os.path.join(self.storage_path, data_row[1], 'files', data_row[2])
        new_file_name = os.path.join(self.storage_path, data_row[1], 'files', data_row[3])

        os.rename(old_file_name, new_file_name)

        print('file {}\trenamed to {}'.format(old_file_name, new_file_name))

    def init_supplier_folders(self):
        shutil.rmtree(self.storage_path)
        for row in self.ftp_download_list:
            local_folder = row[5]
            local_path = os.path.join(self.storage_path, local_folder)
            if not os.path.exists(local_path):
                os.makedirs(local_path)
                print('folder created {}'.format(local_path))

