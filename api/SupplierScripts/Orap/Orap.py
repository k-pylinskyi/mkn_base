import os
import io
import pandas as pd
from pandas.errors import EmptyDataError

from api.SupplierScripts import *
from ftplib import FTP
from dateutil.parser import parse
from urllib import request
from pandasql import sqldf
from zipfile import ZipFile
from api.Services.Logger.wrapper import timeit
from api.Services.Processors.DataFrameReader import *


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
    DataFrameReader.dataframe_to_db_orap(table_name, get_orap_data())


def get_orap_data():
    orap = Orap()
    dataframes = orap.process()
    data = dataframes
    dat = pd.DataFrame()
    dat['manufacturer'] = data['brand']
    dat['currency'] = 'EUR'
    dat['supplier_part_number'] = data['code']
    dat['part_number'] = data['code']
    dat['delivery'] = data['delivery_time']
    dat['quantity'] = data['quantity']
    dat['price'] = (data['price']).str.replace(',', '').astype(float).round(decimals=2)
    # query = '''
    #             SELECT
    #                 data.brand as manufacturer,
    #                 data.code as supplier_part_number,
    #                 data.code as part_number,
    #                 data.quantity as quantity,
    #                 ROUND(data.price, 2) as price
    #             FROM
    #                 data
    #             '''
    print(dat)
    print(dat.shape[0])
    return dat
    # return sqldf(query)


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

    sep_dict = {'Price_Porsche': [';', pd.read_csv], 'Price_Toyota': [';', pd.read_csv], 'oapnal': ['\t', pd.read_excel]}
    for el in file_names.items():
        name = el[1].split('.')[0]
        if name in sep_dict.keys():
            print(f'in dict {name}')
            sepa = sep_dict[name][0]
            func = sep_dict[name][1]
        else:
            sepa = '\t'
            func = pd.read_csv
        print(f'file: {name}, sep = {sepa}, func = {func.__name__}')

        if 'oapnal' in el[1]:
            FTPconn = request.urlopen(f'{folder_url}{el[0]}')
            file = io.BytesIO(FTPconn.read())
            with ZipFile(file, 'r') as zip:
                df = func(zip.open('oapnal.xlsx'), skiprows=1, header=None)
                df.rename(columns=data_columns, inplace=True)
        else:
            try:
                df = func(f'{folder_url}{el[0]}', compression='zip', sep=sepa,
                          encoding_errors='ignore', skiprows=1, header=None, low_memory=False,
                          on_bad_lines='skip', lineterminator='\n')
                df.rename(columns=data_columns, inplace=True)
            except EmptyDataError:
                df = pd.DataFrame(columns=data_columns)

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
            0: 'brand',
            1: 'code',
            2: 'quantity',
            3: 'price',
            4: 'delivery_time',
            5: 'minimum_lot',
            6: 'deposit',
            7: 'name',
            8: 'weight',
            9: 'oe'
        }
        self.file_names, self.files = get_files(self.folder_url, self.data_columns)

    def process(self):
        dfs = []
        for el in self.files.keys():
            self.files[el]['File'] = el
            dfs.append(self.files[el])
            out = pd.concat(dfs, ignore_index=False)
        return out
