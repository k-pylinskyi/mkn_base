from pandasql import sqldf
import pandas as pd
from Services.DataframeUtilis import DataframeUtilis
import os

class QueryAutomator:
    def __init__(self, folder):
        self.file_list = os.listdir(folder)

    def get_dataframe(self, query):
        for file in self.file_list:
            file_name = os.path.splitext(os.path.basename(file))[0]
            locals()[file_name] = DataframeUtilis.read_csv(file, ';')

        query = query

        queried_data = sqldf(query)

        return queried_data

    