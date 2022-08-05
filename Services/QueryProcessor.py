from pandasql import sqldf
import pandas as pd
import Services.CsvUtilis as csv_utilis

class QueryAutomator:
    def __init__(self, file_list, data):
        self.data = csv_utilis.read_csv(data)

    def query(self, query):
        data = self.data

        query = query

        queried_data = sqldf(query)

        return queried_data

    