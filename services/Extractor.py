import gzip
import os
import shutil
import zipfile


class Extractor:
    @staticmethod
    def extract_one(archive_path, out_folder, old_filename, new_filename):
        old_filename_path = os.path.join(out_folder, old_filename)
        new_filename_path = os.path.join(out_folder, new_filename)

        try:
            if archive_path.lower().endswith('.zip'):

                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(out_folder)

                if os.path.exists(new_filename_path):
                    os.remove(new_filename_path)

                for root, dirs, files in os.walk(out_folder):
                    for file in files:
                        if file.startswith(old_filename):
                            os.rename(old_filename_path, new_filename_path)
                            print('File renamed\n{}\n{}'.format(old_filename_path, new_filename_path))

                if os.path.exists(old_filename_path):
                    os.remove(old_filename_path)

                print('File extracted\t{}'.format(new_filename_path))

            elif archive_path.lower().endswith('.gz'):
                with gzip.open(archive_path, 'rb') as file_in:
                    with open(new_filename_path, 'wb') as file_out:
                        shutil.copyfileobj(file_in, file_out)
                print('extracted\n{}'.format(new_filename_path))

        except Exception as ex:
            print('Error on file\t{}\n{}'.format(new_filename_path, ex))
