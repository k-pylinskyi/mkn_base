import pandas as pd
from pandasql import sqldf
from Services.Processors.DataFrameReader import DataFrameReader


class Packeto:
    def __init__(self):
        self.data_columns = {0: 'part_number', 1: 'price', 2: 'currency', 3: 'qty'}

        location = './TemporaryStorage/PAKETO/files/paketo_data.csv'
        self.data = pd.read_csv(location, encoding_errors='ignore', sep=';', header=None, skiprows=1)

    def process(self):
        self.data.drop(self.data.columns[[4]], axis=1, inplace=True)
        self.data.rename(columns=self.data_columns, inplace=True)
        self.data.set_index('part_number', inplace=True)
        self.data.columns = self.data.columns.str.strip()
        return self.data


def process_paketo():
    packeto = Packeto()
    data = packeto.process()
    query = '''
        SELECT data.part_number, data.price, data.currency, data.qty
        FROM data
        WHERE data.qty NOT LIKE '0.0' AND data.price NOT LIKE '0.0'
    '''
    df = pd.DataFrame(sqldf(query))
    return df.head(10).to_json()
