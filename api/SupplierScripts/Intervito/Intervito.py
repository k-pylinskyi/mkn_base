from SupplierScripts import *

def intervito_to_db():
    table_name = 'inter_vito'
    print('Pushing {} to Data Base'.format(table_name))
    DataFrameReader.dataframe_to_db(table_name, get_intervito_data())
    DataFrameReader.supplier_to_ftp(table_name)


def get_intervito_data():
    intervito = Intervito()
    data = intervito.process()
    # RTRIM(data.supplier_part_number, LENGTH(data.supplier_part_number) - INSTR(data.supplier_part_number," ")) AS part_number,
    query = '''
        SELECT
        27 as supplier_id,
        data.manufacturer,
        data.supplier_part_number,
        IFNULL(data.part_number, RTRIM(data.supplier_part_number, LENGTH(data.supplier_part_number) - INSTR(data.supplier_part_number," "))) AS part_number,
        REPLACE(data.price, ',', '.') as price,
        data.qty as quantity,
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
                             2: 'part_name', 3: 'part_number', 5: 'qty', 6: 'price', 7: 'currency', 8: 'pack'}

        data_url = 'ftp://intervito:iZ5sG6nT2qsZ0e@138.201.56.185/cennik_6090.csv'

        self.data = pd.read_csv(data_url, encoding_errors='ignore',
                                sep=';', header=None, usecols=[0, 1, 2, 3, 5, 6, 7, 8], low_memory=False, skiprows=1, decimal=',')


    def process(self):
        self.data.rename(columns=self.data_columns, inplace=True)
        print(self.data.head())

        return (self.data)
