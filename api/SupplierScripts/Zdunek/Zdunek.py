from SupplierScripts import *
import pandas as pd
from pandasql import sqldf


def zdunek_to_db():
    table_name = 'zdunek_bmw'
    print('Pushing {} to Data Base'.format(table_name))
    DataFrameReader.dataframe_to_db(table_name, get_zdunek_data())
    DataFrameReader.supplier_to_ftp(table_name)


def get_zdunek_data():
    zdunek = Zdunek()
    dataframes = zdunek.process()
    data = dataframes

    query = '''
    
        SELECT
            "BMW" AS manufacturer,
            999 AS quantity,
            data.supplier_part_number,
            data.supplier_part_number AS part_number,
            data.comment,
            data.price,
            ROUND (data.price,2)
        FROM
            data
    
    '''
    return sqldf(query)


class Zdunek :

    def __init__(self):
        data_url = "ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/zdunek/zdunek_data.xlsx"

        self.data_columns = {

            0: 'supplier_part_number',
            1: 'comment',
            4: 'price'
        }

        self.data = pd.read_excel(data_url, header=None, skiprows=1)


    def process(self):
        self.data.rename(columns=self.data_columns, inplace=True)
        return self.data