from SupplierScripts import *
import pandas as pd
from pandasql import sqldf


def autofusbmw_to_db():
    table_name = 'autofusbmw'
    print('Pushing {} to Data Base'.format(table_name))
    DataFrameReader.dataframe_to_db(table_name, get_autofusbmw_data())
    DataFrameReader.supplier_to_ftp(table_name)


def get_autofusbmw_data():
    autofusbmw = AutoFusBmw()
    dataframes = autofusbmw.process()
    data = dataframes[0]
    dict = dataframes[1]

    query = '''

        SELECT 
            data.supplier_part_number,
            data.part_number,
            data.discount_code,
            ROUND(data.price*(1-(dict.discount/100.0)), 2) AS price
        FROM 
            data
        INNER JOIN
            dict
        ON 
            data.discount_code = dict.discount_code
    '''
    return sqldf(query)


class AutoFusBmw:

    def __init__(self):
        data_url = "ftp://138.201.56.185/suppliers/autofus/bmw/auto_fus_bmw_data.xlsx"
        dict_url = "ftp://138.201.56.185/suppliers/autofus/bmw/autofus_bmw_rabat.csv"

        self.data_columns = {
            0: 'supplier_part_number',
            1: 'part_number',
            2: 'price',
            3: 'discount_code'
        }

        self.dict_columns = {
            1: 'discount_code',
            2: 'discount'
        }

        self.data = pd.read_csv(data_url, sep=';', encoding_errors='ignore', header=None,
                                low_memory=False, usecols=[0, 1, 2, 3])

        self.dict = pd.read_csv(dict_url, sep=';', header=None, skiprows=1, usecols=[1, 2])


    def process(self):
        self.data.rename(columns=self.data_columns, inplace=True)
        self.dict.rename(columns=self.dict_columns, inplace=True)

        return [self.data, self.dict]

