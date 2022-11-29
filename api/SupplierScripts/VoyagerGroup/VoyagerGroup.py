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
    dfs = voyagerGroup.process()
    data_5_days = dfs[0]
    data_3_days = dfs[1]

    query = '''
        SELECT
            'MAZDA' as manufacturer,
            data_5_days.supplier_part_number as supplier_part_number,
            data_5_days.supplier_part_number as part_number,
            data_5_days.price as supplier_price,
            data_5_days.discount,
            CAST(data_5_days.price as NUMERIC) - data_5_days.price*CAST(REPLACE(discount, '%', '') as NUMERIC)/100 as price,
            '999' as quantity,
            5 as delivery,
            'szt.' as measure,
            '5_days_stock' as localization
        FROM
            data_5_days
        UNION
            SELECT
            'MAZDA' as manufacturer,
            data_3_days.supplier_part_number as supplier_part_number,
            data_3_days.supplier_part_number as part_number,
            data_3_days.price as supplier_price,
            0 as discount,
            data_3_days.price as price,
            data_3_days.quantity,
            3 as delivery,
            data_3_days.measure,
            data_3_days.localization
        FROM
            data_3_days
        '''

    return sqldf(query)


class VoyagerGroup:
    def __init__(self):
        self.data_5_days_url = 'ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/voyager_group/voyager_data.CSV'
        self.data_3_days_url = 'ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/voyager_group/voyager_3_days.csv'

        self.data_5_days_columns = {
            0: 'date',
            1: 'supplier_part_number',
            2: 'part_name',
            3: 'price',
            4: 'discount',
        }

        self.data_3_days_columns = {
            0: 'supplier_part_number',
            1: 'localization',
            2: 'part_name',
            3: 'measure',
            4: 'quantity',
            5: 'price',
        }

    def process(self):
        data_5_days = pd.read_csv(self.data_5_days_url, sep=';', header=None, decimal=',',
                          skiprows=1, on_bad_lines='skip', encoding='latin1')
        data_5_days.rename(columns=self.data_5_days_columns, inplace=True)

        data_3_days = pd.read_csv(self.data_3_days_url, sep=';', header=None, decimal=',',
                          skiprows=1, on_bad_lines='skip', encoding='latin1')
        data_3_days.rename(columns=self.data_3_days_columns, inplace=True)
        return [data_5_days, data_3_days]
