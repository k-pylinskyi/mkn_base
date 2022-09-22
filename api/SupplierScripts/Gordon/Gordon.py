from api.SupplierScripts import *


def get_queried_data():
    gordon = Gordon()
    dataframes = gordon.process()
    data = dataframes[0]
    dict = dataframes[1]

    query = '''
        SELECT 
        22 as supplier_id,
        dict.supplier_part_number,
        dict.part_number,
        dict.manufacturer,
        data.qty1 + data.qty2 as quantity,
        data.price,
        data.tecdoc_number_1,
        data.tecdoc_number_2
        FROM dict
        INNER JOIN data
        ON dict.supplier_part_number = data.supplier_part_number
        '''

    return sqldf(query)


class Gordon:
    def __init__(self):
        direcotry = '../TemporaryStorage//GORDON//files'

        self.dict_columns = [
            'supplier_part_number',
            'sufix',
            'part_number',
            'manufacturer'
        ]
        self.data_columns = [
            'supplier_part_number',
            'part_name',
            'tecdoc_number_1',
            'manufacturer',
            'price',
            'tecdoc_number_2',
            'qty1',
            'qty2',
            'idsafo'
        ]
        self.dict = pd.read_csv(os.path.join(direcotry, 'gordon_dict.csv'), sep='\t', decimal=',', skiprows=2,
                                error_bad_lines=False, low_memory=False, encoding_errors='ignore')
        self.data = pd.read_csv(os.path.join(direcotry, 'gordon_data.csv'), sep='\t', decimal=',', skiprows=1,
                                error_bad_lines=False, low_memory=False, encoding_errors='ignore')

    def process(self):
        self.dict.columns = self.dict_columns
        self.dict['part_number'] = DataFrameReader.format_column(self.dict['part_number'])

        self.data.columns = self.data_columns

        return [self.data, self.dict]
