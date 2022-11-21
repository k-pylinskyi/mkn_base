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

    query = '''
    
        SELECT
            data.part_number,
            data.index,
            data.price
        FROM
            data
        INNER JOIN 
            stock
        ON
            data.part_number = stock.part_number
        DELETE FROM
            stock
        WHERE stock.index LIKE '%CHRYSLER%' 
        OR LIKE '%FIAT%'
        OR LIKE '%FORD%'
        OR LIKE '%FORD TRUCKS%'
        OR LIKE '%HONDA%'
        OR LIKE '%HYUNDAI%'
        OR LIKE '%KIA%'
        OR LIKE '%MAZDA%'
        OR LIKE '%MERCEDES%'
        OR LIKE '%MITSUBISHI%'
        OR LIKE '%NISSAN%'
        OR LIKE '%OE CLAAS%'
        OR LIKE '%OE GERMANY%'
        OR LIKE '%OE INDUSTRY%'
        OR LIKE '%OE JCB%'
        OR LIKE '%OE MAZ%'
        OR LIKE '%OEM%'
        OR LIKE '%OPEL%'
        OR LIKE '%PEUGEOT%'
        OR LIKE '%RENAULT%'
        OR LIKE '%SEAT%'
        OR LIKE '%SKODA%'
        OR LIKE '%SUZUKI%'
        OR LIKE '%TOYOTA%'
        OR LIKE '%VOLVO%'
        OR LIKE '%VOLVO PENTA%'
        OR LIKE '%VW%'    
        
            
    '''
    return sqldf(query)

class InterCars:

    def __init__(self):

        data_url = 'ftp://3036856:0cL4X5@138.201.56.185/suppliers/intercars/data.csv'
        stock_url = 'ftp://3036856:0cL4X5@138.201.56.185/suppliers/intercars/stock.csv'

        self.data_columns = {
            0: 'part_number',
            1: 'index',
            2: 'tec_doc',
            3: 'tec_doc_prod',
            4: 'supplier_price',
            5: 'discounts',
            6: 'price'
        }

        self.stock_columns = {
            0: 'part_number',
            1: 'part_number',
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

