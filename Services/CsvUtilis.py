import pandas as pd

def read_csv(path, separator):
    try:
        df = pd.read_csv(path, sep=separator, encoding='latin1')
        print(df.dtypes)
        print(df.head())
        return df
    except FileNotFoundError as e:
        print(e)

def read_excel(path):
    try:
        df = pd.read_excel(path)
        print(df.dtypes)
        print(df.head())
        return df

    except FileNotFoundError as e:
        print(e)

def save_csv(df, path):
    df.to_csv(path, sep='\t', index=False)