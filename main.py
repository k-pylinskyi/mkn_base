from Services.DbService import DbService
from Services.DownloadProcessor import DownloadProcessor
from Services.QueryProcessor import QueryProcessor
from Services.FileConverter import FileConverter

if __name__ == '__main__':
    db = DbService()
    db.initial_create()

    dp = DownloadProcessor()
    dp.download_parallel()

    # qa = QueryProcessor('D:\\Work\\MNK_PRICES\\DB_FILES\\HART\\files')
    # qa.get_dataframe('')

    # fc = FileConverter()

    # fc.convert_all()
