from api.Services.Db import DbService
from api.Services.Processors import DownloadProcessor
from api.Services.Processors.DataFrameReader import DataFrameReader
from api.SupplierScripts.Emoto.Emoto import process_emoto
from api.SupplierScripts.Gordon.Gordon import Gordon
from api.SupplierScripts.AutopartnerGdansk.AutopartnerGdansk import process_autopartner_gdansk
from api.SupplierScripts.Paketo.Packeto import process_paketo
from api.SupplierScripts.Motorol.Motorol import get_queried_data

if __name__ == '__main__':
    #DbService.connect()
    #DownloadProcessor.download()


    # DataFrameReader.dataframe_to_db('autopartner_gdansk', process_autopartner_gdansk())
    # DataFrameReader.dataframe_to_db('emoto', process_emoto())
    # DataFrameReader.dataframe_to_db('paketo', process_paketo())
    # print(process_autopartner_gdansk())
    # print(process_emoto())
    # print(process_paketo())
    # DataFrameReader.dataframe_to_db('gordon', Gordon.get_queried_data())
    # print(Gordon.get_queried_data())

    DataFrameReader.dataframe_to_db('motorol', get_queried_data())

    #Gordon = Gordon()
    #gordon_df = Gordon.process()
    # print(gordon_df.head())
    #DataFrameReader.dataframe_to_db('Gordon', gordon_df)

    # qa = QueryProcessor('D:\\Work\\MNK_PRICES\\DB_FILES\\Hart\\files')
    # qa.get_dataframe('')

    # fc = FileConverter()

    # fc.convert_all()
