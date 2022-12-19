import numpy as np
from SupplierScripts import *
from Services.Processors.DataFrameReader import *
import pandas as pd
from pandasql import sqldf
from Services.Logger.wrapper import timeit


@timeit
def autopartner_to_db():
    table_name = 'autopartner'
    print('Pushing {} to Data Base'.format(table_name))
    data, ftp_cred = get_autopartner_data()
    DataFrameReader.dataframe_to_db(table_name, data)
    return ftp_cred


@timeit
def get_autopartner_data():
    autopartner = Autopartner()
    ftp_cred = parse_ftp(autopartner)
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
    return sqldf(query), ftp_cred


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

        data['delivery'] = np.where(data['filia'] == '72 Filia', '1',
                                    np.where(data['filia'] == '01 Filia', '1',
                                             np.where(data['filia'] == '03 Filia', '3', 'None')))

        # print('Overall rows before dropna:' + str(data.shape[0]))
        # print('Overall na: ' + str(data['delivery'].isin(['None']).sum()))
        data = data[~data['delivery'].isin(['None'])]

        # print(data['delivery'].value_counts())
        # print(data['filia'].value_counts())
        #
        # print('Overall rows after drop na:' + str(data.shape[0]))
        return data
