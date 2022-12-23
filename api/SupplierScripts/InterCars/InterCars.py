from api.Services.Processors.DataFrameReader import *
import pandas as pd
from pandasql import sqldf
from api.Services.Loader.APILoader import *
from datetime import datetime
import os


def intercars_to_db():
    table_name = 'intercars'
    print('Pushing {} to Data Base'.format(table_name))
    DataFrameReader.dataframe_to_db(table_name, get_intercars_data())


def get_intercars_data():
    print('querying')
    intercars = InterCars()
    dataframes = intercars.process()
    data = dataframes[0]
    price = dataframes[1]
    stock = dataframes[2]
    exclude = dataframes[3]
    data['supplier_part_number'] = data.apply(f, axis=1)
    query = '''
        SELECT
            data.manufacturer,
            data.product_number,
            data.supplier_part_number,
            data.supplier_part_number as part_number,
            data.tec_doc,
            data.tec_doc_prod,
            data.article_number,
            data.short_description,
            data.description,
            data.barcode,
            data.weight,
            data.length * data.width * data.height as volume,
            data.custom_code,
            stock.warehaous,
            "PLN" AS currency,
            stock.quantity,
            REPLACE(price.supplier_price, ",", ".") as supplier_price,
            REPLACE(price.deposit, ",", ".") as deposit,
            REPLACE(price.price, ",", ".") as price,
            1 AS delivery
        FROM data
        INNER JOIN price
            ON data.supplier_part_number = price.supplier_part_number
        INNER JOIN stock
            ON data.supplier_part_number = stock.supplier_part_number
        LEFT JOIN exclude
            ON data.manufacturer = exclude.manufacturer
        WHERE
            exclude.manufacturer is null
        
    '''
    table = sqldf(query)
    return table


def f(row):
    if len(str(row['tec_doc'])) > 2:
        if row['supplier_part_number'] != row['tec_doc']:
            val = row['tec_doc']
        else:
            val = row['supplier_part_number']
    else:
        val = row['article_number']
    return val


def get_files():
    files = {'Stock': 'Stock', 'WholesalePricing': 'Wholesale_Pricing', 'ProductInformation': 'ProductInformation'}

    lastOverallDate = overallDateParser(files)

    for key in files.keys():
        remove_old_csv(f'../TemporaryStorage/intercars/{files[key]}.csv')
        url_dict = {
            'baseurl': f'https://data.webapi.intercars.eu/customer/99FIIU/{key}/{files[key]}_{lastOverallDate}.csv.zip',
            'supplier_name': 'intercars', 'payload': ('FjAqKSFg7j6NwSf8', '99FIIU'), 'zip': True}
        downloadFileFromAPI(url_dict)
        optimize_filenames(files, key, lastOverallDate)


class InterCars:
    def __init__(self):
        get_files()

        data_path = '../TemporaryStorage/intercars/ProductInformation.csv'
        price_path = '../TemporaryStorage/intercars/Wholesale_Pricing.csv'
        stock_path = '../TemporaryStorage/intercars/Stock.csv'
        exclude_url = 'ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/intercars/intercars_oe.csv'

        self.price_columns = {
            0: 'product_number',
            1: 'supplier_part_number',
            2: 'tec_doc_number',
            3: 'tec_doc_manufacturer',
            4: 'supplier_price',
            5: 'deposit',
            6: 'price'
        }

        self.data_columns = {
            0: 'product_number',
            1: 'supplier_part_number',
            2: 'tec_doc',
            3: 'tec_doc_prod',
            4: 'article_number',
            5: 'manufacturer',
            6: 'short_description',
            7: 'description',
            8: 'barcode',
            9: 'weight',
            10: 'length',
            11: 'width',
            12: 'height',
            13: 'custom_code'
        }

        self.stock_columns = {
            0: 'product_number',
            1: 'supplier_part_number',
            2: 'tec_doc',
            3: 'tec_doc_prod',
            4: 'warehaous',
            5: 'quantity'
        }

        self.data = pd.read_csv(data_path, sep=';', encoding_errors='ignore', header=None, low_memory=False,
                                decimal=',')
        self.price = pd.read_csv(price_path, sep=';', encoding_errors='ignore', header=None, low_memory=False,
                                 decimal=',')
        self.stock = pd.read_csv(stock_path, sep=';', encoding_errors='ignore', header=None, low_memory=False,
                                 decimal=',')
        self.exclude = pd.read_csv(exclude_url, sep=';', encoding_errors='ignore', header=None, low_memory=False,
                                   decimal=',')

    def process(self):
        print('processing')
        self.data.rename(columns=self.data_columns, inplace=True)
        self.price.rename(columns=self.price_columns, inplace=True)
        self.stock.rename(columns=self.stock_columns, inplace=True)
        self.exclude.columns = ['manufacturer']

        return [self.data, self.price, self.stock, self.exclude]


def overallDateParser(files):
    lastOverallDate = datetime.today().strftime("%Y-%m-%d")
    filesDates = {}
    for key in files.keys():
        print(f'Files in directory /{key}')
        dates = fileDate(url_dict=
                 {'baseurl': f'https://data.webapi.intercars.eu/customer/99FIIU/{key}',
                  'supplier_name': 'intercars', 'payload': ('FjAqKSFg7j6NwSf8', '99FIIU'), 'zip': True})
        filesDates[key] = dates
    keys = [filesDates[key].values() for key in filesDates]

    intersection = set.intersection(*map(set, keys))
    lastOverallDate = max([datetime.strptime(el, '%Y-%m-%d') for el in intersection])
    print('Last intersection day: ' + lastOverallDate.strftime('%Y-%m-%d'))
    return lastOverallDate.strftime('%Y-%m-%d')


def remove_old_csv(path):
    if os.path.exists(path):
        os.remove(path)


def optimize_filenames(dir, key, date_):
    os.remove(f'../TemporaryStorage/intercars/{dir[key]}_{date_}.csv.zip')
    os.rename(f'../TemporaryStorage/intercars/{dir[key]}_{date_}.csv',
              f'../TemporaryStorage/intercars/{dir[key]}.csv')
