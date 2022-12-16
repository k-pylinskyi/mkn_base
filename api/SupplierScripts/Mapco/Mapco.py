from api.SupplierScripts import *
import pandas as pd
from pandasql import sqldf

from api.Services.Processors.DataFrameReader import DataFrameReader


def mapco_to_db():
    table_name = 'mapco'
    print('Pushing {} to Data Base'.format(table_name))
    DataFrameReader.dataframe_to_db(table_name, get_mapco_data())
    DataFrameReader.supplier_to_ftp(table_name)


def get_mapco_data():
    mapco = Mapco()
    dataframes = mapco.process()
    data = dataframes[0]
    data2 = dataframes[1]

    query = '''
        SELECT
            data.part_number,
            data.part_number as supplier_part_number,
            "EUR" AS currency,
            5 AS delivery,
            data.name,
            data.price,
            2 AS quantity,
            "MAPCO" AS manufacturer 
        FROM
            data
        INNER JOIN
            data2
        ON
            data.part_number = data2.part_number
    '''
    return sqldf(query)


class Mapco:

    def __init__(self):
        data_url = "ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/mapco/PRICE.xlsx"
        data2_url = "ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/mapco/Kratnost.csv"

        self.data_columns = {
            0: 'part_number',
            1: 'name',
            3: 'group',
            4: 'price'
        }

        self.data2_columns = {
            0: 'part_number',
            1: 'comment',
            2: 'description'
        }

        self.data = pd.read_excel(data_url, header=None)
        self.data2 = pd.read_csv(data2_url, sep=';', header=None, encoding_errors='ignore')

    def process(self):

        self.data.rename(columns=self.data_columns, inplace=True)
        self.data2.rename(columns=self.data2_columns, inplace=True)

        return [self.data, self.data2]
