from Services.DbService import DbService
from Services.DownloadProcessor import DownloadProcessor


if __name__ == '__main__':
    db = DbService()
    db.initial_create()

    dp = DownloadProcessor()
    dp.download_parallel()
    dp.extract_parallel()
    dp.rename_parallel()

