from SupplierScripts import *
import pandas as pd
from pandasql import sqldf


def autofusbmw_to_db():
    table_name = 'auto_fus_bmw'
    print('Pushing {} to Data Base'.format(table_name))
    DataFrameReader.dataframe_to_db(table_name, get_autofusbmw_data())
    DataFrameReader.supplier_to_ftp(table_name)


def get_autofusbmw_data():
    autofusbmw = AutoFusBmw()
    dataframes = autofusbmw.process()
    data = dataframes[0]
    discount = dataframes[1]

    query = '''

        SELECT 
            "BMW" AS manufacturer,
            data.supplier_part_number,
            data.supplier_part_number AS part_number,
            data.discount_code,
            discount.discount,
            ROUND(data.price*(1-(discount.discount/100)), 2) AS price,
            999 AS quantity,
            6 AS delivery     
        FROM 
            data
        INNER JOIN
            discount
        ON 
            data.discount_code = discount.discount_code
    '''
    return sqldf(query)


class AutoFusBmw:

    def __init__(self):
        data_url = "ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/autofus/bmw/auto_fus_bmw_data.xlsx"
        discount_url = "ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/autofus/bmw/autofus_bmw_rabat.csv"

        self.data_columns = {
            0: 'supplier_part_number',
            1: 'price',
            2: 'discount_code'
        }

        self.discount_columns = {
            0: 'discount_code',
            1: 'discount'
        }

        self.data = pd.read_excel(data_url, header=None)
        self.discount = pd.read_csv(discount_url, sep='\t', header=None, decimal=',')


    def process(self):

        self.data.rename(columns=self.data_columns, inplace=True)
        self.discount.rename(columns=self.discount_columns, inplace=True)

        return [self.data, self.discount]

