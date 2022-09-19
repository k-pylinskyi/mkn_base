from api.Services.Db.DbService import DbService
from api.Services.Processors.DownloadProcessor import DownloadProcessor
from api.SupplierScripts.Hart.Hart import Hart
from api.Services.Processors.DataFrameReader import DataFrameReader

if __name__ == '__main__':
    db = DbService()
    db.initial_create()

    #dp = DownloadProcessor()
    #dp.download_parallel()

    hart = Hart()
    hart_df = hart.process()
    DataFrameReader.dataframe_to_db('Hart', hart_df)

    # qa = QueryProcessor('D:\\Work\\MNK_PRICES\\DB_FILES\\Hart\\files')
    # qa.get_dataframe('')

    # fc = FileConverter()

    # fc.convert_all()
