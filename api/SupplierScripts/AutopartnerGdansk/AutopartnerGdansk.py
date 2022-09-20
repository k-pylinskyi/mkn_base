import pandas as pd
from pandasql import sqldf
import re

from api.Services.Processors.DataFrameReader import DataFrameReader


class AutopartnerGdansk:
    def __init__(self):
        dictionary = './autopartner_gdansk_helper.csv'
        location = '../../../TemporaryStorage/AUTO_PARTNER_GDANSK/files/autopartner_gdansk_data.csv'
        self.data = pd.read_csv(location, sep=';', skiprows=1, decimal=',', low_memory=False, encoding_errors='ignore')
        self.dictionary = pd.read_csv(dictionary, sep='\t', skiprows=1, decimal=',', low_memory=False,
                                      encoding_errors='ignore')

    def process(self):
        self.dictionary.columns = [
            'supplier_part_number',
            'part_number',
            'manufacturer',
            'part_name'
        ]
        self.data.columns = [
            'supplier_part_number',
            'part_name',
            'supplier_manufacturer',
            'qty',
            'price',
            '',
            'part_number',
            '',
            '',
        ]

        self.data['part_number'] = DataFrameReader.format_column(self.data['part_number'])


        query = """
        SELECT DISTINCT 7 AS supplier_id,
        data.supplier_part_number AS supplier_part_number
        FROM data
        """
        # print(self.dictionary)
        # print(self.data)
        self.data.dropna(how='any', axis=1)
        # nan_val = float("NaN")
        # self.data.replace("test", nan_val, inplace=True)
        print(self.data)


autopartner_gdansk = AutopartnerGdansk()
autopartner_gdansk.process()
