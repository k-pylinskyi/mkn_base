from Services.Processors.DataFrameReader import *
import pandas as pd
from pandasql import sqldf
from api.Services.Logger.wrapper import timeit


@timeit
def autopartner_to_db():
    table_name = 'autopartner'
    print('Pushing {} to Data Base'.format(table_name))
    DataFrameReader.dataframe_to_db(table_name, get_autopartner_data())


@timeit
def get_autopartner_data():
    autopartner = Autopartner()
    data = autopartner.process()

    query = '''
        SELECT 
        6 as supplier_id,
        data.manufacturer,
        data.supplier_part_number,
        data.part_number, 
        data.part_name, 
        data.price,
        data.delivery,
        ROUND(data.weight, 2) AS weight,
        REPLACE(data.qty1 + data.qty2 + data.qty3, '.0', '') AS quantity,
        data.filia
        FROM data
        WHERE quantity NOT LIKE '0'
    '''

    # dat = sqldf(query)
    # quer = '''SELECT dat.filia, COUNT(*)
    #                FROM dat
    #                GROUP BY dat.filia;'''
    #
    # print(sqldf(quer))
    return sqldf(query)


class Autopartner:
    def __init__(self):
        self.data_url = 'ftp://3036856:0cL4X5@ftp.autopartner.dev/VIP_PORTAL_3036856_File_2.csv'
        self.delivery_data_url = 'ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/autopartner/Auto ' \
                                 'partner_magazyny.txt '
        self.data_columns = {0: 'part_number', 1: 'part_name', 2: 'supplier_part_number', 3: 'manufacturer', 4: 'price',
                             6: 'currency', 7: 'weight', 9: 'bar_code', 10: 'supplier_part_number',
                             11: 'part_description',
                             12: 'qty1', 13: 'filia', 15: 'qty2', 16: 'qty3', 17: 'manufacturer_code'}

    def process(self):

        data = pd.read_csv(self.data_url, encoding_errors='ignore', sep=';', on_bad_lines='skip', header=None,
                           low_memory=False)

        delivery = pd.read_csv(self.delivery_data_url, encoding_errors='ignore', sep=';', on_bad_lines='skip',
                               header=None,
                               low_memory=False)

        delivery = delivery.to_dict(orient='list')

        data.drop(data.columns[[5, 8, 14]], axis=1, inplace=True)
        data.rename(columns=self.data_columns, inplace=True)
        data['delivery'] = pd.Series(dtype='int')

        for i, row in enumerate(data.itertuples(), 1):
            if row[12] in delivery[0]:
                val = delivery[1][delivery[0].index(row[12])]
                data.at[i, 'delivery'] = val
        return data
