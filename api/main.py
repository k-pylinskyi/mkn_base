from api.Services.Db.DbService import DbService
from api.Services.Processors.DownloadProcessor import DownloadProcessor
from api.SupplierScripts.Hart.Hart import Hart
from api.SupplierScripts.Gordon.Gordon import Gordon
from api.Services.Processors.DataFrameReader import DataFrameReader

if __name__ == '__main__':
    #db = DbService()
    #db.initial_create()

    #dp = DownloadProcessor()
    #dp.download_parallel()

    Gordon = Gordon()
    gordon_df = Gordon.process()
    print(gordon_df.head())
    DataFrameReader.dataframe_to_db('Gordon', gordon_df)

    # qa = QueryProcessor('D:\\Work\\MNK_PRICES\\DB_FILES\\Hart\\files')
    # qa.get_dataframe('')

    # fc = FileConverter()

    # fc.convert_all()
