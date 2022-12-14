from SupplierScripts import *
import pandas as pd
from pandasql import sqldf


def autofrance_to_db():
    table_name = 'autofrance'
    print('Pushing {} to Data Base'.format(table_name))
    DataFrameReader.dataframe_to_db(table_name, get_autofrance_data())
    DataFrameReader.supplier_to_ftp(table_name)


def get_autofrance_data():
    autofrance = AutoFrance()
    dataframes = autofrance.process()
    data = dataframes
    data = data.fillna(0)


    query = '''
        SELECT
            data.part_number,
            data.part_number as supplier_part_number,
            data.manufacturer,
            1 AS delivery,
            data.comment,
            CAST(TRIM(data.price) AS REAL) as price,
            data.currency,
            CAST(TRIM(data.quantity) AS INTEGER) as quantity
        FROM
            data
        WHERE CAST(TRIM(data.quantity) AS INTEGER) > 0
    '''

    return sqldf(query)


class AutoFrance:
    def __init__(self):
        self.data_url = "ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/auto_france/OFERTA.txt"

        self.data_columns = {
            0: 'supplier_part_number',
            1: 'part_number',
            2: 'manufacturer',
            3: 'comment',
            4: 'price',
            5: 'currency',
            6: 'quantity'
        }


    def process(self):
        data = pd.read_csv(self.data_url, sep='\t', header=None, on_bad_lines='skip', encoding_errors='ignore',
                                decimal=',', skiprows=1)
        data.rename(columns=self.data_columns, inplace=True)

        return data