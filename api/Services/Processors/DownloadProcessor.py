from threading import Thread, active_count

from Services.Db.DbService import *
from Services.Ftp.FtpConection import FtpConnection
from Utils.consts import CONSOLE_COLOR, PATHS, ERRORS


def download():
    dp = DownloadProcessor()
    dp.download_parallel()


def run_parallel(func, data):
    threads = []
    for data_row in data:
        thread = Thread(target=func, args=[data_row])
        thread.start()
        threads.append(thread)
        print(
            f'\n{CONSOLE_COLOR.SUCCESS}========== Active download threads {str(active_count())} =========='
            f'{CONSOLE_COLOR.NC}\n')
    for thread in threads:
        thread.join()


def rename_one(data_row):
    old_file_name = os.path.join(PATHS.TEMP_STORAGE, data_row[1], 'files', data_row[2])
    new_file_name = os.path.join(PATHS.TEMP_STORAGE, data_row[1], 'files', data_row[3])

    os.rename(old_file_name, new_file_name)

    print(f'File {old_file_name} renamed to {new_file_name}\n')


def create_folder(folder):
    local_folder = folder
    folder_path = os.path.join(PATHS.TEMP_STORAGE, local_folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f'Created folder {folder_path}\n')


def download_one(data_row):
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

        local_path = os.path.join(PATHS.TEMP_STORAGE, local, filename)
        create_folder(local)

        if os.path.exists(local_path):
            os.remove(local_path)

        ftp = FtpConnection(ip, login, password)
        ftp.download_file(remote, local_path)

    except Exception as ex:
        print(f'{CONSOLE_COLOR.ERROR}{ERRORS.DOWNLOAD_ERROR} {ex}{CONSOLE_COLOR.NC}\n')


class DownloadProcessor:
    def __init__(self):
        db = DbService()
        if os.path.exists(PATHS.TEMP_STORAGE):
            pass
        else:
            os.makedirs(PATHS.TEMP_STORAGE)
            print('The temporary storage directory was created\n')
        self.ftp_download_list = db.select('select_ftp_download.sql')
        self.rename_files_list = db.select('select_rename_files.sql')

    def download_parallel(self):
        run_parallel(download_one, self.ftp_download_list)

    def rename_parallel(self):
        run_parallel(rename_one, self.rename_files_list)
