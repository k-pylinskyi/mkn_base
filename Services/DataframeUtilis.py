import pandas as pd

class DataframeUtilis:
    def read_csv(self, path, separator):
        try:
            df = pd.read_csv(path, sep=separator, encoding='latin1')
            print(df.dtypes)
            print(df.head())
            return df
        except FileNotFoundError as e:
            print(e)

    def read_excel(self, path):
        try:
            df = pd.read_excel(path)
            print(df.dtypes)
            print(df.head())
            return df

        except FileNotFoundError as e:
            print(e)

    def save_csv(self, df, path):
        df.to_csv(path, sep='\t', index=False)