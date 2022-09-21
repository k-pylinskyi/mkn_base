from api.Services.Processors.DataFrameReader import DataFrameReader
from api.SupplierScripts.Emoto.Emoto import process_emoto
from api.SupplierScripts.Gordon.Gordon import Gordon
from api.SupplierScripts.AutopartnerGdansk.AutopartnerGdansk import process_autopartner_gdansk

if __name__ == '__main__':
    # db = DbService()
    # db.initial_create()

    # dp = DownloadProcessor()
    # dp.download_parallel()

    DataFrameReader.dataframe_to_db('autopartner_gdansk', process_autopartner_gdansk())
    DataFrameReader.dataframe_to_db('emoto', process_emoto())
    print(process_autopartner_gdansk())
    print(process_emoto())

    # Gordon = Gordon()
    # gordon_df = Gordon.process()
    # print(gordon_df.head())
    # DataFrameReader.dataframe_to_db('Gordon', gordon_df)

    # qa = QueryProcessor('D:\\Work\\MNK_PRICES\\DB_FILES\\Hart\\files')
    # qa.get_dataframe('')

    # fc = FileConverter()

    # fc.convert_all()
