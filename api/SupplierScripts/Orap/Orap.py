from ftplib import FTP
from dateutil.parser import parse
from urllib import request
import io
from zipfile import ZipFile

import pandas as pd
from pandasql import sqldf

from api.Services.Logger.wrapper import timeit


def is_date(string, fuzzy=False):
    """
    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


@timeit
def orap_to_db():
    table_name = 'orap'
    print('Pushing {} to Data Base'.format(table_name))
    data = get_orap_data()
    print("=================================")
    print(data)
    print("=================================")
    # DataFrameReader.dataframe_to_db(table_name, data)


def get_orap_data():
    orap = Orap()
    data = orap.process()
    print(data)
    print("=================================")
    print(data.columns)
    query = '''
                SELECT
                    data.Brand as manufacturer,
                    data.Code as supplier_part_number,
                    data.Code as part_number,
                    data.Quantity as quantity,
                    ROUND(data.Price, 2) as price
                    FROM data
                    LIMIT 100;
                '''

    return sqldf(query)


def get_files(folder_url, data_columns):
    ftp = FTP('138.201.56.185')
    ftp.login(user='ph6802', passwd='z7lIh8iv10pLRt')
    ftp.cwd('suppliers/orap/')
    dir_list = []
    ftp.dir(dir_list.append)

    file_names = {}
    files = {}
    el_txt = ''
    el_zip = ''
    dir_list = [line.strip().split(' ') for line in dir_list]
    for line in dir_list:
        for el in line:
            if 'oapnal' not in el:
                if '.zip' in el:
                    el_txt = el.replace(".zip", ".txt")
                    el_zip = el
                    previous = line.index(el) - 1
                    previous_el = line[previous]
                    while not is_date(previous_el):
                        el_zip = f'{previous_el} {el_zip}'
                        el_txt = f'{previous_el} {el_txt}'
                        previous = previous - 1
                        previous_el = line[previous]
                    file_names[el_zip] = el_txt
                    # print(el_zip, file_names[el_zip])
                    print(el_zip, file_names[el_zip])
            elif 'oapnal' in el:
                if '.zip' in el:
                    el_txt = el.replace(".zip", ".xlsx")
                    el_zip = el

                    file_names[el_zip] = el_txt

    for el in file_names.items():
        if 'oapnal' not in el[1] and "Porsche" not in el[1] and "Toyota" not in el[1]:
            df = pd.read_csv(f'{folder_url}{el[0]}', compression='zip', sep='\t',
                             encoding_errors='ignore', skiprows=1, header=None, low_memory=False,
                             on_bad_lines='skip', lineterminator='\n')
            df.rename(columns=data_columns, inplace=True)
        elif "Porsche" in el[1] and "Toyota" in el[1]:
            df = pd.read_csv(f'{folder_url}{el[0]}', compression='zip', sep=';',
                             encoding_errors='ignore', skiprows=1, header=None, low_memory=False,
                             on_bad_lines='skip', lineterminator='\n')
            df.rename(columns=data_columns, inplace=True)
        elif 'oapnal' in el[1]:
            FTPconn = request.urlopen(f'{folder_url}{el[0]}')
            file = io.BytesIO(FTPconn.read())
            with ZipFile(file, 'r') as zip:
                df = pd.read_excel(zip.open('oapnal.xlsx'), skiprows=1, header=None)
                df.rename(columns=data_columns, inplace=True)
        files[el[1]] = df
    sum_rows = 0
    for el in files:
        # print(f'{el} | rows: {len(files[el])}, columns: {len(files[el].columns)}'
        # f'| col_num: {len(files[el].columns)}')
        # print(files[el].columns)
        sum_rows += len(files[el])

    print(f'sum = {sum_rows}')
    return file_names, files


class Orap:
    def __init__(self):
        self.folder_url = "ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/orap/"
        self.data_columns = {
            0: 'Brand',
            1: 'Code',
            2: 'Quantity',
            3: 'Price',
            4: 'Delivery_time',
            5: 'Minimum_lot',
            6: 'Deposit',
            7: 'Name',
            8: 'Weight',
            9: 'OE'
        }
        self.file_names, self.files = get_files(self.folder_url, self.data_columns)

    def process(self):
        dfs = []
        for el in self.files.keys():
            self.files[el]['File'] = el
            dfs.append(self.files[el])
            out = pd.concat(dfs, ignore_index=False)
        return out
