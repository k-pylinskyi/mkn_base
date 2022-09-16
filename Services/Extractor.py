import os
import platform
import subprocess

import pysnooper

from utils.consts import CONSOLE_COLOR, ERRORS, DEBUG


class Extractor:
    @staticmethod
    def extract_one(archive_path, out_folder, old_filename, new_filename):
        old_filename_path = os.path.join(out_folder, old_filename)
        new_filename_path = os.path.join(out_folder, new_filename)

        if platform.system() == 'Windows':
            extractor = 'start 7z/windows/7z.exe /B'
            try:
                os.system(f'cmd /c {extractor} e {archive_path} -o{out_folder} -y')
            except Exception as ex:
                print(f'{CONSOLE_COLOR.ERROR}{ERRORS.FILE_ERROR} {new_filename_path} {ex}{CONSOLE_COLOR.NC}\n')
        elif platform.system() == 'Darwin':
            extractor = '7z/darwin/7zz'
            if DEBUG:
                with pysnooper.snoop():
                    try:
                        subprocess.run([extractor, "e", archive_path, f'-o{out_folder}', "-y"])
                    except Exception as ex:
                        print(f'{CONSOLE_COLOR.ERROR}{ERRORS.FILE_ERROR} {new_filename_path} {ex}{CONSOLE_COLOR.NC}\n')
            else:
                try:
                    subprocess.run([extractor, "e", archive_path, f'-o{out_folder}', "-y"])
                except Exception as ex:
                    print(f'{CONSOLE_COLOR.ERROR}{ERRORS.FILE_ERROR} {new_filename_path} {ex}{CONSOLE_COLOR.NC}\n')
        else:
            extractor = '7z/linux/7zz'
            try:
                # TODO add linux extractor support
                print('Linux is currently unsupported')
            except Exception as ex:
                print(f'{CONSOLE_COLOR.ERROR}{ERRORS.FILE_ERROR} {new_filename_path} {ex}{CONSOLE_COLOR.NC}\n')

        # if platform.system() == 'Windows':
        #     extractor = 'start 7z/windows/7z.exe'
        # elif platform.system() == 'Darwin':
        #     extractor = '7z/darwin/7zz'
        # else:
        #     extractor = '7z/linux/7zz'
        #
        # try:
        #     subprocess.run([extractor, archive_path])
        # except Exception as ex:
        #     print(f'{CONSOLE_COLOR.ERROR}{ERRORS.FILE_ERROR} {new_filename_path} {ex}{CONSOLE_COLOR.NC}\n')
        #
        # try:
        #     if archive_path.lower().endswith('.zip'):
        #
        #         with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        #             zip_ref.extractall(out_folder)
        #
        #         if os.path.exists(new_filename_path):
        #             os.remove(new_filename_path)
        #
        #         for root, dirs, files in os.walk(out_folder):
        #             for file in files:
        #                 if file.startswith(old_filename):
        #                     os.rename(old_filename_path, new_filename_path)
        #                     print(f'File renamed {old_filename_path} to {new_filename_path}\n')
        #
        #         if os.path.exists(old_filename_path):
        #             os.remove(old_filename_path)
        #
        #         print(f'ZIP file extracted {new_filename_path}\n')
        #
        #     elif archive_path.lower().endswith('.gz'):
        #         with gzip.open(archive_path, 'rb') as file_in:
        #             with open(new_filename_path, 'wb') as file_out:
        #                 shutil.copyfileobj(file_in, file_out)
        #         print(f'GZ file extracted {new_filename_path}\n')
        #
        # except Exception as ex:
        #     print(f'{CONSOLE_COLOR.ERROR}{ERRORS.FILE_ERROR} {new_filename_path} {ex}{CONSOLE_COLOR.NC}\n')
