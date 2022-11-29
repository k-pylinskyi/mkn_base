from Services.Processors.DataFrameReader import *
from Services.load_config import Config
from Services.Loader.LoadController import LoadController
import pandas as pd
from pandasql import sqldf

from Services.Processors.DataFrameReader import DataFrameReader


def VoyagerGroup_to_db():
    table_name = 'voyager_group'
    print('Pushing {} to Data Base'.format(table_name))
    DataFrameReader.dataframe_to_db(table_name, get_VoyagerGroup_data())
    DataFrameReader.supplier_to_ftp(table_name)


def get_VoyagerGroup_data():
    voyagerGroup = VoyagerGroup()
    dataframes = voyagerGroup.process()
    data = dataframes[0]
    day3 = dataframes[1]

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
        UNION
            SELECT
                'MAZDA' as manufacturer,
                day3.supplier_part_number as supplier_part_number,
                day3.supplier_part_number as part_number,
                ROUND(day3.quantity, -1),
                ROUND(day3.price, 2),
                3 as delivery
            FROM
                day3
                
        '''

    return sqldf(query)


class VoyagerGroup:
    def __init__(self):
        self.data_url = 'ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/voyager_group/voyager_data.CSV'
        self.day3_url = 'ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/voyager_group/voyager_3_day.csv'
        self.data_columns = {
            0: 'date',
            1: 'supplier_part_number',
            2: 'part_name',
            3: 'price',
            4: 'discount',
        }

        self.day3_columns = {

            0: 'supplier_part_number',
            1: 'location',
            2: 'part_name',
            3: 'unit',
            4: 'quantity',
            5: 'price'
        }
        data = pd.read_csv(self.data_url, sep=';', header=None,
                           skiprows=1, on_bad_lines='skip', encoding='latin1', low_memory=False)
        day3 = pd.read_csv(self.day3_url, sep=';', header=None,
                           skiprows=1, on_bad_lines='skip', low_memory=False)

    def process(self):

        self.data.rename(columns=self.data_columns, inplace=True)
        self.day3.rename(columns=self.day3_columns, inplace=True)

        return [self.data, self.day3]
