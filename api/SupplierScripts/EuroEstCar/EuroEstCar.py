from Services.Processors.DataFrameReader import *
from Services.load_config import Config
from Services.Loader.LoadController import LoadController
import pandas as pd
from pandasql import sqldf


def euroestcar_to_db():
    table_name = 'euro_est_car'
    print('Pushing {} to Data Base'.format(table_name))
    DataFrameReader.dataframe_to_db(table_name, get_euroestcar_data())


def get_euroestcar_data():
    euro_est_car = EuroEstCar()
    data = euro_est_car.process()

    query = '''
        SELECT
            manufacturer,
            supplier_part_number,
            supplier_part_number as part_number,
            CAST(REPLACE(quantity, '>', '') AS INTEGER) as quantity,
            price
        FROM
            data
    '''

    return sqldf(query)


def get_file():
    config = Config()
    auth = config.get_app_service_auth('main', 'main')
    loader = LoadController(auth[0], auth[1])
    loader.download('mail', 'euro_est_car', 'euro_est_car.xlsx',
                    params={'sender': 'margareta.peptenaru@euroestcar.ro', 'subject': 'STOCK EEC'})


class EuroEstCar:
    def __init__(self):
        self.data_url = "ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/euro_est_car/export.xlsx"

        self.data_columns = {
            0: 'supplier_part_number',
            1: 'part_name',
            2: 'manufacturer',
            3: 'quantity',
            4: 'price'
        }

        self.xl = pd.ExcelFile(self.data_url)
        self.sheet_names = self.xl.sheet_names

    def process(self):
        get_file()
        dfs = []
        for name in self.sheet_names:
            df = pd.read_excel(self.data_url, name, skiprows=1, header=None)
            df.rename(columns=self.data_columns, inplace=True)
            dfs.append(df)
        out = pd.concat(dfs, ignore_index=False)
        return out
