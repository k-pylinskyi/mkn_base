import pandas as pd
from pandasql import sqldf


class AutopartnerGdansk:
    pd.set_option('display.max_columns', 999)

    def __init__(self):
        self.data_columns = {0: 'manufacturer', 1: 'part_name', 2: 'part_art', 3: 'qty', 4: 'price', 6: 'part_number'}
        self.dict_columns = {0: 'part_art', 1: 'part_number', 2: 'manufacturer', 3: 'part_name'}
        location = './TemporaryStorage/AUTO_PARTNER_GDANSK/files/autopartner_gdansk_data.csv'
        dictionary = './api/SupplierScripts/AutopartnerGdansk/autopartner_gdansk_helper.csv'

        self.data = pd.read_csv(location, encoding_errors='ignore', sep=';', header=None, low_memory=False)
        self.dict = pd.read_csv(dictionary, encoding_errors='ignore', sep='\t', header=None, skiprows=1)

    def process(self):
        self.data.drop(self.data.columns[[5, 7, 8]], axis=1, inplace=True)
        self.data.rename(columns=self.data_columns, inplace=True)
        self.data.set_index('part_number', inplace=True)

        self.dict.rename(columns=self.dict_columns, inplace=True)
        self.dict.set_index('part_number', inplace=True)
        return [self.data, self.dict]


def process_autopartner_gdansk():
    autopartner_gdansk = AutopartnerGdansk()
    dataframes = autopartner_gdansk.process()
    data = dataframes[0]
    dict = dataframes[1]
    query = '''
        SELECT dict.part_number, dict.manufacturer, data.part_name, data.price,
        REPLACE(REPLACE(data.qty, '-', '0'), '>', '') AS qty
        FROM data
        INNER JOIN dict
        ON dict.part_art = data.part_art
        WHERE qty NOT LIKE '0'
    '''
    return sqldf(query)
