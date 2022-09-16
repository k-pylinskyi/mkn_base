import pandas as pd
import os

class DataFrameReader:
    @staticmethod
    def get_data_frames(directory, skip):
        files = os.listdir(directory)

        dfs_dict = dict()
        for file in files:
            file_name = os.path.splitext(file)[0]
            path = os.path.join(directory, file)
            df = pd.read_csv(path, sep=';', skiprows=skip, error_bad_lines=False, low_memory=False)
            dfs_dict[file_name] = df

        return dfs_dict
