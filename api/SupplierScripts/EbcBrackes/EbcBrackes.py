from api.SupplierScripts import *
import pandas as pd
from pandasql import sqldf

from api.Services.Processors.DataFrameReader import DataFrameReader


def ebcbrackes_to_db():
    table_name = 'ebc_brackes'
    print('Pushing {} to Data Base'.format(table_name))
    DataFrameReader.dataframe_to_db(table_name, get_ebcbrackes_data())


def get_ebcbrackes_data():
    ebcbrackes = EbcBrackes()
    dataframes = ebcbrackes.process()
    data = dataframes

    query = '''
        SELECT
            data.part_number,
            data.part_number AS supplier_part_number,
            data.price_netto AS price,
            22 AS delivery,
            999 AS quantity,
            "EBC" AS manufacturer,
            "PLN" AS currency
        FROM
            data
        WHERE price NOT LIKE 'TBC'    
    '''
    return sqldf(query)
    print(data)


class EbcBrackes:

    def __init__(self):
        data_url = "ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/ebc_brackes/cennik.xlsx"

        self.data_columns = {
            0: 'part_number',
            1: 'price_netto',
            2: 'price_brutto',
            3: 'seria'
        }
        self.data = pd.read_excel(data_url, header=None, skiprows=1)

    def process(self):
        self.data.rename(columns=self.data_columns, inplace=True)
        return self.data
