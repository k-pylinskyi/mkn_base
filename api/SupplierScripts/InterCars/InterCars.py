from Services.Processors.DataFrameReader import *
import pandas as pd
from pandasql import sqldf


def intercars_to_db():
    table_name = 'intercars'
    print('Pushing {} to Data Base'.format(table_name))
    DataFrameReader.dataframe_to_db(table_name, get_intercars_data())
    DataFrameReader.supplier_to_ftp(table_name)


def get_intercars_data():
    intercars = InterCars()
    dataframes = intercars.process()
    data = dataframes[0]
    stock = dataframes[1]
    print(stock)
    query_stock = '''
            DELETE FROM stock
                WHERE stock.ind 
                LIKE '%CHRYSLER%'
                OR '%FIAT%'
                OR '%FORD%'
                OR '%FORD TRUCKS%'
                OR '%HONDA%'
                OR '%HYUNDAI%'
                OR '%KIA%'
                OR '%MAZDA%'
                OR '%MERCEDES%'
                OR '%MITSUBISHI%'
                OR '%NISSAN%'
                OR '%OE CLAAS%'
                OR '%OE GERMANY%'
                OR '%OE INDUSTRY%'
                OR '%OE JCB%'
                OR '%OE MAZ%'
                OR '%OEM%'
                OR '%OPEL%'
                OR '%PEUGEOT%'
                OR '%RENAULT%'
                OR '%SEAT%'
                OR '%SKODA%'
                OR '%SUZUKI%'
                OR '%TOYOTA%'
                OR '%VOLVO%'
                OR '%VOLVO PENTA%'
                OR '%VW%'    
            '''
    stock = sqldf(query_stock)

    print(stock)

    query = '''
        SELECT
            data.part_number,
            stock.ind,
            data.price
        FROM
            data
        INNER JOIN 
            stock
        ON
            data.part_number = stock.part_number
    '''
    return sqldf(query)


class InterCars:
    def __init__(self):

        data_url = 'ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/intercars/data.csv'
        stock_url = 'ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/intercars/stock.csv'

        self.data_columns = {
            0: 'part_number',
            1: 'ind',
            2: 'tec_doc',
            3: 'tec_doc_prod',
            4: 'supplier_price',
            5: 'discounts',
            6: 'price'
        }

        self.stock_columns = {
            0: 'part_number',
            1: 'ind',
            2: 'tec_doc_prod',
            3: 'warehouse',
            4: 'quantity'
        }

        self.data = pd.read_csv(data_url, sep=';', encoding_errors='ignore', header=None, low_memory=False, decimal=',')
        self.stock = pd.read_csv(stock_url, sep=';', encoding_errors='ignore', usecols=[0, 1, 4], header=None)

    def process(self):
        self.data.rename(columns=self.data_columns, inplace=True)
        self.stock.rename(columns=self.stock_columns, inplace=True)

        return [self.data, self.stock]

