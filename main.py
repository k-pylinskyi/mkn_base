from Services.Db.DbService import DbService
from Services.Processors.DownloadProcessor import DownloadProcessor
from SupplierScripts.Hart.Hart import Hart as hart


if __name__ == '__main__':
    db = DbService()
    db.initial_create()

    dp = DownloadProcessor()
    dp.download_parallel()

    hart = hart()
    hart.process()

    # qa = QueryProcessor('D:\\Work\\MNK_PRICES\\DB_FILES\\Hart\\files')
    # qa.get_dataframe('')

    # fc = FileConverter()

    # fc.convert_all()
