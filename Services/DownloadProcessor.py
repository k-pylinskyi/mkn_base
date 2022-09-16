from threading import Thread, active_count

from Services.DbService import *
from Services.Extractor import Extractor
from Services.FtpConection import FtpConnection
from utils.consts import CONSOLE_COLOR, PATHS, ERRORS


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


def extract_one(archive, supplier_folder, old_filename, new_filename):
    archive_path = os.path.join(PATHS.TEMP_STORAGE, supplier_folder, 'archive', archive)
    out_dir = os.path.join(PATHS.TEMP_STORAGE, supplier_folder, 'files')

    print(f'Extracting {archive_path} ...\n')
    try:
        Extractor.extract_one(archive_path, out_dir, old_filename, new_filename)
        # Extractor.rename_file(archive_path, out_dir, old_filename, new_filename)
    except Exception as ex:
        print(f'{CONSOLE_COLOR.ERROR}{ERRORS.EXTRACTION_ERROR} {ex}{CONSOLE_COLOR.NC}')


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

        if local_path.lower().endswith(('.zip', '.gz', '.rar', '.7z')):
            extract_one(filename, supplier_folder, old_filename, new_filename)

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
