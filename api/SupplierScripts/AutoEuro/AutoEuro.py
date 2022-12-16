from api.SupplierScripts import *
import pandas as pd
from pandasql import sqldf


def autoeuro_to_db():
    table_name = 'autoeuro'
    print('Pushing {} to Data Base'.format(table_name))
    DataFrameReader.dataframe_to_db(table_name, get_autoeuro_data())
    DataFrameReader.supplier_to_ftp(table_name)


def get_autoeuro_data():
    autoeuro = AutoEuro()
    dataframes = autoeuro.process()
    data = dataframes[0]

    query = '''

        SELECT 
            data.manufacturer,
            data.part_name,
            data.supplier_part_number,
            data.part_number,
            data.price,
            CAST(REPLACE(data.quantity, '> ', '') AS INTEGER) AS quantity,
            1 AS delivery,
            data.cn_number,
            data.comment,
            "PLN" AS currency,
            data.part_group_id
        FROM 
            data
        WHERE data.manufacturer is not null AND data.part_number is not null
    '''
    return sqldf(query)


class AutoEuro:

    def __init__(self):
        data_url = "ftp://auto_euro:rR0eX3cN3d@138.201.56.185/29452_ce.csv"

        self.data_columns = {
            0: 'supplier_part_number',
            1: 'part_name',
            2: 'quantity',
            3: 'comment',
            4: 'price',
            5: 'part_number',
            6: 'part_group_id',
            7: 'manufacturer',
            8: 'cn_number'
        }

        self.data = pd.read_csv(data_url, header=None, sep=';', low_memory=False, on_bad_lines='skip')


    def process(self):

        self.data.rename(columns=self.data_columns, inplace=True)

        return [self.data]

