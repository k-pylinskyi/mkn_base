from api.SupplierScripts import *


def autopartner_gdansk_to_db():
    print('Pushing Auto Partner Gdansk to Data Base')
    DataFrameReader.dataframe_to_db('autopartner_gdansk', get_autopartner_gdansk_data())


def get_autopartner_gdansk_data():
    autopartner_gdansk = AutopartnerGdansk()
    dataframes = autopartner_gdansk.process()
    data = dataframes[0]
    dict = dataframes[1]
    query = '''
        SELECT 
        7 as supplier_id,
        dict.manufacturer,
        data.supplier_part_number,
        dict.part_number, 
        data.part_name, 
        data.price,
        CAST(REPLACE(REPLACE(data.qty, '-', '0'), '> ', '') AS INTEGER) AS quantity
        FROM data
        INNER JOIN dict
        ON dict.supplier_part_number = data.supplier_part_number
        WHERE qty NOT LIKE '0'
    '''
    return sqldf(query)


class AutopartnerGdansk:
    pd.set_option('display.max_columns', 999)

    def __init__(self):
        self.data_columns = {0: 'manufacturer', 1: 'part_name', 2: 'supplier_part_number', 3: 'qty', 4: 'price', 6: 'part_number'}
        self.dict_columns = {0: 'supplier_part_number', 1: 'part_number', 2: 'manufacturer', 3: 'part_name'}
        location = '../TemporaryStorage/AUTO_PARTNER_GDANSK/files/autopartner_gdansk_data.csv'
        dictionary = '../TemporaryStorage/AUTO_PARTNER_GDANSK/files/autopartner_gdansk_dict.csv'

        self.data = pd.read_csv(location, encoding_errors='ignore', sep=';', header=None, low_memory=False)
        self.dict = pd.read_csv(dictionary, encoding_errors='ignore', sep='\t', header=None, skiprows=1)

    def process(self):
        self.data.drop(self.data.columns[[5, 7, 8]], axis=1, inplace=True)
        self.data.rename(columns=self.data_columns, inplace=True)
        self.data.set_index('part_number', inplace=True)

        self.dict.rename(columns=self.dict_columns, inplace=True)
        self.dict.set_index('part_number', inplace=True)
        return [self.data, self.dict]
