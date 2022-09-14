from Services.DataframeUtilis import DataframeUtilis as dfutilis
import os

class DataFrameReader:
    @staticmethod
    def get_data_frames(self, directory):
        files = os.listdir(directory)

        dfs_dict = {"name": [], "dataframe": []}
        for file in files:
            file_name = os.path.splitext(file)[0]
            path = os.path.join(directory, file)
            df = dfutilis.read_csv(path)
            dfs_dict["name"].append(file_name)
            dfs_dict["dataframe"].append(df)