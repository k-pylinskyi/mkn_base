from api.SupplierScripts import *

class Motorol:
    def __init__(self):
        directory = "../TemporaryStorage//MOTOROL//files"
        self.data = pd.read_csv(os.path.join(directory, 'motorol_data.csv'), sep='\t', decimal=',', skiprows=0,
                                error_bad_lines=False, low_memory=False, encoding_errors='ignore')
        self.dictionary = pd.read_csv(os.path.join(directory, 'motorol_dict.csv'), sep='\t', decimal=',', skiprows=1,
                                error_bad_lines=False, low_memory=False, encoding_errors='ignore')

    def process(self):
        data = self.data
        data.columns = [

        ]

        dictionary = self.dictionary
        dictionary = [

        ]

        query = """
        
        """

        return sqldf(query)