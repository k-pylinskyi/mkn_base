import pandas as pd

class DataframeUtilis:
    @staticmethod
    def read_csv(path):
        try:
            df = pd.read_csv(path, sep=';')
            #print(df.dtypes)
            #print(df.head())
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