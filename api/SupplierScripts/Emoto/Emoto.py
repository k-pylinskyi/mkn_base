import os

import pandas as pd
from pandasql import sqldf


class Emoto:
    pd.set_option('display.max_columns', 999)

    def __init__(self):
        self.data_columns = {0: 'part_number', 1: 'part_name', 2: 'price', 3: 'qty', 4: 'part_desc', 5: 'manufacturer'}
        self.dict_columns = {1: 'manufacturer', 2: 'prefix', 3: 'brand'}
        self.part_numbers_columns = {0: 'supplier_part_number', 1: 'part_number'}

        location = './TemporaryStorage/EMOTO/files/emoto_data.csv'
        dictionary = './SupplierScripts/Emoto/emoto_dict.csv'
        self.part_numbers = './SupplierScripts/Emoto/emoto_dict.txt'

        self.data = pd.read_csv(location, encoding_errors='ignore', sep=';', header=None, skiprows=1)
        self.dict = pd.read_csv(dictionary, sep=';', header=None, skiprows=1)

        with open(self.part_numbers, 'w') as fp:
            for item in self.data[0]:
                fp.write("%s;\n" % item)

    def process(self):
        self.data.rename(columns=self.data_columns, inplace=True)
        self.data.replace('>', '', regex=True, inplace=True)
        self.data.replace('.00', '', regex=True, inplace=True)

        self.dict.rename(columns=self.dict_columns, inplace=True)
        self.dict.drop(self.dict.columns[[0]], axis=1, inplace=True)

        prefix_list = self.dict['prefix']
        for item in prefix_list:
            regex = r'^(' + item + ')'
            self.data['part_number'].replace(regex, '', regex=True, inplace=True)
        part_numbers = pd.read_csv(self.part_numbers, sep=';', header=None)
        part_numbers[1] = self.data['part_number']
        part_numbers.rename(columns=self.part_numbers_columns, inplace=True)
        os.remove(self.part_numbers)

        return [self.data, self.dict, part_numbers]


def process_emoto():
    emoto = Emoto()
    dataframes = emoto.process()
    data = dataframes[0]
    dict = dataframes[1]
    part_numbers = dataframes[2]
    query = '''
        SELECT data.part_number, data.price, data.qty, dict.brand AS manufacturer, data.part_name, part_numbers.supplier_part_number
        FROM data
        INNER JOIN dict
        ON dict.manufacturer = data.manufacturer
        INNER JOIN part_numbers
        ON part_numbers.part_number = data.part_number
        WHERE qty NOT LIKE '0'
    '''
    return sqldf(query)
