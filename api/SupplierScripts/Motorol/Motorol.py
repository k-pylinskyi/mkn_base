from api.SupplierScripts import *


class Motorol:
    pd.set_option('display.max_columns', 999)
    def __init__(self):
        directory = "../TemporaryStorage//MOTOROL//files"

        self.data_columns = ['manufacturer', 'part_name', 'part_art', 'qty', 'price', 'part_number']
        self.dict_columns = ['part_art', 'part_number', 'manufacturer', 'part_name']

        self.data = pd.read_csv(os.path.join(directory, 'motorol_data.csv'), sep='\t', decimal=',', skiprows=0,
                                error_bad_lines=False, low_memory=False, encoding_errors='ignore')
        self.dictionary = pd.read_csv(os.path.join(directory, 'motorol_dict.csv'), sep='\t', decimal=',', skiprows=1,
                                error_bad_lines=False, low_memory=False, encoding_errors='ignore')

    def process(self):
        self.data.drop(self.data.columns[[5, 7, 8]], axis=1, inplace=True)
        self.data.rename(columns=self.data_columns, inplace=True)
        self.data.set_index('part_number', inplace=True)

        self.dict.rename(columns=self.dict_columns, inplace=True)
        self.dict.set_index('part_number', inplace=True)
        return [self.data, self.dict]

    @staticmethod
    def get_queried_data():
        motorol = Motorol()
        dataframes = motorol.process()
        data = dataframes[0]
        dict = dataframes[1]

        query = '''
        
        '''

        return sqldf(query)