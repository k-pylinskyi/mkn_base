from Services.Ftp.FtpConnection import FtpConnection
from Services.Processors.DataFrameReader import *
from Services.load_config import Config
from Services.Loader.LoadController import LoadController

import pandas as pd
from pandasql import sqldf


def materom_to_db():
    table_name = 'materom'
    print('Pushing {} to Data Base'.format(table_name))
    data = get_materom_data()
    DataFrameReader.dataframe_to_db(table_name, data)


def get_materom_data():
    materom = Materom()
    out = materom.process()
    # print(out)
    query = '''
            SELECT
                out.manufacturer as manufacturer,
                out.supplier_part_number as supplier_part_number,
                out.part_number as part_number,
                out.quantity as quantity,
                (out.price + out.deposit) as price,
                out.price as supplier_price,
                out.deposit as deposit,
                3 as delivery
            FROM
                out'''

    return sqldf(query)


class Materom:
    def __init__(self):
        self.data_url = 'ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/materom/21467.CSV'

        self.data_columns ={
            0: 'supplier_part_number',  # 'Materom_Nummer'
            1: 'description',  # 'Bezeichnung'
            2: 'manufacturer',  # 'Hersteller'
            3: 'part_number',  # 'TecDoc_Artikel_Nr.'
            4: 'tecdoc_id',  # ???
            5: 'quantity',  # Bestand
            6: 'price',  # preis
            7: 'pack',  # pack Mindestbellmenge
            8: 'deposit'  # pfand
        }

    def process(self):
        data = pd.read_csv(self.data_url, sep=';', header=None,
                           skiprows=1, on_bad_lines='skip')
        data.rename(columns=self.data_columns, inplace=True)
        return data