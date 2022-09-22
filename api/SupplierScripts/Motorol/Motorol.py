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
    pd.set_option('display.max_columns', 999)

    def __init__(self):
        directory = "../TemporaryStorage/MOTOROL/files"

        self.data_columns = ['supplier_part_number', 'part_number', 'part_name', 'manufacturer', 'qty', 'price']
        self.dict_columns = ['supplier_part_number', 'part_number', 'manufacturer', 'deposit']

        self.data = pd.read_csv(os.path.join(directory, 'motorol_data.csv'), sep='\t', decimal=',', header=None, encoding_errors='ignore')
        self.dict = pd.read_csv(os.path.join(directory, 'motorol_dict.csv'), sep='\t', decimal=',', skiprows=1, encoding_errors='ignore')

    def process(self):
        self.data.columns = self.data_columns
        self.data['part_number'] = DataFrameReader.format_column(self.data['part_number'])

        self.dict.columns = self.dict_columns
        return [self.data, self.dict]