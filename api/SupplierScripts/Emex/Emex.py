from api.SupplierScripts import *
from api.Services.Loader.UrlLoader import UrlLoader
import patoolib
import shutil


def emex_48h_to_db():
    table_name = 'emex_48h'
    print('Pushing {} to Data Base'.format(table_name))
    data = get_h48_data()
    DataFrameReader.dataframe_to_db(table_name, data)

def emex_emir_to_db():
    table_name = 'emex_emir'
    print('Pushing {} to Data Base'.format(table_name))
    data = get_emir_data()
    DataFrameReader.dataframe_to_db(table_name, data)

def emex_emis_to_db():
    table_name = 'emex_emis'
    print('Pushing {} to Data Base'.format(table_name))
    data = get_emis_data()
    DataFrameReader.dataframe_to_db(table_name, data)

def get_h48_data():
    e = Emex()

    df = pd.merge(e.makes, e.process_h48(), on=['key'], how='inner')
    df['part_number'] = df['supplier_part_number']
    df['price'] = round(np.multiply(df['supplier_price'], 0.93), 2)
    df['quantity'] = 999
    df['delivery'] = 20

    return df

def get_emis_data():
    e = Emex()

    df = pd.merge(e.makes, e.process_emis(), on=['key'], how='inner')
    df['part_number'] = df['supplier_part_number']
    df['price'] = round(np.multiply(df['supplier_price'], 0.93), 2)
    df['quantity'] = 999
    df['delivery'] = 21

    return df

def get_emir_data():
    e = Emex()

    df = pd.merge(e.makes, e.process_emir(), on=['key'], how='inner')
    df['part_number'] = df['supplier_part_number']
    df['price'] = round(np.multiply(df['supplier_price'], 0.93), 2)
    df['quantity'] = 999
    df['delivery'] = 20

    return df


def get_files():
    if os.path.exists('../TemporaryStorage/MEX'):
        shutil.rmtree('../TemporaryStorage/MEX')
    urls = {
        'Makes.rar': 'ftp://anonymous:@emexonline.com/megaprice/Makes.rar',
        '48H.rar': 'ftp://anonymous:@emexonline.com/megaprice/48H.rar',
        'EMIS.rar': 'ftp://anonymous:@emexonline.com/megaprice/EMIS.rar',
        'EMIR.rar': 'ftp://anonymous:@emexonline.com/megaprice/EMIR.rar'
            }
    save_paths = []

    for key, value in urls.items():
        save_paths.append(UrlLoader.get_file('MEX', value, key))

    return save_paths


class Emex:
    def __init__(self):
        paths = get_files()
        for path in paths:
            patoolib.extract_archive(path, outdir="../TemporaryStorage/MEX")

        self.makes = '../TemporaryStorage/MEX/Makes.txt'
        self.h48 = '../TemporaryStorage/MEX/48H.txt'
        self.emis = '../TemporaryStorage/MEX/EMIS.txt'
        self.emir = '../TemporaryStorage/MEX/EMIR.txt'

        self.columns = {
            0: 'key',
            1: 'supplier_part_number',
            2: 'supplier_price',
            3: 'part_name',
            4: 'logo',
            5: 'quantity',
            6: 'pack',
            7: 'reliability',
            8: 'weight',
            9: 'volume_weight',
            10: 'currency'
        }

        self.makes = self.process_makes()

    def process_makes(self):
        makes = pd.read_csv(self.makes, sep=",", header=None, engine='python', skiprows=1,
                           on_bad_lines='skip', encoding='WINDOWS-1251', usecols=[0, 1])
        makes.columns = ['key', 'manufacturer']
        return makes

    def process_h48(self):
        h48 = pd.read_csv(self.h48, sep="\t", header=None, engine='python', skiprows=1,
                            on_bad_lines='skip', encoding='WINDOWS-1251', usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        h48.rename(columns=self.columns, inplace=True)
        return h48

    def process_emis(self):
        emis = pd.read_csv(self.emis, sep="\t", header=None, engine='python', skiprows=1,
                            on_bad_lines='skip', encoding='WINDOWS-1251', usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        emis.rename(columns=self.columns, inplace=True)
        return emis

    def process_emir(self):
        emir = pd.read_csv(self.emir, sep="\t", header=None, engine='python', skiprows=1,
                            on_bad_lines='skip', encoding='WINDOWS-1251', usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        emir.rename(columns=self.columns, inplace=True)
        return emir
