from pandasql import sqldf
import pandas as pd
from Services.DataframeUtilis import DataframeUtilis
import os


class QueryProcessor:
    def __init__(self, folder):
        fl = os.listdir(folder)
        self.file_list = []
        for file in fl:
            self.file_list.append(os.path.join(folder, file))

    def get_dataframe(self, query):
        data_frames = []
        for file in self.file_list:
            file_name = os.path.splitext(os.path.basename(file))[0]
            df = DataframeUtilis.read_csv(file)
            locals()[file_name] = df
            data_frames.append(df)

        for frame in data_frames:
            frame.head()

        print('hart data')

        # query = query

        # queried_data = sqldf(query)

        # return queried_data
