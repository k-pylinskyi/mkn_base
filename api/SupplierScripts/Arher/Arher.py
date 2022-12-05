from Services.Processors.DataFrameReader import *
import pandas as pd
from pandasql import sqldf
from Services.Logger.wrapper import timeit

@timeit
def arher_to_db():
    table_name = 'arher'
    print('Pushing {} to Data Base'.format(table_name))
    data = get_arher_data()
    print(data)
    DataFrameReader.dataframe_to_db(table_name, data)
    # DataFrameReader.supplier_to_ftp(table_name)


def get_arher_data():
    autoeuro = Arher()
    data = autoeuro.process()

    query = '''
        SELECT 
            'HONDA' AS manufacturer,
            data.part_number AS supplier_part_number,
            data.part_number AS part_number,
            7 AS delivery,
            999 AS quantity,
            (CAST(data.netto_price AS REAL) - CAST(data.netto_price AS REAL)*0.16) AS price
        FROM 
            data
        
    '''
    return sqldf(query)


class Arher:

    def __init__(self):
        self.data_url = "ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/arher/CennikHONDA.xlsx"

        self.data_columns = {
            0: 'part_number',
            1: 'part_name',
            2: 'model_poc',
            3: 'model_konc',
            4: 'netto_price'
        }

        self.data = pd.read_excel(self.data_url, skiprows=1, header=None)

    def process(self):
        self.data.rename(columns=self.data_columns, inplace=True)

        return self.data
