import pandas as pd
from pandasql import sqldf

from api.Services.Processors.DataFrameReader import DataFrameReader


class Motogama:
    pd.set_option('display.max_columns', 999)

    def __init__(self):
        self.data_columns = {0: 'supplier_part_number', 1: 'part_name', 2: 'qty', 3: 'price', 5: 'part_number',
                             7: 'manufacturer', 8: 'consignment'}
        location = './TemporaryStorage/MOTOGAMA/files/motogama_data.csv'

        self.data = pd.read_csv(location, encoding_errors='ignore', sep=';', header=None, low_memory=False)

    def process(self):
        self.data.drop(self.data.columns[[4, 6, 9, 10, 11, 12]], axis=1, inplace=True)
        self.data.rename(columns=self.data_columns, inplace=True)
        self.data.set_index('supplier_part_number', inplace=True)
        self.data['part_number'] = DataFrameReader.format_column(self.data['part_number'])
        return self.data


def process_motogama():
    motogama = Motogama()
    data = motogama.process()
    query = '''
        SELECT data.supplier_part_number,  data.part_name, data.price, data.part_number, data.consignment,
        REPLACE(data.qty, '>', '') AS qty
        FROM data
        WHERE qty NOT LIKE '0'
    '''
    return sqldf(query)
