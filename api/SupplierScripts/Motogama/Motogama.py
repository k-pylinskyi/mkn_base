from SupplierScripts import *


def motogama_to_db():
    print('Pushing Motogama to Data Base')
    DataFrameReader.dataframe_to_db('motogama', get_motogama_data())


def get_motogama_data():
    motogama = Motogama()
    data = motogama.process()
    query = '''
        SELECT
            40 as supplier_id,
            manufacturer,
            supplier_part_number,
            part_number,
            price,
            CAST(REPLACE(qty, '> ', '') AS INTEGER) as quantity,
            pack,
            part_name
        FROM
            data
        WHERE
            CAST(REPLACE(qty, '> ', '') AS INTEGER) > 0 
    '''
    return sqldf(query)


class Motogama:
    def __init__(self):
        self.data_columns = {
            0: 'supplier_part_number', 1: 'part_name', 2: 'qty',
            3: 'price', 5: 'part_number', 7: 'manufacturer', 8: 'pack'
        }
        self.data = pd.read_csv('.//TemporaryStorage//MOTOGAMA//files//motogama_data.csv',
                                sep=';', header=None, encoding_errors='ignore', usecols=[0, 1, 2, 3, 5, 7, 8])

    def process(self):
        self.data.rename(columns=self.data_columns, inplace=True)

        return self.data
