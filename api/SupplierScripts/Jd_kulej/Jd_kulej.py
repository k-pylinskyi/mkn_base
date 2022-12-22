import os
import zipfile
from ftplib import FTP

from Services.Ftp.FtpConnection import FtpConnection
from Services.Processors.DataFrameReader import *
from Services.load_config import Config
from Services.Loader.LoadController import LoadController

import pandas as pd
from pandasql import sqldf


def jd_kulej_to_db():
    table_name = 'jd_kulej'
    print('Pushing {} to Data Base'.format(table_name))
    data = get_jd_kulej_data()
    print(data)
    DataFrameReader.dataframe_to_db(table_name, data)


def get_jd_kulej_data():
    jd = Jd_kulej()
    out = jd.process()
    query = '''
                    SELECT
                        'PSA' AS manufacturer,
                        out.part_number AS part_number,
                        out.part_number AS supplier_part_number,
                        CAST(out.price AS FLOAT)/100 as supplier_price,
                        CAST(out.price AS FLOAT)/100 - CAST(out.price AS FLOAT)/100*CAST(out.discount_perc AS FLOAT)/100
                            as price,
                        out.discount_category,
                        out.discount_perc as discount_percent,
                        'PLN' AS currency,
                        999 AS quantity,
                        10 AS delivery,
                        out.pack, 
                        out.replacement
                    FROM out
                    '''
    return sqldf(query)


class Jd_kulej:
    def __init__(self):
        self.host = '138.201.56.185'
        self.user = 'ph6802'
        self.password = 'z7lIh8iv10pLRt'
        self.path = '/suppliers/jd_kulej/XP0006_MULTI.txt'

        self.data_columns = {
            0: 'g1',
            1: 'g2',
            2: 'part_number',
            3: 'part_name',
            4: 'g3',
            5: 'price',
            6: 'replacement',
            7: 'pack',
            8: 'g4',
            9: 'discount_category',
        }

        self.discount = \
            {
                'A': '0',
                'B': '5',
                'C': '5',
                'D': '15',
                'E': '20',
                'F': '25',
                'G': '30',
                'H': '35'
            }

    def process(self):
        absolute_path = path_creator('jd_kulej')

        ftp = FtpConnection(host=self.host, username=self.user, password=self.password)
        print(absolute_path)
        if os.path.exists(absolute_path + r'\kulej.txt'):
            os.remove(absolute_path + r'\kulej.txt')
        else:
            pass
        ftp.download_file(self.path, absolute_path + r'\kulej.txt')

        indices = [0, 25, 33, 51, 85, 87, 111, 135, 141, 156, 161]
        with open(absolute_path + r'\kulej.txt', encoding='latin1') as file:
            lines = [[line[i:j] for i, j in zip(indices, indices[1:] + [None])] for line in file]

        df = pd.DataFrame(lines)
        df.rename(columns=self.data_columns, inplace=True)
        df = df.drop(['g1', 'g2', 'g3', 'g4', 10], axis=1)
        df["part_number"] = df["part_number"].str.replace(" ", "")
        df["price"] = df["price"].replace(" ", "")
        df["replacement"] = df["replacement"].replace(" ", "")
        df["pack"] = df["pack"].replace(" ", "")
        df["discount_category"] = df["discount_category"].str.replace(" ", "").replace('\d+', '')

        df["price"] = df["price"].replace(r"(0)\1{3,}", "", regex=True)
        df["price"] = df["price"].replace(" ", "")
        df["price"] = df["price"].fillna(0)
        df["pack"] = df["pack"].replace(r"(0)\1{3,}", "", regex=True).str.match("([1-9]+0*)")
        df['discount_perc'] = df['discount_category'].apply(lambda x: self.discount.get(x)).fillna('')
        print(df.head(5))
        return df


def path_creator(supp_name):
    folder_name = f'\\{supp_name}'
    print(folder_name)
    path_parent = os.path.dirname(os.getcwd())
    os.chdir(path_parent)
    os.chdir('TemporaryStorage')
    absolute_path = os.getcwd() + folder_name

    if not os.path.exists(folder_name[1:]):
        os.makedirs(folder_name[1:])
        print("Directory Created")
    else:
        print("Directory Exists")
    return absolute_path
