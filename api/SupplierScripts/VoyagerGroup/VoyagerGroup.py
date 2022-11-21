from api.Services.Processors.DataFrameReader import *
from api.Services.load_config import Config
from api.Services.Loader.LoadController import LoadController
import pandas as pd
from pandasql import sqldf

from api.Services.Processors.DataFrameReader import DataFrameReader


def voyagerGroup_to_db():
    table_name = 'voyager_group'
    print('Pushing {} to Data Base'.format(table_name))
    data = get_VoyagerGroup_data()
    print(data)
    DataFrameReader.dataframe_to_db(table_name, data)


def get_VoyagerGroup_data():
    voyagerGroup = VoyagerGroup()
    data = voyagerGroup.process()

    query = '''
        SELECT
            'MAZDA' as manufacturer,
            data.supplier_part_number as supplier_part_number,
            data.supplier_part_number as part_number,
            '999' as quantity,
            price as supplier_price,
            discount,
            CAST(data.price as NUMERIC) - data.price*CAST(REPLACE(discount, '%', '') as NUMERIC)/100 as price,
            5 as delivery
        FROM
            data
        '''

    return sqldf(query)


class VoyagerGroup:
    def __init__(self):
        self.data_url = 'ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/voyager_group/voyager_data.CSV'

        self.data_columns = {
            0: 'date',
            1: 'supplier_part_number',
            2: 'part_name',
            3: 'price',
            4: 'discount',
        }

    def process(self):
        data = pd.read_csv(self.data_url, sep=';', header=None,
                          skiprows=1, on_bad_lines='skip', encoding='latin1')
        data.rename(columns=self.data_columns, inplace=True)
        return data
