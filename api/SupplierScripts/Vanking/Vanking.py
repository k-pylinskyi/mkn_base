from Services.Processors.DataFrameReader import *
from Services.load_config import Config
from Services.Loader.LoadController import LoadController
import pandas as pd
from pandasql import sqldf


def vanking_to_db():
    table_name = 'vanking'
    print('Pushing {} to Data Base'.format(table_name))
    DataFrameReader.dataframe_to_db(table_name, get_vanking_data())


def get_vanking_data():
    vanking = Vanking()
    dataframes = vanking.process()
    data = dataframes

    query = '''
        SELECT
            manufacturer,
            supplier_part_number,
            part_name1,
            part_name2,
            part_number,
            1 AS delivery,
            price,
            CAST(quantity AS INTEGER) as quantity
        FROM
            data

    '''

    return sqldf(query)


def get_file():
    config = Config()
    auth = config.get_app_service_auth('main', 'main')
    loader = LoadController(auth[0], auth[1])
    loader.download('mail', 'vanking', 'vanking.xlsx',
                                params={'sender': 'raporty@vanking.com.pl', 'subject': None})


class Vanking:
    def __init__(self):
        get_file()
        data = 'ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/vanking/export.xlsx'
        self.data_columns = {
            0: 'supplier_part_number',
            1: 'manufacturer',
            2: 'part_number',
            3: 'part_name1',
            4: 'quantity',
            5: 'price',
            6: 'currency',
            7: 'part_name2'
        }

        self.data = pd.read_excel(data, skiprows=1, header=None)

    def process(self):
        self.data.rename(columns=self.data_columns, inplace=True)
        return self.data

