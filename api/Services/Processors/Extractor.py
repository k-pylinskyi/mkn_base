import os
import platform
import subprocess
import time

from api.Utils.consts import CONSOLE_COLOR, ERRORS


class Extractor:
    @staticmethod
    def rename_file(new_filename_path, out_folder, old_filename, old_filename_path):
        if os.path.exists(new_filename_path):
            os.remove(new_filename_path)

        for root, dirs, files in os.walk(out_folder):
            for file in files:
                if file.startswith(old_filename):
                    os.rename(old_filename_path, new_filename_path)
                    print(f'File renamed {old_filename_path} to {new_filename_path}\n')

        if os.path.exists(old_filename_path):
            os.remove(old_filename_path)

    @staticmethod
    def extract_one(archive_path, out_folder, old_filename, new_filename):
        old_filename_path = os.path.join(out_folder, old_filename)
        new_filename_path = os.path.join(out_folder, new_filename)

        if platform.system() == 'Windows':
            extractor = 'start ../7z/windows/7z.exe'
            try:
                os.system(f'cmd /c {extractor} e {archive_path} -o{out_folder} -y')
                time.sleep(3)
                Extractor.rename_file(new_filename_path, out_folder, old_filename, old_filename_path)
            except Exception as ex:
                print(f'{CONSOLE_COLOR.ERROR}{ERRORS.FILE_ERROR} {new_filename_path} {ex}{CONSOLE_COLOR.NC}\n')

        elif platform.system() == 'Darwin':
            extractor = '../7z/darwin/7zz'
            try:
                subprocess.run([extractor, "e", archive_path, f'-o{out_folder}', "-y"])
                time.sleep(3)
                Extractor.rename_file(new_filename_path, out_folder, old_filename, old_filename_path)
            except Exception as ex:
                print(f'{CONSOLE_COLOR.ERROR}{ERRORS.FILE_ERROR} {new_filename_path} {ex}{CONSOLE_COLOR.NC}\n')
        elif platform.system() == 'Linux':
            # TODO add linux extractor support
            # extractor = '7z/linux/7zz'
            try:
                print('Linux is currently unsupported')
            except Exception as ex:
                print(f'{CONSOLE_COLOR.ERROR}{ERRORS.FILE_ERROR} {new_filename_path} {ex}{CONSOLE_COLOR.NC}\n')
        else:
            print('Unsupported platform')
