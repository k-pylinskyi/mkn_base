from api.SupplierScripts import *
import pandas as pd
from pandasql import sqldf

from api.Services.Processors.DataFrameReader import DataFrameReader

def caffaro_to_db():
    table_name = 'caffaro'
    print('Pushing {} to Data Base'.format(table_name))
    DataFrameReader.dataframe_to_db(table_name, get_caffaro_data())
    DataFrameReader.supplier_to_ftp(table_name)


def get_caffaro_data():
    caffaro = Caffaro()
    dataframes = caffaro.process()
    data = dataframes

    query = '''
        SELECT
            data.part_number,
            data.part_number AS supplier_part_number,
            data.price,
            "CAFFARO" AS manufacturer,
            5 AS delivery,
            "PLN" AS currency,
            IFNULL(data.dimensions, 0) AS dimensions,
            data.weight,
            IFNULL(data.quantity, 0) AS quantity,
            IFNULL(data.oe1, 0) AS oe1,
            IFNULL(data.oe2, 0) AS oe2,
            IFNULL(data.oe3, 0) AS oe3,
            IFNULL(data.oe4, 0) AS oe4,
            IFNULL(data.oe5, 0) AS oe5,
            IFNULL(data.cross_bta, 0) AS cross_bta,
            IFNULL(data.cross_dayco, 0) AS cross_dayco,
            IFNULL(data.cross_febi_bilstein, 0) AS cross_febi_bilstein,
            IFNULL(data.cross_gates, 0) AS cross_gates,
            IFNULL(data.cross_ina, 0) AS cross_ina,
            IFNULL(data.cross_magneti_marelli, 0) AS cross_magneti_marelli,
            IFNULL(data.cross_optimal, 0) AS cross_optimal,
            IFNULL(data.cross_snr, 0) AS cross_snr,
            IFNULL(data.cross_skf, 0) AS cross_skf
        FROM
            data
    
    '''
    return sqldf(query)

class Caffaro:

    def __init__(self):
        data_url = "ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/caffaro/caffaro.xlsx"

        self.data_columns = {
            0: 'part_number',
            4: 'price',
            6: 'dimensions',
            9: 'weight',
            11: 'quantity',
            15: 'oe1',
            16: 'oe2',
            17: 'oe3',
            18: 'oe4',
            19: 'oe5',
            20: 'cross_bta',
            21: 'cross_dayco',
            22: 'cross_febi_bilstein',
            23: 'cross_gates',
            24: 'cross_ina',
            25: 'cross_magneti_marelli',
            26: 'cross_optimal',
            27: 'cross_ruville',
            28: 'cross_snr',
            29: 'cross_skf'

        }
        self.data = pd.read_excel(data_url, header=None)

    def process(self):
        self.data.rename(columns=self.data_columns, inplace=True)
        return self.data