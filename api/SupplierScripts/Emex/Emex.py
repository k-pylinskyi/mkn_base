# import shutil
#
# from api.Services.Logger.wrapper import timeit
# from api.SupplierScripts import *
# from api.Services.Loader.UrlLoader import UrlLoader
# import patoolib
#
#
# def emex_to_db():
#     emex = Emex()
#     # if os.path.exists(emex.save_dir):
#     #     shutil.rmtree(emex.save_dir)
#     # emex.load_makes()
#     # emex.load_48h()
#     # emex.load_emis()
#     # emex.load_emir()
#
#     makes = emex.process_makes()
#     h48 = emex.process_48h()
#     emex_48h_to_db(makes, h48)
#     emis = emex.process_emis()
#     emex_emis_to_db(makes, emis)
#     emir = emex.process_emir()
#     emex_emir_to_db(makes, emir)
#
# @timeit
# def emex_48h_to_db(makes, h48):
#     table_name = 'emex_48h'
#     print('Pushing {} to Data Base'.format(table_name))
#     data = get_h48_data(makes, h48)
#     DataFrameReader.dataframe_to_db(table_name, data)
#
# @timeit
# def emex_emir_to_db(makes, emir):
#     table_name = 'emex_emir'
#     print('Pushing {} to Data Base'.format(table_name))
#     data = get_emir_data(makes, emir)
#     DataFrameReader.dataframe_to_db_big(table_name, data)
#
# @timeit
# def emex_emis_to_db(makes, emis):
#     table_name = 'emex_emis'
#     print('Pushing {} to Data Base'.format(table_name))
#     data = get_emis_data(makes, emis)
#     DataFrameReader.dataframe_to_db_big(table_name, data)
#
# @timeit
# def get_h48_data(makes, h48):
#     df = pd.merge(makes, h48, on=['MakeLogo'], how='inner')
#     out = {'manufacturer': df.Brand,
#              'supplier_part_number': df.DetailNum,
#              'part_number': df.DetailNum,
#              'quantity': df.Quantity.fillna(5),
#              'price': round(np.multiply(df.DetailPrice, 0.93), 2),
#              'delivery': 20}
#
#     return pd.DataFrame(out)
#
# @timeit
# def get_emis_data(makes, emis):
#     df = pd.merge(makes, emis, on=['MakeLogo'], how='inner')
#     out = {'manufacturer': df.Brand,
#            'supplier_part_number': df.DetailNum,
#            'part_number': df.DetailNum,
#            'quantity': df.Quantity.fillna(5),
#            'price': round(np.multiply(df.DetailPrice, 0.93), 2),
#            'delivery': 20}
#
#     return pd.DataFrame(out)
#
# @timeit
# def get_emir_data(makes, emir):
#     df = pd.merge(makes, emir, on=['MakeLogo'], how='inner')
#     out = {'manufacturer': df.Brand,
#            'supplier_part_number': df.DetailNum,
#            'part_number': df.DetailNum,
#            'quantity': df.Quantity.fillna(5),
#            'price': round(np.multiply(df.DetailPrice, 0.93), 2),
#            'delivery': 20}
#
#     return pd.DataFrame(out)
#
#
# def get_file(file_url, file_name):
#     save_path = UrlLoader.get_file('MEX', file_url, file_name)
#     print(save_path)
#     patoolib.extract_archive(save_path, outdir="../TemporaryStorage/MEX")
#
#
# class Emex:
#     def __init__(self):
#         self.save_dir = "../TemporaryStorage/MEX"
#         self.urls = {
#             'Makes': 'ftp://anonymous:@emexonline.com/megaprice/Makes.rar',
#             '48H': 'ftp://anonymous:@emexonline.com/megaprice/48H.rar',
#             'EMIS': 'ftp://anonymous:@emexonline.com/megaprice/EMIS.rar',
#             'EMIR': 'ftp://anonymous:@emexonline.com/megaprice/EMIR.rar'
#         }
#
#         self.makes = r'C:\Users\admino4ka\PycharmProjects\mkn_base\TemporaryStorage\MEX\Makes.txt'
#         self.h48 = r'C:\Users\admino4ka\PycharmProjects\mkn_base\TemporaryStorage\MEX\48H.txt'
#         self.emis = r'C:\Users\admino4ka\PycharmProjects\mkn_base\TemporaryStorage\MEX\EMIS.txt'
#         self.emir = r'C:\Users\admino4ka\PycharmProjects\mkn_base\TemporaryStorage\MEX\EMIR.txt'
#
#     @timeit
#     def load_makes(self):
#         print('loading makes')
#         get_file(self.urls['Makes'], 'Makes.rar')
#
#     @timeit
#     def process_makes(self):
#         print('processing makes')
#         makes = pd.read_csv(self.makes, sep=",", header=None, engine='python', skiprows=1,
#                            on_bad_lines='skip', encoding='WINDOWS-1251', usecols=[0, 1])
#         makes.columns = ['MakeLogo', 'Brand']
#         return makes
#
#     @timeit
#     def load_48h(self):
#         print('loading 48H')
#         get_file(self.urls['48H'], '48H.rar')
#
#     @timeit
#     def process_48h(self):
#         print('processing 48H')
#         return pd.read_csv(self.h48, delimiter="\t", low_memory=False, error_bad_lines=False, encoding='WINDOWS-1251')
#
#     @timeit
#     def load_emis(self):
#         print('loading EMIS')
#         get_file(self.urls['EMIS'], 'EMIS.rar')
#
#     @timeit
#     def process_emis(self):
#         print('proceesing EMIS')
#         return pd.read_csv(self.emis, delimiter="\t", low_memory=False, error_bad_lines=False, encoding='WINDOWS-1251')
#
#     @timeit
#     def load_emir(self):
#         print('loading EMIR')
#         get_file(self.urls['EMIR'], 'EMIR.rar')
#
#     @timeit
#     def process_emir(self):
#         print('processing EMIR')
#         return pd.read_csv(self.emir, delimiter="\t", low_memory=False, error_bad_lines=False, encoding='WINDOWS-1251')

import shutil

from api.Services.Logger.wrapper import timeit
from api.SupplierScripts import *
from api.Services.Loader.UrlLoader import UrlLoader
import patoolib


def emex_to_db():
    emex = Emex()
    if os.path.exists(emex.save_dir):
        shutil.rmtree(emex.save_dir)
    emex.load_makes()
    emex.load_48h()
    emex.load_emis()
    emex.load_emir()

    makes = emex.process_makes()
    h48 = emex.process_48h()
    emex_48h_to_db(makes, h48)
    emis = emex.process_emis()
    emex_emis_to_db(makes, emis)
    emir = emex.process_emir()
    emex_emir_to_db(makes, emir)


@timeit
def emex_48h_to_db(makes, h48):
    table_name = 'emex_48h'
    print('Pushing {} to Data Base'.format(table_name))
    data = get_h48_data(makes, h48)
    DataFrameReader.dataframe_to_db(table_name, data)


@timeit
def emex_emir_to_db(makes, emir):
    table_name = 'emex_emir'
    print('Pushing {} to Data Base'.format(table_name))
    data = get_emir_data(makes, emir)
    DataFrameReader.dataframe_to_db_big(table_name, data)


@timeit
def emex_emis_to_db(makes, emis):
    table_name = 'emex_emis'
    print('Pushing {} to Data Base'.format(table_name))
    data = get_emis_data(makes, emis)
    DataFrameReader.dataframe_to_db_big(table_name, data)


def get_h48_data(makes, h48):
    df = pd.merge(makes, h48, on=['MakeLogo'], how='inner')
    out = {'manufacturer': df.Brand,
           'supplier_part_number': df.DetailNum,
           'part_number': df.DetailNum,
           'quantity': df.Quantity.fillna(5),
           'price': round(np.multiply(df.DetailPrice, 0.93), 2),
           'delivery': 20}

    return pd.DataFrame(out)


def get_emis_data(makes, emis):
    df = pd.merge(makes, emis, on=['MakeLogo'], how='inner')
    out = {'manufacturer': df.Brand,
           'supplier_part_number': df.DetailNum,
           'part_number': df.DetailNum,
           'quantity': df.Quantity.fillna(5),
           'price': round(np.multiply(df.DetailPrice, 0.93), 2),
           'delivery': 20}

    return pd.DataFrame(out)


def get_emir_data(makes, emir):
    df = pd.merge(makes, emir, on=['MakeLogo'], how='inner')
    out = {'manufacturer': df.Brand,
           'supplier_part_number': df.DetailNum,
           'part_number': df.DetailNum,
           'quantity': df.Quantity.fillna(5),
           'price': round(np.multiply(df.DetailPrice, 0.93), 2),
           'delivery': 20}

    return pd.DataFrame(out)


def get_file(file_url, file_name):
    save_path = UrlLoader.get_file('MEX', file_url, file_name)
    print(save_path)
    patoolib.extract_archive(save_path, outdir="../TemporaryStorage/MEX")


class Emex:
    def __init__(self):
        self.save_dir = "../TemporaryStorage/MEX"
        self.urls = {
            'Makes': 'ftp://anonymous:@emexonline.com/megaprice/Makes.rar',
            '48H': 'ftp://anonymous:@emexonline.com/megaprice/48H.rar',
            'EMIS': 'ftp://anonymous:@emexonline.com/megaprice/EMIS.rar',
            'EMIR': 'ftp://anonymous:@emexonline.com/megaprice/EMIR.rar'
        }

        self.makes = '../TemporaryStorage/MEX/Makes.txt'
        self.h48 = '../TemporaryStorage/MEX/48H.txt'
        self.emis = '../TemporaryStorage/MEX/EMIS.txt'
        self.emir = '../TemporaryStorage/MEX/EMIR.txt'

    def load_makes(self):
        print('loading makes')
        get_file(self.urls['Makes'], 'Makes.rar')

    def process_makes(self):
        print('processing makes')
        makes = pd.read_csv(self.makes, sep=",", header=None, engine='python', skiprows=1,
                            on_bad_lines='skip', encoding='WINDOWS-1251', usecols=[0, 1])
        makes.columns = ['MakeLogo', 'Brand']
        return makes

    def load_48h(self):
        print('loading 48H')
        get_file(self.urls['48H'], '48H.rar')

    def process_48h(self):
        print('processing 48H')
        return pd.read_csv(self.h48, delimiter="\t", low_memory=False, error_bad_lines=False, encoding='WINDOWS-1251')

    def load_emis(self):
        print('loading EMIS')
        get_file(self.urls['EMIS'], 'EMIS.rar')

    @timeit
    def process_emis(self):
        print('proceesing EMIS')
        mylist = []

        for chunk in pd.read_csv(self.emis, sep="\t", low_memory=False,
                                 on_bad_lines='skip', encoding='WINDOWS-1251', chunksize=20000):
            mylist.append(chunk)

        emis = pd.concat(mylist, axis=0)
        del mylist
        return emis

    @timeit
    def load_emir(self):
        print('loading EMIR')
        get_file(self.urls['EMIR'], 'EMIR.rar')

    @timeit
    def process_emir(self):
        print('processing EMIR')
        mylist = []

        for chunk in pd.read_csv(self.emir, sep="\t", low_memory=False,
                                 error_bad_lines=False, encoding='WINDOWS-1251', chunksize=20000):
            mylist.append(chunk)

        emir = pd.concat(mylist, axis=0)
        del mylist
        return emir
