from services.DbService import DbService
from services.DownloadProcessor import DownloadProcessor
from services.QueryProcessor import QueryProcessor
from services.FileConverter import FileConverter

if __name__ == '__main__':
    db = DbService()
    db.initial_create()

    dp = DownloadProcessor()
    dp.download_parallel()

    # qa = QueryProcessor('D:\\Work\\MNK_PRICES\\DB_FILES\\Hart\\files')
    # qa.get_dataframe('')

    # fc = FileConverter()

    # fc.convert_all()
