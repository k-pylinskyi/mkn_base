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
        self.rename_files_list = db.select('select_rename_files.sql')

    def download_parallel(self):
        run_parallel(self.download_one, self.ftp_download_list)

    def download_one(self, data_row):
        try:
            ip = data_row[1]
            login = data_row[2]
            password = data_row[3]
            remote = data_row[4]
            supplier_folder = data_row[5]
            filename = data_row[6]
            old_filename = data_row[7]
            new_filename = data_row[8]
            local = supplier_folder

            if filename.lower().endswith(('.zip', '.gz', '.rar', '.7z')):
                local = os.path.join(local, 'archive')
            else:
                local = os.path.join(local, 'files')

            local_path = os.path.join(self.storage_path, local, filename)
            self.create_folder(local)

            if os.path.exists(local_path):
                os.remove(local_path)

            ftp = FtpConnection(ip, login, password)
            ftp.download_file(remote, local_path)

            if local_path.lower().endswith(('.zip', '.gz', '.rar', '.7z')):
                self.extract_one(filename, supplier_folder, old_filename, new_filename)

        except Exception as ex:
            print('Downloading file error')
            print(ex)

    def extract_one(self, archive, supplier_folder, old_filename, new_filename):
        archive_path = os.path.join(self.storage_path, supplier_folder, 'archive', archive)
        out_dir = os.path.join(self.storage_path, supplier_folder, 'files')

        print('Extracting {} ...'.format(archive_path))
        try:
            Extracter.extract_one(archive_path, out_dir, old_filename, new_filename)
        except Exception as ex:
            print('Extracting file error\n{}'.format(ex))

    def rename_parallel(self):
        run_parallel(self.rename_one, self.rename_files_list)

    def rename_one(self, data_row):
        old_file_name = os.path.join(self.storage_path, data_row[1], 'files', data_row[2])
        new_file_name = os.path.join(self.storage_path, data_row[1], 'files', data_row[3])

        os.rename(old_file_name, new_file_name)

        print('file {}\trenamed to {}'.format(old_file_name, new_file_name))

    def create_folder(self, folder):
        local_folder = folder
        folder_path = os.path.join(self.storage_path, local_folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print('folder created {}'.format(folder_path))

