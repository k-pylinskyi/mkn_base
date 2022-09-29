import os
import zipfile

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
        new_filename_path = os.path.join(out_folder, new_filename)
        old_filename_path = os.path.join(out_folder, old_filename)
        with zipfile.ZipFile(archive_path,"r") as zip_ref:
            if not os.path.exists(out_folder):
                os.makedirs(out_folder)
            zip_ref.extractall(out_folder)
            Extractor.rename_file(new_filename_path, out_folder, old_filename, old_filename_path)
            print(f'{CONSOLE_COLOR.SUCCESS} {old_filename} was extracted to {new_filename_path}{CONSOLE_COLOR.NC}')
