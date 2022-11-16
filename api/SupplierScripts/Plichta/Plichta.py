from api.Services.Processors.DataFrameReader import *
from api.Services.load_config import Config
from api.Services.Loader.LoadController import LoadController
import pandas as pd
from pandasql import sqldf

from api.Services.Processors.DataFrameReader import DataFrameReader


def plichta_to_db():
    table_name = 'plichta'
    print('Pushing {} to Data Base'.format(table_name))
    data = get_plichta_data()
    print(data)
    DataFrameReader.dataframe_to_db(table_name, data  )


def get_plichta_data():
    plichta = Plichta()
    out, dict = plichta.process()

    query = '''
        SELECT
            'VAG' as manufacturer,
            out.supplier_part_number as supplier_part_number,
            dict.part_number as part_number,
            16 AS delivery,
            CAST(quantity AS INTEGER) as quantity,
            ROUND(out.price, 2) as price
            FROM out 
        INNER JOIN dict 
            ON out.supplier_part_number = dict.part_number'''

    return sqldf(query)


class Plichta:
    def __init__(self):
        self.data_url = 'ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/plichta/plichta_data.xlsx'
        self.dict_url = 'ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/plichta/plichta_dict.csv'

        self.data_columns = {
                0: 'supplier_part_number',
                1: 'part_name',
                2: 'price_netto',
                3: 'group',
                4: 'cn',
                5: 'quantity',
                6: 'price'
            }

        self.xl = pd.ExcelFile(self.data_url)
        self.sheet_names = self.xl.sheet_names

    def process(self):
        dfs = []
        for name in self.sheet_names:
            df = pd.read_excel(self.data_url, name, skiprows=1, header=None)
            df.rename(columns=self.data_columns, inplace=True)
            dfs.append(df)
        out = pd.concat(dfs, ignore_index=False)
        dic = pd.read_csv(self.dict_url, sep=';', usecols=[0])
        dic.columns = ['part_number']
        return out, dic
