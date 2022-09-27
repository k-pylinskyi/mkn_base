from api.SupplierScripts import *


def motorol_to_db():
    print('Pushing Motorol to Data Base')
    DataFrameReader.dataframe_to_db('motorol', get_motorol_data())


def get_motorol_data():
    motorol = Motorol()
    dataframes = motorol.process()
    data = dataframes[0]
    dict = dataframes[1]

    query = '''
        SELECT
        42 as supplier_id,
        data.manufacturer,
        data.supplier_part_number,
        data.part_number,
        data.part_name,
        IIF(dict.deposit is not null, data.price + dict.deposit, data.price) as price,
        data.qty as quantity
        FROM data
        LEFT JOIN dict
        ON data.supplier_part_number = dict.supplier_part_number
        WHERE
        IIF(dict.deposit is not null, data.price + dict.deposit, data.price) is not null
        AND
        data.qty > 0
    '''

    return sqldf(query)


class Motorol:

    def __init__(self):
        directory = "../TemporaryStorage/MOTOROL/files"

        self.data_columns = {0: 'supplier_part_number', 1: 'part_number', 2: 'part_name',
                             3: 'manufacturer', 4: 'qty', 5: 'price'}
        self.dict_columns = {0: 'supplier_part_number', 1: 'part_number', 2: 'manufacturer', 3: 'deposit'}

        self.data = pd.read_csv(os.path.join(directory, 'motorol_data.csv'), sep='\t', decimal=',',
                                header=None, encoding_errors='ignore')
        self.dict = pd.read_csv(os.path.join(directory, 'motorol_dict.csv'), sep='\t', decimal=',',
                                header=None, skiprows=1, encoding_errors='ignore')

    def process(self):
        self.data.rename(columns=self.data_columns, inplace=True)
        self.dict.rename(columns=self.dict_columns, inplace=True)

        return [self.data, self.dict]