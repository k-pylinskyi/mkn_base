from api.SupplierScripts import *


def autoland_to_db():
    print('Pushing Auto Land to Data Base')
    DataFrameReader.dataframe_to_db('autoland', get_autoland_data())


def get_autoland_data():
    autoland = AutoLand()
    data = autoland.process()

    query = '''
        SELECT
            5 as supplier_id,
            manufacturer,
            supplier_part_number,
            part_number,
            CAST(REPLACE(qty, '>', '') AS INTEGER) as quantity,
            price,
            pack
        FROM
            data
        WHERE
            part_number is not null
    '''

    return sqldf(query)

class AutoLand:
    def __init__(self):
        self.data_columns = {
            0: 'supplier_part_number',
            1: 'part_name',
            2: 'qty',
            3: 'price',
            4: 'part_number',
            6: 'manufacturer',
            7: 'pack',
        }

        self.data = pd.read_csv(
            'D:\\Work\\MNK_PRICES\\DB_SCRIPT\\script_main_files\\TemporaryStorage\\AUTO_LAND\\archive\\autoland_data.zip',
            compression='zip', sep=';', encoding_errors='ignore', header=None, low_memory=False,
            usecols=[0, 1, 2, 3, 4, 6, 7])

    def process(self):
        self.data.rename(columns=self.data_columns, inplace=True)

        return self.data