from SupplierScripts import *
import pandas


def intervito_to_db():
    print('Pushing Intervito to Data Base')
    DataFrameReader.dataframe_to_db(
        'intervito', get_intervito_data())


def get_intervito_data():
    intervito = Intervito()
    data = intervito.process()
    query = '''
        SELECT
        27 as supplier_id,
        data.manufacturer,
        data.supplier_part_number,
        RTRIM(data.supplier_part_number, LENGTH(data.supplier_part_number) - INSTR(data.supplier_part_number," ")) AS part_number,
        data.price,
        data.qty as quantity,
        data.delievery,
        data.pack
        FROM data
        WHERE
        data.qty > 0
        AND
        data.manufacturer is not null
    '''
    
    return sqldf(query)


class Intervito:
    def __init__(self):
        self.data_columns = {0: 'manufacturer', 1: 'supplier_part_number',
                             2: 'qty', 3: 'price', 4: 'currency', 5: 'pack', 6: 'delievery'}
        location = '../TemporaryStorage/INTERVITO/files/intervito_data.csv'

        self.data = pd.read_csv(
            location, encoding_errors='ignore', sep=';', header=None, low_memory=False, skiprows=1)

    def process(self):
        self.data.rename(columns=self.data_columns, inplace=True)
        self.data.drop(self.data.columns[[4]], axis=1, inplace=True)  # type: ignore

        return (self.data)
