import os

from Services.Processors.DataFrameReader import *
import pandas as pd
from pandasql import sqldf


def autopartner_to_db():
    print('Pushing Autopartner to Data Base')
    DataFrameReader.dataframe_to_db('autopartner', get_autopartner_data())


def get_autopartner_data():
    autopartner = Autopartner()
    dataframes = autopartner.process()
    data = dataframes
    query = '''
        SELECT 
        6 as supplier_id,
        data.manufacturer,
        data.supplier_part_number,
        data.part_number, 
        data.part_name, 
        data.price,
        ROUND(data.weight, 2) AS weight,
        REPLACE(data.qty1 + data.qty2 + data.qty3, '.0', '') AS quantity
        FROM data
        WHERE quantity NOT LIKE '0'
    '''
    return sqldf(query)


class Autopartner:
    def __init__(self):
        location = '../TemporaryStorage/AUTO_PARTNER/files/VIP_PORTAL_3036856_File_1.csv'
        self.data_columns = {0: 'part_number', 1: 'part_name', 2: 'supplier_part_number', 3: 'manufacturer', 4: 'price',
                             6: 'currency', 7: 'weight', 9: 'bar_code', 10: 'supplier_part_number', 11: 'part_description',
                             12: 'qty1', 15: 'qty2', 16: 'qty3', 17: 'manufacturer_code'}

        self.data = pd.read_csv(location, encoding_errors='ignore', sep=';', error_bad_lines=False, header=None, low_memory=False)

    def process(self):
        self.data.drop(self.data.columns[[5, 8, 13, 14]], axis=1, inplace=True)
        self.data.rename(columns=self.data_columns, inplace=True)
        return self.data
