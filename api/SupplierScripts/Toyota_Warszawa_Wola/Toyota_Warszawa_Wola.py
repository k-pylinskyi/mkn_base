import os
import zipfile
from ftplib import FTP

from Services.Ftp.FtpConnection import FtpConnection
from Services.Processors.DataFrameReader import *
from Services.load_config import Config
from Services.Loader.LoadController import LoadController

import pandas as pd
from pandasql import sqldf


def toyota_warszawa_wola_to_db():
    table_name = 'toyota_warszawa_wola'
    print('Pushing {} to Data Base'.format(table_name))
    data = get_tww_data()
    print(data)
    DataFrameReader.dataframe_to_db(table_name, data)


def get_tww_data():
    tww = Toyota_warszawa_wola()
    out = tww.process()
    query = '''
                    SELECT
                        'Toyota' as manufacturer,
                        CAST(out.part_number AS VARCHAR) as part_number,
                        CAST(out.part_number AS VARCHAR) as supplier_part_number,
                        CAST(out.price as FLOAT)/100 as supplier_price,
                        CAST(out.discount as FLOAT)/100 as supplier_discount,
                        (case when CAST(out.discount as FLOAT)/100 >= 25 then CAST(0.8 as FLOAT)
                              when CAST(out.discount as FLOAT)/100 >= 21 then CAST(0.85 as FLOAT)
                              when CAST(out.discount as FLOAT)/100 >= 16 then CAST(0.9 as FLOAT)
                              when CAST(out.discount as FLOAT)/100 >= 11 then CAST(0.95 as FLOAT)
                              else CAST(0 as FLOAT)/100 end) as discount,
                        (case when CAST(out.discount as FLOAT)/100 >= 25 then ROUND(CAST(out.price as FLOAT)/100*0.8, 2)
                              when CAST(out.discount as FLOAT)/100 >= 21 then ROUND(CAST(out.price as FLOAT)/100*0.85, 2)
                              when CAST(out.discount as FLOAT)/100 >= 16 then ROUND(CAST(out.price as FLOAT)/100*0.9, 2)
                              when CAST(out.discount as FLOAT)/100 >= 11 then ROUND(CAST(out.price as FLOAT)/100*0.95, 2)
                              else CAST(out.price as FLOAT)/100 end) as price,
                        999 as quantity,
                        5 as delivery
                        FROM out
                    '''
    return sqldf(query)


class Toyota_warszawa_wola:
    def __init__(self):
        self.path = '/suppliers/toyota_warszawa_wola/CENY (1).zip'

        self.user = 'ph6802'
        self.host = '138.201.56.185'
        self.password = 'z7lIh8iv10pLRt'

        self.data_columns = {
            0: 'part_number',
            1: 'price',
            2: 'part_name1',
            3: 'part_name2',
            4: 'g2',
            5: 'g3',
            6: 'g4',
            7: 'g5',
            8: 'discount',
            9: 'g6'
        }

    def process(self):
        absolute_path = path_creator()

        ftp = FtpConnection(host=self.host, username=self.user, password=self.password)
        print(absolute_path)
        ftp.download_file(self.path, absolute_path + r'\CENY (1).zip')
        passw = 'tmp_asd_'
        with zipfile.ZipFile(absolute_path + r'\CENY (1).zip', 'r') as zip_ref:
            zip_ref.extractall(absolute_path, pwd=passw.encode())

        if os.path.exists(absolute_path + r'\cennik.toy'):
            if os.path.exists(absolute_path + r'\cennik.txt'):
                os.remove(absolute_path + r'\cennik.txt')
            else:
                pass
            os.rename(absolute_path + r'\cennik.toy', absolute_path + r'\cennik.txt')
        indices = [0, 27, 39, 74, 109, 114, 124, 133, 136, 141, 150, 160]
        with open(absolute_path + r'\cennik.txt') as file:
            lines = [[line[i:j] for i, j in zip(indices, indices[1:] + [None])] for line in file]
            ### ONLY IN THIS FILE ###
            lines = lines[: -1]

        df = pd.DataFrame(lines)
        df = df.drop(columns=[10, 11])
        df.rename(columns=self.data_columns, inplace=True)
        df = df.drop(['g2', 'g3', 'g4', 'g5', 'g6'], axis=1)
        # df['part_number'] = df['part_number'].str.replace('[\W]+', '', regex=True)
        return df


def path_creator():
    folder_name = '\\toyota_warszawa_wola'
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
