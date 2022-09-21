from api.SupplierScripts import *


class Gordon:
    def __init__(self):
        direcotry = '../TemporaryStorage//GORDON//files'
        self.dict = pd.read_csv(os.path.join(direcotry, 'gordon_dict.csv'), sep='\t', decimal=',', skiprows=2,
                                error_bad_lines=False, low_memory=False, encoding_errors='ignore')
        self.data = pd.read_csv(os.path.join(direcotry, 'gordon_data.csv'), sep='\t', decimal=',', skiprows=1,
                                error_bad_lines=False, low_memory=False, encoding_errors='ignore')

    def process(self):
        dictionary = self.dict
        dictionary.columns = [
            'supplier_part_number',
            'sufix',
            'part_number',
            'manufacturer'
        ]
        dictionary['part_number'] = DataFrameReader.format_column(self.dict['part_number'])

        data = self.data
        data.columns = [
            'supplier_part_number',
            'part_name',
            'tecdoc_number',
            'manufacturer',
            'price',
            'tecdoc_number_2',
            'qty1',
            'qty2',
            'idsafo'
        ]

        query = """
            SELECT 
            22 as supplier_id,
            dictionary.supplier_part_number,
            dictionary.part_number,
            dictionary.manufacturer,
            data.qty1 + data.qty2 as quantity,
            data.price
            FROM dictionary
            INNER JOIN data
            ON dictionary.supplier_part_number = data.supplier_part_number
        """

        return sqldf(query)