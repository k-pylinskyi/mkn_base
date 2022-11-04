from Services.Processors.DataFrameReader import *
from Services.load_config import Config
from Services.Loader.LoadController import LoadController
import pandas as pd
from pandasql import sqldf


def bronowski_to_db():
    table_name = 'bronowski'
    print('Pushing {} to Data Base'.format(table_name))
    DataFrameReader.dataframe_to_db(table_name, get_bronowski_data())


def get_bronowski_data():
    bronowski = Bronowski()
    dataframes = bronowski.process()
    data = dataframes[0]
    dict = dataframes[1]

    query = '''
        SELECT
            dict.manufacturer,
            dict.supplier_part_number,
            data.part_name,
            dict.part_number,
            data.price,
            CAST(data.quantity AS INTEGER) as quantity
        FROM
            data
        INNER JOIN
            dict
        ON
            data.supplier_part_number = dict.supplier_part_number
    '''

    return sqldf(query)


def get_file():
    config = Config()
    auth = config.get_app_service_auth('main', 'main')
    loader = LoadController(auth[0], auth[1])
    loader.download('mail', 'bronowski', 'bronowski.xls',
                                params={'sender': 'bronek@bronowski.pl', 'subject': 'Odbiorca 71233712 Oferta towarowa'})


class Bronowski:
    def __init__(self):
        get_file()
        data = 'ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/bronowski/export.xls'
        dict = 'ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/bronowski/bronowski_dict.csv'
        self.data_columns = {
            0: 'supplier_part_number',
            1: 'part_number',
            2: 'part_name',
            3: 'price',
            4: 'currency',
            5: 'quantity'
        }

        self.data = pd.read_excel(data, skiprows=4, header=None)
        self.dict = pd.read_csv(dict, sep='\t')

    def process(self):
        self.data.rename(columns=self.data_columns, inplace=True)
        return [self.data, self.dict]

